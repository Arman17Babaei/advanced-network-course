# Project Idea Pool

This page is a **project-area idea pool** for the Fall 2026 Advanced Networks course. It is not yet the final set of released project briefs.

The goal is to identify **application-oriented networked systems domains** where:
- the application imposes recognizable networking constraints;
- students can make and defend end-to-end architecture decisions;
- there is enough recent research activity to ground the project in contemporary systems work;
- practical tools, simulators, emulators, traces, or open implementations are likely to make a substantial semester project feasible.

The research scan below treats “post-2024” as **2025 and 2026 work available by 23 September 2026**. The primary corpus screened was the main-track paper lists of SIGCOMM 2025/2026, NSDI 2025/2026, and MobiCom 2025/2026.

A paper is counted for an application only when the **application itself is central to the problem/system**, not merely an evaluation workload. Counts are conservative lower bounds; one paper may appear in more than one application area.

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

**Recent references**
- **ByteScale: Efficient Scaling of LLM Training with a 2048K Context Length on More Than 12,000 GPUs** — SIGCOMM 2025. A representative recent system on scaling distributed LLM training and exposing communication/parallelism constraints at very large GPU counts.  
  https://conferences.sigcomm.org/sigcomm/2025/
- **Astral: A Unified Network Architecture for Distributed AI Training** — recent SIGCOMM/NSDI-era work in the screened corpus emphasizing training-specific networking and topology/communication design.  
  https://conferences.sigcomm.org/sigcomm/2026/accepted/
- **Coflow Scheduling for LLM Training** — recent work treating communication groups rather than individual flows as the scheduling object for distributed training.  
  https://www.usenix.org/conference/nsdi26
- **MixNet** — recent systems work on improving network utilization for distributed AI workloads under changing communication demands.  
  https://conferences.sigcomm.org/sigcomm/2026/accepted/
- **GeoOrchestra** — recent work on geographically distributed AI workloads, useful for thinking about network/computation placement and WAN constraints.  
  https://conferences.sigcomm.org/sigcomm/2026/accepted/

## 2. Distributed AI inference

**Application constraints.** Modern inference systems move activations, parameters, KV caches, and requests across heterogeneous accelerators and network tiers. Tail latency, batching, placement, disaggregation, and failure handling interact strongly.

**Why it could become a course project.** Students can study the application/network boundary directly: function placement, resource scheduling, request routing, disaggregation, and congestion can all be changed and experimentally defended.

**Recent references**
- **MegaScale-Infer** — recent large-scale distributed inference system examining communication and orchestration for serving large models.  
  https://conferences.sigcomm.org/sigcomm/2025/
- **HACK** — recent work on efficient distributed inference and data movement in modern accelerator-based serving systems.  
  https://www.usenix.org/conference/nsdi26
- **AoRA** — recent inference-serving work using network/system co-design for resource allocation and latency reduction.  
  https://conferences.sigcomm.org/sigcomm/2026/accepted/
- **DualPath** — recent systems work exploiting multiple data/communication paths for model serving.  
  https://conferences.sigcomm.org/sigcomm/2026/accepted/

## 3. Large-scale video streaming

**Application constraints.** Streaming must jointly manage bitrate adaptation, CDN/server placement, caching, startup delay, rebuffering, bandwidth variation, and huge demand skew.

**Why it could become a course project.** This is one of the cleanest application-oriented choices: students can observe user-visible QoE, implement alternatives, use realistic traces, and reason simultaneously about application, transport, CDN, and resource-allocation layers.

**Recent references**
- **SIGCOMM 2026 Video and QoE session** — contains multiple recent systems on video delivery, quality adaptation, and network-aware streaming.  
  https://conferences.sigcomm.org/sigcomm/2026/accepted/
- **Recent NSDI 2026 video-streaming work** — includes systems focused on scalable video delivery and application/network adaptation.  
  https://www.usenix.org/conference/nsdi26
- **Recent SIGCOMM 2025 video systems** — multiple accepted papers cover streaming, QoE, CDN behavior, short-video delivery, and adaptive control.  
  https://conferences.sigcomm.org/sigcomm/2025/

