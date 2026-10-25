# Research Corpus and Project-Area Coverage

This README documents the literature corpus used to build the Advanced Networks project idea pool and the research density of each **domain × design-aspect** cell.

## Counting methodology

- The validated literature corpus contains **16,959 unique papers**.
- The project-area matrix below uses the stricter **7,595-paper project-mappable subset**: each included paper has both a defensible project domain and a meaningful design aspect.
- Each paper is counted **once** using its **primary merged domain** and **primary design aspect**, so aspect counts sum exactly to each domain total.
- Secondary domains, secondary aspects, and technology/context tags are intentionally not double-counted here; they remain useful for narrowing individual projects.
- The current corpus contains 2023–2026 papers. 2027 stays empty until real publication/acceptance metadata exists.

Machine-readable domain/aspect counts: [`PROJECT_DOMAIN_ASPECT_COUNTS.csv`](PROJECT_DOMAIN_ASPECT_COUNTS.csv).
Project taxonomy and domain/tag hierarchy: [`../PROJECT_IDEA_POOL.md`](../PROJECT_IDEA_POOL.md).

## Corpus files

- [`all_conference_papers.csv`](all_conference_papers.csv) — collected conference inventory.
- [`ieee_transactions_network.csv`](ieee_transactions_network.csv) — networking-relevant IEEE Transactions subset.
- [`recent_networking_papers.csv`](recent_networking_papers.csv) — combined 16,959-paper corpus.
- [`PAPER_CORPUS_COVERAGE.csv`](PAPER_CORPUS_COVERAGE.csv) — venue/year coverage.
- [`PAPER_CORPUS_SUMMARY.md`](PAPER_CORPUS_SUMMARY.md) — generated corpus statistics.
- [`venues/`](venues/) and [`transactions/`](transactions/) — frozen validated source snapshots.

## Venues analyzed

### Conferences

| Venue | Total | 2023 | 2024 | 2025 | 2026 | 2027 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| SIGCOMM | 330 | 71 | 62 | 88 | 109 | 0 |
| CoNEXT | 180 | 30 | 40 | 50 | 60 | 0 |
| NSDI | 442 | 96 | 112 | 83 | 151 | 0 |
| ICNP | 213 | 35 | 49 | 61 | 68 | 0 |
| INFOCOM | 1,106 | 251 | 256 | 272 | 327 | 0 |
| SIGMETRICS | 222 | 54 | 48 | 66 | 54 | 0 |
| IMC | 256 | 52 | 55 | 72 | 77 | 0 |
| ACM Multimedia | 3,825 | 1013 | 1237 | 1575 | 0 | 0 |
| NINeS | 28 | 0 | 0 | 0 | 28 | 0 |
| MobiCom | 357 | 91 | 103 | 76 | 87 | 0 |
| MMSys | 227 | 57 | 69 | 41 | 60 | 0 |
| IPDPS | 390 | 95 | 88 | 106 | 101 | 0 |
| ICDCS | 445 | 83 | 121 | 103 | 138 | 0 |
| OSDI | 298 | 55 | 53 | 53 | 137 | 0 |
| USENIX Security | 1,672 | 422 | 418 | 455 | 377 | 0 |

### IEEE Transactions journals

Only networking-relevant papers are retained from these journals.

| Journal | Total | 2023 | 2024 | 2025 | 2026 | 2027 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| IEEE Transactions on Cloud Computing | 149 | 25 | 38 | 36 | 50 | 0 |
| IEEE Transactions on Communications | 337 | 72 | 87 | 98 | 80 | 0 |
| IEEE Transactions on Dependable and Secure Computing | 180 | 31 | 32 | 54 | 63 | 0 |
| IEEE Transactions on Green Communications and Networking | 211 | 42 | 64 | 53 | 52 | 0 |
| IEEE Transactions on Mobile Computing | 1,101 | 156 | 234 | 349 | 362 | 0 |
| IEEE Transactions on Multimedia | 37 | 9 | 6 | 9 | 13 | 0 |
| IEEE Transactions on Network Science and Engineering | 417 | 80 | 84 | 164 | 89 | 0 |
| IEEE Transactions on Network and Service Management | 1,672 | 366 | 429 | 421 | 456 | 0 |
| IEEE Transactions on Networking | 1,131 | 239 | 219 | 335 | 338 | 0 |
| IEEE Transactions on Parallel and Distributed Systems | 126 | 47 | 25 | 30 | 24 | 0 |
| IEEE Transactions on Vehicular Technology | 1,160 | 274 | 281 | 323 | 282 | 0 |
| IEEE Transactions on Wireless Communications | 447 | 139 | 116 | 100 | 92 | 0 |

