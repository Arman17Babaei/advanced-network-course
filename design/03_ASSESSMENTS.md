# 3. Assessments

**Course/Module/Session:** Advanced Networks  
**Date:** Fall 2026

This section contains only the evidence used to decide whether students have achieved the learning outcomes. Practice work, paper study, ordinary project work, and other experiences intended primarily to support learning belong in [4. Activities](04_ACTIVITIES.md), even when they prepare students directly for an assessment.

- **Aligned Learning Outcome(s):** Copy/paste a learning outcome from [2. Learning Outcomes](02_LEARNING_OUTCOMES.md). The assessment will measure whether students have achieved that specific learning outcome.
- **Assessment Task(s):** Complete the prompt, *“Students will show that they’ve achieved the learning outcome(s) by...”*
- **AI Use:** Decide whether to require, allow, or ban AI use for the assessment.

## Assessment overview

| Assessment | What it establishes | Bloom level(s) | AI |
| --- | --- | --- | --- |
| **Quizzes** | Individual understanding of networking foundations and individual analysis of project-related research papers. | Understand, Analyze | **Ban** |
| **Midterm exam** | Individual understanding and reasoning over material covered in the first part of the course. | Understand, possibly Analyze | **Ban** |
| **Bi-weekly project discussions** | Ongoing evidence of architectural reasoning, discoveries, experimental reasoning, changing design decisions, integration, and sensible next steps. | Create | **AI is integral to project work; discussion is live** |
| **Completed team project** | Ability to create and experimentally evaluate a substantial networked system, and ability to apply AI-assisted engineering to make that scope feasible. | Create, Apply | **Require** |
| **75-minute project presentation** | Ability to report and present substantial technical work clearly; also creates shared technology and architecture case studies for the class. | Apply | **Allow in preparation; presentation and discussion are live** |
| **Final exam** | Individual recall of modern concepts and technologies; understanding of foundations; architecture analysis of presented systems; and transfer of architecture principles and practices to new situations. | Remember, Understand, Analyze, Create | **Ban** |

## Assessment Plan

| Aligned Learning Outcome(s) | Assessment Task(s) | AI Use |
| --- | --- | --- |
| **Modern networking concepts and technologies — Remember.** Recognize and recall major contemporary networking concepts, technologies, and system patterns covered in the course, including the problems and operating contexts with which they are commonly associated. | Students will show that they have achieved this outcome by **individually recalling, recognizing, and contextualizing important modern concepts and technologies in the final exam**, including material introduced through lectures and other teams’ project presentations. | **Ban** |
| **Networking foundations — Understand.** Explain the principles and mechanisms underlying the common networking foundation of the course. | Students will show that they have achieved this outcome through **individual quizzes, the midterm, and the final exam**, explaining mechanisms, interpreting system behavior, and reasoning from networking principles. | **Ban** |
| **Networking research — Analyze.** Analyze networking research by decomposing a work into its problem, assumptions, architecture, mechanisms, evaluation, and conclusions and relating them to one another and to alternative designs. | Students will show that they have achieved this outcome by **individually analyzing project-related research papers in no-AI quizzes or in-class assessments** after studying and exploring those papers as learning activities. Research-derived architectural ideas may also appear in later project discussions and exams. | **Ban for assessed individual analysis** |
| **Network architecture and design — Create.** Design a coherent networked system for a given workload and set of constraints, integrating relevant concerns such as performance, scalability, reliability, sustainability/resource efficiency, and deployability across the domains of that system. | Students will show that they have achieved this outcome through **the completed team project and bi-weekly project discussions**, explaining evolving architectural decisions, alternatives, discoveries, trade-offs, and revisions. The **final exam additionally provides individual evidence** by asking students to analyze architectures encountered during the semester and apply architecture principles and practices to new scenarios. | **Require for project; Ban for final exam** |
| **Experimental systems engineering — Create.** Design and carry out experiments that characterize a networked system, test assumptions, compare alternatives, expose behavior under scale and failure, and generate evidence that supports or challenges design decisions. | Students will show that they have achieved this outcome through **the project’s experimental work and bi-weekly discussions**, presenting experimental questions, methodology, observations, unexpected behavior, interpretation, and resulting changes to the system or its design. The completed project provides the final integrated evidence. | **Require** |
| **AI-assisted engineering — Apply.** Use course-provided AI coding agents effectively for specification, implementation, experimentation, debugging, verification, and review while remaining responsible for understanding and validating the resulting system and conclusions. | Students will show that they have achieved this outcome by **successfully using the course-provided AI environment throughout the substantial team project** to implement, experiment with, debug, and iterate on a system whose intended scope depends on AI assistance. Evidence also naturally appears during bi-weekly project discussions. | **Require** |
| **Technical reporting and presentation — Apply.** Apply effective technical reporting and presentation practices to communicate a networked system’s problem, context, architecture, design decisions, experimental methodology, results, limitations, and conclusions to a technically knowledgeable audience. | Students will show that they have achieved this outcome through a **75-minute final project presentation and discussion** that communicates the project’s complete engineering story. The presentation must provide enough technical depth that other students can subsequently reason about the technologies and architecture in the final exam. | **Allow in preparation; live presentation and discussion** |

