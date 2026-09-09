# Collaboration

Course design follows the [MIT Sloan AI-resilient learning design flow](https://mitsloanedtech.mit.edu/ai/teach/4-steps-to-design-an-ai-resilient-learning-experience/): Learners → Learning Outcomes → Assessments → Activities.

The four design artifacts are maintained in [`design/`](design/README.md).

## Ownership and change policy

| Step | Artifact | Change policy |
| --- | --- | --- |
| 1. Learners | [`design/01_LEARNERS.md`](design/01_LEARNERS.md) | May be modified only by the course professor. |
| 2. Learning Outcomes | [`design/02_LEARNING_OUTCOMES.md`](design/02_LEARNING_OUTCOMES.md) | May be modified only by the course professor. |
| 3. Assessments | [`design/03_ASSESSMENTS.md`](design/03_ASSESSMENTS.md) | Changes should be made through a pull request and require at least one review from a different teaching-team subgroup. |
| 4. Activities | [`design/04_ACTIVITIES.md`](design/04_ACTIVITIES.md) | Changes should be made through a pull request and require at least one review from a different teaching-team subgroup. |

Steps 1 and 2 define the shared course-level specification. Teaching-team members may discuss and propose changes to them, but the course professor is responsible for making the final edits.

Steps 3 and 4 are the main collaboration surface. Different subgroups may work in parallel on assessments, assignments, lectures, labs, infrastructure, and related material, but changes should be integrated through pull requests rather than direct commits to `main`.

## Cross-team review

Every pull request affecting Steps 3 or 4 should have at least one reviewer who is not part of the subgroup that authored the change. The review should check that the proposed assessment or activity:

- remains aligned with the learning outcomes;
- is consistent with related assessments and activities owned by other subgroups;
- makes its intended AI use clear; and
- is feasible to operate, evaluate, and maintain.

Authors should resolve review comments before merging. When a change in Steps 3 or 4 exposes a problem with the Learners or Learning Outcomes specification, raise it with the course professor rather than editing Steps 1 or 2 directly.
