# ContextHub Graph Vocabulary

Nodes: `SourceFile`, `IcebergTable`, `Column`, `SQLAsset`.

Edges: `FEEDS`, `TRANSFORMS_INTO`, `HAS_COLUMN`, `READS_FROM`, `WRITES_TO`.

The generated JSON is a seed, not authoritative column lineage. Regex SQL parsing is deliberately simple; replace with SQLGlot / compiled query plan for robust lineage. Store Git SHA, code owner, governance policies, test coverage, execution outcomes, and semantic definitions as additional nodes/edges in a full production graph.

Example Cypher import approach: use Neo4j driver and allowlisted node labels and relationship types; MERGE nodes by `id`, edges by `(source, relation, target)`. Avoid constructing Cypher from unchecked strings.