## Team and individual evidence

The course intentionally uses different assessments for team capability and individual learning.

- The **completed project, bi-weekly project discussions, and project presentation** provide substantial evidence about team-level capability.
- **Quizzes, the midterm, and the final exam** provide authenticated individual evidence.
- Directed questions during bi-weekly project discussions and the final presentation can provide additional individual evidence, especially around assigned responsibilities.
- Shared agent logs, code authorship, or commit counts should **not** be treated as sufficient evidence of individual competence. The agent environment is shared and the project is intentionally collaborative.

## Project responsibility matrix — assessment design note

Each team owns one substantial project **end-to-end**. The project should expose several project-specific **domains** (for example application/QoE, transport, network, host/NIC, control plane, measurement/deployment) and several project-specific **design aspects** (for example performance, scalability, reliability, sustainability/resource efficiency, deployability, or function placement).

The project is organized as a **domain × design-aspect matrix**:

|  | Domain 1 | Domain 2 | Domain 3 | Domain 4 |
| --- | --- | --- | --- | --- |
| **Design aspect 1** | intersection | intersection | intersection | intersection |
| **Design aspect 2** | intersection | intersection | intersection | intersection |
| **Design aspect 3** | intersection | intersection | intersection | intersection |
| **Design aspect 4** | intersection | intersection | intersection | intersection |

For a four-person team, each student owns **one domain (one column)** and **one design aspect (one row)**. Ownership is accountability for understanding, integration, and defense; it is not an exclusive code boundary.

- Through **domain ownership**, the student must collaborate with the owners of the different design aspects and understand how those concerns affect that domain.
- Through **design-aspect ownership**, the student must collaborate with the owners of the different domains and understand that design concern across the end-to-end system.
- The **team remains jointly responsible for the integrated system** and for decisions at the intersections of the matrix.
- The concrete rows and columns should be chosen to fit the project; their importance is expected to vary between projects rather than being artificially uniform.

This structure should be reflected in later rubrics so that team-system quality and identifiable individual understanding can be assessed separately.

## Bi-weekly project discussions

The project should be assessed as an evolving engineering process rather than only as a terminal artifact. Approximately every two weeks, each team should discuss its project with the teaching team.

The discussion should surface:

- what the team has learned since the previous meeting;
- important discoveries or unexpected system behavior;
- architectural or implementation decisions that changed and why;
- experimental evidence that supported or challenged assumptions;
- integration issues across project domains and design aspects;
- the questions and tasks the team considers most important next.

Assessment should emphasize **reasoning, evidence, adaptation, and choice of next steps**, not simply whether every previously planned task was completed. Discovering that an earlier plan was wrong can be strong evidence of learning when the team can explain the evidence and resulting change.

## Project presentations as shared course material

The **75-minute final project presentations** serve three roles:

1. **Assessment of technical reporting and presentation — Apply** for the presenting team.
2. **Exposure to contemporary networking concepts and technologies** for the rest of the class.
3. **Shared architecture case studies** that can later be analyzed, compared, modified, or reused in the individual final exam.

The presenting team should communicate enough of the complete engineering story for other students to reason about the system: problem and context, important technologies, assumptions, alternatives, architecture, implementation choices, experiments, discoveries, design changes, limitations, and conclusions.

Students are not expected to memorize arbitrary implementation details from other teams. They are expected to retain the important concepts and technologies and to understand enough of the architectures, assumptions, trade-offs, and experimental discoveries to reason about them later.

## Final exam scope

The individual no-AI final exam may assess four kinds of evidence:

- **Remember:** recognize contemporary concepts and technologies and recall the problem spaces and contexts in which they are commonly used.
- **Understand:** explain underlying networking mechanisms and principles.
- **Analyze:** decompose, compare, and reason about architectures encountered in lectures, papers, class discussion, and project presentations, including how their assumptions and trade-offs interact.
- **Create:** use architecture principles and practices encountered throughout the semester to design or modify a system for a new workload, constraint set, or operating context.

The projects and presentations therefore become sources of transferable architecture knowledge, not material to memorize verbatim.

## Professional dispositions — retain for rubric design

- **Meticulous:** Students are particular about the specifics of understanding and creating networking protocols and systems.
- **Collaborative:** Students work together to develop interacting components and respond to failures and threats.
- **Proactive:** Students anticipate failures, threats, and mitigations rather than operating only reactively.
- **Professional:** Students account for community expectations, operational responsibilities, and applicable regulatory constraints in a networked environment.
- **Responsive:** Students respond appropriately to changes in requirements, configurations, and user needs.
- **Adaptive:** Students reconfigure and revise systems under varying modes of operation.

These dispositions should only become graded criteria when an assessment produces credible evidence for them; they should not be scored merely because they appear desirable.

## Design references

- Biggs, J. (1996), “Enhancing teaching through constructive alignment,” *Higher Education*, 32, 347–364. Assessments should produce evidence at the cognitive level stated in the learning outcomes.
- Johnson, D. W. & Johnson, R. T. (2009), “An Educational Psychology Success Story: Social Interdependence Theory and Cooperative Learning,” *Educational Researcher*. The responsibility matrix intentionally combines **positive interdependence** with **individual accountability**.