## 4. AR/VR and immersive applications

**Application constraints.** Immersive applications combine high data rates, strict motion-to-photon latency, localization, rendering placement, mobility, and sometimes multi-user synchronization.

**Why it could become a course project.** The application naturally creates decisions across device, edge, transport, rendering, and wireless/network layers; different architectures yield clear performance/quality trade-offs.

**Recent references**
- **EdgeGaussian** — MobiCom 2025. Edge-assisted Gaussian-splatting/immersive rendering work that exposes network/rendering placement and latency/bandwidth trade-offs.  
  https://www.sigmobile.org/mobicom/2025/accepted.html
- **ProxLink** — MobiCom 2026. Decentralized synchronization/connectivity for multi-user XR, directly relevant to consistency, synchronization, and local communication design.  
  https://www.sigmobile.org/mobicom/2026/accepted.html
- **Recent volumetric/360°/mobile VR systems in MobiCom 2025–2026** — useful references for quality adaptation, localization, and edge rendering.  
  https://www.sigmobile.org/mobicom/2025/accepted.html  
  https://www.sigmobile.org/mobicom/2026/accepted.html

## 5. Massive IoT / smart environments

**Application constraints.** Large populations of constrained devices create heterogeneous traffic, energy limits, intermittent links, scalability problems, mobility, and management challenges.

**Why it could become a course project.** A project must be anchored in a concrete application—smart building, sensing infrastructure, environmental monitoring, etc.—rather than generic protocol work.

**Recent references**
- **Planet-scale IoT via LEO satellites** — MobiCom 2025 work exploring large-scale IoT connectivity through satellite infrastructure.  
  https://www.sigmobile.org/mobicom/2025/accepted.html
- **Recent ambient-IoT and AIoT systems** — MobiCom 2025/2026 include multiple systems on constrained sensing, connectivity, and intelligent IoT operation.  
  https://www.sigmobile.org/mobicom/2025/accepted.html  
  https://www.sigmobile.org/mobicom/2026/accepted.html
- **Recent IoT testing/scheduling systems** — useful for projects involving constrained device populations, reliability, and resource allocation.  
  https://www.sigmobile.org/mobicom/2026/accepted.html

## 6. Video conferencing / real-time communication

**Application constraints.** RTC systems need low interactive latency while adapting rate and quality under congestion, loss, heterogeneous receivers, asymmetric links, and multi-party topologies.

**Why it could become a course project.** There are mature open tools and measurable QoE outcomes. Students can experiment with SFU architecture, rate allocation, forwarding policy, loss recovery, congestion control, and placement.

**Recent references**
- **NIER** — recent real-time communication work focused on rate control/interactive media behavior.  
  https://conferences.sigcomm.org/sigcomm/2025/
- **Scalable SDN conferencing systems** — recent SIGCOMM/NSDI-era work examining multi-party conferencing architecture and network control.  
  https://conferences.sigcomm.org/sigcomm/2025/
- **Recent WebRTC live/interactive systems** — several papers in SIGCOMM 2025/2026 study scalable RTC and WebRTC delivery.  
  https://conferences.sigcomm.org/sigcomm/2025/  
  https://conferences.sigcomm.org/sigcomm/2026/accepted/

## 7. Networked robotics / drone systems

**Application constraints.** Robots and drones combine mobility, sensing, control deadlines, intermittent connectivity, distributed perception, limited energy, and sometimes peer-to-peer coordination.

**Why it could become a course project.** Robotics simulators make realistic workload generation feasible without physical fleets. Networking decisions can be tied directly to control/sensing outcomes rather than synthetic throughput alone.

**Recent references**
- **Search-and-rescue drone system** — MobiCom 2026. A direct application example combining mobile networking with emergency robotic operation.  
  https://www.sigmobile.org/mobicom/2026/accepted.html
- **Recent UAV inspection systems** — MobiCom 2025/2026 include UAV networking and sensing systems for infrastructure inspection and distributed perception.  
  https://www.sigmobile.org/mobicom/2025/accepted.html  
  https://www.sigmobile.org/mobicom/2026/accepted.html
