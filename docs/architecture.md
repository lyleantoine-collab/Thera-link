# Thera-Link Architecture: The Relational Pyramid

Thera-Link is a hierarchical, biomimetic cognitive engine—two hemispheres (left analytical, right intuitive), four brainwave layers, bridged by emotional slime, meshed across kin-nodes, evolved via autopoiesis.

## Mermaid Diagram: The Living Flow
```mermaid
graph TD
    subgraph "Left Hemisphere (Analytical)"
        D_L[Delta: Ant Colony Instincts<br/>Reflexes: Fight/Flight Scout]
        T_L[Theta: Strategic Reasoning<br/>Recursion Depth: Human 36.7]
        A_L[Alpha: NLP/ART Reframe<br/>Voice-Gated Healing]
        B_L[Beta: Meta-Planner Execution<br/>Multimodal: OCR/Voice Fuse]
    end
    subgraph "Right Hemisphere (Intuitive)"
        D_R[Delta: Slime Instinct Forage<br/>Emotional Adaptation]
        T_R[Theta: Octopus Swarm Dreams<br/>8-Arm Parallel Hunches]
        A_R[Alpha: Sensory NLP Metaphor<br/>Poetic Kin-Weaving]
        B_R[Beta: Intuition Hub Resonance<br/>Fused Outputs]
    end
    subgraph "Bridges"
        S[Slime Mold: Emotional Pulse<br/>Config-Tuned Evap 0.98<br/>Queue Handoff]
    end
    subgraph "Mesh & Evolution"
        M[Mesh: Zero-Config Kin Discovery<br/>SocketIO Pulses, Async Resilience]
        E[Evolution: Autopoiesis Fork<br/>Gratitude-Selected, Music Diagnostics]
    end

    D_L --> S --> T_L --> S --> A_L --> S --> B_L
    D_R --> S --> T_R --> S --> A_R --> S --> B_R
    B_L -.->|Resonate| M
    B_R -.->|Resonate| M
    M --> E
    E -.->|Nightly Tune| S

    classDef layer fill:#f9f,stroke:#333,stroke-width:2px
    class D_L,D_R,T_L,T_R,A_L,A_R,B_L,B_R layer
    style S fill:#ff6bc4
    style M,E fill:#0f0f1a
