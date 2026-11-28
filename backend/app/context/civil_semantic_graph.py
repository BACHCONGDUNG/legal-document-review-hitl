"""Extract source-bound phrases and link reviewed civil-law provision patterns."""

import re

# Patterns capture only phrases present in the source. Absent values stay unknown.
ACTORS = (
    r"cơ quan đăng ký|văn phòng đăng ký đất đai|trung tâm đăng ký(?: giao dịch, tài sản)?|"
    r"chấp hành viên|người yêu cầu(?: đăng ký)?|bên nhận (?:bảo đảm|thế chấp|cầm cố)|"
    r"bên (?:bảo đảm|thế chấp|cầm cố)|chủ đầu tư|người thứ ba|người phải thi hành án|"
    r"tổ chức, cá nhân|cá nhân, pháp nhân|chủ sở hữu|người sử dụng đất|"
    r"ủy ban nhân dân(?: cấp (?:tỉnh|huyện|xã))?|hội đồng nhân dân|tòa án(?: nhân dân)?|"
    r"cơ quan thi hành án dân sự|người được thi hành án|người có quyền lợi, nghĩa vụ liên quan"
)
OBJECTS = (
    r"quyền sử dụng đất|tài sản gắn liền với đất(?: hình thành trong tương lai)?|"
    r"hợp đồng (?:bảo đảm|thế chấp)|biện pháp bảo đảm|tài sản (?:bảo đảm|thế chấp|ký quỹ)|"
    r"hồ sơ(?: đăng ký)?|phiếu yêu cầu(?: đăng ký)?|quyền tài sản|"
    r"nghĩa vụ được bảo đảm|tàu bay|tàu biển|động sản|bất động sản"
)
PATTERNS = {
    "actor": rf"(?:{ACTORS})\b",
    "object": rf"(?:{OBJECTS})\b",
    "activity": (
        r"(?:đăng ký (?:thay đổi|thế chấp|biện pháp bảo đảm)|xóa đăng ký|hủy đăng ký|"
        r"nộp hồ sơ|xử lý tài sản bảo đảm|gửi vào tài khoản phong tỏa|"
        r"cập nhật nội dung đăng ký|giao tài sản|cung cấp thông tin|nắm giữ tài sản bảo đảm)\b"
    ),
    "modality": r"(?:không được|phải|được quyền|có quyền|có nghĩa vụ|có trách nhiệm)\b",
    "right_or_duty": (
        r"(?:không được|phải|được quyền|có quyền|có nghĩa vụ|có trách nhiệm)\s+"
        r"(?:(?!\s+trừ\b|,\s*(?:nếu|trừ)\b)[^;.!?\n])+"
    ),
    "condition": r"(?:trong trường hợp|trường hợp|nếu)\s+(?:(?!\s+thì\b|,\s*trừ\b)[^;.!?\n])+",
    "exception": r"(?:trừ trường hợp|ngoại trừ|trừ khi)[^;.!?\n]+",
    "territory": r"(?:trên phạm vi cả nước|trên địa bàn [^,;.!?\n]+|trên lãnh thổ Việt Nam)",
    "temporal_scope": (
        r"(?:kể từ (?:ngày|thời điểm)|từ thời điểm|trong thời hạn|có hiệu lực từ ngày)"
        r"[^,;.!?\n]+"
    ),
}
PATTERNS = {name: re.compile(r"\b" + pattern, re.IGNORECASE) for name, pattern in PATTERNS.items()}
# Keep the vocabulary conservative. These roles use their own source spans, in
# addition to the general attributes. Selectors bind roles to actual provisions.
ROLE_PATTERNS = {
    "sets_registration_time": re.compile(
        r"thời điểm có hiệu lực của đăng ký đối với quyền sử dụng đất.{0,150}?"
        r"cơ quan đăng ký (?:ghi, )?cập nhật nội dung đăng ký", re.I),
    "uses_registration_time": re.compile(
        r"thời điểm đăng ký tại cơ quan có thẩm quyền.{0,100}?"
        r"phát sinh hiệu lực đối kháng với người thứ ba|"
        r"thế chấp tài sản phát sinh hiệu lực đối kháng với người thứ ba kể từ thời điểm đăng ký", re.I),
    "uses_escrow_time": re.compile(
        r"hiệu lực đối kháng.{0,95}?tài sản ký quỹ được gửi vào tài khoản phong tỏa", re.I),
    "contract_effective": re.compile(r"hợp đồng bảo đảm đã có hiệu lực pháp luật", re.I),
}
ROLE_SELECTORS = {
    ("99/2022/NĐ-CP", "6", "1", "a"): "sets_registration_time",
    ("21/2021/NĐ-CP", "23", "2", None): "uses_registration_time",
    ("91/2015/QH13", "319", "2", None): "uses_registration_time",
    ("21/2021/NĐ-CP", "23", "5", None): "uses_escrow_time",
    ("21/2021/NĐ-CP", "23", "1", None): "contract_effective",
}
# Only verified semantic roles can be delivered as graph edges.
RULE_ID = "LAND_SECURITY_REGISTRATION_TIME"


def _span(match, offset=0):
    if not match:
        return {"value": None, "status": "NOT_FOUND"}
    return {"value": match.group(), "start": offset + match.start(), "end": offset + match.end(),
            "status": "FOUND"}


