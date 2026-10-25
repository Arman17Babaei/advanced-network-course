# Project Idea Pool

This page is a **research-grounded project-area pool** for the Fall 2026 Advanced Networks course. It is not a final set of released project briefs.

The previous version inferred project areas mainly from SIGCOMM, NSDI, and MobiCom 2025–2026. This revision broadens the evidence base to the requested venue families and uses a **paper/keyword-first taxonomy**: recurring research topics are identified from recent papers, normalized into clusters, and only then translated into candidate project areas.

## Scope and methodology

### Time window

The intended window is **2023–2027**. As of **25 October 2026**, essentially all usable accepted-paper evidence is from 2023–2026. Most 2027 venues have not yet published accepted-paper lists. In particular, NINeS 2027 notifications are scheduled for 27 November 2026, so no 2027 NINeS papers are counted yet.

### Corpus and venue scope

The machine-readable evidence base is now a validated, checked-in corpus rather than a representative sample:

- [`data/master_paper_corpus.csv`](data/master_paper_corpus.csv) — master combined corpus with paper metadata plus explicit source-vs-derived keyword fields;
- [`data/all_conference_papers.csv`](data/all_conference_papers.csv) — **9,991** papers from the requested conference series;
- [`data/ieee_transactions_network.csv`](data/ieee_transactions_network.csv) — **6,968** networking-relevant papers from selected IEEE Transactions journals;
- [`data/recent_networking_papers.csv`](data/recent_networking_papers.csv) — the combined **16,959-record** corpus used for topic/category analysis;
- [`data/PAPER_CORPUS_SUMMARY.md`](data/PAPER_CORPUS_SUMMARY.md) — generated venue/year coverage, keyword provenance, and category counts;
- [`data/PAPER_CORPUS_COVERAGE.csv`](data/PAPER_CORPUS_COVERAGE.csv) — auditable per-venue/per-year counts;
- [`data/venues/`](data/venues/) — frozen, independently validated conference snapshots;
- [`data/transactions/`](data/transactions/) — networking-only IEEE Transactions snapshots.

The conference corpus covers **SIGCOMM, CoNEXT, NSDI, ICNP, INFOCOM, SIGMETRICS/POMACS, IMC, ACM Multimedia, NINeS, MobiCom, MMSys, IPDPS, ICDCS, OSDI, and USENIX Security**.

IEEE Transactions are handled differently because the family is much broader than networking. The checked-in journal snapshots retain only papers with explicit networking or networked-systems relevance. Core networking journals such as IEEE Transactions on Networking and IEEE Transactions on Network and Service Management are retained broadly; adjacent Transactions journals are filtered using paper title/keyword signals and then validated separately.

Every row records paper title, authors, venue, year, DOI/publication URL, keyword labels, keyword provenance, topic labels where available, normalized project categories, and source metadata identifiers when available.

### Keyword extraction and provenance

The corpus distinguishes **source metadata** from **derived research labels**:

- conference inventory comes from official venue/program/proceedings pages or a pinned bibliographic endpoint that was validated against plausible/exact yearly counts;
- IEEE Transactions metadata comes primarily from OpenAlex journal/work records, with journal identity pinned explicitly;
- OpenAlex paper keywords are model-generated aboutness labels, **not author-supplied keywords**;
- publisher/Crossref keywords are retained when exposed;
- when a source exposes no usable keywords, the builder uses a deterministic title- or title/abstract-derived fallback;
- `keyword_provenance` records which path produced each row's keywords;
- project categories are generated separately from a version-controlled vocabulary in `tools/research/paper_corpus_config.json`.

The generated corpus currently contains **11,155 records with OpenAlex model-generated keywords**, **3,773 with deterministic title-derived keywords**, and **2,031 with deterministic title/abstract-derived category terms**. These labels are sufficient for research-cluster discovery, but they should not be interpreted as a bibliometric dataset of author-supplied keywords.

## Research-cluster summary

Counts below come from the full 16,959-record corpus. Categories are **not mutually exclusive**: one paper may contribute to several clusters. Raw counts also reflect venue mix—for example, wireless/networking Transactions produce many more papers than systems conferences—so the recommendation column combines research density with course fit rather than ranking by count alone.

| Cluster | Corpus records | Evidence signal | Project-pool recommendation |
| --- | ---: | --- | --- |
| **AI cluster networks and distributed training** | 278 | Repeated across SIGCOMM, NSDI, OSDI, ICNP, ICDCS, IPDPS, TPDS; rapidly growing | **Top-tier** |
| **Distributed / disaggregated AI inference** | 94 | Smaller but very recent, concentrated in SIGCOMM/NSDI/MobiCom/ICDCS/TPDS | **Top-tier** |
| **Datacenter transport and programmable networking** | 2,311 | Extremely broad and mature across networking/systems venues | **Top-tier** |
| **Network operations, telemetry, diagnosis, and verification** | 411 | Strong systems/measurement cluster with excellent experimental fit | **Top-tier** |
| **Satellite / non-terrestrial networking** | 815 | Large cross-venue cluster spanning transport, routing, edge, and measurement | **Top-tier** |
| **Cellular / 5G / 6G / RAN systems** | 4,002 | Largest category, amplified by wireless Transactions coverage | **Strong** |
| **Real-time media and interactive video** | 587 | Strong across SIGCOMM/NSDI/IMC/MMSys/ACM MM | **Top-tier** |
| **Immersive / XR / volumetric media** | 307 | Focused cluster with strong MobiCom/MM/MMSys presence | **Strong** |
| **Edge intelligence and mobile AI** | 2,359 | Very broad across mobile, distributed, and Transactions venues | **Strong** |
| **Robotics, UAVs, vehicles, and cyber-physical networking** | 1,874 | Strong but often application-heavy; project must keep networking central | **Strong** |
| **Internet measurement and infrastructure** | 1,357 | Deep, methodologically mature cluster with public datasets | **Top-tier** |
| **Network security, privacy, and censorship resistance** | 1,748 | Strong across USENIX Security, IMC, SIGCOMM, ICNP, Transactions | **Strong** |
| **Cloud, serverless, and disaggregated systems** | 983 | Strong systems cluster; must be scoped around communication/network behavior | **Strong** |
| **Deterministic / industrial networking** | 133 | Smaller, technically coherent TSN/deadline-oriented cluster | **Targeted** |
| **Quantum networking** | 64 | Small but visible and growing; simulation-heavy | **Exploratory** |
| **Sustainable networking and computing** | 468 | Cross-cutting constraint rather than a standalone networking stack | **Exploratory** |

