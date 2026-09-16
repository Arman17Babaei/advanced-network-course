# 1. Learners

**Course/Module/Session:** Advanced Networks  
**Date:** Fall 2026

Start your design process by thinking about your students and their context.

- What program are they enrolled in?
- Are there any prerequisites for this learning experience?
- What prior knowledge and skills do they have?
- What are their career goals?
- What’s their previous experience with generative AI?
- What access to generative AI will they have during the learning experience?
- How might they use generative AI in their future professional roles?

## Decisions / Notes

### Student population and motivations

The course is intended for Computer Engineering students, primarily master's students, with a smaller number of advanced bachelor's students.

Students are likely to enter the course with different, overlapping motivations. Representative profiles include:

- bachelor's students preparing for careers in DevOps, cloud infrastructure, platform engineering, systems engineering, or other roles that work close to the network layer;
- bachelor's students interested in networking or distributed-systems research;
- master's students in the networked-systems area who take the course as part of their broader specialization and may later work in infrastructure, cloud, networking, or systems roles;
- master's students whose thesis or research directly involves networking or networked systems.

These are representative motivations rather than mutually exclusive tracks.

### Prior networking knowledge

All students are expected to have completed Sharif's undergraduate **Computer Networks (40443)** course or have equivalent preparation.

That course gives students introductory exposure to a broad range of topics, including socket programming, IP forwarding and addressing, TCP and UDP, congestion control, DNS/DHCP/ARP, switches and bridges, link-state and distance/path-vector routing, BGP, overlays and peer-to-peer systems, multimedia streaming, circuit switching, wireless and mobile networks, CDNs, middleware, and software-defined networking.

Because this breadth is covered within a single three-credit undergraduate course, the expected baseline is **broad exposure rather than deep mastery**. Students should generally recognize these concepts and retain basic mental models of their purpose and operation, but the course should not assume that they can recall protocol details, analyze subtle behavior, or confidently apply all of these mechanisms.

Knowledge is expected to be uneven. A student may remember TCP well but little about BGP, or understand basic routing while having only a vague recollection of wireless networking or SDN.

The advanced course may therefore revisit prerequisite material when necessary, but should do so to reach greater depth or support design reasoning rather than simply repeat the introductory syllabus.

### Programming and systems background

Students are expected to be comfortable programming before entering the course.

They should also have enough systems background to reason about software below the application level. They are expected to be familiar with operating-system and low-level systems concepts such as processes, concurrency, memory, system interfaces, and the interaction between applications and the operating system.

This does not imply hardware-level expertise, kernel-development experience, or substantial professional systems experience.

### Practical networking and design experience

The course should **not** assume substantial prior experience designing, operating, evaluating, or debugging realistic networks.

In particular, students are not assumed to already be proficient at:

- designing a network architecture from an open-ended set of requirements;
- configuring or operating substantial network infrastructure;
- diagnosing failures using packet traces, logs, metrics, or other operational evidence;
- conducting controlled network performance experiments;
- reasoning systematically about scalability and reliability;
- understanding behavior that emerges when multiple network mechanisms interact;
- making and defending architecture-level trade-offs.

Developing these abilities is part of the purpose of Advanced Networks. This direction is also aligned with the work of computer network architects described by the U.S. Bureau of Labor Statistics: network design, deployment, performance analysis, identification of bottlenecks and failure points, evaluation of technologies, documentation, and troubleshooting.

### Experience with generative AI

Students are assumed to have roughly three years of exposure to generative AI in coursework and exams and to be comfortable using ChatGPT-like systems as general-purpose assistants.

However, familiarity with generative AI should **not** be treated as evidence that students already know how to collaborate effectively with coding agents.

The course does not assume prior mastery of:

- writing precise specifications for an agent;
- decomposing large engineering problems into suitable tasks;
- supervising implementation work performed by an agent;
- reviewing generated code and designs critically;
- designing tests that expose incorrect agent output;
- distinguishing plausible explanations from validated conclusions;
- recovering when an agent pursues an incorrect approach;
- deciding what should be delegated to an agent and what requires direct human reasoning.

These are engineering skills the course intends to develop explicitly.

### AI resources available to students

Each team of roughly four students will be provided with access to at least one capable coding agent, currently expected to be Codex with a paid ChatGPT account shared by the team.

Students may additionally use their own AI systems, including Claude, Qwen, Z.ai, or other tools. There is no restriction to a particular vendor or model.

Assignments should therefore assume that every team has access to a capable coding agent while avoiding dependence on features unique to one model.

AI agents are expected to act as engineering companions throughout design and implementation. They may help students explore design alternatives, implement prototypes and experimental infrastructure, identify possible problems, propose diagnoses and fixes, review implementations, generate hypotheses, construct tests and experiments, and analyze evidence.

Students remain responsible for understanding, validating, and defending the systems and conclusions produced with AI assistance.

### Expected future use

Many students are expected to continue working close to the network layer in roles such as DevOps, cloud infrastructure, platform engineering, systems engineering, low-level systems design, network architecture, or research. In these roles, AI agents are likely to be used as collaborators for system design, implementation, debugging, experimentation, and operational analysis rather than merely as question-answering tools.

The course should therefore prepare students both to reason independently about networked systems and to supervise AI-assisted engineering work critically.

### Overall entry assumption

> Students enter Advanced Networks as competent programmers with systems knowledge and **broad but shallow and uneven prior exposure to computer networking**. They know enough networking vocabulary and basic mechanisms that the course does not need to begin from first principles, but they are not assumed to have the depth or practical experience required to design, evaluate, operate, or debug complex networked systems. They are experienced users of generative AI, but are not assumed to be skilled supervisors of coding agents.

The course should move students from familiarity with networking mechanisms toward the ability to use those mechanisms to reason about **network design, scalability, reliability, performance, experimentation, and failure**.

## References

- Sharif University of Technology, Computer Engineering Department, **Computer Networks (40443)** course description: https://docs.ce.sharif.edu/courses/40443
- U.S. Bureau of Labor Statistics, **Computer Network Architects**, Occupational Outlook Handbook: https://www.bls.gov/ooh/computer-and-information-technology/computer-network-architects.htm
- ACM/IEEE-CS/AAAI, **Computer Science Curricula 2023 (CS2023)**, Networking and Communication knowledge area: https://csed.acm.org/wp-content/uploads/2025/11/CS2023-Report.htm
