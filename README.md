# Advanced Network Course

Fall 2026 course-development repository for **Advanced Networks**.

The high-level course design is now considered **complete**. Current work is focused on turning that design into concrete teaching, assessment, project, and infrastructure materials.

## Status at a glance

| Area | Status | Available now | Main remaining work |
| --- | --- | --- | --- |
| **Course design** | **Complete** | [Learner profile](design/01_LEARNERS.md), [learning outcomes](design/02_LEARNING_OUTCOMES.md), [assessment design](design/03_ASSESSMENTS.md), and [activity design](design/04_ACTIVITIES.md) | Treat these as the course-level specification; revise only when implementation exposes a design issue |
| **Semester plan** | **Draft available** | [Fall 2026 timeline](TIMELINE.md) with the session sequence, assessments, project period, and TA/out-of-class windows | Finalize details as concrete materials are released |
| **Project design** | **Proof of concept available** | [Research-backed project-area pool](materials/assessments/PROJECT_IDEA_POOL.md) and one full draft project: [AR/VR & Immersive Scene Delivery](materials/assessments/projects/AR_VR_IMMERSIVE.md) | Turn selected areas from the pool into additional release-ready project briefs; finalize project rubrics, evaluation, starter material, and verification |
| **Assessment materials** | **Pending detail** | Structure and required contents are defined in [materials/assessments/](materials/assessments/) | Produce concrete quizzes, exams, project-discussion evaluation, final-project evaluation, presentation evaluation, rubrics, and reproducible grading/verification material |
| **Activity materials** | **Pending detail** | Structure and activity families are defined in [materials/activities/](materials/activities/) | Produce concrete foundation practice, paper-analysis guidance, project support, agent onboarding, experimental-systems activities, and reporting/presentation guidance |
| **AI-agent infrastructure** | **Architecture selected; validation pending** | [Agent infrastructure plan](tools/infrastructure/AGENT_INFRASTRUCTURE.md), currently centered on 9Router behind a reverse proxy with one shared allocation per team | Validate logging completeness for assessment/research, harden deployment, and operationalize team access |
| **Collaboration process** | **Defined** | [Collaboration and review policy](COLLABORATION.md) | Apply the review process as implementation material is added |

## Repository guide

### Course design

The four design artifacts define the intended course and are treated as complete at this stage:

1. [Learners](design/01_LEARNERS.md)
2. [Learning Outcomes](design/02_LEARNING_OUTCOMES.md)
3. [Assessments](design/03_ASSESSMENTS.md)
4. [Activities](design/04_ACTIVITIES.md)

The design follows the MIT Sloan Teaching & Learning Technologies **AI-Resilient Learning Experience** workflow. The design files describe **what** students should learn, what evidence should demonstrate that learning, and what experiences should support it.

### Timeline

[**TIMELINE.md**](TIMELINE.md) contains the Fall 2026 session-by-session plan, including the foundation block, paper analysis, project exploration and selection, quizzes, midterm, project work, presentations, final review, and final exam.

### Concrete course materials

[**materials/**](materials/) is where the course design is turned into material that can actually be released or run.

- [Assessment materials](materials/assessments/) — statements, methodology, rubrics, evaluation procedures, verification scripts/resources, and supporting material.
- [Activity materials](materials/activities/) — instructions, facilitation guidance, AI-use policy, expected learning process, and supporting resources.

Most of this layer is still to be produced.

### Project development

Project development currently has a working proof of concept:

- [**Project Idea Pool**](materials/assessments/PROJECT_IDEA_POOL.md) — a research-backed scan of active application-oriented networking areas, based on recent SIGCOMM, NSDI, and MobiCom work, with representative papers and an initial assessment of project suitability.
- [**AR/VR & Immersive Scene Delivery**](materials/assessments/projects/AR_VR_IMMERSIVE.md) — the first draft seven-week team project, including its design space, responsibility matrix, and research questions.

The next step is to use the idea pool to create the remaining project briefs at comparable depth and then add the common project evaluation and release material.

### AI-agent infrastructure

[**tools/infrastructure/AGENT_INFRASTRUCTURE.md**](tools/infrastructure/AGENT_INFRASTRUCTURE.md) records the requirements, alternatives considered, and current infrastructure decision.

The current direction is a **9Router deployment behind a hardened reverse proxy**, with one shared coding-agent allocation per student team. The key unresolved technical question is whether the logging is complete and reliable enough for both assessment of agentic engineering practice and research instrumentation.

### Collaboration

[**COLLABORATION.md**](COLLABORATION.md) defines ownership and review rules. In particular, the learner profile and learning outcomes remain under professor control, while implementation work around assessments and activities should be integrated through cross-team review.

## Core principles

- Students should learn to reason about network design decisions and be able to assess and design networks for scalability, reliability, and performance.

- AI should expand the scope and ambition of assignments rather than merely make traditional assignments easier or faster.

- Students are responsible for understanding, validating, and defending the systems and conclusions produced with AI assistance, regardless of who or what wrote the code.

- Effective collaboration with coding agents — specification, decomposition, supervision, verification, review, and recovery — is an explicit engineering skill and should be taught and assessed.

- Team project output and individual understanding should be evaluated separately.

- The syllabus, evaluation structure, and the **scope and expected complexity of every assignment** should be clear at the start of the semester. Detailed assignment materials including evaluation methodology, scripts, etc. may be finalized closer to release, but should be ready by the release date.

- Assignments should have clear deliverables and rubrics that make evaluation efficient, reproducible, and verifiable by the teaching team, with AI-assisted evaluation where useful.

- The course and its assignments should be maintainable without depending on substantial recurring effort from any single person, with each semester leaving the material substantially ready for the next semester.

- Course-provided AI agents should be shared by teams of roughly four students to control cost and provide a common working environment.

- AI interactions should remain private to the student team and teaching team, while being available to the teaching team for assessment of agentic engineering practice.

- The course should remain robust to rapid improvements in AI capability; assignment difficulty should come primarily from design judgment, experimentation, verification, trade-offs, and system behavior rather than from tasks that current models happen to find difficult.

- The course should be **research-auditable**: its design, student activity, AI-agent usage, assessment, and outcomes should be instrumented and documented well enough to rigorously study the effects of integrating AI agents into the course.