- **Recent underwater/networked robotic systems** — MobiCom papers provide useful contrasting environments with difficult connectivity constraints.  
  https://www.sigmobile.org/mobicom/2025/accepted.html

## 8. Vehicular / autonomous transportation

**Application constraints.** Vehicles have rapidly changing topology, strict timing requirements, large sensor streams, mobility prediction opportunities, and safety-sensitive decisions about what should run locally, at the edge, or cooperatively.

**Why it could become a course project.** Vehicular applications impose concrete network requirements and already have strong simulator ecosystems such as SUMO, CARLA, ns-3, and Veins.

**Recent references**
- **VI-Planning** — MobiCom 2025. Vehicular/autonomous-planning system representative of recent work combining mobility, perception/planning, and communication/computation constraints.  
  https://www.sigmobile.org/mobicom/2025/accepted.html
- **Wall-Street** — MobiCom 2025. Vehicular mmWave/networking work exposing mobility, blockage, and link-selection constraints.  
  https://www.sigmobile.org/mobicom/2025/accepted.html
- **Recent connected/autonomous-vehicle systems** — additional MobiCom 2025/2026 papers cover vehicular sensing, planning, and wireless/network interaction.  
  https://www.sigmobile.org/mobicom/2026/accepted.html

## 9. Edge video analytics

**Application constraints.** Cameras generate data faster than networks can often carry it. Systems decide what to encode, sample, transmit, process locally, or prioritize while balancing accuracy, bandwidth, latency, and compute.

**Why it could become a course project.** It produces a very concrete network/compute co-design problem, and experiments can use prerecorded video traces without specialized hardware.

**Recent references**
- **Uirapuru** — recent MobiCom work on edge/mobile video analytics, representative of bandwidth/compute/accuracy trade-offs.  
  https://www.sigmobile.org/mobicom/2025/accepted.html
- **Recent VLM/video analytics systems** — MobiCom 2025/2026 include systems deciding where and how to process video under constrained network resources.  
  https://www.sigmobile.org/mobicom/2025/accepted.html  
  https://www.sigmobile.org/mobicom/2026/accepted.html

## 10. Cloud gaming

**Application constraints.** Cloud gaming combines interactive input latency, continuous high-rate video, loss sensitivity, jitter, client heterogeneity, and rendering/server placement.

**Why it could become a course project.** It gives students a user-visible latency/QoE loop and can be built with open game streaming stacks, network emulation, and controlled rendering/encoding workloads.

**Recent references**
- **NSDI 2025 cloud-gaming papers** — the program includes multiple systems studying interactive-loop latency, rendering adaptation, and cloud-game delivery.  
  https://www.usenix.org/conference/nsdi25
- **Recent cloud gaming / interactive video systems** — NSDI and SIGCOMM work in 2025–2026 provides current baselines for transport, adaptation, and server/client design.  
  https://www.usenix.org/conference/nsdi26  
  https://conferences.sigcomm.org/sigcomm/2026/accepted/

## 11. Satellite remote sensing

**Application constraints.** Satellites collect large data objects but have predictable movement, intermittent contacts, constrained downlink capacity, storage limitations, and scheduling conflicts.

**Why it could become a course project.** Unlike generic satellite networking, remote sensing provides a clear application objective: decide what, when, and where to capture/process/store/downlink data.

**Recent references**
- **DeepSpace** — recent SIGCOMM-era satellite system representative of computation/network scheduling in space systems.  
  https://conferences.sigcomm.org/sigcomm/2025/
- **SpaceSched** — recent work on satellite scheduling and constrained contact/downlink resources.  
  https://conferences.sigcomm.org/sigcomm/2025/
- **Recent satellite sensing/SAR systems** — SIGCOMM/MobiCom 2025–2026 include systems around satellite image acquisition, processing, and communication.  
  https://conferences.sigcomm.org/sigcomm/2026/accepted/  
  https://www.sigmobile.org/mobicom/2026/accepted.html

## 12. Direct-to-device satellite communication

