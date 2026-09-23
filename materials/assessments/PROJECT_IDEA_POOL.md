# Project Idea Pool

This page is a **project-area idea pool** for the Fall 2026 Advanced Networks course. It is not yet the final set of released project briefs.

The goal is to identify **application-oriented networked systems domains** where:
- the application imposes recognizable networking constraints;
- students can make and defend end-to-end architecture decisions;
- there is enough recent research activity to ground the project in contemporary systems work;
- practical tools, simulators, emulators, traces, or open implementations are likely to make a substantial semester project feasible.

The research scan below treats “post-2024” as **2025 and 2026 work available by 23 September 2026**. The primary corpus screened was the main-track paper lists of SIGCOMM 2025/2026, NSDI 2025/2026, and MobiCom 2025/2026.

A paper is counted for an application only when the **application itself is central to the problem/system**, not merely an evaluation workload. Counts are conservative lower bounds; one paper may appear in more than one application area.

The paper lists below are **representative references, not complete bibliographies** for every paper counted. Every reference is given with its full title and, where available, a direct paper/publication link.

## Summary

### Corpus screened

| Venue | Papers screened |
| --- | ---: |
| SIGCOMM 2025 | 88 |
| SIGCOMM 2026 | 110 |
| NSDI 2025 | 83 |
| NSDI 2026 | 150 |
| MobiCom 2025 | 77 |
| MobiCom 2026 | 87 |
| **Total** | **595** |

### Application-area signal

| Application area | Recent main-track papers found | Initial project-design signal |
| --- | ---: | --- |
| **Large-scale AI training** | **≥35** | Extremely active research area; strong architecture depth, but realistic experimentation may require abstraction/simulation because production-scale GPU clusters are unavailable. |
| **Distributed AI inference** | **≥18** | Strong systems/network interaction around placement, KV movement, disaggregation, MoE communication, latency, and heterogeneous resources. |
| **Large-scale video streaming** | **≥15** | Excellent project family: strong QoE metrics, public tools/traces, CDN/ABR/caching choices, and meaningful network/application interaction. |
| **AR/VR and immersive applications** | **≥11** | Strong fit for application-driven design: latency, rendering placement, bandwidth, localization, and mobility interact naturally. |
| **Massive IoT / smart environments** | **≥11** | Broad tool ecosystem and many deployment constraints, but final briefs should avoid generic “IoT” and anchor projects in a concrete application. |
| **Video conferencing / RTC** | **≥9** | Excellent fit: latency, rate control, SFU architecture, heterogeneous clients, loss recovery, and QoE are directly observable. |
| **Networked robotics / drones** | **≥7** | Strong project candidate where communication directly affects sensing/control; simulation and robotics frameworks make experimentation plausible. |
| **Vehicular / autonomous transportation** | **≥5** | Particularly attractive application domain because mobility, deadlines, sensing, computation placement, and safety constraints are explicit. |
| **Edge video analytics** | **≥5** | Useful intersection of network and compute design: what to send, compress, infer locally, schedule, or discard under bandwidth constraints. |
| **Cloud gaming** | **≥4** | Compact but high-quality research cluster; unusually clean latency/QoE constraints and practical client/server experimentation opportunities. |
| **Satellite remote sensing** | **≥4** | Interesting constrained-systems project family: predictable mobility, intermittent contacts, large data objects, storage, scheduling, and downlink constraints. |
| **Direct-to-device satellite communication** | **≥4** | Young but rapidly developing; strong mobility/handover/capacity constraints, though realistic infrastructure access is limited. |
| **Smart grid / energy infrastructure** | **≥4** | Some recent systems work, but much of it is monitoring/inspection rather than grid-control networking; needs careful scoping. |
| **Live interactive broadcasting** | **≥4** | Good combination of large fan-out and latency sensitivity; overlaps substantially with RTC/video infrastructure. |
| **Industrial automation** | **≥2** | Conceptually strong, but relatively sparse in the screened flagship networking corpus. |
| **Emergency / disaster response** | **≥1** | Strong constraints and social relevance, but current flagship-paper density is low; likely needs workshop/specialized-venue references. |
| **Collaborative AR / shared virtual worlds** | **≥1** | Promising as a specialized XR project, especially around synchronization and consistency/latency trade-offs. |
| **Teleoperation** | **0 main-track hits** | Still active in robotics/networking workshops and specialized venues; not absent as a research problem, but weak in this flagship corpus. |
| **Multiplayer online games** | **0 main-track hits** | Cloud gaming is active, but networked multiplayer state synchronization itself is sparse in the screened main tracks. |
| **Content delivery in poor-connectivity regions** | **0 main-track hits** | Valuable problem, but this scan did not find a recent flagship cluster; would need deliberately curated specialized/canonical references. |