## Representative paper anchors

The tables below are **human-readable anchors selected from the full machine-readable corpus**. They are deliberately biased toward papers that can generate network-design projects for this course; the exhaustive paper inventory is in `data/recent_networking_papers.csv`.

### AI cluster networks and distributed training

| Paper | Venue / year | Normalized keywords |
| --- | --- | --- |
| **ByteScale: Communication-Efficient Scaling of LLM Training with a 2048K Context Length on 16384 GPUs** | SIGCOMM 2025 | LLM training, communication efficiency, long context, GPU clusters |
| **MixNet: A Runtime Reconfigurable Optical-Electrical Fabric for Distributed Mixture-of-Experts Training** | SIGCOMM 2025 | MoE, optical networking, topology reconfiguration, distributed training |
| **Coflow Scheduling for LLM Training** | SIGCOMM 2025 | coflows, scheduling, LLM training, flow dependency |
| **SyCCL: Exploiting Symmetry for Efficient Collective Communication Scheduling** | SIGCOMM 2025 | collectives, scheduling, topology, distributed training |
| **SchedEP: Online Scheduling of EP Communication with Token Aggregation and Load Balancing** | ICNP 2026 | expert parallelism, token aggregation, load balancing |
| **Taming Step Misalignment in the Network for Collective Operations** | ICNP 2026 | collective communication, synchronization, network scheduling |
| **Shuffle-Exchange: Enhancing Collective Communication Efficiency for Large Model Training** | ICDCS 2025 | large-model training, collectives, communication optimization |
| **RAPIDSCRIBE: Bandwidth-aware Parallel Snapshots for Distributed Neural-Network Training** | ICDCS 2025 | checkpointing, bandwidth allocation, distributed training |
| **Enhancing In-network Aggregation with Adaptive Gradient Quantization for Multi-tenant Learning** | ICDCS 2025 | in-network aggregation, quantization, multi-tenancy, distributed learning |
| **ACCL+: an FPGA-Based Collective Engine for Distributed Applications** | OSDI 2024 | FPGA, collectives, RDMA, offload |
| **HiCCL: A Hierarchical Collective Communication Library** | IPDPS 2025 | hierarchical collectives, HPC, topology-aware communication |
| **Air-FedGA: A Grouping Asynchronous Federated Learning Mechanism Exploiting Over-the-air Computation** | IPDPS 2025 | federated learning, wireless aggregation, over-the-air computation |
| **PC4: Precision Collective Communication Congestion Control for AI Cluster** | INFOCOM 2025 | AI clusters, collectives, congestion control |

### Distributed / disaggregated AI inference

| Paper | Venue / year | Normalized keywords |
| --- | --- | --- |
| **MegaScale-Infer: Efficient Mixture-of-Experts Model Serving with Disaggregated Expert Parallelism** | SIGCOMM 2025 | MoE serving, disaggregation, expert parallelism, inference |
| **DualPath: Accelerating Agentic LLM Inference by Harvesting Disaggregated KV-Cache Storage I/O** | SIGCOMM 2026 | agentic inference, KV cache, disaggregated storage, I/O |
| **KVServe: Service-Aware KV Cache Compression for Communication-Efficient Disaggregated LLM Serving** | SIGCOMM 2026 | KV cache, compression, disaggregated serving |
| **AoRA: AI-on-RAN for Backhaul-free Edge Inference** | SIGCOMM 2025 | edge inference, RAN, communication avoidance |
| **LLMSched: Uncertainty-Aware Workload Scheduling for Compound LLM Applications** | ICDCS 2025 | LLM serving, scheduling, uncertainty |
| **MCaM: Efficient LLM Inference with Multi-tier KV Cache Management** | ICDCS 2025 | KV cache, hierarchy, inference |
| **S2M3: Split-and-Share Multi-Modal Models for Distributed Multi-Task Inference on the Edge** | ICDCS 2025 | split inference, edge AI, multimodal |
| **CFMoE: Cache-Friendly Mixture of Experts Model Serving System on Edge Devices** | MobiCom 2026 | edge serving, MoE, caching |
| **CRISP: Co-designing Pruning and Scheduling for Efficient MoE Inference on Edge Servers** | MobiCom 2026 | MoE, pruning, scheduling, edge inference |
| **NPUGen: NPU as KV Generator for Stable Long-Context Mobile LLM Inference** | MobiCom 2026 | mobile LLMs, NPU, KV generation |

### Datacenter transport and programmable networking

| Paper | Venue / year | Normalized keywords |
| --- | --- | --- |
| **Fast, Scalable, and Accurate Rate Limiter for RDMA NICs** | SIGCOMM 2024 | RDMA, NIC, rate limiting |
| **OptimusPrime: Unleash Dataplane Programmability through a Transformable Architecture** | SIGCOMM 2024 | programmable dataplane, P4-like processing, switch architecture |
| **Hawkeye: Diagnosing RDMA Network Performance Anomalies with PFC Provenance** | SIGCOMM 2025 | RDMA, PFC, diagnosis |
| **ByteDance Jakiro: Enabling RDMA and TCP over Virtual Private Cloud** | SIGCOMM 2025 | RDMA, TCP, VPC, cloud networking |
| **Simulate Before Sending: Rethinking Transport in Datacenter Networks** | NINeS 2026 | datacenter transport, predictive control, congestion |
| **No Signal to Rule Them All: A Systematic Analysis of In-Network Congestion Signals** | NINeS 2026 | ECN, congestion signals, transport design |
| **Making Congestion Control Algorithms Insensitive to Underlying Propagation Delays** | NINeS 2026 | congestion control, RTT robustness |
| **PEE: Precise ECN Encoding for Efficient Congestion Control in Data Center Networks** | ICDCS 2025 | ECN, datacenter congestion control |
| **Enabling Rate-Aware Load Balancing for Datacenter Networks** | ICNP 2026 | load balancing, rate awareness, datacenter |
| **Poison comes in small packages: Application-driven Reexamination of Datacenter Microbursts** | SIGMETRICS 2025 | microbursts, queueing, datacenter traffic |
| **Taurus: Towards A High-Performance and Generic Congestion Control Framework for Datacenter Networks** | CoNEXT 2025 | congestion control, datacenter, framework |
| **L4Span: Spanning Congestion Signaling over NextG Networks for Interactive Applications** | CoNEXT 2025 | 5G, ECN, low latency, congestion signaling |
| **VCCAnalyzer: Identifying Congestion Control Algorithms used by Video Streaming Services** | CoNEXT 2025 | video streaming, congestion-control inference, measurement |

