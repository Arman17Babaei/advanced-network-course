# Project Candidate: Network-Aware Immersive Scene Delivery

**Status:** Draft project candidate  
**Duration:** 7 weeks  
**Team:** 4 students  
**Expected effort:** approximately one 8-hour day per student per week (~28 person-days / 224 nominal person-hours)  
**AI:** course-provided coding agent is required for implementation, experimentation, debugging, and review.

## Project idea

Build and experimentally evaluate a small end-to-end system for **interactive delivery of an immersive 3D scene over a changing network**.

The project should start from an **existing 3D Gaussian Splatting (3DGS) scene, renderer/viewer, and preprocessing pipeline** rather than asking students to train a new representation or build a renderer from scratch. Recent systems such as **EdgeGaussian**, **L3GS**, and **Vega** show that immersive 3D delivery naturally couples scene representation, viewport-dependent usefulness, rendering placement, and network scheduling.

The course project narrows that design space to one networking question:

> **Can application-relevant information from a programmable network help an immersive scene-delivery system deliver the most useful content sooner under changing network conditions?**

A minimal target architecture is:

```text
pre-generated immersive scene
        |
        v
content/chunk server ---- delivery controller
        |                       ^
        v                       |
   P4/BMv2 network ---- network measurements
        |
        v
XR-like client/viewer
(viewpoint trace + QoE instrumentation)
```

The scene should be divided into a manageable number of **spatial chunks and/or quality layers**. At a given time, some data is immediately useful for the current viewport, some is likely to become useful soon, and some is background or enhancement data.

The network should include a controllable bottleneck and cross traffic. A small P4 program should expose application-relevant network state—such as traffic-class counters, link utilization, congestion, or queue information—to the controller. The controller then decides which scene content should be sent next and/or at what priority.

The project should compare at least:

- an **end-host-only baseline** that adapts using information available without programmable-network assistance; and
- a **P4-assisted policy** that incorporates network state from the programmable data plane.

The objective is **not** to prove that P4 is always better. A good project should identify when network visibility helps, how much it helps, what it costs, and when the extra information is unnecessary or actively harmful.

## Scope boundaries

The following are **not required** for the core project:

- training a 3DGS model;
- inventing a new 3D representation;
- implementing a new renderer;
- physical AR/VR headset deployment;
- dynamic/4D scene reconstruction;
- multi-user shared-world synchronization;
- in-network rendering or ML inference;
- large in-network caches;
- production-scale programmable hardware.

These may become stretch directions only after the baseline system, instrumentation, and main experiments work end-to-end.

The intended environment is a supplied or known-working viewer/scene plus a software P4 environment such as **BMv2 + Mininet + P4Runtime**. The project should spend its limited time on architecture, adaptation, and experimental reasoning rather than environment construction.

## Responsibility matrix

Each student owns one **implementation domain (column)** and one **cross-cutting design concern (row)**. Ownership means being able to implement, integrate, reason about, experiment with, and defend that area.

The matrix is **not a checklist of sixteen features**. Some intersections are central, some only need characterization, and some may prove irrelevant. The team should explicitly justify where effort is concentrated.

| Design concern ↓ / Implementation domain → | **Content pipeline** | **XR client/runtime** | **Programmable network** | **Delivery controller/server** |
| --- | --- | --- | --- | --- |
| **Latency & experiential quality** | **Strong:** which chunks/layers become useful first? | **Strong:** viewport response, visible quality, incomplete views | Relevant: how quickly useful congestion state becomes visible | **Strong:** what should be transmitted next? |
| **Scalability & capacity** | Light: larger scenes / more chunks | Light: higher viewpoint-change rate or limited multi-client test | Relevant: bottleneck sharing and cross traffic | Relevant: scheduling as demand grows |
| **Reliability & adaptation** | Light: behavior when chunks are late/missing | Relevant: graceful rendering with incomplete content | **Strong:** loss, delay, congestion, measurement freshness | **Strong:** recovery and reprioritization |
| **Resource efficiency** | **Strong:** bytes versus useful visual improvement | Light: client memory/render cost | Light: telemetry/control overhead | Relevant: stale/speculative bytes and wasted transmission |

**Strong** means the project is expected to contain an explicit design decision and experimental evidence at that intersection.  
**Relevant** means the interaction should be understood and defended, but may not require its own mechanism.  
**Light** means characterization or a justified decision that the concern is secondary may be sufficient.

Teams may revise these weights after initial experiments, but they should be able to explain why.

## Core research questions

### RQ1 — Does programmable-network visibility improve immersive delivery?

**Can a P4-assisted delivery policy reduce the time required to obtain useful/high-quality viewport content under changing network conditions compared with an end-host-only baseline?**