## Domain totals

| Domain | Project-mappable papers | Share of 7,595-paper subset |
| --- | ---: | ---: |
| Cellular & Wireless Access Networks | 1,570 | 20.7% |
| Edge, Cloud & Networked Services | 1,526 | 20.1% |
| Packet Networks & End-to-End Protocols | 833 | 11.0% |
| Autonomous & Cyber-Physical Networks | 615 | 8.1% |
| IoT, Sensor & Industrial Networks | 568 | 7.5% |
| Datacenter & AI Cluster Networks | 401 | 5.3% |
| Network Security, Privacy & Censorship | 321 | 4.2% |
| Real-Time Media & Immersive Networking | 295 | 3.9% |
| Distributed AI & LLM Systems | 290 | 3.8% |
| Satellite & Non-Terrestrial Networks | 275 | 3.6% |
| Network Measurement & Operations | 267 | 3.5% |
| Programmable Network Infrastructure | 256 | 3.4% |
| Internet Routing, WAN & CDN | 184 | 2.4% |
| P2P & Decentralized Networks | 120 | 1.6% |
| Quantum Networks | 46 | 0.6% |
| Harsh-Environment & Delay-Tolerant Networks | 28 | 0.4% |
| **Total** | **7,595** | **100%** |

## Domain × design-aspect counts

Only non-zero cells are shown. Domains are sorted by total paper count; design aspects are sorted from densest to sparsest within each domain.

### Cellular & Wireless Access Networks — 1,570 papers

| Design aspect | Papers | Share of domain |
| --- | ---: | ---: |
| Scheduling & Resource Allocation | 249 | 15.9% |
| MAC, Spectrum & Radio Resource Management | 234 | 14.9% |
| Security, Privacy & Trust | 150 | 9.6% |
| Mobility & Handover | 136 | 8.7% |
| Admission Control & Network Slicing | 118 | 7.5% |
| Latency & Deadline Optimization | 57 | 3.6% |
| Placement, Offloading & Partitioning | 55 | 3.5% |
| Routing & Path Selection | 54 | 3.4% |
| Energy, Carbon & Sustainability | 48 | 3.1% |
| Architecture & System Design | 46 | 2.9% |
| Transport & Congestion Control | 33 | 2.1% |
| Application Adaptation & Cross-Layer Control | 27 | 1.7% |
| Caching & Content Placement | 26 | 1.7% |
| Service Chaining & Virtualization | 26 | 1.7% |
| Coding, Compression & Redundancy | 25 | 1.6% |
| Reliability, Fault Tolerance & Recovery | 25 | 1.6% |
| Throughput, Capacity & Scalability | 24 | 1.5% |
| Control-Plane Design & Management | 22 | 1.4% |
| Topology, Fabric & Architecture | 22 | 1.4% |
| QoS, QoE & SLO Management | 21 | 1.3% |
| Data/Traffic Prediction & Forecasting | 20 | 1.3% |
| Protocol Design & Interoperability | 19 | 1.2% |
| Measurement & Characterization | 18 | 1.1% |
| Localization & Positioning | 17 | 1.1% |
| Fairness, Isolation & Multi-Tenancy | 15 | 1.0% |
| Freshness & Age of Information | 14 | 0.9% |
| Cost, Economics & Provisioning | 12 | 0.8% |
| Distributed Coordination & Consensus | 10 | 0.6% |
| Programmability & Hardware Offload | 9 | 0.6% |
| Telemetry & Monitoring | 9 | 0.6% |
| Queueing & Stability | 7 | 0.4% |
| Traffic Engineering & Load Balancing | 7 | 0.4% |
| Diagnosis & Root Cause Analysis | 6 | 0.4% |
| Synchronization & Consistency | 3 | 0.2% |
| Traffic Analysis & Classification | 3 | 0.2% |
| Verification & Correctness | 2 | 0.1% |
| Packet Processing & Data Structures | 1 | 0.1% |

### Edge, Cloud & Networked Services — 1,526 papers