### Network operations, telemetry, diagnosis, and verification

| Paper | Venue / year | Normalized keywords |
| --- | --- | --- |
| **Raha: A General Tool to Analyze WAN Degradation** | SIGCOMM 2025 | WAN diagnosis, degradation, root cause |
| **CAPA: An Architecture For Operating Cluster Networks With High Availability** | NSDI 2024 | network operations, change safety, availability |
| **POSEIDON: A Consolidated Virtual Network Controller that Manages Millions of Tenants via Config Tree** | NSDI 2024 | virtual networks, control plane, scalability |
| **Raising the Level of Abstraction for Sketch-Based Network Telemetry with SketchPlan** | IMC 2024 | telemetry, sketches, abstraction |
| **INT-MC: Low-Overhead In-Band Network-Wide Telemetry Based on Matrix Completion** | SIGMETRICS 2025 | in-band telemetry, matrix completion, overhead |
| **SlaRepair: Service-Aware Closed-Loop Network Fault Repair via Constrained LLM Arbitration** | ICNP 2026 | network repair, LLM agents, closed-loop operations |
| **VeriNC: Finding Design Risks of In-Network Computing Systems** | ICNP 2026 | verification, in-network computing, design risk |
| **Automatic Generation of Digital Twins for Network Testing** | ICDCS 2025 workshop | digital twins, network testing |

### Satellite and non-terrestrial networking

| Paper | Venue / year | Normalized keywords |
| --- | --- | --- |
| **Democratizing Direct-to-Cell Low Earth Orbit Satellite Networks** | NSDI 2024 | direct-to-cell, LEO, mobility, cellular integration |
| **LeoCC: Making Internet Congestion Control Robust to LEO Satellite Dynamics** | SIGCOMM 2025 | LEO, congestion control, variable RTT |
| **StarCDN: Moving Content Delivery Networks to Space** | SIGCOMM 2025 | satellite CDN, caching, content delivery |
| **Direct-to-Cell Satellite Network without Satellite Navigation** | SIGCOMM 2025 | direct-to-cell, positioning, NTN |
| **DeepSpace: Super Resolution Powered Efficient and Reliable Satellite Image Data Acquisition** | SIGCOMM 2025 | remote sensing, downlink, compression |
| **What Obstructed Skies Teach Us about Satellite Internet** | NINeS 2026 | satellite measurements, obstruction, reliability |
| **CrowdLink: Unlocking Idle LEO Network Capacity with User Terminals** | NINeS 2026 | LEO capacity, user terminals, cooperative networking |
| **A Global Perspective on the Past, Present, and Future of Video Streaming over Starlink** | SIGMETRICS 2025 | Starlink, video streaming, performance measurement |
| **Space Booking: Enabling Performance-Critical Applications in Broadband Satellite Networks** | ICDCS 2025 | satellite scheduling, reservations, application QoS |
| **Partitioning or Not? Hierarchical Task Offloading Optimization in Collaborative Satellite Edge Computing Networks** | ICDCS 2025 | satellite edge, offloading, partitioning |
| **Direct-to-Cell Satellite Radio Signal Traceback at Scale** | MobiCom 2026 | direct-to-cell, RF measurement, traceback |
| **DynaFilter: Cloud-Driven Dynamic Filtering for Satellite Edge Intelligence** | MobiCom 2026 | satellite edge, filtering, edge intelligence |
| **Joint Service Caching and Resource Allocation Over Different Timescales in Satellite Edge Computing Networks** | IEEE TMC 2025 | satellite edge, caching, resource allocation |
| **Multi-Attribute Consistency Segment Resilient Routing for LEO Satellite Mega Constellations** | IEEE TMC 2025 | LEO routing, failures, segment routing |
| **Prediction-Based Task Offloading for Ultra-Dense LEO Satellite Edge Computing** | IEEE TMC 2026 Early Access | prediction, task offloading, LEO edge |
| **NovaPlan: An Efficient Plan of Renting Ground Stations for Emerging LEO Satellite Networks** | INFOCOM 2025 | LEO, ground stations, planning |
| **StableRoute: When Dijkstra's Algorithm Meets Topology-Varying Satellite Networks** | INFOCOM 2025 | LEO routing, dynamic topology |

### Cellular / RAN / mobile networking

| Paper | Venue / year | Normalized keywords |
| --- | --- | --- |
| **RANBooster: Democratizing advanced cellular connectivity through fronthaul middleboxes** | SIGCOMM 2025 | RAN, fronthaul, middleboxes |
| **Performance Isolation for 5G RAN Slices Across Multiple Interfering Cells** | NINeS 2026 | 5G slicing, isolation, interference |
| **EcoCell: Energy Conservation through Traffic Shaping in Cellular Radio Access Networks** | NINeS 2026 | RAN, energy, traffic shaping |
| **BISCAY: Practical Radio KPI Driven Congestion Control for Mobile Networks** | NINeS 2026 | mobile congestion control, radio KPI |
| **Through the Telco Lens: A Countrywide Empirical Study of Cellular Handovers** | IMC 2024 | handover, cellular measurement |
| **Automated, Cross-Layer Root Cause Analysis of 5G Video-Conferencing Quality Degradation** | IMC 2025 | 5G, QoE, root cause analysis |
| **An In-Depth Look into 5G ON-OFF Loops in the Wild** | IMC 2025 | 5G, control loops, measurement |
| **Chronos: Scalable and Cost-Effective Cloud-based RAN Emulation System** | MobiCom 2026 | RAN emulation, cloud RAN |
| **Nexus: Efficient and Scalable Multi-Cell mmWave Baseband Processing with Heterogeneous Compute** | MobiCom 2026 | mmWave, baseband, heterogeneous compute |

