"""Batch extract civil-law attributes from DOCX and export semantic relations."""

import argparse
from collections import Counter, defaultdict
import csv
from hashlib import sha256
import json
from pathlib import Path
from tempfile import TemporaryDirectory
from xml.etree.ElementTree import ParseError
from zipfile import BadZipFile

from .app.context.civil_semantic_graph import extract_attributes, relate, verify_change
from .app.document_processing.parser.legal_structure_parser import parse_docx

DATA = Path("data/legal-dataset-study/data")
DEFAULT_FIXTURE = Path("data/semantic-relation-cases/sources.json")


def write_json(path, payload):
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def read_catalog(path):
    if path is None:
        return {}
    matches = defaultdict(list)
    with path.open(encoding="utf-8-sig", newline="") as stream:
        for row in csv.DictReader(stream):
            if row.get("download_status") == "success" and row.get("download_path"):
                matches[Path(row["download_path"]).name].append(row)
    return matches


def scan(path, display_path, metadata, source=None):
    row = metadata[0] if len(metadata) == 1 else {}
    doc_id = f"dataset:{row['id']}" if row else f"file:{display_path}"
    node = {
        "document_id": doc_id, "number": row.get("so_ky_hieu"),
        "title": row.get("title") or path.stem,
        "source_url": row.get("source_url"), "path": display_path,
        "metadata_status": ("MATCHED" if row else "AMBIGUOUS" if metadata else "MISSING"),
        "source_kind": source or "CORPUS_DOCX", "version_sha256": None,
        "catalog_effective_from": row.get("ngay_co_hieu_luc") or None,
        "catalog_effective_to": row.get("ngay_het_hieu_luc") or None,
        "legal_version_verified": False,
    }
    try:
        digest = sha256(path.read_bytes()).hexdigest()
        node["version_sha256"] = digest
        tree = parse_docx(path, doc_id)
        attrs = list(extract_attributes(tree, doc_id, node["number"]))
        node.update(
            status="EXTRACTED" if attrs else "NO_GROUNDED_ATTRIBUTES",
            attributes_count=len(attrs), parser_status=tree["status"],
            parser_warnings=sorted({warning["code"] for warning in tree["warnings"]}),
        )
    except (OSError, ValueError, KeyError, ParseError, BadZipFile, RecursionError) as exc:
        node.update(status="READ_ERROR", attributes_count=0, reason=f"{type(exc).__name__}: {exc}")
        attrs = []
    return node, attrs


def validate_cases(edges, fixture, corpus, catalog):
    """Run the real-source acceptance cases through the same DOCX and relation pipeline."""
    positive, = [edge for edge in edges if edge["target"]["number"] == "21/2021/NĐ-CP"
                 and edge["target"]["clause"] == "2"]
    negative, = [edge for edge in edges if edge["target"]["number"] == "21/2021/NĐ-CP"
                 and edge["target"]["clause"] == "5"]
    docx_paths = [p for p in corpus.rglob("*") if p.suffix.lower() == ".docx"
                  and any(r["so_ky_hieu"] == "21/2021/NĐ-CP" for r in catalog.get(p.name, []))]
    nd21, = docx_paths
    nd21_text = "\n".join(block["text"] for block in parse_docx(nd21)["source_blocks"])
    check_no_citation = "99/2022" not in nd21_text and "21/2021" not in positive["source"]["quote"]
    change = {**fixture["change"], "target_id": positive["source_id"]}
    impact = verify_change(positive, change)
    return [
        {"case": "RG-04", "passed": positive["status"] == "SUPPORTED" and check_no_citation,
         "edge": positive, "no_direct_reference_checked": check_no_citation,
         "reference_check_scope": "NĐ 21 DOCX và đoạn Điều 6 NĐ 99 dùng trong kiểm thử"},
        {"case": "RG-05", "passed": negative["status"] == "REJECTED", "decision": negative},
        {"case": "RG-06", "passed": impact["status"] == "NO_IMPACT_SHOWN",
         "edge": positive, "impact": impact},
    ]


