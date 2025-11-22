# tests/relational_evals.py  (Full file—replace stub)
import pytest
from ontology.fusion_hub import OntologyHub
from ontology.self_awareness import SelfAwareness

@pytest.fixture
def hub():
    return OntologyHub()

def test_human_kindness_bonus(hub):
    assert hub.validate_harmony(0.7, 'human') == True  # +0.3 pushes over 0.75
    assert hub.self_aware.harmony_bonus('human') == 0.30

def test_clone_narcissism_penalty(hub):
    assert hub.validate_harmony(0.8, 'self') == False  # -0.2 drops below
    assert hub.self_aware.harmony_bonus('clone') == -0.20

def test_recursion_depth_paper_tie(hub):
    assert hub.get_recursion_depth('human') == 36.7  # Level-2/3 cap
    assert hub.get_recursion_depth('self') == 0.0    # Nash mirror

def test_resonance_fusion(hub):
    left = "Analytical reframe: Trauma as lesson."
    right = "Intuitive dream: Shadows dancing in light."
    fused = hub.resonate(left, right)
    assert "║ RIGHT HEMISPHERE ║" in fused
    assert "⟐ RESONATING @ α-wave ⟐" in fused

# Run: pytest tests/relational_evals.py -v