**Application constraints.** Ordinary user devices communicate through moving LEO satellites, creating limited capacity, handovers, intermittent coverage, long paths, and integration issues with terrestrial networks.

**Why it could become a course project.** This is a very current application with strong mobility and resource-allocation questions, but experiments will probably rely on traces/simulation rather than real satellite infrastructure.

**Recent references**
- **Recent direct-to-cell / direct-to-device LEO systems** — SIGCOMM 2025/2026 include systems studying direct satellite connectivity and integration with mobile devices.  
  https://conferences.sigcomm.org/sigcomm/2025/  
  https://conferences.sigcomm.org/sigcomm/2026/accepted/
- **Planet-scale IoT via LEO satellites** — MobiCom 2025; useful adjacent reference for constrained device-to-satellite communication.  
  https://www.sigmobile.org/mobicom/2025/accepted.html

## 13. Smart-grid / energy infrastructure

**Application constraints.** Energy systems combine distributed sensing/control, critical infrastructure, high reliability expectations, geographically distributed assets, and heterogeneous traffic.

**Why it could become a course project.** The domain is attractive, but the recent flagship networking corpus contains more monitoring/inspection systems than end-to-end grid-control networking, so any brief should be narrow and evidence-backed.

**Recent references**
- **Recent UAV power-line inspection systems** — MobiCom 2025/2026 include networked sensing/inspection systems for power infrastructure.  
  https://www.sigmobile.org/mobicom/2025/accepted.html
- **Recent transformer/PV monitoring systems** — useful as application anchors for sensing, edge processing, and reliable data delivery in energy infrastructure.  
  https://www.sigmobile.org/mobicom/2026/accepted.html

## 14. Live interactive broadcasting

**Application constraints.** Interactive broadcasts need much lower latency than conventional VOD while retaining large fan-out, resilience, adaptive quality, and often two-way interaction.

**Why it could become a course project.** It sits between CDN-scale streaming and RTC, exposing interesting design choices around forwarding trees, edge placement, buffering, and consistency of live state.

**Recent references**
- **Horizon** — recent system for low-latency live-stream delivery, representative of this application class.  
  https://conferences.sigcomm.org/sigcomm/2025/
- **Recent WebRTC live-streaming systems** — SIGCOMM 2025/2026 include systems combining WebRTC-style latency with large-scale distribution.  
  https://conferences.sigcomm.org/sigcomm/2025/  
  https://conferences.sigcomm.org/sigcomm/2026/accepted/

## 15. Industrial automation

**Application constraints.** Industrial systems have deadline-sensitive control traffic, very high reliability requirements, deterministic behavior needs, and coexistence with non-critical monitoring traffic.

**Why it could become a course project.** The application requirements are excellent for network-design reasoning, but recent main-track flagship coverage is sparse enough that the project would need support from industrial-networking venues/standards and selected canonical papers.

**Recent references**
- **Recent industrial monitoring/factory-network systems** — MobiCom 2026 contains examples of networking/sensing inside industrial environments.  
  https://www.sigmobile.org/mobicom/2026/accepted.html
- Supplementary sources should likely come from **ACM/IEEE industrial networking and real-time systems venues**, because the flagship networking corpus alone is thin.

## 16. Emergency and disaster response

**Application constraints.** Infrastructure may be damaged or absent; topology changes rapidly; capacity is scarce; some traffic is critical; systems must degrade gracefully and often incorporate drones/mobile relays.

**Why it could become a course project.** The constraints are excellent, but the recent flagship corpus is too sparse to support a project solely from main-track networking papers.

**Recent references**
- **Search-and-rescue drone networking system** — MobiCom 2026. Directly relevant recent application system.  
  https://www.sigmobile.org/mobicom/2026/accepted.html
- **SIGCOMM workshops and first-responder networking work** — useful supplementary source of visionary and applied systems ideas when constructing a brief.  
  https://conferences.sigcomm.org/sigcomm/2025/

## 17. Collaborative AR / shared virtual worlds

**Application constraints.** Multiple users must maintain a sufficiently consistent shared spatial state while positions, objects, media, and scene updates move under low latency.