## 1. Large-scale AI training

**Application constraints.** Distributed training creates structured, repeated communication patterns such as all-reduce, all-to-all, parameter/activation movement, and pipeline transfers. Performance depends on topology, job placement, congestion, collective scheduling, failures, and load imbalance.

**Why it could become a course project.** The network is directly in the critical path and architecture decisions have measurable job-completion consequences. The main concern is experimental realism: student projects would probably need emulation/simulation or small-cluster scale-down rather than pretending to reproduce hyperscale environments.

**Representative recent references**
- **ByteScale: Communication-Efficient Scaling of LLM Training with a 2048K Context Length on 16384 GPUs** — ACM SIGCOMM 2025.  
  https://ir.pku.edu.cn/handle/20.500.11897/771313
- **MixNet: A Runtime Reconfigurable Optical-Electrical Fabric for Distributed Mixture-of-Experts Training** — ACM SIGCOMM 2025.  
  https://mixnet-project.github.io/
- **Coflow Scheduling for LLM Training** — ACM SIGCOMM 2025 short paper; presents Hermod, a coflow scheduler for LLM training.  
  https://xcwanandy.github.io/papers/2025/hermod-sigcomm25short.pdf
- **Astral: A Datacenter Infrastructure for Large Language Model Training at Scale** — ACM SIGCOMM 2025.  
  https://conferences.sigcomm.org/sigcomm/2025/accepted-papers/

## 2. Distributed AI inference

**Application constraints.** Modern inference systems move activations, parameters, KV caches, and requests across heterogeneous accelerators and network tiers. Tail latency, batching, placement, disaggregation, and failure handling interact strongly.

**Why it could become a course project.** Students can study the application/network boundary directly: function placement, resource scheduling, request routing, disaggregation, and congestion can all be changed and experimentally defended.

**Representative recent references**
- **MegaScale-Infer: Efficient Mixture-of-Experts Model Serving with Disaggregated Expert Parallelism** — ACM SIGCOMM 2025.  
  https://doi.org/10.1145/3718958.3750506
- **DualPath: Accelerating Agentic LLM Inference by Harvesting Disaggregated KV-Cache Storage I/O** — ACM SIGCOMM 2026.  
  https://everythinginsigcomm.group/t/dualpath-accelerating-agentic-llm-inference-by-harvesting-disaggregated-kv-cache-storage-i-o/459
- **KVServe: Service-Aware KV Cache Compression for Communication-Efficient Disaggregated LLM Serving** — ACM SIGCOMM 2026.  
  https://conferences.sigcomm.org/sigcomm/2026/program/papers/

## 3. Large-scale video streaming

**Application constraints.** Streaming must jointly manage bitrate adaptation, CDN/server placement, caching, startup delay, rebuffering, bandwidth variation, and huge demand skew.

**Why it could become a course project.** This is one of the cleanest application-oriented choices: students can observe user-visible QoE, implement alternatives, use realistic traces, and reason simultaneously about application, transport, CDN, and resource-allocation layers.

**Representative recent references**
- **HyperEdge: An Edge CDN Infrastructure for Cost Efficient Video Streaming** — USENIX NSDI 2026.  
  https://www.usenix.org/conference/nsdi26/presentation/wei