| Design aspect | Papers | Share of domain |
| --- | ---: | ---: |
| Placement, Offloading & Partitioning | 631 | 41.3% |
| Scheduling & Resource Allocation | 264 | 17.3% |
| Security, Privacy & Trust | 97 | 6.4% |
| Mobility & Handover | 82 | 5.4% |
| Latency & Deadline Optimization | 58 | 3.8% |
| Caching & Content Placement | 57 | 3.7% |
| MAC, Spectrum & Radio Resource Management | 37 | 2.4% |
| Cost, Economics & Provisioning | 32 | 2.1% |
| Coding, Compression & Redundancy | 31 | 2.0% |
| Energy, Carbon & Sustainability | 25 | 1.6% |
| Routing & Path Selection | 22 | 1.4% |
| Reliability, Fault Tolerance & Recovery | 19 | 1.2% |
| Architecture & System Design | 17 | 1.1% |
| QoS, QoE & SLO Management | 16 | 1.0% |
| Application Adaptation & Cross-Layer Control | 14 | 0.9% |
| Topology, Fabric & Architecture | 13 | 0.9% |
| Freshness & Age of Information | 12 | 0.8% |
| Service Chaining & Virtualization | 11 | 0.7% |
| Programmability & Hardware Offload | 9 | 0.6% |
| Fairness, Isolation & Multi-Tenancy | 8 | 0.5% |
| Protocol Design & Interoperability | 8 | 0.5% |
| Traffic Engineering & Load Balancing | 7 | 0.5% |
| Queueing & Stability | 6 | 0.4% |
| Throughput, Capacity & Scalability | 6 | 0.4% |
| Verification & Correctness | 6 | 0.4% |
| Admission Control & Network Slicing | 5 | 0.3% |
| Data/Traffic Prediction & Forecasting | 5 | 0.3% |
| Control-Plane Design & Management | 4 | 0.3% |
| Distributed Coordination & Consensus | 4 | 0.3% |
| Telemetry & Monitoring | 4 | 0.3% |
| Transport & Congestion Control | 4 | 0.3% |
| Diagnosis & Root Cause Analysis | 3 | 0.2% |
| Measurement & Characterization | 3 | 0.2% |
| Traffic Analysis & Classification | 3 | 0.2% |
| Model/State Placement & Movement | 1 | 0.1% |
| Packet Processing & Data Structures | 1 | 0.1% |
| Synchronization & Consistency | 1 | 0.1% |

### Packet Networks & End-to-End Protocols — 833 papers

| Design aspect | Papers | Share of domain |
| --- | ---: | ---: |
| Transport & Congestion Control | 111 | 13.3% |
| Routing & Path Selection | 93 | 11.2% |
| Security, Privacy & Trust | 78 | 9.4% |
| Scheduling & Resource Allocation | 64 | 7.7% |
| Reliability, Fault Tolerance & Recovery | 39 | 4.7% |
| Protocol Design & Interoperability | 32 | 3.8% |
| Traffic Engineering & Load Balancing | 30 | 3.6% |
| Latency & Deadline Optimization | 28 | 3.4% |
| Cost, Economics & Provisioning | 26 | 3.1% |
| Coding, Compression & Redundancy | 24 | 2.9% |
| Topology, Fabric & Architecture | 24 | 2.9% |
| Control-Plane Design & Management | 23 | 2.8% |
| Caching & Content Placement | 22 | 2.6% |
| Throughput, Capacity & Scalability | 22 | 2.6% |
| Placement, Offloading & Partitioning | 21 | 2.5% |
| Measurement & Characterization | 19 | 2.3% |
| QoS, QoE & SLO Management | 18 | 2.2% |
| Traffic Analysis & Classification | 16 | 1.9% |
| Programmability & Hardware Offload | 15 | 1.8% |
| Application Adaptation & Cross-Layer Control | 13 | 1.6% |
| Queueing & Stability | 13 | 1.6% |
| Data/Traffic Prediction & Forecasting | 12 | 1.4% |
| Verification & Correctness | 11 | 1.3% |
| Distributed Coordination & Consensus | 10 | 1.2% |
| Localization & Positioning | 10 | 1.2% |
| Fairness, Isolation & Multi-Tenancy | 9 | 1.1% |
| Service Chaining & Virtualization | 9 | 1.1% |
| Energy, Carbon & Sustainability | 8 | 1.0% |
| Diagnosis & Root Cause Analysis | 7 | 0.8% |
| Freshness & Age of Information | 7 | 0.8% |
| Packet Processing & Data Structures | 6 | 0.7% |
| MAC, Spectrum & Radio Resource Management | 4 | 0.5% |
| Mobility & Handover | 4 | 0.5% |
| Architecture & System Design | 2 | 0.2% |
| Synchronization & Consistency | 2 | 0.2% |
| Admission Control & Network Slicing | 1 | 0.1% |

### Autonomous & Cyber-Physical Networks — 615 papers

