# Student Project Proposal — First TA Meeting

**Course:** Advanced Networks, Fall 2026  
**Team (3–4 students):** [Names]  
**Selected project area:** [An area announced by the course]  
**Working title:** [Title]  
**Date / version:** [Date]  
**Submission deadline / method:** [To be announced by the course/TA; complete before distribution]

> **Purpose:** Present an initial research direction that the team can discuss and revise with its TA. Focus on the **matrix, research question(s), and relation to research**. This is not an implementation contract or a final task breakdown. Keep the Markdown document concise and focused; use only the detail needed to justify your choices and support the first TA discussion. Replace the bracketed instructions.
>
> **Required preparation:** Before the first TA meeting, **every student must be sufficiently familiar with the selected project topic to explain and defend the team's research questions and its choice of domains, design aspects, and investigated matrix cells**. Be ready to discuss relevant networking mechanisms and prior work, alternative choices, assumptions, expected trade-offs, and how the questions might be investigated. Each student should be able to identify at least one relevant alternative and explain why the team's initial direction is worth testing. A list of buzzwords or AI-generated justifications without understanding is not sufficient. The TA may question any member about the whole proposal, with particular emphasis on their owned domain and design aspect.

## 1. Problem and motivation

[In 3–6 sentences: Which *networking* problem will you study, in what system/workload, and why do network design choices matter? Mention the intended outcome and any key constraints. The project must investigate a genuine networking design issue—not merely use a network to run an application.]

**Initial boundary:** [What will you deliberately not investigate? What existing systems, data, or infrastructure may you reuse?]

## 2. Project matrix

**Terminology:** A **domain** is a part of the networked system or application context you will analyze (e.g., client, transport, or edge serving). A **design aspect** is a concern or decision to investigate across domains (e.g., latency, reliability, or placement). A **technology/context tag** narrows the setting or identifies a possible mechanism (e.g., QUIC, P4, or mobility); it is not automatically a required tool. An **intersection** is the effect of one design aspect within one domain.

**Matrix–question relationship:** Start with a plausible design space, formulate worthwhile research questions, then revise the matrix and selected cells to match those questions and the feasible scope. **You do not need a research question or implementation for every cell.**

[Define **your own** domains (columns) and design aspects (rows) for the selected project area. Each student must own **one domain AND one design aspect**; for a three-person team, a 3×3 ownership matrix is a natural starting point, and for a four-person team, a 4×4 matrix. Adapt the dimensions with the TA where justified, without losing dual ownership. Add optional technology/context tags to narrow the question; technologies are possibilities, not mandatory implementation choices. Mark intersections **P** (primary investigation), **C** (comparison, baseline, or supporting characterization), or **—** (currently out of scope). Do **not** fill every cell.]

**Optional technology/context tags:** [e.g., QUIC, P4, edge offloading, wireless mobility—or none yet]

| Design aspect ↓ / Subdomain → | [Domain A] | [Domain B] | [Domain C] |
| --- | --- | --- | --- |
| [Aspect 1] | P | C | — |
| [Aspect 2] | — | P | C |
| [Aspect 3] | C | — | P |

**Why these domains, aspects, and cells?** [Justify the selected domains and design aspects, the primary intersections and their interactions, and significant exclusions. Explain why alternatives were not prioritized. You must understand and be able to defend these decisions. A narrow, well-supported scope is preferable to covering the matrix.]