- **Syntra: Synthesizing Cross-Layer Controllers for Low-Latency Video Streaming** — USENIX NSDI 2026.  
  https://www.usenix.org/conference/nsdi26/presentation/pan
- **Morphe: High-Fidelity Generative Video Streaming with Vision Foundation Model** — USENIX NSDI 2026.  
  https://www.usenix.org/conference/nsdi26/presentation/gong
- **Predict, Prune, Play: Efficient Video Playback Optimization Under Device Diversity and Drift** — USENIX NSDI 2026.  
  https://www.usenix.org/conference/nsdi26/presentation/sharma

## 4. AR/VR and immersive applications

**Application constraints.** Immersive applications combine high data rates, strict motion-to-photon latency, localization, rendering placement, mobility, and sometimes multi-user synchronization.

**Why it could become a course project.** The application naturally creates decisions across device, edge, transport, rendering, and wireless/network layers; different architectures yield clear performance/quality trade-offs.

**Representative recent references**
- **EdgeGaussian: Real-time Free-Viewpoint Video for Mobile VR via Edge-Client Collaborative Neural Rendering** — ACM MobiCom 2025.  
  https://www.sigmobile.org/mobicom/2025/program.html
- **L3GS: Layered 3D Gaussian Splats for Efficient 3D Scene Delivery** — ACM MobiCom 2025.  
  https://www.sigmobile.org/mobicom/2025/program.html
- **Vega: Fully Immersive Mobile Volumetric Video Streaming with 3D Gaussian Splatting** — ACM MobiCom 2025.  
  https://www.sigmobile.org/mobicom/2025/accepted.html
- **ProxLink: A Lightweight Decentralized Synchronization Framework for Multi-User XR** — ACM MobiCom 2026.  
  https://www.sigmobile.org/mobicom/2026/accepted.html

## 5. Massive IoT / smart environments

**Application constraints.** Large populations of constrained devices create heterogeneous traffic, energy limits, intermittent links, scalability problems, mobility, and management challenges.

**Why it could become a course project.** A project must be anchored in a concrete application—smart building, sensing infrastructure, environmental monitoring, etc.—rather than generic protocol work.

**Representative recent references**
- **Towards Next-Generation Global IoT: Empowering Massive Connectivity with Harmonious Multi-Network Coexistence** — ACM SIGCOMM 2025.  
  https://web.comp.polyu.edu.hk/csyqzheng/papers/AlphaWAN_SIGCOMM2025.pdf
- **Planet-Scale IoT Connectivity via LEO Satellites** — ACM SIGCOMM 2026.  
  https://dblp.org/rec/conf/sigcomm/ZhangXLLZKL26.html
- **LLM-Assisted IoT Testing: Finding Conformance Bugs in Matter SDKs** — ACM MobiCom 2025.  
  https://www.sigmobile.org/mobicom/2025/accepted.html

## 6. Video conferencing / real-time communication

**Application constraints.** RTC systems need low interactive latency while adapting rate and quality under congestion, loss, heterogeneous receivers, asymmetric links, and multi-party topologies.

**Why it could become a course project.** There are mature open tools and measurable QoE outcomes. Students can experiment with SFU architecture, rate allocation, forwarding policy, loss recovery, congestion control, and placement.

**Representative recent references**
- **NIER: Practical Neural-enhanced Low-bitrate Video Conferencing** — ACM SIGCOMM 2025.  
  https://conferences.sigcomm.org/sigcomm/2025/program/papers-info/
- **ACE: Sending Burstiness Control for High-Quality Real-time Communication** — ACM SIGCOMM 2025.  
  https://conferences.sigcomm.org/sigcomm/2025/accepted-papers/
- **Artic: AI-oriented Real-time Communication for MLLM Video Assistant** — ACM SIGCOMM 2026.  
  https://conferences.sigcomm.org/sigcomm/2026/program/papers/
- **Mowgli: Passively Learned Rate Control for Real-Time Video** — USENIX NSDI 2025.  
  https://www.usenix.org/conference/nsdi25/technical-sessions

## 7. Networked robotics / drone systems

