PRAGMA foreign_keys = ON;
BEGIN;
-- One row per document version in one fixed corpus snapshot.
CREATE TABLE document (
    id TEXT PRIMARY KEY NOT NULL,
    snapshot TEXT NOT NULL,
    version TEXT NOT NULL,
    title TEXT NOT NULL,
    number TEXT,
    document_type TEXT,
    issuer TEXT,
    source_uri TEXT,
    full_text_status TEXT NOT NULL,
    legal_version_verified INTEGER NOT NULL CHECK (legal_version_verified IN (0, 1))
);
CREATE TABLE source_block (
    document_id TEXT NOT NULL REFERENCES document(id),
    source_ref TEXT NOT NULL,
    text TEXT NOT NULL CHECK (length(trim(text)) > 0),
    PRIMARY KEY (document_id, source_ref)
);
-- Reviewed vocabulary. Two phrases may map to the same concept only in context.
CREATE TABLE concept (id TEXT PRIMARY KEY NOT NULL, meaning TEXT NOT NULL);
CREATE TABLE semantic_rule (
    id TEXT PRIMARY KEY NOT NULL,
    provider_role TEXT NOT NULL,
    consumer_role TEXT NOT NULL,
    explanation TEXT NOT NULL,
    UNIQUE (provider_role, consumer_role)
);
INSERT INTO semantic_rule VALUES
 ('CONDITION', 'SETS_CONDITION', 'USES_CONDITION', 'A đặt điều kiện mà hoạt động trong B phải đáp ứng.'),
 ('DEFINITION', 'DEFINES', 'USES_DEFINITION', 'A định nghĩa khái niệm mà quy định trong B sử dụng theo nghĩa đó.'),
 ('PROCEDURE', 'SETS_PROCEDURE', 'REQUIRES_PROCEDURE', 'A quy định thủ tục mà B yêu cầu thực hiện.'),
 ('LIMIT', 'SETS_LIMIT', 'USES_LIMIT', 'A đặt ngưỡng hoặc thời hạn áp dụng cho hoạt động trong B.');
-- A facet describes ONE legal proposition, never an entire document by keyword.
CREATE TABLE facet (
    id TEXT PRIMARY KEY NOT NULL,
    document_id TEXT NOT NULL,
    source_ref TEXT NOT NULL,
    clause TEXT NOT NULL,
    role TEXT NOT NULL CHECK (role IN ('SETS_CONDITION','USES_CONDITION','DEFINES',
        'USES_DEFINITION','SETS_PROCEDURE','REQUIRES_PROCEDURE','SETS_LIMIT','USES_LIMIT')),
    concept_id TEXT NOT NULL REFERENCES concept(id),
    actor TEXT, activity TEXT, object TEXT, modality TEXT, condition_text TEXT, exception_text TEXT,
    -- Normalized applicable groups. '*' explicitly covers all in THIS dimension; NULL is unknown.
    actor_scope TEXT, use_scope TEXT, territory TEXT,
    valid_from TEXT, valid_to TEXT,
    -- Set only after checking qualifications and exceptions in context.
    qualifications_checked INTEGER NOT NULL CHECK (qualifications_checked IN (0, 1)),
    CHECK (valid_from IS NULL OR (date(valid_from) IS NOT NULL AND date(valid_from) = valid_from)),
    CHECK (valid_to IS NULL OR (date(valid_to) IS NOT NULL AND date(valid_to) = valid_to)),
    CHECK (valid_from IS NULL OR valid_to IS NULL OR valid_from <= valid_to),
    FOREIGN KEY (document_id, source_ref) REFERENCES source_block(document_id, source_ref)
);
-- Only record a resolved target. Unresolved mentions remain in the source for review.
CREATE TABLE document_reference (
    id TEXT PRIMARY KEY NOT NULL, source_id TEXT NOT NULL, target_id TEXT NOT NULL REFERENCES document(id),
    source_ref TEXT NOT NULL, relation TEXT NOT NULL CHECK (relation IN
        ('CITES','BASIS','AMENDS','SUPPLEMENTS','REPEALS')),
    CHECK (source_id <> target_id),
    FOREIGN KEY (source_id, source_ref) REFERENCES source_block(document_id, source_ref)
);
CREATE INDEX facet_by_concept_role ON facet(concept_id, role);
CREATE VIEW semantic_pair AS
SELECT r.id AS rule_id, a.id AS provider_facet, b.id AS consumer_facet,
       a.document_id AS source_id, b.document_id AS target_id,
       CASE
         WHEN (a.territory <> b.territory AND a.territory <> '*' AND b.territory <> '*')
           OR (a.actor_scope <> b.actor_scope AND a.actor_scope <> '*' AND b.actor_scope <> '*')
           OR (a.use_scope <> b.use_scope AND a.use_scope <> '*' AND b.use_scope <> '*')
           OR a.valid_from > b.valid_to OR b.valid_from > a.valid_to THEN 'OUT_OF_SCOPE'
         WHEN a.territory IS NULL OR b.territory IS NULL OR a.actor_scope IS NULL OR b.actor_scope IS NULL
           OR a.use_scope IS NULL OR b.use_scope IS NULL OR a.valid_from IS NULL OR b.valid_from IS NULL
           OR a.valid_to IS NULL OR b.valid_to IS NULL
           OR a.qualifications_checked = 0 OR b.qualifications_checked = 0 THEN 'NEEDS_REVIEW'
         ELSE 'SUPPORTED_IN_SCOPE'
       END AS status
FROM semantic_rule r
JOIN facet a ON a.role = r.provider_role
JOIN facet b ON b.role = r.consumer_role AND b.concept_id = a.concept_id AND b.document_id <> a.document_id
JOIN document da ON da.id = a.document_id
JOIN document db ON db.id = b.document_id AND db.snapshot = da.snapshot;
-- Parallel edges are intentional. A semantic edge names the specific pair of provisions.
CREATE VIEW graph_edge AS
SELECT 'DOCUMENT' AS family, d.relation, d.source_id, d.target_id,
       d.source_ref, NULL AS target_ref, NULL AS provider_facet, NULL AS consumer_facet,
       NULL AS rule_id, d.id AS reference_id
FROM document_reference d
UNION ALL
SELECT 'SEMANTIC', 'MAY_AFFECT', p.source_id, p.target_id, a.source_ref, b.source_ref,
       a.id, b.id, p.rule_id, NULL
FROM semantic_pair p
JOIN facet a ON a.id = p.provider_facet
JOIN facet b ON b.id = p.consumer_facet
WHERE p.status = 'SUPPORTED_IN_SCOPE';
COMMIT;