| Design aspect | Papers | Share of domain |
| --- | ---: | ---: |
| Scheduling & Resource Allocation | 115 | 18.7% |
| Placement, Offloading & Partitioning | 112 | 18.2% |
| Security, Privacy & Trust | 67 | 10.9% |
| Mobility & Handover | 64 | 10.4% |
| Routing & Path Selection | 43 | 7.0% |
| MAC, Spectrum & Radio Resource Management | 32 | 5.2% |
| Latency & Deadline Optimization | 31 | 5.0% |
| Caching & Content Placement | 20 | 3.3% |
| Energy, Carbon & Sustainability | 15 | 2.4% |
| Architecture & System Design | 14 | 2.3% |
| Application Adaptation & Cross-Layer Control | 12 | 2.0% |
| Reliability, Fault Tolerance & Recovery | 11 | 1.8% |
| Coding, Compression & Redundancy | 10 | 1.6% |
| Freshness & Age of Information | 9 | 1.5% |
| Distributed Coordination & Consensus | 7 | 1.1% |
| Localization & Positioning | 7 | 1.1% |
| Protocol Design & Interoperability | 6 | 1.0% |
| Admission Control & Network Slicing | 5 | 0.8% |
| Throughput, Capacity & Scalability | 5 | 0.8% |
| Measurement & Characterization | 4 | 0.7% |
| Topology, Fabric & Architecture | 4 | 0.7% |
| Telemetry & Monitoring | 3 | 0.5% |
| Transport & Congestion Control | 3 | 0.5% |
| Control-Plane Design & Management | 2 | 0.3% |
| Cost, Economics & Provisioning | 2 | 0.3% |
| Fairness, Isolation & Multi-Tenancy | 2 | 0.3% |
| Packet Processing & Data Structures | 2 | 0.3% |
| QoS, QoE & SLO Management | 2 | 0.3% |
| Data/Traffic Prediction & Forecasting | 1 | 0.2% |
| Diagnosis & Root Cause Analysis | 1 | 0.2% |
| Model/State Placement & Movement | 1 | 0.2% |
| Programmability & Hardware Offload | 1 | 0.2% |
| Queueing & Stability | 1 | 0.2% |
| Verification & Correctness | 1 | 0.2% |

### IoT, Sensor & Industrial Networks — 568 papers

| Design aspect | Papers | Share of domain |
| --- | ---: | ---: |
| Scheduling & Resource Allocation | 114 | 20.1% |
| Security, Privacy & Trust | 105 | 18.5% |
| Routing & Path Selection | 29 | 5.1% |
| Placement, Offloading & Partitioning | 26 | 4.6% |
| Latency & Deadline Optimization | 22 | 3.9% |
| MAC, Spectrum & Radio Resource Management | 21 | 3.7% |
| Localization & Positioning | 20 | 3.5% |
| Throughput, Capacity & Scalability | 19 | 3.3% |
| Energy, Carbon & Sustainability | 18 | 3.2% |
| Topology, Fabric & Architecture | 18 | 3.2% |
| Coding, Compression & Redundancy | 16 | 2.8% |
| Architecture & System Design | 14 | 2.5% |
| Reliability, Fault Tolerance & Recovery | 13 | 2.3% |
| Cost, Economics & Provisioning | 11 | 1.9% |
| Mobility & Handover | 11 | 1.9% |
| Control-Plane Design & Management | 10 | 1.8% |
| Protocol Design & Interoperability | 8 | 1.4% |
| QoS, QoE & SLO Management | 8 | 1.4% |
| Queueing & Stability | 8 | 1.4% |
| Measurement & Characterization | 7 | 1.2% |
| Service Chaining & Virtualization | 7 | 1.2% |
| Telemetry & Monitoring | 7 | 1.2% |
| Traffic Analysis & Classification | 7 | 1.2% |
| Caching & Content Placement | 6 | 1.1% |
| Freshness & Age of Information | 6 | 1.1% |
| Programmability & Hardware Offload | 6 | 1.1% |
| Synchronization & Consistency | 6 | 1.1% |
| Transport & Congestion Control | 5 | 0.9% |
| Application Adaptation & Cross-Layer Control | 4 | 0.7% |
| Distributed Coordination & Consensus | 4 | 0.7% |
| Admission Control & Network Slicing | 3 | 0.5% |
| Data/Traffic Prediction & Forecasting | 3 | 0.5% |
| Traffic Engineering & Load Balancing | 3 | 0.5% |
| Diagnosis & Root Cause Analysis | 1 | 0.2% |
| Packet Processing & Data Structures | 1 | 0.2% |
| Verification & Correctness | 1 | 0.2% |

### Datacenter & AI Cluster Networks — 401 papers