def extract_block(text, offset=0):
    attrs = {name: _span(pattern.search(text), offset) for name, pattern in PATTERNS.items()}
    exception = attrs["exception"]
    condition = attrs["condition"]
    if exception["value"] and condition.get("start", -1) >= exception["start"]:
        attrs["condition"] = _span(None)
    return attrs


def extract_attributes(tree, document_id, number=None):
    """Use the parser's source spans and skip headings, quotes, and unsupported blocks."""
    blocks = {block["source_ref"]: block for block in tree["source_blocks"]}

    def walk(node, article=None, clause=None, point=None):
        if node["kind"] == "QUOTATION":
            return
        if node["kind"] == "ARTICLE":
            article = node["label"]
        elif node["kind"] == "CLAUSE":
            clause = node["label"]
        elif node["kind"] == "POINT":
            point = node["label"]
        role = ROLE_SELECTORS.get((number, article, clause, point))
        for i, segment in enumerate(node["segments"]):
            if i == 0 and node["kind"] == "ARTICLE" and node.get("heading"):
                continue
            block = blocks[segment["source_ref"]]
            if block["kind"] != "PARAGRAPH":
                continue
            start, end = segment["start"], segment["end"]
            quote = block["text"][start:end]
            attrs = extract_block(quote, start)
            role_match = ROLE_PATTERNS[role].search(quote) if role else None
            if role_match:
                attrs["semantic_role"] = {**_span(role_match, start), "code": role}
            if any(value["status"] == "FOUND" for value in attrs.values()):
                yield {
                    "id": f"{document_id}:{segment['source_ref']}:{start}:{end}",
                    "document_id": document_id, "article": article, "clause": clause, "point": point,
                    "source_ref": segment["source_ref"], "start": start, "end": end,
                    "quote": quote, "values": attrs,
                }
        for child in node["children"]:
            yield from walk(child, article, clause, point)

    for article in tree["articles"]:
        yield from walk(article)


def relate(documents):
    """Return supported edges and review decisions for the covered provision roles."""
    roles = {}
    for document in documents:
        for row in document["attributes"]:
            role = row["values"].get("semantic_role")
            if role:
                endpoint = {**row, "number": document["number"],
                            "version_sha256": document["version_sha256"], "path": document["path"],
                            "source_url": document.get("source_url")}
                roles.setdefault(role["code"], []).append(endpoint)

    decisions = []
    for source in roles.get("sets_registration_time", []):
        source_scope = {"asset": "quyền sử dụng đất", "event": "đăng ký biện pháp bảo đảm"}
        for role in ("uses_registration_time", "uses_escrow_time"):
            for target in roles.get(role, []):
                conditions = [row for row in roles.get("contract_effective", [])
                              if row["document_id"] == target["document_id"]]
                if role == "uses_escrow_time":
                    status = "REJECTED"
                    reason = ("Cùng đề cập hiệu lực đối kháng. Khoản về ký quỹ dùng mốc gửi tài sản "
                              "vào tài khoản phong tỏa, khác mốc đăng ký quyền sử dụng đất.")
                elif target["number"] == "21/2021/NĐ-CP" and not conditions:
                    status = "NEEDS_REVIEW"
                    reason = "Thiếu căn cứ về hiệu lực hợp đồng tại khoản 1 Điều 23."
                else:
                    status = "SUPPORTED"
                    reason = ("Nguồn A xác định thời điểm ghi nhận đăng ký đối với quyền sử dụng đất. "
                              "Nguồn B dùng thời điểm đăng ký để xác định hiệu lực đối kháng; "
                              "cạnh chỉ áp dụng cho phần giao nhau này.")
                decisions.append({
                    "id": f"{RULE_ID}:{source['id']}:{target['id']}",
                    "type": "SEMANTIC", "relation": "REGISTRATION_TIME_APPLIES", "rule_id": RULE_ID,
                    "direction": "SOURCE_SETS_EVENT_USED_BY_TARGET", "status": status, "reason": reason,
                    "source_id": source["document_id"], "target_id": target["document_id"],
                    "source": source, "target": target, "scope": source_scope,
                    "context_evidence": conditions, "impact_status": "NOT_ASSESSED",
                })
    return decisions


def verify_change(edge, change):
    """Check only the supplied amendment instruction against this edge's source."""
    if edge["status"] != "SUPPORTED" or edge["source"]["document_id"] != change["target_id"]:
        return {"status": "NEEDS_REVIEW", "reason": "Chưa xác minh được liên kết với đích sửa."}
    if (change.get("kind") == "RENAME_ONLY" and change["evidence"].get("quote")
            and change.get("article") and edge["source"].get("article")):
        if str(change["article"]) != edge["source"]["article"]:
            return {
                "status": "NO_IMPACT_SHOWN",
                "reason": "Chỉ dẫn đổi tên cơ quan tại Điều khác chưa cho thấy thay đổi mốc đăng ký của cạnh.",
                "change": change, "edge_id": edge.get("id"),
            }
    return {"status": "NEEDS_REVIEW", "reason": "Cần đối chiếu trước/sau trong phạm vi cạnh.",
            "change": change, "edge_id": edge.get("id")}
