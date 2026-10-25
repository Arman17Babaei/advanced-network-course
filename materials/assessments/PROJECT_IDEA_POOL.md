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

## Updated project-area pool

The pool below is the course-facing result of the literature scan. Areas are ranked not merely by paper count but by whether they force students to make and defend **network architecture decisions** across scalability, reliability, and performance.

### 1. AI cluster networks for large-model training

**Why this moved to the top.** Recent SIGCOMM, ICNP, ICDCS, OSDI, IPDPS/TPDS-style work makes communication architecture itself a first-class part of large-model training: topology, collectives, scheduling, optical/electrical fabrics, RDMA, in-network aggregation, placement, and failures.

**Good project question shape.** Given a training workload with a known communication graph, what combination of topology, collective algorithm, flow/coflow scheduling, placement, and failure recovery minimizes job completion time under realistic oversubscription and failures?

**Likely tools.** ns-3 / OMNeT++, SimAI or similar simulators, small-scale NCCL/MPI experiments, Mininet/container testbeds, synthetic collective traces.

**Research anchors.** ByteScale; MixNet; SyCCL; SchedEP; Taming Step Misalignment; Shuffle-Exchange; ACCL+.

### 2. Distributed and disaggregated LLM inference

**Why it is distinct from training.** Inference has different communication structure: request routing, batching, KV-cache movement, disaggregated prefill/decode, expert placement, edge/cloud split, and tail-latency SLOs.

**Good project question shape.** Under a heterogeneous cluster or edge/cloud hierarchy, where should model state and computation live, how should requests be routed, and when is moving KV/model state cheaper than recomputation?

**Likely tools.** vLLM/SGLang-like serving stacks where feasible, trace-driven simulation, container clusters, synthetic KV-transfer workloads.

**Research anchors.** MegaScale-Infer; KVServe; DualPath; MCaM; CFMoE; CRISP.

### 3. Datacenter transport, congestion control, and programmable data planes

**Why it is a core project family.** The literature remains dense and technically deep, but the project should avoid becoming “implement one congestion-control algorithm.” Students should instead compare architectures under mixed workloads and failure/queueing regimes.

**Good project question shape.** How should endpoints, switches, and NICs divide responsibility for congestion signals, load balancing, rate control, and loss recovery for mixed TCP/RDMA/collective workloads?

**Likely tools.** ns-3, Mininet, Linux traffic control, P4/BMv2, eBPF, DPDK, programmable-switch emulators.

**Research anchors.** No Signal to Rule Them All; Simulate Before Sending; PEE; Fast RDMA Rate Limiter; Hawkeye; OptimusPrime.

### 4. Network telemetry, diagnosis, reliability, and automated operations

**Why it became a separate area.** Across SIGCOMM, NSDI, IMC, SIGMETRICS, and ICNP there is sustained work on observing, explaining, verifying, and repairing large networks. This fits the course especially well because students must reason about observability gaps and failure modes, not only optimize steady-state throughput.

**Good project question shape.** What telemetry should be collected, at what granularity and cost, to detect and localize a chosen class of failures quickly enough for safe automated remediation?

**Likely tools.** P4 telemetry, eBPF, Prometheus/OpenTelemetry, emulated WAN/datacenter topologies, fault injection, network digital twins.

**Research anchors.** Raha; Hawkeye; SketchPlan; INT-MC; CAPA; SlaRepair; VeriNC.

### 5. LEO satellite and non-terrestrial networks

**Why this is now broader than “satellite remote sensing.”** Recent work spans direct-to-cell, congestion control, CDN placement, task offloading, routing, measurement, capacity markets, remote sensing, and satellite-edge intelligence. It is one of the clearest multi-layer design spaces in the corpus.

**Good project question shape.** For a moving LEO constellation and terrestrial users, how should routing, handover, congestion control, caching/compute placement, and admission/reservation interact for a specific workload?

**Likely tools.** Hypatia/SatGen-style constellation simulation, ns-3, public TLEs, Starlink measurement traces, trace-driven application models.

**Research anchors.** Democratizing Direct-to-Cell LEO Networks; LeoCC; StarCDN; CrowdLink; Space Booking; MCSR routing; prediction-based LEO offloading.

### 6. 5G/6G RAN and mobile network control

**Why this is a project area.** The research cluster combines radio conditions with transport, slicing, energy, fronthaul, control-plane behavior, and application QoE. It gives students an explicit cross-layer design problem.