| Design aspect | Papers | Share of domain |
| --- | ---: | ---: |
| Transport & Congestion Control | 75 | 18.7% |
| Scheduling & Resource Allocation | 49 | 12.2% |
| Programmability & Hardware Offload | 35 | 8.7% |
| Placement, Offloading & Partitioning | 33 | 8.2% |
| Routing & Path Selection | 22 | 5.5% |
| Traffic Engineering & Load Balancing | 22 | 5.5% |
| Latency & Deadline Optimization | 17 | 4.2% |
| Architecture & System Design | 16 | 4.0% |
| Coding, Compression & Redundancy | 14 | 3.5% |
| Topology, Fabric & Architecture | 14 | 3.5% |
| Security, Privacy & Trust | 12 | 3.0% |
| Throughput, Capacity & Scalability | 12 | 3.0% |
| Reliability, Fault Tolerance & Recovery | 10 | 2.5% |
| Diagnosis & Root Cause Analysis | 8 | 2.0% |
| Fairness, Isolation & Multi-Tenancy | 8 | 2.0% |
| Distributed Coordination & Consensus | 7 | 1.7% |
| Measurement & Characterization | 7 | 1.7% |
| Telemetry & Monitoring | 7 | 1.7% |
| Control-Plane Design & Management | 6 | 1.5% |
| Synchronization & Consistency | 5 | 1.2% |
| Energy, Carbon & Sustainability | 4 | 1.0% |
| Cost, Economics & Provisioning | 3 | 0.7% |
| Protocol Design & Interoperability | 3 | 0.7% |
| Queueing & Stability | 3 | 0.7% |
| Localization & Positioning | 2 | 0.5% |
| Service Chaining & Virtualization | 2 | 0.5% |
| Admission Control & Network Slicing | 1 | 0.2% |
| Caching & Content Placement | 1 | 0.2% |
| Data/Traffic Prediction & Forecasting | 1 | 0.2% |
| MAC, Spectrum & Radio Resource Management | 1 | 0.2% |
| Verification & Correctness | 1 | 0.2% |

### Network Security, Privacy & Censorship — 321 papers

| Design aspect | Papers | Share of domain |
| --- | ---: | ---: |
| Security, Privacy & Trust | 183 | 57.0% |
| Traffic Analysis & Classification | 77 | 24.0% |
| Control-Plane Design & Management | 8 | 2.5% |
| Programmability & Hardware Offload | 4 | 1.2% |
| Scheduling & Resource Allocation | 4 | 1.2% |
| Telemetry & Monitoring | 4 | 1.2% |
| Architecture & System Design | 3 | 0.9% |
| Coding, Compression & Redundancy | 3 | 0.9% |
| Measurement & Characterization | 3 | 0.9% |
| Packet Processing & Data Structures | 3 | 0.9% |
| Placement, Offloading & Partitioning | 3 | 0.9% |
| Routing & Path Selection | 3 | 0.9% |
| Transport & Congestion Control | 3 | 0.9% |
| Application Adaptation & Cross-Layer Control | 2 | 0.6% |
| Cost, Economics & Provisioning | 2 | 0.6% |
| Distributed Coordination & Consensus | 2 | 0.6% |
| Protocol Design & Interoperability | 2 | 0.6% |
| Service Chaining & Virtualization | 2 | 0.6% |
| Topology, Fabric & Architecture | 2 | 0.6% |
| Traffic Engineering & Load Balancing | 2 | 0.6% |
| Admission Control & Network Slicing | 1 | 0.3% |
| Diagnosis & Root Cause Analysis | 1 | 0.3% |
| Fairness, Isolation & Multi-Tenancy | 1 | 0.3% |
| Mobility & Handover | 1 | 0.3% |
| Reliability, Fault Tolerance & Recovery | 1 | 0.3% |
| Synchronization & Consistency | 1 | 0.3% |

### Real-Time Media & Immersive Networking — 295 papers