**Application constraints.** Robots and drones combine mobility, sensing, control deadlines, intermittent connectivity, distributed perception, limited energy, and sometimes peer-to-peer coordination.

**Why it could become a course project.** Robotics simulators make realistic workload generation feasible without physical fleets. Networking decisions can be tied directly to control/sensing outcomes rather than synthetic throughput alone.

**Representative recent references**
- **Auto-UIT: Automating UAV Inspection Trajectory by Recognizing Pylon Structure from 3D Point Cloud** — ACM MobiCom 2025.  
  https://dblp.org/rec/conf/mobicom/0001HLDWZ0LC25.html
- **Scalable and Low Power Localization for Underwater Robots** — ACM MobiCom 2025.  
  https://www.sigmobile.org/mobicom/2025/program.html
- **Designing, Deployment and Field Testing of C2Stack for Networked Intelligent Software-Defined UAVs** — ACM MobiCom 2026.  
  https://www.sigmobile.org/mobicom/2026/accepted.html
- **"Take Me Home, Wi-Fi Drone": A Drone-based Wireless System for Wilderness Search and Rescue** — ACM MobiCom 2026.  
  https://www.sigmobile.org/mobicom/2026/accepted.html

## 8. Vehicular / autonomous transportation

**Application constraints.** Vehicles have rapidly changing topology, strict timing requirements, large sensor streams, mobility prediction opportunities, and safety-sensitive decisions about what should run locally, at the edge, or cooperatively.

**Why it could become a course project.** Vehicular applications impose concrete network requirements and already have strong simulator ecosystems such as SUMO, CARLA, ns-3, and Veins.

**Representative recent references**
- **VI-Planning: Infrastructure-Assisted Real-Time Planning Optimization for Autonomous Driving** — ACM MobiCom 2025.  
  https://doi.org/10.1145/3680207.3765255
- **UrgenGo: Urgency-Aware Transparent GPU Kernel Launching for Autonomous Driving** — ACM MobiCom 2025.  
  https://www.sigmobile.org/mobicom/2025/accepted.html
- **Wall-Street: An Intelligent Vehicular Surface for Reliable mmWave Handover** — ACM MobiCom 2026.  
  https://www.sigmobile.org/mobicom/2026/accepted.html

## 9. Edge video analytics

**Application constraints.** Cameras generate data faster than networks can often carry it. Systems decide what to encode, sample, transmit, process locally, or prioritize while balancing accuracy, bandwidth, latency, and compute.

**Why it could become a course project.** It produces a very concrete network/compute co-design problem, and experiments can use prerecorded video traces without specialized hardware.

**Representative recent references**
- **Uirapuru: Timely Video Analytics for High-Resolution Steerable Cameras on Edge Devices** — ACM MobiCom 2025.  
  https://doi.org/10.1145/3680207.3765260
- **Artic: AI-oriented Real-time Communication for MLLM Video Assistant** — ACM SIGCOMM 2026; an adjacent example where video transmission decisions are driven by downstream machine understanding rather than human viewing.  
  https://conferences.sigcomm.org/sigcomm/2026/program/papers/

## 10. Cloud gaming

**Application constraints.** Cloud gaming combines interactive input latency, continuous high-rate video, loss sensitivity, jitter, client heterogeneity, and rendering/server placement.

**Why it could become a course project.** It gives students a user-visible latency/QoE loop and can be built with open game streaming stacks, network emulation, and controlled rendering/encoding workloads.

**Representative recent references**
- **Dissecting and Streamlining the Interactive Loop of Mobile Cloud Gaming** — USENIX NSDI 2025.  
  https://www.usenix.org/conference/nsdi25/presentation/li-yang
- **Tooth: Toward Optimal Balance of Video QoE and Redundancy Cost by Fine-Grained FEC in Cloud Gaming Streaming** — USENIX NSDI 2025.  
  https://www.usenix.org/conference/nsdi25/presentation/an
- **Stimpack: An Adaptive Rendering Optimization System for Scalable Cloud Gaming** — USENIX NSDI 2026.  
  https://www.usenix.org/conference/nsdi26/presentation/heo