**Good project question shape.** How should a mobile network expose and use radio/network state to allocate capacity or control transport while preserving isolation, stability, and energy efficiency?

**Likely tools.** srsRAN/OpenAirInterface, Colosseum-like traces where available, ns-3 5G-LENA, RAN emulation.

**Research anchors.** RANBooster; 5G RAN slice isolation; BISCAY; EcoCell; 5G video-conferencing root-cause analysis; Chronos.

### 7. Real-time communication, conferencing, and interactive streaming

**Why this remains one of the best course projects.** It has direct user-visible outcomes, open-source implementations, network/application cross-layer choices, and meaningful reliability/performance trade-offs.

**Good project question shape.** For heterogeneous receivers and changing paths, what combination of congestion control, bitrate/quality adaptation, forwarding topology, redundancy/FEC, and edge placement maximizes interactive QoE?

**Likely tools.** WebRTC, Pion/mediasoup/Janus, tc/netem, Mahimahi, video traces, objective QoE metrics.

**Research anchors.** Scalable Video Conferencing Using SDN Principles; NIER; ACE; Mowgli; Syntra; Tight Loops, Smooth Streams.

### 8. XR, immersive telepresence, and volumetric media

**Why it deserves its own project family.** The recent mobile/multimedia literature has shifted from ordinary 2D video toward 3D representations, neural rendering, multi-user synchronization, mmWave-aware delivery, and smart glasses.

**Good project question shape.** Which representation, partitioning, rendering placement, transport, caching, and synchronization strategy gives the best motion-to-photon latency and visual quality under mobility and bandwidth variation?

**Likely tools.** Unity/Unreal, WebXR, 3D Gaussian Splatting pipelines, trace-driven network emulation.

**Research anchors.** EdgeGaussian; L3GS; Vega; ProxLink; RadioSight; Apple Vision Pro telepresence measurement.

### 9. Edge intelligence and collaborative perception

**Why this is broader than “edge video analytics.”** Recent work includes split multimodal inference, collaborative 3D perception, mobile agents, on-device LLMs, service placement, and semantic communication.

**Good project question shape.** What information should devices process locally, compress, summarize, or transmit, and where should downstream inference run when bandwidth, energy, accuracy, and latency all matter?

**Likely tools.** PyTorch, edge devices or emulated resource limits, prerecorded sensor/video data, network emulation.

**Research anchors.** S2M3; CoPe; DiVE; TASP; DeltaAR; on-device / edge MoE serving work.

### 10. Networked robotics, UAVs, vehicles, and autonomous control

**Why it is attractive.** Networking choices affect the physical system’s objective, not just packet metrics. The literature spans UAV mesh networks, search and rescue, autonomous-driving planning, collaborative perception, and cloud-augmented control.

**Good project question shape.** What data/control functions should be local, peer-to-peer, edge-assisted, or cloud-assisted under mobility, deadlines, failures, and changing wireless capacity?

**Likely tools.** CARLA, SUMO, AirSim, ROS2, ns-3/Veins, network emulation.

**Research anchors.** VI-Planning; U-Mesh; TURBO; Failure-Aware Tasking for Teams of Drones; Take Me Home, Wi-Fi Drone.

### 11. Internet measurement, routing, naming, and CDN infrastructure

**Why this is now a major pool area.** IMC and related SIGCOMM/NINeS work show a deep research stream around BGP, DNS, IPv6, Internet topology, submarine cables, CDN replica selection, scanning, and residential access.

**Good project question shape.** Can students make a falsifiable claim about how a real Internet mechanism behaves, then design a measurement methodology robust to missing data, bias, and confounding?

**Likely tools.** RIPE Atlas, RouteViews/RIS, CAIDA data, Censys/Shadowserver-style datasets where licensed, public DNS/BGP datasets, active probing with strict ethical controls.

**Research anchors.** MetAS Critic; BGP Communities study; Threading the Ocean; Monitoring Latency on Submarine Cables; CDN Replica Selection; IPv6 discovery work.

### 12. Network security and censorship-resilient infrastructure

**Why it belongs in an advanced networking course.** The most useful subset of security papers treats the network protocol or Internet infrastructure itself as the object of study: BGP, DNSSEC, QUIC censorship, scanning, DDoS, encrypted traffic, and P2P privacy.

**Good project question shape.** How does an attacker exploit a network protocol’s assumptions, and what deployable defense changes the attacker/defender trade-off without unacceptable performance or compatibility cost?