| Design aspect | Papers | Share of domain |
| --- | ---: | ---: |
| Latency & Deadline Optimization | 53 | 18.0% |
| Architecture & System Design | 39 | 13.2% |
| Application Adaptation & Cross-Layer Control | 35 | 11.9% |
| Transport & Congestion Control | 30 | 10.2% |
| QoS, QoE & SLO Management | 26 | 8.8% |
| Scheduling & Resource Allocation | 20 | 6.8% |
| Coding, Compression & Redundancy | 18 | 6.1% |
| Placement, Offloading & Partitioning | 10 | 3.4% |
| Measurement & Characterization | 9 | 3.1% |
| Caching & Content Placement | 8 | 2.7% |
| Security, Privacy & Trust | 7 | 2.4% |
| Control-Plane Design & Management | 6 | 2.0% |
| Cost, Economics & Provisioning | 4 | 1.4% |
| Reliability, Fault Tolerance & Recovery | 4 | 1.4% |
| Data/Traffic Prediction & Forecasting | 3 | 1.0% |
| Energy, Carbon & Sustainability | 3 | 1.0% |
| Telemetry & Monitoring | 3 | 1.0% |
| Admission Control & Network Slicing | 2 | 0.7% |
| Diagnosis & Root Cause Analysis | 2 | 0.7% |
| Distributed Coordination & Consensus | 2 | 0.7% |
| MAC, Spectrum & Radio Resource Management | 2 | 0.7% |
| Routing & Path Selection | 2 | 0.7% |
| Fairness, Isolation & Multi-Tenancy | 1 | 0.3% |
| Mobility & Handover | 1 | 0.3% |
| Programmability & Hardware Offload | 1 | 0.3% |
| Protocol Design & Interoperability | 1 | 0.3% |
| Queueing & Stability | 1 | 0.3% |
| Throughput, Capacity & Scalability | 1 | 0.3% |
| Topology, Fabric & Architecture | 1 | 0.3% |

### Distributed AI & LLM Systems — 290 papers

| Design aspect | Papers | Share of domain |
| --- | ---: | ---: |
| Security, Privacy & Trust | 67 | 23.1% |
| Scheduling & Resource Allocation | 54 | 18.6% |
| Coding, Compression & Redundancy | 30 | 10.3% |
| Model/State Placement & Movement | 22 | 7.6% |
| Placement, Offloading & Partitioning | 16 | 5.5% |
| Cost, Economics & Provisioning | 12 | 4.1% |
| Latency & Deadline Optimization | 12 | 4.1% |
| Energy, Carbon & Sustainability | 10 | 3.4% |
| Caching & Content Placement | 6 | 2.1% |
| Throughput, Capacity & Scalability | 6 | 2.1% |
| Architecture & System Design | 5 | 1.7% |
| MAC, Spectrum & Radio Resource Management | 4 | 1.4% |
| Measurement & Characterization | 4 | 1.4% |
| Routing & Path Selection | 4 | 1.4% |
| Topology, Fabric & Architecture | 4 | 1.4% |
| Traffic Engineering & Load Balancing | 4 | 1.4% |
| Application Adaptation & Cross-Layer Control | 3 | 1.0% |
| Mobility & Handover | 3 | 1.0% |
| Programmability & Hardware Offload | 3 | 1.0% |
| QoS, QoE & SLO Management | 3 | 1.0% |
| Synchronization & Consistency | 3 | 1.0% |
| Traffic Analysis & Classification | 3 | 1.0% |
| Data/Traffic Prediction & Forecasting | 2 | 0.7% |
| Distributed Coordination & Consensus | 2 | 0.7% |
| Admission Control & Network Slicing | 1 | 0.3% |
| Diagnosis & Root Cause Analysis | 1 | 0.3% |
| Fairness, Isolation & Multi-Tenancy | 1 | 0.3% |
| Freshness & Age of Information | 1 | 0.3% |
| Protocol Design & Interoperability | 1 | 0.3% |
| Reliability, Fault Tolerance & Recovery | 1 | 0.3% |
| Telemetry & Monitoring | 1 | 0.3% |
| Verification & Correctness | 1 | 0.3% |

### Satellite & Non-Terrestrial Networks — 275 papers

| Design aspect | Papers | Share of domain |
| --- | ---: | ---: |
| Routing & Path Selection | 61 | 22.2% |
| Scheduling & Resource Allocation | 31 | 11.3% |
| Mobility & Handover | 24 | 8.7% |
| Placement, Offloading & Partitioning | 22 | 8.0% |
| Latency & Deadline Optimization | 15 | 5.5% |
| Architecture & System Design | 13 | 4.7% |
| Control-Plane Design & Management | 12 | 4.4% |
| Transport & Congestion Control | 12 | 4.4% |
| Service Chaining & Virtualization | 11 | 4.0% |
| Measurement & Characterization | 10 | 3.6% |
| Security, Privacy & Trust | 10 | 3.6% |
| MAC, Spectrum & Radio Resource Management | 9 | 3.3% |
| Reliability, Fault Tolerance & Recovery | 8 | 2.9% |
| Coding, Compression & Redundancy | 6 | 2.2% |
| Cost, Economics & Provisioning | 5 | 1.8% |
| Application Adaptation & Cross-Layer Control | 3 | 1.1% |
| Caching & Content Placement | 3 | 1.1% |
| QoS, QoE & SLO Management | 3 | 1.1% |
| Queueing & Stability | 3 | 1.1% |
| Topology, Fabric & Architecture | 3 | 1.1% |
| Traffic Engineering & Load Balancing | 3 | 1.1% |
| Data/Traffic Prediction & Forecasting | 2 | 0.7% |
| Programmability & Hardware Offload | 2 | 0.7% |
| Protocol Design & Interoperability | 2 | 0.7% |
| Packet Processing & Data Structures | 1 | 0.4% |
| Throughput, Capacity & Scalability | 1 | 0.4% |

