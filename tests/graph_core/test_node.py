import pytest
from src.graph_core.node import Node


class TestNodeFields:
    def test_core_fields_present(self):
        """R1 + next_edges: Seven core fields exist on every Node."""
        core_fields = {"id", "type", "payload_ref", "parents", "children", "tags", "next_edges"}
        verdict_fields = {"verdict", "confidence", "evidence_runs", "contradicts", "supports"}
        node = Node(id="n1", type="idea")
        all_fields = set(vars(node).keys())
        # Core fields always present
        assert core_fields.issubset(all_fields), f"Missing core fields: {core_fields - all_fields}"
        # Verdict fields present (may be None/empty)
        assert verdict_fields.issubset(all_fields), f"Missing verdict fields: {verdict_fields - all_fields}"
        # Core values correct for default construction
        assert node.id == "n1"
        assert node.type == "idea"
        assert node.payload_ref is None
        assert node.parents == set()
        assert node.children == set()
        assert node.tags == set()
        assert node.next_edges == []

    def test_id_type_required(self):
        """id and type are mandatory positional args."""
        node = Node("n1", "idea")
        assert node.id == "n1"
        assert node.type == "idea"

    def test_payload_ref_defaults_to_none(self):
        """payload_ref is None when not provided."""
        node = Node("n1", "idea")
        assert node.payload_ref is None

    def test_parents_defaults_to_empty_set(self):
        """parents is an empty set when not provided."""
        node = Node("n1", "idea")
        assert node.parents == set()

    def test_children_defaults_to_empty_set(self):
        """children is an empty set when not provided."""
        node = Node("n1", "idea")
        assert node.children == set()

    def test_tags_defaults_to_empty_set(self):
        """tags is an empty set when not provided."""
        node = Node("n1", "idea")
        assert node.tags == set()


class TestNodeStructure:
    def test_root_node_no_parents(self):
        """R1.2: No-parent node is accepted as root."""
        node = Node(id="n1", type="idea", parents=set())
        assert node.parents == set()

    def test_leaf_node_no_children(self):
        """R1.2: No-child node is accepted as leaf."""
        node = Node(id="n1", type="idea", children=set())
        assert node.children == set()

    def test_node_with_parents_and_children(self):
        """Full node with all fields populated."""
        node = Node(
            id="n1",
            type="hypothesis",
            payload_ref="ref-42",
            parents={"p1", "p2"},
            children={"c1"},
            tags={"tag-a", "tag-b"},
            next_edges=["v1", "v2"],
        )
        assert node.id == "n1"
        assert node.type == "hypothesis"
        assert node.payload_ref == "ref-42"
        assert node.parents == {"p1", "p2"}
        assert node.children == {"c1"}
        assert node.tags == {"tag-a", "tag-b"}
        assert node.next_edges == ["v1", "v2"]


class TestVerdictMetadataFields:
    """Verdict metadata fields loaded by loader (chain-engine extension)."""

    def test_verdict_node_has_proved(self):
        """A verdict node with verdict=proved has those fields populated."""
        node = Node(
            id="verdict:test",
            type="verdict",
            verdict="proved",
            confidence=0.95,
            evidence_runs=["run1", "run2"],
            contradicts=["verdict:other"],
            supports=[],
        )
        assert node.verdict == "proved"
        assert node.confidence == 0.95
        assert node.evidence_runs == ["run1", "run2"]
        assert node.contradicts == ["verdict:other"]
        assert node.supports == []

    def test_non_verdict_node_defaults(self):
        """Non-verdict nodes have verdict fields as None/empty."""
        node = Node(id="hyp:test", type="hypothesis")
        assert node.verdict is None
        assert node.confidence is None
        assert node.evidence_runs == []
        assert node.contradicts == []
        assert node.supports == []


class TestNodeTagsIsolation:
    def test_tags_mutation_does_not_affect_parents(self):
        """R1.4: Mutating tags does not affect parents/children."""
        node = Node(id="n1", type="idea", parents={"p1"}, children={"c1"}, tags={"x"})
        original_parents = node.parents.copy()
        node.tags.add("y")
        assert node.parents == original_parents

    def test_tags_mutation_does_not_affect_children(self):
        """R1.4: Mutating tags does not affect children."""
        node = Node(id="n1", type="idea", parents={"p1"}, children={"c1"}, tags={"x"})
        original_children = node.children.copy()
        node.tags.add("y")
        assert node.children == original_children

    def test_tags_independent_from_typed_links(self):
        """R1.4: tags is independent of typed links."""
        node = Node(
            id="n1",
            type="idea",
            parents={"p1", "p2"},
            children={"c1", "c2", "c3"},
            tags={"urgent", "tier-1"},
        )
        assert node.tags != node.parents
        assert node.tags != node.children
        node.tags.clear()
        assert node.parents == {"p1", "p2"}
        assert node.children == {"c1", "c2", "c3"}
