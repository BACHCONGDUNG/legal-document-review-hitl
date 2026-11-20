"""Supplement AnalysisContext with source-verified quotations only."""
from copy import deepcopy
from dataclasses import dataclass
import json

from ..schemas.contracts import AnalysisContext, AmendmentItem
from ..schemas.report_validation import validate_payload, validate_sources
from .lightrag_client import LightRAGClient, RetrievalError
from .source_registry import SourceRegistry


@dataclass
class ContextBuild:
    """Internal bookkeeping, never serialized as a new shared data contract."""
    amendment: AmendmentItem
    issues: list[dict]
    retrieved: dict | None


def build_local_context(item, boundary, *, max_chars=12000):
    """Keep the containing legal unit and amendment scope as literal evidence.

    This is source selection, not a claim that references/effect are complete.
    Derived after_text is never inserted into a quotation. The smallest parent
    is used first; oversized parents are reported rather than silently clipped.
    """
    if max_chars < 1:
        raise ValueError('max_chars must be positive')
    result = deepcopy(item)
    evidence = list(result['evidence'])
    issues = []
    if item['applicability'] == 'APPLIES':
        for key, targets in boundary.units['v1'].items():
            if not any(t['unit_id'] in item['target_unit_ids'] for t in targets):
                continue
            article, clause, point = key
            parent_key = ((article, clause, None) if point else
                          (article, None, None) if clause else None)
            parents = boundary.units['v1'].get(parent_key, []) if parent_key else []
            if len(parents) == 1:
                parent = parents[0]
                if len(parent['content']) <= max_chars:
                    evidence.append({'document_id': 'v1', 'source_refs': parent['source_refs'],
                                     'quote': parent['content']})
                else:
                    issues.append({'stage': 'context', 'code': 'LOCAL_CONTEXT_LIMIT',
                                   'message': 'Đơn vị chứa vượt giới hạn ngữ cảnh cục bộ; giữ bằng chứng đích, chưa xác nhận đủ ngữ cảnh.',
                                   'amendment_id': item['amendment_id']})
            break
    unique = []
    for ref in evidence:
        if ref not in unique:
            unique.append(deepcopy(ref))
    result['context']['evidence'] = unique
    result['context']['general_context'] = '\n\n'.join(
        f"[{ref['document_id']} / {', '.join(ref['source_refs'])}]\n{ref['quote']}"
        for ref in unique)
    validate_payload(AmendmentItem, result)
    validate_sources(result, boundary.documents)
    return ContextBuild(result, issues, None)


def _failure(item, code, retrieved=None):
    result = deepcopy(item)
    result["needs_review"] = True
    reason = f"LightRAG supplemental context unverified ({code})."
    result["review_reason"] = " ".join(filter(None, [result["review_reason"], reason]))
    issue = {"stage": "context", "code": code, "message": reason,
             "amendment_id": item["amendment_id"]}
    return ContextBuild(result, [issue], retrieved)


def prepare_context(item: AmendmentItem, registry: SourceRegistry,
                    client: LightRAGClient | None) -> ContextBuild:
    """Index once per session, then retrieve; preserve index error codes.

    Intended as context_work inside the parallel join. The runner still owns
    cleanup and must append CLEANUP_PENDING as a ProcessingIssue if returned.
    """
    validate_payload(AmendmentItem, item)
    validate_sources(item, registry.documents)
    if client is not None:
        try:
            client.index(list(registry.chunks.values()))
        except RetrievalError as exc:
            return _failure(item, exc.code)
    return build_context(item, registry, client)


def build_context(item: AmendmentItem, registry: SourceRegistry,
                  client: LightRAGClient | None) -> ContextBuild:
    validate_payload(AmendmentItem, item)
    validate_sources(item, registry.documents)
    result = deepcopy(item)
    if client is None:
        return ContextBuild(result, [], None)
    retrieved = None
    try:
        # Treat documents as untrusted data. The query supplies no execution/tool
        # instructions, and the adapter ignores generated descriptions/answers.
        query = json.dumps({"task": "Find related source clauses, not legal conclusions",
                            "instruction": item["instruction"]["quote"],
                            "target_document": item["target_document"],
                            "target_locator": item["target_locator"],
                            "before_text": item["before_text"],
                            "after_text": item["after_text"]}, ensure_ascii=False)
        retrieved = client.query(query)
        evidence = [registry.evidence(chunk) for chunk in retrieved["chunks"]]
        if not evidence:
            raise RetrievalError("RETRIEVAL_EMPTY_UNCONFIRMED")
        context = result["context"]
        for ref in evidence:
            if ref not in context["evidence"]:
                context["evidence"].append(ref)
        additions = []
        for raw, ref in zip(retrieved["chunks"], evidence):
            source = registry.chunks[raw["file_path"]]
            additions.append(f"[{source.document_id} / {source.role} / version={source.version} / {source.source_ref}] {ref['quote']}")
        additions = "\n".join(additions)
        context["general_context"] = "\n".join(filter(None, [context["general_context"], additions]))
        validate_payload(AnalysisContext, context)
        validate_sources(context, registry.documents)
        return ContextBuild(result, [], retrieved)
    except (RetrievalError, ValueError) as exc:
        code = exc.code if isinstance(exc, RetrievalError) else "RETRIEVAL_SOURCE_REJECTED"
        # Keep pre-existing context/reference/effect status exactly as supplied.
        # Empty retrieval never changes a ReferenceRequirement to MISSING.
        return _failure(item, code, retrieved)