### Network Measurement & Operations — 267 papers

| Design aspect | Papers | Share of domain |
| --- | ---: | ---: |
| Telemetry & Monitoring | 132 | 49.4% |
| Measurement & Characterization | 21 | 7.9% |
| Security, Privacy & Trust | 19 | 7.1% |
| Diagnosis & Root Cause Analysis | 17 | 6.4% |
| Packet Processing & Data Structures | 16 | 6.0% |
| Routing & Path Selection | 11 | 4.1% |
| Programmability & Hardware Offload | 6 | 2.2% |
| Control-Plane Design & Management | 5 | 1.9% |
| Topology, Fabric & Architecture | 5 | 1.9% |
| Traffic Engineering & Load Balancing | 4 | 1.5% |
| Architecture & System Design | 3 | 1.1% |
| Coding, Compression & Redundancy | 3 | 1.1% |
| Data/Traffic Prediction & Forecasting | 3 | 1.1% |
| Cost, Economics & Provisioning | 2 | 0.7% |
| Energy, Carbon & Sustainability | 2 | 0.7% |
| Freshness & Age of Information | 2 | 0.7% |
| Latency & Deadline Optimization | 2 | 0.7% |
| Placement, Offloading & Partitioning | 2 | 0.7% |
| Protocol Design & Interoperability | 2 | 0.7% |
| Scheduling & Resource Allocation | 2 | 0.7% |
| Transport & Congestion Control | 2 | 0.7% |
| Localization & Positioning | 1 | 0.4% |
| QoS, QoE & SLO Management | 1 | 0.4% |
| Queueing & Stability | 1 | 0.4% |
| Throughput, Capacity & Scalability | 1 | 0.4% |
| Traffic Analysis & Classification | 1 | 0.4% |
| Verification & Correctness | 1 | 0.4% |

### Programmable Network Infrastructure — 256 papers

| Design aspect | Papers | Share of domain |
| --- | ---: | ---: |
| Programmability & Hardware Offload | 93 | 36.3% |
| Service Chaining & Virtualization | 60 | 23.4% |
| Packet Processing & Data Structures | 19 | 7.4% |
| Security, Privacy & Trust | 10 | 3.9% |
| Scheduling & Resource Allocation | 9 | 3.5% |
| Control-Plane Design & Management | 8 | 3.1% |
| Placement, Offloading & Partitioning | 8 | 3.1% |
| Measurement & Characterization | 6 | 2.3% |
| Reliability, Fault Tolerance & Recovery | 6 | 2.3% |
| Verification & Correctness | 5 | 2.0% |
| Routing & Path Selection | 4 | 1.6% |
| Throughput, Capacity & Scalability | 3 | 1.2% |
| Transport & Congestion Control | 3 | 1.2% |
| Architecture & System Design | 2 | 0.8% |
| Coding, Compression & Redundancy | 2 | 0.8% |
| Distributed Coordination & Consensus | 2 | 0.8% |
| Localization & Positioning | 2 | 0.8% |
| Queueing & Stability | 2 | 0.8% |
| Topology, Fabric & Architecture | 2 | 0.8% |
| Traffic Engineering & Load Balancing | 2 | 0.8% |
| Caching & Content Placement | 1 | 0.4% |
| Cost, Economics & Provisioning | 1 | 0.4% |
| Data/Traffic Prediction & Forecasting | 1 | 0.4% |
| Fairness, Isolation & Multi-Tenancy | 1 | 0.4% |
| Latency & Deadline Optimization | 1 | 0.4% |
| Protocol Design & Interoperability | 1 | 0.4% |
| QoS, QoE & SLO Management | 1 | 0.4% |
| Telemetry & Monitoring | 1 | 0.4% |

### Internet Routing, WAN & CDN — 184 papers