- **From Source to Solution: Tackling Packet Losses in Large-scale Cloud Gaming Systematically and Precisely** — USENIX NSDI 2026.  
  https://www.usenix.org/conference/nsdi26/presentation/wang-jing

## 11. Satellite remote sensing

**Application constraints.** Satellites collect large data objects but have predictable movement, intermittent contacts, constrained downlink capacity, storage limitations, and scheduling conflicts.

**Why it could become a course project.** Unlike generic satellite networking, remote sensing provides a clear application objective: decide what, when, and where to capture/process/store/downlink data.

**Representative recent references**
- **DeepSpace: Super Resolution Powered Efficient and Reliable Satellite Image Data Acquistion** — ACM SIGCOMM 2025.  
  https://doi.org/10.1145/3718958.3750523
- **SpaceSched: A Constellation-Wide Scheduling System for Resolving Ground Track Congestion in Remote Sensing** — ACM MobiCom 2025.  
  https://doi.org/10.1145/3680207.3765249
- **CommSAR: Enabling Bidirectional Communication in SAR Imaging Satellites via Shared Waveform** — ACM SIGCOMM 2026.  
  https://conferences.sigcomm.org/sigcomm/2026/program/papers/
- **DynaFilter: Cloud-Driven Dynamic Filtering for Satellite Edge Intelligence** — ACM MobiCom 2026.  
  https://www.sigmobile.org/mobicom/2026/accepted.html

## 12. Direct-to-device satellite communication

**Application constraints.** Ordinary user devices communicate through moving LEO satellites, creating limited capacity, handovers, intermittent coverage, long paths, and integration issues with terrestrial networks.

**Why it could become a course project.** This is a very current application with strong mobility and resource-allocation questions, but experiments will probably rely on traces/simulation rather than real satellite infrastructure.

**Representative recent references**
- **Direct-to-Cell Satellite Network without Satellite Navigation** — ACM SIGCOMM 2025.  
  https://doi.org/10.1145/3718958.3750522
- **A Variegated Look at Direct-to-Cell Satellites in the Wild** — Proceedings of the ACM on Measurement and Analysis of Computing Systems / SIGMETRICS 2026.  
  https://doi.org/10.1145/3788086
- **Planet-Scale IoT Connectivity via LEO Satellites** — ACM SIGCOMM 2026; adjacent direct-device/IoT satellite connectivity work.  
  https://dblp.org/rec/conf/sigcomm/ZhangXLLZKL26.html

## 13. Smart-grid / energy infrastructure

**Application constraints.** Energy systems combine distributed sensing/control, critical infrastructure, high reliability expectations, geographically distributed assets, and heterogeneous traffic.

**Why it could become a course project.** The domain is attractive, but the recent flagship networking corpus contains more monitoring/inspection systems than end-to-end grid-control networking, so any brief should be narrow and evidence-backed.

**Representative recent references**
- **Auto-UIT: Automating UAV Inspection Trajectory by Recognizing Pylon Structure from 3D Point Cloud** — ACM MobiCom 2025.  
  https://dblp.org/rec/conf/mobicom/0001HLDWZ0LC25.html
- **DD-LIVM: Pioneering Cross-Domain Photovoltaic Defect Detection Using Large Infrared-Visible Model** — ACM MobiCom 2025.  
  https://doi.org/10.1145/3680207.3765266
- **A3TP: Automated, Accurate, and Adaptive UAV Task Planning for Large-Scale Power Transmission Networks Inspection** — ACM MobiCom 2026.  
  https://www.sigmobile.org/mobicom/2026/accepted.html
- **Monitoring Electrical Transformer Mechanics via Crowdsourced Imaging** — ACM MobiCom 2026.  
  https://www.sigmobile.org/mobicom/2026/accepted.html

## 14. Live interactive broadcasting

**Application constraints.** Interactive broadcasts need much lower latency than conventional VOD while retaining large fan-out, resilience, adaptive quality, and often two-way interaction.

