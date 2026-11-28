-- Run against the populated database. The result is one JSON document.
WITH node_json AS (
    SELECT d.id, json_object(
        'id', d.id, 'title', d.title, 'number', d.number, 'document_type', d.document_type,
        'issuer', d.issuer, 'source', d.source_uri, 'snapshot', d.snapshot, 'version', d.version,
        'full_text_status', d.full_text_status, 'legal_version_verified',
        json(CASE d.legal_version_verified WHEN 1 THEN 'true' ELSE 'false' END),
        'attributes', (SELECT json_group_array(json_object(
            'id', f.id, 'clause', f.clause, 'role', f.role, 'concept', f.concept_id,
            'actor', f.actor, 'activity', f.activity, 'object', f.object, 'modality', f.modality,
            'condition', f.condition_text, 'exception', f.exception_text,
            'actor_scope', f.actor_scope, 'use_scope', f.use_scope, 'territory', f.territory,
            'valid_from', f.valid_from, 'valid_to', f.valid_to,
            'qualifications_checked', json(CASE f.qualifications_checked WHEN 1 THEN 'true' ELSE 'false' END),
            'evidence', json_object('document_id', f.document_id,
                'source_refs', json_array(f.source_ref), 'quote', s.text)))
          FROM facet f JOIN source_block s USING(document_id, source_ref) WHERE f.document_id = d.id)
    ) AS payload FROM document d ORDER BY d.id
), edge_json AS (
    SELECT json_object(
        'id', CASE e.family WHEN 'DOCUMENT' THEN 'doc:' || e.reference_id
              ELSE 'sem:' || json_array(e.rule_id, e.provider_facet, e.consumer_facet) END,
        'source_id', e.source_id, 'target_id', e.target_id, 'family', e.family, 'relation', e.relation,
        'rule_id', e.rule_id, 'reason', r.explanation, 'source_facet_id', e.provider_facet,
        'target_facet_id', e.consumer_facet, 'impact_status', 'NOT_ASSESSED',
        'evidence', (SELECT json_group_array(json_object('document_id', s.document_id,
                       'source_refs', json_array(s.source_ref), 'quote', s.text))
                     FROM source_block s WHERE (s.document_id = e.source_id AND s.source_ref = e.source_ref)
                        OR (s.document_id = e.target_id AND s.source_ref = e.target_ref))
    ) AS payload FROM graph_edge e LEFT JOIN semantic_rule r ON r.id = e.rule_id
    ORDER BY e.family, e.source_id, e.target_id, e.provider_facet, e.consumer_facet
)
SELECT json_object('nodes', (SELECT json_group_array(json(payload)) FROM node_json),
                   'edges', (SELECT json_group_array(json(payload)) FROM edge_json),
                   'needs_review', (SELECT json_group_array(json_object('rule_id', rule_id,
                       'source_facet_id', provider_facet, 'target_facet_id', consumer_facet))
                       FROM semantic_pair WHERE status = 'NEEDS_REVIEW'));