The experiment should examine conditions such as stable bandwidth, sudden capacity reduction, bursty competing traffic, and increased loss/delay.

Possible dependent variables include:

- time to a usable viewport;
- visible quality over time;
- time spent with incomplete or degraded content;
- stale or unused bytes delivered;
- total bytes transmitted.

### RQ2 — Which network information is actually useful?

**Which programmable-network signals provide enough additional information to change a good application-level decision?**

Candidates might include:

- per-class byte/packet counters;
- link utilization;
- queue occupancy or congestion indication;
- observed cross-traffic load;
- short-window rate estimates.

The team should avoid adding telemetry merely because it is available. The question is whether a particular signal enables a decision that the end-host-only system cannot make as well or as quickly.

### RQ3 — How should content utility and network state interact?

**How should the sender combine application knowledge about content importance with current network conditions when deciding what to transmit next?**

For example, the controller may distinguish among:

- immediately visible/base content;
- likely-next-view content;
- enhancement layers;
- speculative/background content.

The project should compare at least one reasonable baseline scheduling policy with the team's network-aware design.

### RQ4 — What does network assistance cost, and when does it stop helping?

**Under what workloads does programmable-network assistance provide little benefit or introduce unnecessary overhead, instability, or incorrect adaptation?**

Relevant costs include:

- telemetry traffic;
- controller/P4Runtime update rate;
- stale measurements;
- reaction oscillation;
- extra implementation complexity;
- unnecessary content reprioritization.

A negative result in some regimes is valuable if the team can explain it experimentally.

## Minimum experimental scenarios

The final experiment plan may evolve, but the core system should support at least these scenarios:

1. **Stable ample bandwidth** — establishes whether the network-aware mechanism adds unnecessary overhead when there is no bottleneck.
2. **Sudden bandwidth reduction** — tests response speed and adaptation.
3. **Bursty competing traffic** — tests whether direct bottleneck visibility improves content scheduling.
4. **Loss and/or additional delay** — tests robustness and distinguishes capacity problems from other network impairment.

A small scale/capacity experiment—larger scene, more chunks, or a small number of simultaneous clients—may be included, but should not displace the main end-to-end experiments.

## Expected system outcome

By the middle of the project, the team should have a complete baseline path:

```text
scene -> server -> emulated programmable network -> client/viewer -> measurements
```

The remaining project time should be used primarily for **design iteration and experiments**, not for expanding the feature set.

A successful final project is therefore not the largest XR implementation. It is a system where the team can defend:

- why the selected network information is useful;
- how that information changes content-delivery decisions;
- what user-visible or resource-level effect follows;
- how the mechanism behaves under stress and failure;
- which parts of the architecture matter most and which matrix intersections do not;
- what the experiments support, and what they do not support.

## Research grounding

The scope is intentionally derived from recent immersive-systems work while removing components that would consume the semester without strengthening the networking question:

- **EdgeGaussian: Real-time Free-Viewpoint Video for Mobile VR via Edge-Client Collaborative Neural Rendering** — ACM MobiCom 2025. Motivates splitting immersive rendering/content processing across client and edge.  
  https://doi.org/10.1145/3680207.3765245
- **L3GS: Layered 3D Gaussian Splats for Efficient 3D Scene Delivery** — ACM MobiCom 2025. Motivates layered/spatial scene delivery, viewport-dependent usefulness, scheduling, and experiments using network/viewpoint traces.  
  https://arxiv.org/abs/2504.05517
- **Vega: Fully Immersive Mobile Volumetric Video Streaming with 3D Gaussian Splatting** — ACM MobiCom 2025. Demonstrates the interaction among volumetric representation, mobile rendering, bandwidth, and streaming decisions.  
  https://www.sigmobile.org/mobicom/2025/accepted.html
- **ProxLink: A Lightweight Decentralized Synchronization Framework for Multi-User XR** — ACM MobiCom 2026. Shows that multi-user synchronization is itself a substantial systems problem; it is therefore deliberately excluded from the required seven-week core.  
  https://www.sigmobile.org/mobicom/2026/accepted.html
- **P4: Programming Protocol-Independent Packet Processors** — ACM SIGCOMM CCR, 2014. Foundational motivation for exposing application-relevant behavior through a programmable data plane.  
  https://doi.org/10.1145/2656877.2656890
- **P4 Tutorials** — P4.org/p4lang maintained tutorials for BMv2, Mininet, P4Runtime, counters, and programmable-switch exercises; intended as the implementation starting point rather than asking teams to construct the P4 environment themselves.  
  https://github.com/p4lang/tutorials