**Initial individual responsibilities:** [Assign every student **one domain (column) and one design aspect (row)**. Ownership means understanding, integration, and defense across the matrix—not exclusive coding or independent subprojects. Each student should be able to justify *both* assigned choices and their links to the team's research questions. The team remains jointly responsible for the integrated project.]

| Member | Owned domain | Owned design aspect | Relevant matrix cells / connections |
| --- | --- | --- | --- |
| [Student 1] | [...] | [...] | [...] |
| [Student 2] | [...] | [...] | [...] |
| [Student 3] | [...] | [...] | [...] |
| [Student 4, if applicable] | [...] | [...] | [...] |

## 3. Initial research questions

[State **one primary question**, plus optional subquestions. Be prepared to explain **why these questions matter**, how they follow from the matrix and research context, which competing explanations or architectural alternatives exist, and what evidence could change your mind. Questions should allow a defensible result from comparison, measurement, or analysis—not simply ask whether a technology can be implemented.]

**RQ1:** [Under which conditions / with which trade-offs does design A affect outcome B?]  
**Optional RQ2:** [Which architectural alternative or interaction needs investigation?]

| Question | Matrix cell(s) | Initial baseline / comparison | What evidence could answer it? |
| --- | --- | --- | --- |
| RQ1 | [...] | [...] | [Workload, metrics, network conditions, observations] |
| RQ2 (optional) | [...] | [...] | [...] |

**Initial method and feasibility:** [What tools, testbed/emulator, traces/data, measurement or analytical approach could you use? What are the largest uncertainties? Briefly say how the investigation fits the three phases. This plan may change after TA feedback and early evidence.]

## 4. Connection to research

[Identify **relevant research and technical background** supporting the proposal. For each paper already explored, summarize the useful idea and say how it affects your question, choice of domains/aspects, comparison, or method. Include concrete title, venue/year, and DOI or direct link. A small number of well-chosen preliminary references is sufficient for the first meeting; do not invent findings. **Being able to defend the proposal is required even though all later phase papers are not yet due.**]

| Reference | What it contributes | How it may influence our investigation |
| --- | --- | --- |
| [Paper / link] | [...] | [...] |
| [Paper / link] | [...] | [...] |
| [Optional additional paper / link] | [...] | [...] |

**Literature requirement during the project:** In **each of the three phases**, **each student** must study at least one relevant project-specific research paper and explain its implications at the next TA meeting (at least three papers per student across the project). These are separate from the four shared class papers. **They are not all due with this initial proposal.**

## 5. For the first TA discussion

**Proposed first investigation:** [What should be learned or tested first to reduce uncertainty? Keep it at the level of intent or a candidate experiment.]

**Questions for the TA:** [Which scope, assumptions, comparison, or measurement choices need feedback?]

**To complete together after the meeting:**

| Decision | Agreed outcome |
| --- | --- |
| Approved/revised matrix and research question(s) | [Record after meeting] |
| Scope changes / exclusions | [Record after meeting] |
| Phase 1 tasks, individual owners, and checkable definitions of done | [Record after meeting] |
| Required evidence / next meeting preparation | [Record after meeting] |

## 6. How the first TA meeting is scored

The meeting assesses **preparation, research judgment, and the ability to defend choices**, not completed implementation. Every team member attends and can be questioned. Your team gets a common score for the shared proposal; each student also gets individual scores based on their own preparation and explanations.

**Meeting score (out of 100 per student):** 70 team points + 15 individual contribution/preparation points + 15 individual understanding/defense points. This follows the course project's configured **70% team / 15% contribution / 15% understanding** distinction. **The weight of Meeting 1 within the overall project/course grade is not specified here and must be announced separately**; these points explain how performance *at this meeting* is evaluated.

| Criterion | Points | Evidence the TA looks for |
| --- | ---: | --- |
| **Team — research question and networking motivation** | 25 | Clear and meaningful networking problem; questions are justified, answerable, and connected to trade-offs or alternatives |
| **Team — matrix and scope decisions** | 25 | Coherent domains/aspects; justified primary cells and exclusions; questions align with matrix; feasible project boundary |
| **Team — preliminary research grounding** | 10 | Credible, relevant references and accurate explanation of how their ideas influence the proposed direction |
| **Team — initial validation approach** | 10 | Plausible comparison/baseline, measurements or analysis, and awareness of feasibility risks |
| **Individual — contribution and preparation** | 15 | The student demonstrates substantive preparation for **both** owned responsibilities and contributes useful reasoning to the proposal and meeting |
| **Individual — understanding and defense** | 15 | The student can explain and defend the research question, chosen domain and aspect, relevant mechanisms, assumptions, alternatives, and connections to the integrated design |
| **Total per student** | **100** | 70 shared + up to 30 individual points |

**How points are awarded:** For each criterion the TA awards up to the stated maximum based on observable evidence. **Full credit** requires clear, technically credible, specific reasoning that holds up under questions; **partial credit** reflects sound but incomplete reasoning or important unexplained assumptions; **little or no credit** reflects missing work, unsupported assertions, or inability to explain the choices. The TA records brief evidence/feedback for each category. A polished document alone cannot earn the individual defense points, and code completion is **not** required at this meeting.

The three required project-specific paper analyses **per student** occur across the later phases: only relevant **preliminary** research grounding is assessed here. The **Phase 1 tasks and definitions of done are agreed with the TA during/after this meeting**, not expected to be final before it. Revisions prompted by well-reasoned TA feedback are normal and are not penalized simply for changing the initial proposal.

---

**Proposal check:** The networking problem is explicit; the matrix is selective; the research question maps to chosen cells and possible evidence; preliminary research informs decisions; every student owns **a domain and an aspect**; all team members have enough subject familiarity to **defend the research question, selected domains and aspects, assumptions, and alternatives**; and the proposal leaves room for TA feedback and evidence-driven revisions.

*Background (optional reading): Johnson & Johnson (2009), “An Educational Psychology Success Story: Social Interdependence Theory and Cooperative Learning,” Educational Researcher (individual accountability in cooperative work); Biggs (1996), “Enhancing Teaching through Constructive Alignment,” Higher Education (aligning assessment with intended learning). All instructions needed to prepare the proposal and understand Meeting 1 assessment appear above; no repository access is required.*
