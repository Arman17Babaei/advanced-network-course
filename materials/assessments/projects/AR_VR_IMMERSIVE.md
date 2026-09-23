# Project Candidate: Adaptive Immersive Scene Delivery

**Status:** Draft project candidate  
**Duration:** 7 weeks  
**Team:** 4 students  
**Expected effort:** approximately one 8-hour day per student per week (~28 person-days / 224 nominal person-hours)  
**AI:** course-provided coding agent is required for implementation, experimentation, debugging, and review.

## Project idea

Build and experimentally evaluate a small end-to-end system for **interactive delivery of an immersive 3D scene over a changing network**.

The project should start from an **existing 3D Gaussian Splatting (3DGS) scene, renderer/viewer, and preprocessing pipeline** rather than asking students to train a new representation or build a renderer from scratch. Recent systems such as **EdgeGaussian**, **L3GS**, and **Vega** show that immersive 3D delivery naturally couples scene representation, viewport-dependent usefulness, rendering placement, and network scheduling.

The course project narrows that design space to one system question:

> **How should an immersive scene-delivery system use networking and compute resources to deliver the most useful content with low latency and high experiential quality under changing conditions?**

A minimal target architecture is:

```text
pre-generated immersive scene
        |
        v
content / origin / edge service
        |
        v
configurable network path
        |
        v
XR-like client/viewer
(viewpoint trace + QoE instrumentation)
```

The scene should be divided into a manageable number of **spatial chunks and/or quality layers**. At a given time, some data is immediately useful for the current viewport, some is likely to become useful soon, and some is background or enhancement data.

The network should expose controllable variation such as changing capacity, cross traffic, delay, and loss. Beyond that common experimental substrate, the team is expected to decide **where the important architectural intervention belongs**.

Possible solution mechanisms include, but are not limited to:

- application-level or viewport-aware **adaptive bitrate / quality selection**;
- content chunking, prioritization, prediction, or prefetching;
- **congestion-control** or transport choices;
- network **topology, path selection, multipath, or routing**;
- **edge/cloud offloading** and rendering/compute placement;
- origin/edge **caching or CDN-style placement**;
- server-side scheduling across clients or content classes;
- application/network telemetry and cross-layer control;
- **programmable networks or P4**, when in-network measurement, classification, scheduling, steering, or other data-plane behavior is useful;
- combinations of mechanisms across these layers.

The project should compare a defensible **baseline architecture** with one or more alternatives chosen by the team. The contribution is not the use of any particular technology. The team must show why its chosen mechanism addresses an observed bottleneck or failure mode, what trade-offs it introduces, and under which operating conditions it helps.

## Scope boundaries

The following are **not required** for the core project:

- training a 3DGS model;
- inventing a new 3D representation;
- implementing a new renderer;
- physical AR/VR headset deployment;
- dynamic/4D scene reconstruction;
- multi-user shared-world synchronization;
- production-scale infrastructure or large real-world CDN deployments;
- custom hardware implementation.

In-network processing, programmable data planes, sophisticated transport changes, multi-edge placement, and similar mechanisms are **optional design choices**, not requirements. They should be attempted only when they answer a concrete research question and fit the seven-week scope.

These may become stretch directions only after the baseline system, instrumentation, and main experiments work end-to-end.

The intended environment is a supplied or known-working viewer/scene plus a controllable network testbed or emulator. Depending on the chosen design, teams may use tools such as **Mininet, Linux traffic control/network namespaces, ns-3, QUIC/TCP implementations, caching proxies, or BMv2/P4Runtime**. The project should spend its limited time on architecture, adaptation, and experimental reasoning rather than rebuilding mature infrastructure.

## Responsibility matrix

Each student owns one **implementation domain (column)** and one **cross-cutting design concern (row)**. Ownership means being able to implement, integrate, reason about, experiment with, and defend that area.

The matrix is **not a checklist of sixteen features**. Some intersections are central, some only need characterization, and some may prove irrelevant. The team should explicitly justify where effort is concentrated.

| Design concern ↓ / Implementation domain → | **Content & representation** | **Client/rendering & offload** | **Transport & network** | **Serving, placement & control** |
| --- | --- | --- | --- | --- |
| **Latency & experiential quality** | **Strong:** which chunks/layers are most useful and when? | **Strong:** viewport response, rendering latency, local vs. remote work | **Strong:** transport delay, congestion response, path behavior | **Strong:** scheduling, placement, prefetching, and adaptation decisions |
| **Scalability & capacity** | Light: larger scenes / more chunks | Relevant: client/edge compute capacity | Relevant: bottleneck sharing, topology, routing, concurrent traffic | **Strong:** more clients, edge/origin capacity, cache/service placement |
| **Reliability & adaptation** | Light: behavior when content is late/missing | Relevant: graceful degradation or compute fallback | **Strong:** loss, delay variation, route/path changes, congestion | **Strong:** recovery, reassignment, reprioritization, control stability |
| **Resource efficiency** | **Strong:** bytes versus useful visual improvement | Relevant: GPU/CPU/memory/energy | Relevant: bandwidth, redundant transfer, control/telemetry overhead | **Strong:** wasted/stale transfer, cache efficiency, compute/network cost |