### Real-time media and interactive video

| Paper | Venue / year | Normalized keywords |
| --- | --- | --- |
| **Scalable Video Conferencing Using SDN Principles** | SIGCOMM 2025 | video conferencing, SDN, scaling |
| **NIER: Practical Neural-enhanced Low-bitrate Video Conferencing** | SIGCOMM 2025 | RTC, neural enhancement, bitrate |
| **ACE: Sending Burstiness Control for High-Quality Real-time Communication** | SIGCOMM 2025 | RTC, burst control, congestion |
| **Mowgli: Passively Learned Rate Control for Real-Time Video** | NSDI 2025 | rate control, real-time video |
| **Tooth: Toward Optimal Balance of Video QoE and Redundancy Cost by Fine-Grained FEC in Cloud Gaming Streaming** | NSDI 2025 | cloud gaming, FEC, QoE |
| **Syntra: Synthesizing Cross-Layer Controllers for Low-Latency Video Streaming** | NSDI 2026 | low-latency streaming, cross-layer control |
| **Medley: Optimizing Midgress Bandwidth for Commercial Live Streaming CDNs** | NSDI 2026 | live streaming, CDN, bandwidth |
| **Tight Loops, Smooth Streams: Responsive Congestion Control for Real-Time Video** | NINeS 2026 | real-time video, congestion control |
| **Protocol Compliance in Popular RTC Applications** | IMC 2025 | RTC, protocol compliance, measurement |
| **Characterizing User Platforms for Video Streaming in Broadband Networks** | IMC 2024 | streaming, broadband, client heterogeneity |
| **Low-Latency Volumetric Video Conferencing in Congested Networks Through L4S** | MMSys 2025 | volumetric video, L4S, conferencing, low latency |
| **GenStream: Semantic Streaming Framework for Generative Reconstruction of Human-centric Media** | ACM Multimedia 2025 | semantic streaming, generative reconstruction, bandwidth reduction |
| **Watch, Skip, Repeat: Hotspot-Aware Joint Optimization for Video Streaming** | ACM Multimedia 2025 | video streaming, hotspot prediction, joint optimization |

### Immersive / XR / volumetric media

| Paper | Venue / year | Normalized keywords |
| --- | --- | --- |
| **A First Look at Immersive Telepresence on Apple Vision Pro** | IMC 2024 | XR, telepresence, measurement |
| **EdgeGaussian: Real-time Free-Viewpoint Video for Mobile VR via Edge-Client Collaborative Neural Rendering** | MobiCom 2025 | VR, edge rendering, Gaussian splatting |
| **L3GS: Layered 3D Gaussian Splats for Efficient 3D Scene Delivery** | MobiCom 2025 | 3D delivery, Gaussian splatting, streaming |
| **Vega: Fully Immersive Mobile Volumetric Video Streaming with 3D Gaussian Splatting** | MobiCom 2025 | volumetric video, mobile VR |
| **ProxLink: A Lightweight Decentralized Synchronization Framework for Multi-User XR** | MobiCom 2026 | multi-user XR, synchronization |
| **RadioSight: Predictive mmWave XR Network Optimization from Dynamic Neural Radio Fields** | MobiCom 2026 | XR, mmWave, prediction |
| **DeltaAR: Redundancy-Aware Object Detection for Mobile Augmented Reality** | MobiCom 2026 | mobile AR, redundancy, edge perception |
| **A First Look at Multimodal Mobile Application Performance on XR and AI Smart Glasses** | MobiCom 2026 | smart glasses, XR, mobile AI |

### Edge intelligence, robotics, vehicles, and CPS

| Paper | Venue / year | Normalized keywords |
| --- | --- | --- |
| **VI-Planning: Infrastructure-Assisted Real-Time Planning Optimization for Autonomous Driving** | MobiCom 2025 | autonomous driving, edge assistance, planning |
| **CoPe: Taming Collaborative 3D Perception via Lite Network Attention across Mobile Agents** | ICDCS 2025 | collaborative perception, mobile agents |
| **DiVE: Differential Video Encoding for Online Edge-assisted Video Analytics on Mobile Agents** | ICDCS 2025 | video analytics, edge, mobile agents |
| **U-Mesh: Deploying UAV-Mesh Network for Automatic Powerline Inspection in Remote Areas** | ICDCS 2025 | UAV mesh, remote inspection |
| **Failure-Aware Tasking for Teams of Drones** | ICDCS 2025 | drone fleets, failures, tasking |
| **TURBO: Utility-Aware Bandwidth Allocation for Cloud-Augmented Autonomous Control** | NINeS 2026 | autonomous control, bandwidth allocation, cloud |
| **Scalable Routing in a City-Scale Wi-Fi Network for Disaster Recovery** | NINeS 2026 | disaster recovery, Wi-Fi mesh, routing |
| **“Take Me Home, Wi-Fi Drone”: A Drone-based Wireless System for Wilderness Search and Rescue** | MobiCom 2026 | UAV, Wi-Fi, search and rescue |

### Internet measurement and infrastructure