**Why it could become a course project.** It sits between CDN-scale streaming and RTC, exposing interesting design choices around forwarding trees, edge placement, buffering, and consistency of live state.

**Representative recent references**
- **Medley: Optimizing Midgress Bandwidth for Commercial Live Streaming CDNs** — USENIX NSDI 2026.  
  https://www.usenix.org/conference/nsdi26/presentation/wang-haiping
- **Syntra: Synthesizing Cross-Layer Controllers for Low-Latency Video Streaming** — USENIX NSDI 2026; useful for the low-latency control side of live streaming.  
  https://www.usenix.org/conference/nsdi26/presentation/pan
- **NIER: Practical Neural-enhanced Low-bitrate Video Conferencing** — ACM SIGCOMM 2025; useful adjacent work for interactive low-bitrate media delivery.  
  https://conferences.sigcomm.org/sigcomm/2025/program/papers-info/

## 15. Industrial automation

**Application constraints.** Industrial systems have deadline-sensitive control traffic, very high reliability requirements, deterministic behavior needs, and coexistence with non-critical monitoring traffic.

**Why it could become a course project.** The application requirements are excellent for network-design reasoning, but recent main-track flagship coverage is sparse enough that the project would need support from industrial-networking venues/standards and selected canonical papers.

**Representative recent references**
- **A Scalable Full-Stack System for High-Precision Industrial Vibration Monitoring** — ACM MobiCom 2026.  
  https://www.sigmobile.org/mobicom/2026/accepted.html
- **T(SN)-Ray: Gauging TAS and PSFP Delays of TSN Switches for Predictable Deterministic Networking** — Proceedings of the ACM on Networking / CoNEXT 2025.  
  https://doi.org/10.1145/3768996
- For background framing, **Time-Sensitive Networking (TSN) for Industrial Automation: Current Advances and Future Directions** — ACM Computing Surveys, volume published in 2025 (article first published online in 2024).  
  https://doi.org/10.1145/3695248

## 16. Emergency and disaster response

**Application constraints.** Infrastructure may be damaged or absent; topology changes rapidly; capacity is scarce; some traffic is critical; systems must degrade gracefully and often incorporate drones/mobile relays.

**Why it could become a course project.** The constraints are excellent, but the recent flagship corpus is too sparse to support a project solely from main-track networking papers.

**Representative recent references**
- **"Take Me Home, Wi-Fi Drone": A Drone-based Wireless System for Wilderness Search and Rescue** — ACM MobiCom 2026.  
  https://www.sigmobile.org/mobicom/2026/accepted.html
- **A Variegated Look at Direct-to-Cell Satellites in the Wild** — POMACS/SIGMETRICS 2026; includes direct-to-cell behavior relevant to remote and emergency connectivity.  
  https://doi.org/10.1145/3788086

## 17. Collaborative AR / shared virtual worlds

**Application constraints.** Multiple users must maintain a sufficiently consistent shared spatial state while positions, objects, media, and scene updates move under low latency.

**Why it could become a course project.** The application exposes latency-versus-consistency, local-versus-cloud coordination, multicast/replication, and state-partitioning decisions.

**Representative recent references**
- **ProxLink: A Lightweight Decentralized Synchronization Framework for Multi-User XR** — ACM MobiCom 2026.  
  https://www.sigmobile.org/mobicom/2026/accepted.html
- **LITE: Loss-Resilient Immersive Telepresence** — ACM SIGCOMM 2026; immersive telepresence work centered on recovering dense 3D content under network loss.  
  https://conferences.sigcomm.org/sigcomm/2026/program/papers/

## 18. Teleoperation

**Application constraints.** Human control loops require low latency and jitter while high-rate video/telemetry travels in the reverse direction; failures and delay spikes directly affect task performance.

**Why it could become a course project.** This is pedagogically excellent, but recent flagship-networking main-track density is low. It should be included only if we intentionally draw from robotics/control venues.