**Likely tools.** Mininet, protocol implementations, safe local testbeds, public measurement datasets. No uncontrolled Internet attacks.

**Research anchors.** forged-origin BGP hijack detection; QUIC censorship; UPGen; DNSSEC cache DoS; SAV measurement; encrypted-traffic anomaly detection.

### 13. Cloud, serverless, and disaggregated networked systems

**Why it is useful but should stay network-centered.** The corpus is large, but many systems papers become ordinary resource-management projects. A suitable course project must put communication, placement, network contention, or failure propagation in the critical path.

**Good project question shape.** How should a service partition and place state/functionality across hosts when cold starts, network paths, memory tiers, multi-tenancy, and SLOs interact?

**Research anchors.** Palladium; Autothrottle; Microns; PipeCo; serverless workflow scheduling.

### 14. Deterministic and industrial networking

**Why it is narrower but valuable.** TSN and predictable networking create explicit hard constraints around deadline guarantees, queue scheduling, interference, and fault recovery.

**Good project question shape.** Which scheduling/admission architecture gives bounded latency to critical flows while retaining acceptable utilization for best-effort traffic?

**Likely tools.** ns-3 TSN models, OMNeT++/INET, Linux TSN support, P4.

**Research anchors.** T(SN)-Ray; Elastic Scheduling for Mix-Flow in TSN; industrial monitoring work from MobiCom.

### 15. Quantum networking and distributed quantum systems

**Why it is exploratory.** The cluster is now visible across SIGMETRICS, ICDCS, INFOCOM-style work, and NINeS, but student feasibility depends strongly on simulation and on how much quantum background the course wants to assume.

**Good project question shape.** How should entanglement, routing, scheduling, or remote-gate resources be allocated under fidelity, latency, and fairness constraints?

**Likely tools.** NetSquid, SeQUeNCe, SimulaQron-style simulators.

**Research anchors.** Optimal Scheduling in a Quantum Switch; Quantum Network Optimization; CloudQC; distributed graph-state delivery.

### 16. Sustainable networking and computing

**Why it is exploratory rather than standalone by default.** Energy/carbon is increasingly present, but it is strongest when used as a cross-cutting constraint on another networked system rather than as an isolated optimization exercise.

**Good project question shape.** How much energy/carbon can be saved by changing network scheduling, placement, or traffic shaping without violating latency/reliability SLOs?

**Research anchors.** EcoCell; GreenFL; sustainable large-scale computing work in SIGMETRICS.

## Areas de-emphasized from the previous pool

The broader corpus changes several earlier conclusions:

- **Smart grid / energy infrastructure** should not be a top-level project family unless anchored in a concrete networking problem such as UAV inspection, TSN, or resilient control.
- **Massive IoT** is too broad as a standalone label. Stronger briefs should be phrased as satellite IoT, industrial sensing, edge intelligence, smart environments, or low-power wireless systems.
- **Cloud gaming** is best treated as a subcase of **interactive real-time media**, unless a team has a question specifically about rendering placement or game-streaming FEC.
- **Satellite remote sensing** and **direct-to-device satellite communication** should be merged into the larger **LEO / non-terrestrial networking** family, then specialized by workload.
- **Live interactive broadcasting** belongs under real-time media/CDN design rather than as a separate family.
- **Collaborative AR** belongs under XR / immersive systems.
- **Teleoperation** belongs under networked robotics / autonomous control.
- **Content delivery in poor-connectivity regions** remains a useful application scenario but does not appear as a dense standalone research cluster in this corpus.
- **Multiplayer online games** remains weaker than cloud gaming/RTC/XR in the recent requested venues.

## Recommended shortlist for Fall 2026

If the course wants roughly **6–10 broad project areas**, the strongest set is:

1. AI cluster networks and distributed training
2. Distributed / disaggregated LLM inference
3. Datacenter transport and programmable networking
4. Network telemetry, diagnosis, reliability, and automated operations
5. LEO satellite / non-terrestrial networking
6. 5G/6G RAN and mobile networking
7. Real-time communication and interactive media
8. XR / immersive / volumetric media
9. Edge intelligence + networked autonomous systems
10. Internet measurement, routing, naming, CDN, and network security

The last item can be split into **Internet infrastructure measurement** and **network security** if the teaching team wants more than ten areas.

This shortlist is more robust to rapid AI progress than the previous application-only list because difficulty comes from **architecture choice, experimentation, measurement validity, failure behavior, and trade-offs**, not from implementation difficulty alone.

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
