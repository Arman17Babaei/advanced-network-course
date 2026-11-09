# Student Project Proposal — First TA Meeting

**Course:** Advanced Networks, Fall 2026  
**Team (3–4 students):** [Names]  
**Selected project area:** [An area announced by the course]  
**Working title:** [Title]  
**Date / version:** [Date]  
**Proposal submission:** [Use the course-announced submission method and deadline.]

**Team announcement and TA meeting arrangement:** **By the end of this week**, announce your team (all 3–4 members) through the course-announced channel. **After submitting this proposal**, contact your assigned TA and agree on a time for the first project meeting, also **by the end of this week**. Every team member must attend the meeting. The assigned TA and the meeting time are coordinated separately; do not assume a time is automatically reserved by submitting the proposal.

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

## 4. Research directions and potential references

[Identify relevant research topics and, where available, **candidate papers or technical references** the team could investigate during the project. For each candidate reference, give its title and direct link, and explain the question or design decision it might inform. **Detailed reading or analysis of any project paper is not required before Meeting 1 and is not separately scored at that meeting.** If you have already read relevant work, you may briefly explain what you learned; do not claim unverified results. Your ability to defend the chosen project topic, questions, and design choices is still required.]

| Candidate paper or technical reference (if identified) | Question or decision it may help us investigate |
| --- | --- |
| [Reference / link] | [...] |
| [Optional reference / link] | [...] |

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

The meeting assesses **preparation, research judgment, and the ability to defend choices**, not completed implementation. Every team member attends and may be questioned about the complete proposal, particularly the domain **and** design aspect they own.

**Meeting score (out of 100 per student): 30 team points + 70 individual points.** All members receive the same score for the shared proposal; each student's remaining points depend on their *own* understanding and explanations. The meeting's weight within the overall project/course grade must be announced separately; the 30/70 split below governs this meeting only.

| Criterion | Points | Evidence the TA looks for |
| --- | ---: | --- |
| **Team — networking problem and research question** | 10 | Clear motivation; meaningful, answerable question linked to networking design choices and trade-offs |
| **Team — matrix, priorities, and scope** | 10 | Coherent domains and aspects, justified investigated cells/exclusions, feasible boundaries, and alignment with the question |
| **Team — evaluation approach and feasibility** | 10 | Plausible baseline or comparison, relevant metrics/analysis, and awareness of constraints and risks; no completed paper reading required |
| **Individual — grasp of owned domain and aspect** | 25 | Student explains **both** responsibilities, relevant mechanisms, and how they interact with each other and the end-to-end project |
| **Individual — defense of research questions and choices** | 30 | Student justifies why the questions and selected cells matter, discusses assumptions and credible alternatives, and answers technical follow-ups |
| **Individual — experimental reasoning and limitations** | 15 | Student explains what could be measured or compared, relevant uncertainties and limitations, and what results would support or challenge the proposed question |
| **Total per student** | **100** | **30 shared + up to 70 individually earned points** |

**How points are awarded:** For each criterion, the TA awards up to its maximum based on observed evidence. **Full credit** requires specific, technically sound reasoning that survives follow-up questions; **partial credit** reflects sound but incomplete reasoning or unexplained assumptions; **little or no credit** reflects unsupported claims, missing preparation, or an inability to explain key decisions. The TA records brief evidence and feedback for each criterion **for each student** where applicable. Other students' explanations cannot substitute for an individual's defense. A polished document alone cannot earn the individual points, and completed code is **not** required.

**No points at Meeting 1 are allocated to completing, summarizing, or presenting research papers.** Each student must instead study at least one project-specific research paper in **each of the three subsequent project phases** (three in total), when the paper analysis is assessed. Students can identify prospective references now without having read them in detail. **Phase 1 tasks and definitions of done are agreed with the TA during/after this meeting**, not finalized beforehand. Evidence-based changes after TA feedback are normal and are not penalized simply because the proposal evolves.

---

**Proposal check:** The networking problem is explicit; the matrix is selective; the research question maps to chosen cells and possible evidence; research directions or potential references are identified; every student owns **a domain and an aspect**; all team members have enough subject familiarity to **defend the research question, selected domains and aspects, assumptions, and alternatives**; and the proposal leaves room for TA feedback and evidence-driven revisions.