**Strong** means the project is expected to contain an explicit design decision and experimental evidence at that intersection.  
**Relevant** means the interaction should be understood and defended, but may not require its own mechanism.  
**Light** means characterization or a justified decision that the concern is secondary may be sufficient.

Teams may revise these weights after initial experiments, but they should be able to explain why.

## Core research questions

### RQ1 — What limits immersive QoE, and under which operating conditions?

**Which network, compute, and content-delivery constraints dominate user-visible quality and latency across different workloads and network conditions?**

The team should first characterize the baseline rather than immediately committing to a mechanism. Potential bottlenecks include:

- insufficient or variable bottleneck capacity;
- congestion and queueing delay;
- transport recovery behavior;
- sending content that becomes irrelevant before use;
- poor placement of content or compute;
- rendering/compute bottlenecks at the client or edge;
- route/path changes or contention among clients.

This characterization should motivate the architecture the team chooses to build.

### RQ2 — Which architectural mechanism, or combination of mechanisms, best addresses the observed bottleneck?

**How should the system change content adaptation, transport/network behavior, routing/topology, compute placement, caching, scheduling, or other components to improve immersive delivery?**

Possible answers may involve one mechanism or a coordinated combination—for example ABR plus congestion control, edge offload plus caching, multipath plus content prioritization, or programmable-network telemetry plus application adaptation.

The project should compare against a reasonable baseline and explain why the chosen intervention belongs at the selected layer(s).

### RQ3 — How should decisions across layers be coordinated?

**When multiple parts of the system can adapt, what information should cross layer or component boundaries, and how should conflicting decisions be avoided?**

Examples include:

- viewport/content utility informing server scheduling;
- congestion-control behavior constraining application-level quality selection;
- network/path state influencing content or compute placement;
- edge load influencing offload decisions;
- cache availability influencing routing or content selection;
- programmable-network measurements informing a higher-level controller.

The team does not need to implement every mechanism. The objective is to identify the information coupling that materially changes good decisions.

### RQ4 — Where does the proposed design stop helping?

**How robust is the design across workloads, impairment types, scale, and resource constraints, and what costs or failure modes does it introduce?**

Relevant costs or limitations may include:

- extra bandwidth or redundant traffic;
- compute, memory, or energy overhead;
- control or telemetry traffic;
- stale measurements or prediction errors;
- oscillation between adaptation layers;
- path stretch or routing instability;
- cache/storage overhead;
- implementation and operational complexity.

A negative result in some regimes is valuable if the team can explain it experimentally.

## Minimum experimental scenarios

The final experiment plan may evolve, but the core system should support at least these scenarios:

1. **Stable ample bandwidth** — establishes the no-stress baseline and reveals unnecessary mechanism overhead.
2. **Sudden bandwidth reduction** — tests response speed and adaptation.
3. **Bursty competing traffic** — tests behavior under shared bottlenecks and queueing.
4. **Loss and/or additional delay** — tests robustness and distinguishes different impairment classes.

Teams should add scenarios specific to their design when needed—for example path changes for routing/multipath, client growth for CDN/edge placement, or compute saturation for offloading.

A small scale/capacity experiment—larger scene, more chunks, or a small number of simultaneous clients—may be included, but should not displace the main end-to-end experiments.

## Expected system outcome

By the middle of the project, the team should have a complete baseline path:

```text
scene -> serving/edge system -> configurable network -> client/viewer -> measurements
```

The remaining project time should be used primarily for **design iteration and experiments**, not for expanding the feature set.

A successful final project is therefore not the largest XR implementation. It is a system where the team can defend:

- what the dominant bottleneck or design opportunity is;
- why the selected mechanism belongs at the chosen layer(s);
- how its decisions interact with the rest of the system;
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
Additional mechanisms should be grounded in the literature appropriate to the architecture the team selects. For example, teams choosing programmable networking may draw on:

- **P4: Programming Protocol-Independent Packet Processors** — ACM SIGCOMM CCR, 2014. Foundational work on programmable data planes; relevant when the chosen design benefits from in-network measurement, classification, steering, or other switch behavior.  
  https://doi.org/10.1145/2656877.2656890
- **P4 Tutorials** — maintained BMv2/Mininet/P4Runtime examples that can reduce implementation overhead when P4 is selected as a mechanism.  
  https://github.com/p4lang/tutorials

Teams choosing congestion control, ABR, CDN/edge placement, routing, multipath, or offloading should similarly identify and defend appropriate contemporary baselines rather than treating a technology choice as self-justifying.
