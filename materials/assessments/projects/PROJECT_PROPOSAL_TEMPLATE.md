# Student Project Proposal — Template

**Course:** Advanced Networks, Fall 2026  
**Team:** [Names; 3–4 students]  
**Project area:** [One of the announced areas]  
**Working title:** [Specific and descriptive]  
**Version/date:** [Date]

> **Purpose:** Agree with the TA on *what the team will investigate, why it matters, and how it could be tested*. This is a starting hypothesis, not a fixed implementation contract. Keep the proposal concise (approximately 2–3 pages, excluding references). Replace all bracketed instructions.

## 1. Problem and scope

**Problem.** [In one paragraph, describe the networked application/system, the workload and operating conditions, and the performance, scalability, or reliability problem.]

**Design decision.** [What choices might the team compare? Do not assume a particular technology is required. Explain which network/system layers could matter.]

**Boundaries.** [State what is deliberately excluded, what existing software or datasets you will reuse, and the target scale. Show that the investigation is feasible during the project period.]

## 2. Domain × design-aspect matrix

[Choose project-specific domains (columns) and cross-cutting design aspects (rows). For a four-person team, each student owns one domain and one aspect; adapt the structure with the TA for a three-person team. Mark each intersection **P** (primary investigation), **S** (supporting/characterization), or **—** (out of scope). An empty cell is acceptable; the matrix is not a feature checklist.]

| Design aspect ↓ / Domain → | [Domain A] | [Domain B] | [Domain C] | [Domain D, if applicable] |
| --- | --- | --- | --- | --- |
| [Aspect 1] | P | S | — | — |
| [Aspect 2] | S | P | S | — |
| [Aspect 3] | — | S | P | S |
| [Aspect 4, if applicable] | — | — | S | P |

**Priorities and coupling.** [In 3–5 sentences, justify the primary cells and explain which interactions between domains/aspects are likely to drive architectural trade-offs. Revise the number of rows/columns to fit the team and problem.]

**Ownership.**

| Student | Domain responsibility | Design-aspect responsibility |
| --- | --- | --- |
| [Student 1] | [Domain] | [Aspect] |
| [Student 2] | [Domain] | [Aspect] |
| [Student 3] | [Domain] | [Aspect] |
| [Student 4, if applicable] | [Domain] | [Aspect] |

[Ownership means integration, understanding, and defense, not exclusive coding responsibility. All members remain responsible for the integrated system.]

## 3. Research questions and evidence

[Choose 1–3 focused, falsifiable or empirically answerable questions. Each must be tied to the matrix and an observable comparison; avoid questions that simply ask whether you can implement a tool.]

| ID | Research question / hypothesis | Matrix cells | Baseline vs. alternative(s) | Evidence / metrics |
| --- | --- | --- | --- | --- |
| RQ1 | [Under which conditions does X constrain Y?] | [A×1, B×1] | [Baseline and variations] | [Metric, workload, experimental comparison] |
| RQ2 | [When does design choice A outperform B, and at what cost?] | [B×2, C×2] | [A vs. B] | [Benefit, overhead, failure cases] |
| RQ3 (optional) | [Where does the design stop working?] | [Relevant cells] | [Stress/failure scenarios] | [Limits, resource use, variability] |

**Validation approach.** [Briefly identify the experimental platform or emulator, controllable network conditions, workloads/traces, repetitions, and how you will check measurements. Include at least one stress, scale, or failure condition relevant to your questions. Distinguish observations from assumptions.]

## 4. Related research

[Discuss **at least three** relevant research papers as a team; each student should take responsibility for studying and explaining the project-related papers assigned to them under the course requirements. Cite direct links/DOIs. Papers should meaningfully inform the problem, architecture, methodology, or baseline—not merely share keywords.]

| Paper (title, venue/year, DOI/link) | Relevant finding, mechanism, or method | How it informs *our* question/design | Difference or limitation for our setting |
| --- | --- | --- | --- |
| [Paper 1] | [...] | [...] | [...] |
| [Paper 2] | [...] | [...] | [...] |
| [Paper 3] | [...] | [...] | [...] |

**Positioning.** [In 2–4 sentences, explain what your project will reproduce, adapt, compare, or investigate beyond the selected papers. A novel algorithm is not required; a well-defended architectural comparison is sufficient.]

## 5. Initial execution and review plan

**First milestone.** [A runnable baseline and an end-to-end measurement path; list the minimum concrete deliverables needed to begin answering RQ1.]

**Initial tasks.** [Specify 3–6 near-term tasks, owners, and checkable outputs. Detailed phase tasks will be negotiated with the TA at subsequent meetings; do not lock the entire project schedule now.]

**Biggest uncertainties.** [Top 2–3 technical or experimental risks, how you will test them early, and a fallback scope if they fail.]

**AI-agent use and verification.** [What substantial work will the shared coding agent support? How will the team inspect code, reproduce results, review agent decisions, and retain evidence for discussions? A shared agent log alone does not establish individual understanding.]

---

### Proposal review checklist

- [ ] The problem is a network/system design question, not just a build specification.
- [ ] Matrix rows/columns reflect the actual project; primary intersections have a reason to exist.
- [ ] Research questions map to matrix cells, comparisons, and measurable evidence.
- [ ] At least three concrete papers inform decisions or experiments.
- [ ] The scope fits the team and time available, with a baseline-first plan and fallbacks.
- [ ] Each student has a domain and design-aspect responsibility; joint integration is explicit.

**TA discussion outcome:** [Approved / revise / scope changed; record key decisions after the meeting.]

*Design basis: [Course assessment design](../../../design/03_ASSESSMENTS.md), especially the responsibility matrix, individual/team evidence, and project discussions; [project candidate example](AR_VR_IMMERSIVE.md). The matrix combines cooperative interdependence and individual accountability, consistent with Johnson & Johnson (2009), “An Educational Psychology Success Story: Social Interdependence Theory and Cooperative Learning,” Educational Researcher. Research questions linked to experimental evidence follow established systems-evaluation practice.*