| Paper | Venue / year | Normalized keywords |
| --- | --- | --- |
| **Censys: A Map of Internet Hosts and Services** | SIGCOMM 2025 | Internet scanning, asset discovery |
| **Threading the Ocean: Mapping Digital Routes Across Submarine Cables using Calypso** | SIGCOMM 2025 | submarine cables, path inference |
| **MetAS Critic: Reframing AS-Level Topology Discovery as a Recommendation System** | IMC 2024 | AS topology, inference |
| **The wisdom of the measurement crowd: Building a knowledge graph for the Internet** | IMC 2024 | Internet knowledge graph, measurement |
| **Have you SYN me? Characterizing Ten Years of Internet Scanning** | IMC 2024 | Internet scanning, longitudinal measurement |
| **Collecting Self-reported Semantics of BGP Communities and Investigating Their Consistency with Real-world Usage** | IMC 2024 | BGP communities, routing |
| **Sublet Your Subnet: Inferring IP Leasing in the Wild** | IMC 2024 | IP leasing, address infrastructure |
| **Seeds of Scanning: Understanding the Effects of Datasets, Methods, and Metrics on IPv6 Address Discovery** | IMC 2024 | IPv6, scanning, methodology |
| **Understanding Partial Reachability in the Internet Core** | NINeS 2026 | reachability, Internet core |
| **Monitoring Latency on Submarine Cables: Limitations and Opportunities** | NINeS 2026 | submarine cables, latency measurement |
| **Who Holds the Steering Wheel? Opacity and Consolidation in CDN Replica Selection** | NINeS 2026 | CDN, replica selection, concentration |
| **Beyond Data Points: Regionalizing Crowdsourced Latency Measurements** | SIGMETRICS 2025 | latency measurement, geographic aggregation |
| **Internet Service Usage and Delivery As Seen From a Residential Network** | SIGMETRICS 2025 | residential networks, traffic characterization |

### Network security, privacy, and censorship

| Paper | Venue / year | Normalized keywords |
| --- | --- | --- |
| **A System to Detect Forged-Origin BGP Hijacks** | NSDI 2024 | BGP security, hijack detection |
| **Formalizing Dependence of Web Infrastructure** | SIGCOMM 2025 | infrastructure security, dependency |
| **Reliable and Decentralized Certificate Revocation via DNS: The Case for RevDNS** | SIGCOMM 2025 | PKI, DNS, revocation |
| **Achieving High-Speed and Robust Encrypted Traffic Anomaly Detection with Programmable Switches** | SIGCOMM 2025 | encrypted traffic, anomaly detection, programmable switches |
| **Rumors Stop with the Wise: Unveiling Inbound SAV Deployment through Spoofed ICMP Messages** | IMC 2024 | source-address validation, spoofing |
| **The Age of DDoScovery: An Empirical Comparison of Industry and Academic DDoS Assessments** | IMC 2024 | DDoS, measurement |
| **Exposing and Circumventing SNI-based QUIC Censorship of the Great Firewall of China** | USENIX Security 2025 | QUIC, censorship, measurement |
| **Censorship Evasion with Unidentified Protocol Generation** | USENIX Security 2025 | censorship evasion, protocol generation |
| **Catch-22: Uncovering Compromised Hosts using SSH Public Keys** | USENIX Security 2025 | Internet scanning, compromise detection |
| **Your Shield is My Sword: A Persistent Denial-of-Service Attack via the Reuse of Unvalidated Caches in DNSSEC Validation** | USENIX Security 2025 | DNSSEC, DoS |
| **Deanonymizing Ethereum Validators: The P2P Network Has a Privacy Issue** | USENIX Security 2025 | P2P, privacy, blockchain |

### Cloud, serverless, disaggregated systems, and microservices

| Paper | Venue / year | Normalized keywords |
| --- | --- | --- |
| **Autothrottle: A Practical Bi-Level Approach to Resource Management for SLO-Targeted Microservices** | NSDI 2024 | microservices, SLO, resource control |
| **Palladium: A DPU-enabled Multi-Tenant Serverless Cloud over Zero-copy Multi-node RDMA Fabrics** | SIGCOMM 2025 | DPU, serverless, RDMA, multi-tenancy |
| **The Tale of Errors in Microservices** | SIGMETRICS 2025 | microservices, failures, reliability |
| **Microns: Connection Subsetting for Microservices in Shared Clusters** | SIGMETRICS 2025 | microservices, connections, shared clusters |
| **PipeCo: Pipelining Cold Start of Deep Learning Inference Services on Serverless Platforms** | SIGMETRICS 2025 | serverless, cold start, inference |
| **Exploring Function Granularity for Serverless Machine Learning Application with GPU Sharing** | SIGMETRICS 2025 | serverless, GPU sharing, ML |
| **Octopus: Decentralized Workflow-granular Scheduling for Serverless Workflow** | ICDCS 2025 | serverless, decentralized scheduling |
| **Efficient Serverless Cold Start: Reducing Library Loading Overhead by Profile-guided Optimization** | ICDCS 2025 | serverless, cold start |

### Deterministic networking, quantum networking, and sustainability

| Paper | Venue / year | Normalized keywords |
| --- | --- | --- |
| **T(SN)-Ray: Gauging TAS and PSFP Delays of TSN Switches for Predictable Deterministic Networking** | CoNEXT / Proceedings of the ACM on Networking, 2025 | TSN, deterministic networking, latency |
| **Elastic Scheduling for Mix-Flow in Time-Sensitive Networking** | ICDCS 2025 | TSN, scheduling, mixed criticality |
| **Optimal Scheduling in a Quantum Switch** | SIGMETRICS 2025 | quantum networking, scheduling |
| **Quantum Network Optimization: From Optimal Routing to Fair Resource Allocation** | SIGMETRICS 2025 | quantum routing, fairness |
| **Peer-to-Peer Distribution of Graph States Across Spacetime Quantum Networks of Arbitrary Topology** | SIGMETRICS 2025 | quantum networking, P2P, graph states |
| **CloudQC: A Network-aware Framework for Multi-tenant Distributed Quantum Computing** | ICDCS 2025 | distributed quantum computing, network-aware scheduling |
| **Stealthy Low Earth Orbit Satellite-to-Ground Quantum Communication** | NINeS 2026 | quantum communication, LEO |
| **EcoCell: Energy Conservation through Traffic Shaping in Cellular Radio Access Networks** | NINeS 2026 | energy, RAN, traffic shaping |
| **GreenFL: Carbon-efficient Federated Learning over RE Powered Edge Computing Systems** | ICDCS 2025 | carbon-aware computing, federated learning |
| **ForgetMeNot: Understanding and Modeling the Impact of Forever Chemicals Toward Sustainable Large-Scale Computing** | SIGMETRICS 2025 | sustainability, systems lifecycle |

## Project-domain pool

The project pool is organized as a **domain × design-aspect** matrix, with optional **subdomain / technology tags**. A project should normally choose:

1. one top-level **domain** that defines the system/environment being studied;
2. one or more **design aspects** that define the actual networking decision or trade-off;
3. optional **technology/context tags** that narrow the setting without becoming a separate project family.

This is deliberately different from treating every recurring keyword as a project area. For example, **Wi-Fi**, **TSN**, **V2X**, **UAVs**, **XR**, and **serverless** are useful project contexts, but they are better treated as subdomains/tags inside broader networking domains.

The counts below are based on the stricter project-mappable subset of the corpus: papers must have both a defensible domain and a meaningful design aspect. Counts use the paper's primary mapped domain after merging obvious subdomains.

### 1. Cellular & Wireless Access Networks

This top-level domain absorbs the narrower former domains **Cellular RAN & 5G/6G**, **Wireless Access & Spectrum**, **Wi-Fi / Ad Hoc / Mesh**, and generic **Mobile Connectivity**.

**Corpus signal:** about **1,570** primary-mapped papers.

**Subdomains / technology tags:** cellular RAN; Wi-Fi/WLAN; ad hoc/mesh; spectrum/radio access; **5G**; **6G**; **O-RAN**; network slicing; **Wi-Fi**; **RIS**; **NOMA**; beamforming; **URLLC**; **ISAC**; D2D; massive/cell-free MIMO.

**Strong design aspects:** scheduling & resource allocation; MAC/spectrum/radio-resource management; mobility & handover; admission control/network slicing; latency/deadline optimization; QoS/QoE; throughput/capacity; energy efficiency; security/privacy.

**Typical project shape:** determine how radio/network state should influence scheduling, slicing, handover, transport, or admission while preserving isolation, stability, and application performance.

### 2. Edge, Cloud & Networked Services

This top-level domain absorbs **Edge & MEC Systems** and **Cloud / Serverless / Microservices**.

**Corpus signal:** about **1,526** primary-mapped papers.

**Subdomains / technology tags:** **MEC**; edge intelligence; cloud-edge orchestration; fog computing; serverless; microservices; service mesh; digital twins; disaggregated resources.

**Strong design aspects:** placement/offloading/partitioning; scheduling/resource allocation; latency/deadline optimization; cost/provisioning; QoS/SLO management; energy/sustainability; security/privacy; mobility-aware placement; traffic engineering.

**Typical project shape:** decide where computation/state/services should live and move when network paths, compute capacity, cold starts, SLOs, mobility, and failures interact.

### 3. Packet Networks & End-to-End Protocols

**Corpus signal:** about **833** primary-mapped papers.

**Subdomains / technology tags:** transport protocols; packet routing; queueing; multipath; **TCP**; **QUIC**; **FEC**; SDN-assisted control.

**Strong design aspects:** transport & congestion control; routing & path selection; latency/deadline optimization; scheduling/resource allocation; reliability/fault recovery; throughput/capacity; protocol design/interoperability; queueing/stability.

**Typical project shape:** study a protocol or algorithmic design choice that is not tied to one deployment environment, then validate its behavior across scale, latency, loss, or failure regimes.

### 4. Autonomous & Cyber-Physical Networks

This top-level domain absorbs **Vehicular & V2X Networks**, **UAV & Aerial Networks**, and **Robotics & Cyber-Physical Networks**.

**Corpus signal:** about **615** primary-mapped papers.

**Subdomains / technology tags:** vehicular/V2X; UAV/aerial; robotics/teleoperation; **V2X**; UAV swarms; autonomous driving; cooperative perception; ITS; digital twins; MEC; 5G/6G.

**Strong design aspects:** scheduling/resource allocation; placement/offloading; latency/deadline optimization; mobility/handover; routing; MAC/radio-resource management; reliability/recovery; security/privacy; energy.

**Typical project shape:** decide which sensing/control functions remain local, peer-to-peer, edge-assisted, or cloud-assisted under mobility, deadlines, failures, and changing wireless capacity.

### 5. IoT, Sensor & Industrial Networks

This top-level domain absorbs the narrower former domains **IoT / Sensor / LPWAN** and **Industrial / Deterministic Networking**.

**Corpus signal:** about **568** primary-mapped papers.

**Subdomains / technology tags:** sensor networks; LPWAN; industrial/factory networks; deterministic networking; **TSN**; **LoRa/LPWAN**; **RFID**; backscatter; energy harvesting; industrial IoT; URLLC.

**Strong design aspects:** scheduling/resource allocation; latency/deadline guarantees; security/privacy/trust; energy/sustainability; routing; reliability/recovery; MAC/channel access; QoS; freshness/Age of Information.

**Typical project shape:** trade energy, reliability, bounded delay, and network utilization for constrained sensors or industrial flows with explicit workload/deadline assumptions.

### 6. Datacenter & AI Cluster Networks

**Corpus signal:** about **401** primary-mapped papers.

**Subdomains / technology tags:** datacenter transport; AI/GPU clusters; **RDMA**; **RoCE**; **ECN**; **PFC**; **SmartNIC/DPU**; **collectives**; **coflows**; **in-network aggregation**; optical interconnects; **P4**.

**Strong design aspects:** transport & congestion control; programmability & hardware offload; scheduling & resource allocation; throughput/capacity/scalability; traffic engineering & load balancing; routing/path selection; topology/fabric design; reliability/fault recovery.

**Typical project shape:** compare how endpoints, NICs, switches, topology, and scheduling should divide responsibility for mixed RDMA/TCP/collective workloads under contention and failures.

### 7. Network Security, Privacy & Censorship

**Corpus signal:** about **321** primary-mapped papers.

**Subdomains / technology tags:** routing/DNS security; traffic security; censorship resistance; anonymity; **DDoS**; intrusion detection; encrypted traffic; **DNSSEC**; TLS; QUIC; Tor/onion services.

**Strong design aspects:** security/privacy/trust; traffic analysis/classification; verification/correctness; telemetry/monitoring; control-plane management; packet processing; reliability; protocol design/interoperability.

**Typical project shape:** identify a network/protocol assumption an attacker can exploit, then compare deployable defenses under measurable compatibility, performance, and operational costs.

### 8. Real-Time Media & Immersive Networking