def run(corpus, catalog_path, output, case_sources=None):
    if not corpus.is_dir():
        raise ValueError(f"Không tìm thấy thư mục DOCX: {corpus}")
    paths = sorted(p for p in corpus.rglob("*") if p.is_file() and p.suffix.lower() == ".docx")
    if not paths:
        raise ValueError(f"Không tìm thấy tệp DOCX: {corpus}")
    catalog = read_catalog(catalog_path)
    output.mkdir(parents=True, exist_ok=False)
    statuses, field_counts = Counter(), Counter()
    nodes, role_docs = [], []
    snapshot = sha256()
    fixture = None

    def persist(node, attributes, stream):
        nodes.append(node)
        for attr in attributes:
            stream.write(json.dumps(attr, ensure_ascii=False, separators=(",", ":")) + "\n")
        role_attrs = [attr for attr in attributes if "semantic_role" in attr["values"]]
        if role_attrs:
            role_docs.append({**node, "attributes": role_attrs})

    with (output / "attributes.jsonl").open("w", encoding="utf-8") as stream:
        for path in paths:
            relative = path.relative_to(corpus).as_posix()
            node, attrs = scan(path, relative, catalog.get(path.name, []))
            snapshot.update(json.dumps([relative, node["version_sha256"]]).encode())
            statuses[node["status"]] += 1
            field_counts.update(name for row in attrs for name, value in row["values"].items()
                                if value["status"] == "FOUND")
            persist(node, attrs, stream)
        if case_sources:
            from docx import Document
            fixture = json.loads(case_sources.read_text(encoding="utf-8"))
            supplemental = fixture["supplement"]
            # The test-only source is a labelled transcription, never counted as a corpus document.
            with TemporaryDirectory() as temp:
                path = Path(temp) / "nd99-source-excerpt.docx"
                docx = Document()
                for paragraph in supplemental["paragraphs"]:
                    docx.add_paragraph(paragraph)
                docx.save(path)
                node, attrs = scan(path, case_sources.as_posix(), [supplemental], "SOURCE_EXCERPT")
                # The text transcription is the reproducible source version. DOCX container
                # timestamps from the temporary conversion can vary between runs.
                node["version_sha256"] = sha256(json.dumps(supplemental["paragraphs"],
                                                ensure_ascii=False).encode()).hexdigest()
                node["version_basis"] = "SOURCE_PARAGRAPHS_SHA256"
                persist(node, attrs, stream)

    decisions = relate(role_docs)
    edges = [edge for edge in decisions if edge["status"] == "SUPPORTED"]
    other = [edge for edge in decisions if edge["status"] != "SUPPORTED"]
    connected_ids = {edge[key] for edge in edges for key in ("source_id", "target_id")}
    review_ids = {edge[key] for edge in other if edge["status"] == "NEEDS_REVIEW"
                  for key in ("source_id", "target_id")}
    for node in nodes:
        if node["document_id"] in connected_ids:
            node["relation_status"] = "HAS_RELATION"
        elif node["document_id"] in review_ids:
            node["relation_status"] = "NEEDS_REVIEW"
        elif node["status"] == "EXTRACTED":
            node["relation_status"] = "NO_RELATION_FOUND"
        else:
            node["relation_status"] = "INSUFFICIENT_DATA"

    stats = {
        "schema_version": "1.0", "corpus_snapshot_sha256": snapshot.hexdigest(),
        "files": len(paths), "files_read": len(paths) - statuses["READ_ERROR"],
        "files_passed": statuses["EXTRACTED"], "status_counts": dict(statuses),
        "corpus_attribute_records": sum(n["attributes_count"] for n in nodes if n["source_kind"] == "CORPUS_DOCX"),
        "field_counts": dict(sorted(field_counts.items())), "supplemental_sources": int(fixture is not None),
        "edges": len(edges), "other_decisions": dict(Counter(edge["status"] for edge in other)),
        "file_relation_counts": dict(Counter(n["relation_status"] for n in nodes
                                             if n["source_kind"] == "CORPUS_DOCX")),
    }
    write_json(output / "nodes.json", nodes)
    write_json(output / "relations.json", {"edges": edges, "other_decisions": other})
    write_json(output / "statistics.json", stats)
    cases = validate_cases(decisions, fixture, corpus, catalog) if fixture else []
    if cases:
        write_json(output / "cases.json", cases)
    return stats, cases


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--corpus", type=Path, default=DATA / "lightrag")
    parser.add_argument("--catalog", type=Path, default=DATA / "ung_vien_dan_su.csv")
    parser.add_argument("--no-catalog", action="store_true")
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--verify-cases", type=Path, nargs="?", const=DEFAULT_FIXTURE)
    args = parser.parse_args()
    try:
        stats, cases = run(args.corpus, None if args.no_catalog else args.catalog,
                           args.output_dir, args.verify_cases)
    except (OSError, ValueError) as exc:
        parser.exit(2, f"{exc}\n")
    print(json.dumps(stats, ensure_ascii=False))
    for case in cases:
        print(f"{case['case']}: {'PASS' if case['passed'] else 'FAIL'}")
    return 0 if all(case["passed"] for case in cases) else 1


if __name__ == "__main__":
    raise SystemExit(main())