**Representative recent reference**
- **VISTA: A Benchmark for Real-Time Video Streaming under Network Impairments in Surgical Teleoperation** — presented at the Connected Autonomous Robotic Systems Workshop at IEEE ICRA 2026; includes an open benchmark and code.  
  https://arxiv.org/abs/2605.08886

## 19. Multiplayer online games

**Application constraints.** Players need low-latency state exchange while the system handles geographic distribution, consistency, prediction, cheating, server placement, and changing player groups.

**Why it could become a course project.** The application is intuitive and experimentally accessible, but recent top-tier networking papers focus much more on cloud gaming than multiplayer state synchronization.

**Representative recent reference**
- **Evaluating Browser-Based Networking for Real-Time Multiplayer Games** — USENIX NSDI 2025 poster.  
  https://aaron.gember-jacobson.com/docs/nsdi2025browser-networking_poster.pdf

## 20. Content delivery in poor-connectivity regions

**Application constraints.** Low bandwidth, high cost, intermittent connectivity, sparse infrastructure, and long outages favor caching, opportunistic transfer, replication, delay tolerance, and careful prioritization.

**Why it could become a course project.** The constraints are compelling and distinct from ordinary CDN design, but the recent flagship-paper density is very low and the research base would need to be curated beyond the six main conference editions.

**Representative recent reference**
- **Internet Performance Measurements for Rural Areas: Technical and Policy Challenges in Advancing Internet Equity** — ACM SIGCOMM 2025 non-paper session, focused specifically on measuring and reasoning about rural/underserved connectivity.  
  https://conferences.sigcomm.org/sigcomm/2025/nonpaper/nonpaper-ipmr/

## Notes for turning an area into a project brief

An area should not be released merely because it has many papers. Before promotion into a concrete project, it should have:

1. a **specific application workload and objective**, rather than a technology-only task;
2. at least **two or three interacting network/system domains** where students must make architectural choices;
3. measurable **performance, scalability, and reliability** outcomes;
4. enough tooling, traces, simulators, emulators, or open implementations to support reproducible experiments;
5. at least one plausible **baseline architecture** and several defensible alternatives;
6. failure modes or scale limits students can expose experimentally;
7. enough breadth for a four-person team to own different domains and cross-cutting design aspects;
8. a literature base that is recent enough to keep the project contemporary but stable enough to remain maintainable in later semesters.

## Screening sources

The **counts** on this page were produced by screening the complete accepted-paper lists for these six conference editions; these links are corpus/index sources rather than substitutes for the individual paper references above:

- **ACM SIGCOMM 2025 — accepted papers index**  
  https://conferences.sigcomm.org/sigcomm/2025/accepted-papers/
- **ACM SIGCOMM 2026 — accepted papers index**  
  https://conferences.sigcomm.org/sigcomm/2026/accepted/
- **USENIX NSDI 2025 — technical sessions / proceedings index**  
  https://www.usenix.org/conference/nsdi25/technical-sessions
- **USENIX NSDI 2026 — technical sessions / proceedings index**  
  https://www.usenix.org/conference/nsdi26/technical-sessions
- **ACM MobiCom 2025 — accepted papers index**  
  https://www.sigmobile.org/mobicom/2025/accepted.html
- **ACM MobiCom 2026 — accepted papers index**  
  https://www.sigmobile.org/mobicom/2026/accepted.html

For reproducibility of the denominator, SIGCOMM/MobiCom paper-count cross-checks also used the DBLP-derived **csconf-papers** indexes:

- **SIGCOMM 2025 paper index** — https://github.com/RealZST/csconf-papers/blob/main/papers/2025/SIGCOMM.md
- **MobiCom 2025 paper index** — https://github.com/RealZST/csconf-papers/blob/main/papers/2025/MobiCom.md
- **MobiCom 2026 paper index** — https://github.com/RealZST/csconf-papers/blob/main/papers/2026/MobiCom.md

This is a **research-grounded idea pool**, not a bibliometric claim. The counts are an activity signal; project briefs should be based on inspecting the actual systems, assumptions, artifacts, and evaluation methods in the cited work.