| Design aspect | Papers | Share of domain |
| --- | ---: | ---: |
| Routing & Path Selection | 30 | 16.3% |
| Measurement & Characterization | 29 | 15.8% |
| Security, Privacy & Trust | 29 | 15.8% |
| Architecture & System Design | 15 | 8.2% |
| Traffic Engineering & Load Balancing | 9 | 4.9% |
| Caching & Content Placement | 7 | 3.8% |
| Control-Plane Design & Management | 7 | 3.8% |
| Coding, Compression & Redundancy | 6 | 3.3% |
| Traffic Analysis & Classification | 6 | 3.3% |
| Transport & Congestion Control | 6 | 3.3% |
| Data/Traffic Prediction & Forecasting | 4 | 2.2% |
| Latency & Deadline Optimization | 4 | 2.2% |
| Localization & Positioning | 4 | 2.2% |
| Topology, Fabric & Architecture | 4 | 2.2% |
| Programmability & Hardware Offload | 3 | 1.6% |
| Reliability, Fault Tolerance & Recovery | 3 | 1.6% |
| Verification & Correctness | 3 | 1.6% |
| Application Adaptation & Cross-Layer Control | 2 | 1.1% |
| QoS, QoE & SLO Management | 2 | 1.1% |
| Scheduling & Resource Allocation | 2 | 1.1% |
| Synchronization & Consistency | 2 | 1.1% |
| Throughput, Capacity & Scalability | 2 | 1.1% |
| Cost, Economics & Provisioning | 1 | 0.5% |
| Diagnosis & Root Cause Analysis | 1 | 0.5% |
| Packet Processing & Data Structures | 1 | 0.5% |
| Queueing & Stability | 1 | 0.5% |
| Telemetry & Monitoring | 1 | 0.5% |

### P2P & Decentralized Networks — 120 papers

| Design aspect | Papers | Share of domain |
| --- | ---: | ---: |
| Security, Privacy & Trust | 36 | 30.0% |
| Distributed Coordination & Consensus | 35 | 29.2% |
| Throughput, Capacity & Scalability | 9 | 7.5% |
| Routing & Path Selection | 7 | 5.8% |
| Scheduling & Resource Allocation | 5 | 4.2% |
| Protocol Design & Interoperability | 4 | 3.3% |
| Reliability, Fault Tolerance & Recovery | 4 | 3.3% |
| Topology, Fabric & Architecture | 4 | 3.3% |
| Coding, Compression & Redundancy | 3 | 2.5% |
| Latency & Deadline Optimization | 2 | 1.7% |
| Measurement & Characterization | 2 | 1.7% |
| Mobility & Handover | 2 | 1.7% |
| Verification & Correctness | 2 | 1.7% |
| Architecture & System Design | 1 | 0.8% |
| Caching & Content Placement | 1 | 0.8% |
| Cost, Economics & Provisioning | 1 | 0.8% |
| Energy, Carbon & Sustainability | 1 | 0.8% |
| Placement, Offloading & Partitioning | 1 | 0.8% |

### Quantum Networks — 46 papers

| Design aspect | Papers | Share of domain |
| --- | ---: | ---: |
| Routing & Path Selection | 28 | 60.9% |
| Scheduling & Resource Allocation | 6 | 13.0% |
| Topology, Fabric & Architecture | 3 | 6.5% |
| Cost, Economics & Provisioning | 2 | 4.3% |
| Throughput, Capacity & Scalability | 2 | 4.3% |
| Control-Plane Design & Management | 1 | 2.2% |
| Fairness, Isolation & Multi-Tenancy | 1 | 2.2% |
| Measurement & Characterization | 1 | 2.2% |
| Protocol Design & Interoperability | 1 | 2.2% |
| Verification & Correctness | 1 | 2.2% |

### Harsh-Environment & Delay-Tolerant Networks — 28 papers

| Design aspect | Papers | Share of domain |
| --- | ---: | ---: |
| Routing & Path Selection | 8 | 28.6% |
| Scheduling & Resource Allocation | 6 | 21.4% |
| Security, Privacy & Trust | 4 | 14.3% |
| Control-Plane Design & Management | 3 | 10.7% |
| MAC, Spectrum & Radio Resource Management | 2 | 7.1% |
| Latency & Deadline Optimization | 1 | 3.6% |
| Localization & Positioning | 1 | 3.6% |
| Placement, Offloading & Partitioning | 1 | 3.6% |
| Telemetry & Monitoring | 1 | 3.6% |
| Topology, Fabric & Architecture | 1 | 3.6% |

## Interpretation

These counts are a **research-density signal**, not a recommendation to choose the largest cells automatically. Dense cells usually provide more prior work, baselines, datasets, and implementation references; smaller cells can still produce stronger projects when the research question is sharper or the trade-off is less explored.

The intended project unit is **domain × design aspect × optional technology/context tags**. Tags such as RDMA, O-RAN, LEO, V2X, TSN, WebRTC, KV cache, or P4 narrow a cell without becoming separate top-level project domains.

For maintainability, the source corpus and validation tooling are versioned under [`../../../tools/research/`](../../../tools/research/).