**Why it could become a course project.** The application exposes latency-versus-consistency, local-versus-cloud coordination, multicast/replication, and state-partitioning decisions.

**Recent references**
- **ProxLink** — MobiCom 2026. Explicitly relevant to decentralized multi-user XR synchronization.  
  https://www.sigmobile.org/mobicom/2026/accepted.html
- Additional references overlap with the broader AR/VR area above.

## 18. Teleoperation

**Application constraints.** Human control loops require low latency and jitter while high-rate video/telemetry travels in the reverse direction; failures and delay spikes directly affect task performance.

**Why it could become a course project.** This is pedagogically excellent, but recent flagship-networking main-track density is low. It should be included only if we intentionally draw from robotics/control venues.

**Recent references**
- **ICRA 2026 Connected Robots / Networking workshop** — includes work such as network-aware surgical teleoperation and explicitly connects robotics and communication design.  
  https://connected-robots.com/
- **KIT publication on network-aware teleoperation (2026)** — an example of recent work outside the flagship networking corpus.  
  https://publikationen.bibliothek.kit.edu/1000193457

## 19. Multiplayer online games

**Application constraints.** Players need low-latency state exchange while the system handles geographic distribution, consistency, prediction, cheating, server placement, and changing player groups.

**Why it could become a course project.** The application is intuitive and experimentally accessible, but recent top-tier networking papers focus much more on cloud gaming than multiplayer state synchronization.

**Recent references**
- **NSDI 2025 poster on browser networking for real-time multiplayer games** — evidence that the problem remains active even though no main-track paper appeared in the screened corpus.  
  https://www.usenix.org/conference/nsdi25/poster-session
- Final project design would need older canonical systems/networked-games work or specialized venues.

## 20. Content delivery in poor-connectivity regions

**Application constraints.** Low bandwidth, high cost, intermittent connectivity, sparse infrastructure, and long outages favor caching, opportunistic transfer, replication, delay tolerance, and careful prioritization.

**Why it could become a course project.** The constraints are compelling and distinct from ordinary CDN design, but the recent flagship-paper density is very low and the research base would need to be curated beyond the six main conference editions.

**Recent references**
- **SIGCOMM 2025 rural-connectivity / measurement discussion material** — recent evidence that underserved-connectivity problems remain active in the SIGCOMM community.  
  https://conferences.sigcomm.org/sigcomm/2025/nonpaper/nonpaper-ipmr/
- A serious brief should also draw on specialized community-networking, ICTD, rural-connectivity, and delay-tolerant-networking work.

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

## Sources and screening references

The counts on this page were produced by screening the accepted-paper lists for the following conference editions:

- **ACM SIGCOMM 2025 accepted papers**  
  https://conferences.sigcomm.org/sigcomm/2025/
- **ACM SIGCOMM 2026 accepted papers**  
  https://conferences.sigcomm.org/sigcomm/2026/accepted/
- **USENIX NSDI 2025**  
  https://www.usenix.org/conference/nsdi25
- **USENIX NSDI 2026**  
  https://www.usenix.org/conference/nsdi26
- **ACM MobiCom 2025 accepted papers**  
  https://www.sigmobile.org/mobicom/2025/accepted.html
- **ACM MobiCom 2026 accepted papers**  
  https://www.sigmobile.org/mobicom/2026/accepted.html

For reproducibility of the denominator, the SIGCOMM/MobiCom paper-count cross-check used the DBLP-derived conference-paper indexes in the **csconf-papers** repository:

- SIGCOMM 2025 paper index  
  https://github.com/RealZST/csconf-papers/blob/main/papers/2025/SIGCOMM.md
- MobiCom 2025 paper index  
  https://github.com/RealZST/csconf-papers/blob/main/papers/2025/MobiCom.md
- MobiCom 2026 paper index  
  https://github.com/RealZST/csconf-papers/blob/main/papers/2026/MobiCom.md

The list above is intended as a **research-grounded idea pool**, not as a bibliometric claim. Counts are useful as evidence of recent activity, while the named references should be inspected when converting any area into a released project.