This top-level domain absorbs **Real-Time Media & Streaming** and **XR & Immersive Networking**.

**Corpus signal:** about **295** primary-mapped papers.

**Subdomains / technology tags:** conferencing; interactive/live streaming; cloud gaming; XR/AR/VR; volumetric media; **WebRTC**; **ABR**; **FEC**; **QUIC**; volumetric video; 3D Gaussian splatting.

**Strong design aspects:** latency/deadline optimization; QoS/QoE management; application adaptation & cross-layer control; transport/congestion control; coding/compression/redundancy; placement/offloading; architecture/system design; synchronization.

**Typical project shape:** jointly choose transport, adaptation, redundancy, forwarding topology, representation, and edge placement to optimize interactive QoE under changing capacity and delay.

### 9. Distributed AI & LLM Systems

This remains a top-level domain because the same AI workload spans datacenter, edge, and wireless environments; making it only a datacenter tag would hide important cross-environment design choices.

**Corpus signal:** about **290** primary-mapped papers.

**Subdomains / technology tags:** distributed/federated training; inference/serving; split inference; **federated learning**; distributed training; **LLM inference**; model serving; **MoE**; **KV cache**; collectives; differential privacy.

**Strong design aspects:** scheduling/resource allocation; model/state placement & movement; placement/offloading/partitioning; coding/compression; latency optimization; energy efficiency; security/privacy; cost/provisioning; reliability.

**Typical project shape:** determine where model computation/state should reside and how communication should be scheduled or compressed while meeting throughput, tail-latency, cost, and failure objectives.

### 10. Satellite & Non-Terrestrial Networks

**Corpus signal:** about **275** primary-mapped papers.

**Subdomains / technology tags:** **LEO**; satellite Internet; **Starlink**; direct-to-cell; inter-satellite links; ground stations; satellite-terrestrial integration; NTN; satellite edge.

**Strong design aspects:** routing/path selection; mobility/handover; scheduling/resource allocation; latency optimization; placement/offloading; capacity/scalability; reliability; QoS; cost/provisioning.

**Typical project shape:** combine constellation dynamics with routing, handover, transport, caching/compute placement, or reservations for a concrete workload.

### 11. Network Measurement & Operations

**Corpus signal:** about **267** primary-mapped papers.

**Subdomains / technology tags:** observability; telemetry; troubleshooting; configuration/state management; network digital twins; **P4**; **SDN**; **SRv6**.

**Strong design aspects:** telemetry & monitoring; measurement & characterization; diagnosis & root-cause analysis; verification/correctness; packet-processing data structures; programmability/hardware offload; control-plane management.

**Typical project shape:** decide what to measure, at what granularity/cost, and how to turn partial observations into safe diagnosis, verification, or automated remediation.

### 12. Programmable Network Infrastructure

This is the broader parent for the former **Programmable Networks & NFV** domain.

**Corpus signal:** about **256** primary-mapped papers.

**Subdomains / technology tags:** programmable data planes; NFV; service chaining; in-network computing; middleboxes; **P4**; **eBPF**; **SmartNIC/DPU**; **NFV**; service-function chaining; **SDN**.

**Strong design aspects:** programmability/hardware offload; service chaining/virtualization; packet processing/data structures; control-plane design; placement/offloading; scheduling; latency; verification/correctness; security.

**Typical project shape:** decide what functionality belongs in the switch/NIC/DPU/host/controller and evaluate the resulting performance, correctness, deployability, and failure trade-offs.

### 13. Internet Routing, WAN & CDN

**Corpus signal:** about **184** primary-mapped papers.

**Subdomains / technology tags:** interdomain routing; WANs; naming/addressing; CDNs; **BGP**; **DNS**; **IPv6**; **Anycast**; submarine cables; Internet scanning; Tor/onion services.

**Strong design aspects:** routing/path selection; measurement & characterization; security/privacy/trust; traffic engineering & load balancing; control-plane design; architecture/system design; reliability/fault recovery.

**Typical project shape:** make and test a falsifiable claim about Internet-scale routing, naming, reachability, CDN placement, or path behavior using real measurements and explicit bias/error analysis.

### 14. P2P & Decentralized Networks

**Corpus signal:** about **120** primary-mapped papers.

**Subdomains / technology tags:** peer-to-peer overlays; blockchain networks; decentralized services; **Blockchain/P2P**; payment channels; anonymous communication.

**Strong design aspects:** distributed coordination/consensus; security/privacy/trust; throughput/scalability; reliability/fault recovery; routing; protocol design/interoperability; latency; topology/architecture.

**Typical project shape:** analyze how overlay topology, routing, coordination, incentives, or failure assumptions affect scalability, privacy, or consistency.

### 15. Quantum Networks

**Corpus signal:** about **46** primary-mapped papers; exploratory.

**Subdomains / technology tags:** quantum Internet; entanglement distribution; quantum switches; distributed quantum systems; **quantum entanglement**.

**Strong design aspects:** routing/path selection; scheduling/resource allocation; topology/architecture; capacity/scalability; fairness; placement; reliability; cost/provisioning.

**Typical project shape:** allocate entanglement/routing/scheduling resources under fidelity, latency, capacity, and fairness constraints, normally in simulation.

### 16. Harsh-Environment & Delay-Tolerant Networks

This is the broader parent for the former **Underwater & Harsh-Environment Networks** domain.

**Corpus signal:** about **28** primary-mapped papers; targeted/exploratory.

**Subdomains / technology tags:** underwater acoustic networks; disconnected/intermittent networks; **underwater acoustic**; **DTN**.

**Strong design aspects:** routing; energy efficiency; scheduling/resource allocation; MAC/channel access; reliability; protocol design/interoperability; security; latency under long/intermittent paths.

**Typical project shape:** design routing, access, buffering, or reliability mechanisms where conventional always-connected low-delay assumptions do not hold.

### Cross-cutting aspects, not standalone domains

Several recurring themes should **not** become separate project domains because they are stronger as a design axis applied to another domain:

- **Energy / carbon / sustainability**
- **Reliability / fault tolerance / recovery**
- **Latency / deadline optimization**
- **QoS / QoE / SLO management**
- **Security / privacy / trust**
- **Cost / economics / provisioning**
- **Fairness / isolation / multi-tenancy**
- **Coding / compression / redundancy**
- **Measurement / characterization**
- **Verification / correctness**

For example, a strong project is **Satellite & NTN × Reliability** or **Datacenter & AI Cluster Networks × Energy**, not a generic “reliability project” or “green networking project.”

### How teams should use the pool

A team's matrix should therefore be built from:

**Domain × Design aspect × optional subdomain/technology tag(s)**

Examples:

- **Datacenter & AI Cluster Networks × Transport & Congestion Control × RDMA/RoCE**
- **Cellular & Wireless Access Networks × Admission Control & Network Slicing × O-RAN/5G**
- **Satellite & NTN × Routing & Path Selection × LEO/inter-satellite links**
- **Autonomous & Cyber-Physical Networks × Placement & Offloading × V2X/cooperative perception**
- **Real-Time Media & Immersive Networking × Application Adaptation × WebRTC/ABR**
- **Distributed AI & LLM Systems × Model/State Placement × KV cache/MoE**
- **IoT, Sensor & Industrial Networks × Latency & Deadline Optimization × TSN**

Tags narrow a project; they do not replace the need to articulate a design question. A team may use more than one tag and more than one aspect when the interaction itself is the research question, but the scope should remain small enough to evaluate rigorously in the available project time.

## Areas de-emphasized from the previous pool

The broader corpus changes several earlier conclusions:

- **Smart grid / energy infrastructure** should not be a top-level project family unless anchored in a concrete networking problem such as UAV inspection, TSN, or resilient control.
- **Massive IoT** is too broad as a standalone label. Stronger briefs should be phrased as satellite IoT, industrial sensing, edge intelligence, smart environments, or low-power wireless systems.
- **Cloud gaming** is best treated as a subcase of **interactive real-time media**, unless a team has a question specifically about rendering placement or game-streaming FEC.
- **Satellite remote sensing** and **direct-to-device satellite communication** should be merged into the larger **LEO / non-terrestrial networking** family, then specialized by workload.
- **Live interactive broadcasting** belongs under real-time media/CDN design rather than as a separate family.
- **Collaborative AR** is a tag/subdomain under **Real-Time Media & Immersive Networking**, not a standalone domain.
- **Teleoperation** is a tag/subdomain under **Autonomous & Cyber-Physical Networks**, not a standalone domain.
- **Content delivery in poor-connectivity regions** remains a useful application scenario but does not appear as a dense standalone research cluster in this corpus.
- **Multiplayer online games** remains weaker than cloud gaming/RTC/XR in the recent requested venues.

## Recommended shortlist for Fall 2026

If the course wants to expose students to a smaller menu rather than all sixteen domains, the strongest starting set is listed below in descending order of current project-mappable paper count:

1. Cellular & Wireless Access Networks
2. Edge, Cloud & Networked Services
3. Packet Networks & End-to-End Protocols
4. Autonomous & Cyber-Physical Networks
5. Datacenter & AI Cluster Networks
6. Network Security, Privacy & Censorship
7. Real-Time Media & Immersive Networking
8. Distributed AI & LLM Systems
9. Satellite & Non-Terrestrial Networks
10. Network Measurement & Operations
11. Programmable Network Infrastructure
12. Internet Routing, WAN & CDN

The remaining domains—IoT/industrial, P2P/decentralized, quantum, and harsh-environment/DTN—are still valid project spaces, but are more useful as targeted options when a team or TA has a concrete question and suitable evaluation environment.

The hierarchy is intended to remain robust to AI capability improvements: difficulty should come from selecting and defending the **domain × aspect × tags** combination, designing experiments, validating system behavior, and reasoning about trade-offs rather than from implementation effort alone.

## Project-release gate

An area should become a released project only when it has:

1. a concrete workload or operational objective;
2. at least two interacting network/system design dimensions;
3. measurable scalability, reliability, and performance outcomes;
4. a plausible open toolchain, emulator, simulator, trace, or implementation;
5. at least one baseline and multiple defensible alternative architectures;
6. failures or scale limits that can be experimentally exposed;
7. enough scope for a 3–4 person team without requiring inaccessible hyperscale infrastructure;
8. at least three recent papers from this corpus that disagree, optimize different parts of the stack, or expose a meaningful unresolved trade-off;
9. a research question that students can answer with evidence rather than merely reproduce a paper;
10. an evaluation plan that makes AI-assisted implementation auditable and requires the team to defend its design and validation decisions.

## Corpus provenance and reproducibility

The corpus is intentionally stored as frozen per-venue/per-journal snapshots so future course revisions do not depend on a live endpoint continuing to behave the same way.

Conference adapters were validated venue by venue against official accepted-paper/program/proceedings pages or exact proceedings inventories before being frozen. The current conference coverage is:

- SIGCOMM: 71 / 62 / 88 / 109 papers for 2023–2026;
- CoNEXT: 30 / 40 / 50 / 60;
- NSDI: 96 / 112 / 83 / 151;
- ICNP: 35 / 49 / 61 / 68;
- INFOCOM: 251 / 256 / 272 / 327;
- SIGMETRICS: 54 / 48 / 66 / 54;
- IMC: 52 / 55 / 72 / 77;
- ACM Multimedia: 1,013 / 1,237 / 1,575 for 2023–2025;
- NINeS: 28 papers in 2026;
- MobiCom: 91 / 103 / 76 / 87;
- MMSys: 57 / 69 / 41 / 60;
- IPDPS: 95 / 88 / 106 / 101;
- ICDCS: 83 / 121 / 103 / 138;
- OSDI: 55 / 53 / 53 / 137;
- USENIX Security: 422 / 418 / 455 / 377.

The exact source configuration and collection code are versioned under `tools/research/`. `tools/research/assemble_validated_corpus.py` fails closed if a frozen conference snapshot falls below its configured yearly minimum, violates an exact count where one is known, lacks required paper metadata, or if a Transactions snapshot contains a row not marked network-relevant.

The 2027 portion should be refreshed only after actual 2027 publication/acceptance metadata becomes available; the current corpus does not manufacture future records.
