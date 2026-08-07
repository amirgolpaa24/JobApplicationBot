# Written Interview Draft

This is draft material for the Canonical written interview. Revise it into your own wording before submitting, and do not include your name in the final PDF or filename.

## Education

### How did you rank in your high school, in your final year in maths and hard sciences? Which was your strongest?

In my final year of high school, I was strongest in mathematics and physics. I do not remember the exact official rank, but I was consistently among the stronger students in quantitative subjects. Math was probably my strongest area because I enjoyed problems where I had to reason carefully rather than memorize.

### How did you rank in your high school, in your final year in languages and the arts? Which was your strongest?

I was not as focused on languages and arts as I was on math and science, but I was still a solid student. My strongest area there was probably [English / literature / writing - choose truthfully]. I enjoyed writing more when it involved explaining an idea clearly rather than writing in a decorative way.

### Please state your high school graduation results or university entrance results, along with the system used, and how to understand those.

I completed high school in Iran under the Iranian education system. My university entrance result allowed me to study Computer Engineering at Sharif University of Technology, one of the most selective engineering universities in Iran. [Add exact Konkur rank, diploma GPA, or pre-university score if available.]

### What sort of high school student were you? Outside of class, what were your interests and hobbies?

I was curious, a bit intense about technical subjects, and more interested in understanding things deeply than just passing exams. Outside class, I liked computers, problem solving, and following technical and scientific topics. I think classmates would remember me as someone thoughtful, analytical, and sometimes quiet, but serious when I cared about something.

### Which university and degree did you choose? What other universities did you consider, and why did you select that one?

For my undergraduate degree I chose Computer Engineering at Sharif University of Technology because it was one of the strongest technical universities available to me, and I wanted to study in a demanding environment with strong peers. Later I chose the M.Sc. in Computer Science at the University of Calgary because it gave me the chance to work on research software, large geospatial data, and applied computer science problems.

### At university, did you do particularly well at any area of your degree?

Yes. I did especially well in programming, data systems, machine learning, and research-oriented software development. In my M.Sc., I finished with a 3.94/4.0 GPA and built Python/C++ systems for large Earth observation datasets, including work that became a first-author publication.

### Overall, what was your degree result and how did that reflect on your ability? In high school and university, what did you achieve that was exceptional?

My B.Sc. GPA was 3.69/4.0 at Sharif University of Technology, and my M.Sc. GPA was 3.94/4.0 at the University of Calgary. The achievement I am most proud of academically is my M.Sc. research: I designed and implemented a DGGS-based system for managing spatiotemporal satellite data, published it as first author, and improved performance and storage efficiency through real software implementation rather than only theory.

### What leadership roles did you take on during your education?

Most of my leadership has been technical and mentoring-based. As a teaching assistant at the University of Calgary, I supported students in database systems, big data applications, AWS-based workflows, and data-at-scale courses. In research, I also had to lead parts of my own technical direction: planning experiments, documenting decisions, communicating results, and turning an open-ended problem into a working system.

## Career Development

### How would you describe your level of experience as a professional software engineer?

I would describe myself as an early-career software engineer with strong Python/C++ and backend/research software experience. I have about two years of backend development experience and several years of graduate research software experience where I built data-processing systems, APIs, pipelines, and performance-sensitive tools.

### What are your strengths as a software engineer?

My strengths are careful problem decomposition, Python/C++ implementation, debugging, performance awareness, and writing software that is understandable after the first prototype. I am also good at learning unfamiliar domains by building small working pieces, testing assumptions, and documenting what I find.

### What is your proudest success as a software engineer?

My proudest success is my M.Sc. research system for spatiotemporal Earth observation data. I built C++/Python workflows for satellite data processing, DGGS encoding, storage, retrieval, and performance testing. One concrete result was improving 10-tensor processing from 233 seconds to 26 seconds using C++ multithreading, while also reducing storage in the scaled dataset.

### Outline the role of an engineering manager in shaping a high functioning team.

A good engineering manager creates clarity. They help the team understand priorities, reduce confusion, unblock people, and build a culture where engineers can discuss problems honestly. They should not need to be the best coder in every area, but they should understand enough technically to ask good questions, protect quality, and help people grow.

## Experience

### Describe your level of experience in Python, and how you have attained it.

I have used Python for backend APIs, data pipelines, machine learning, scientific computing, NLP preprocessing, and automation. In backend work, I used Django REST APIs with PostgreSQL. In research, I used Python with NumPy, Pandas, Rasterio, GDAL, PyTorch, and data APIs to process satellite and elevation datasets. More recently, I have used Python-adjacent automation and LLM workflows in my job search automation project.

### When did you start working on Linux? Describe your level of experience as a user and developer on Linux.

I started using Linux seriously during university and research work. I am comfortable as a Linux user and developer for command-line workflows, Python environments, Git, Docker, scripting, data processing, debugging, and running research/software pipelines. I would not claim to be a Linux kernel or low-level systems expert, but I am comfortable working in Linux-based development environments and I want to deepen that further.

### How do you address software performance, systematically, in your products and in your software engineering practices?

I usually start by measuring before optimizing. I try to identify the actual bottleneck, separate I/O issues from algorithmic issues, and build small benchmarks around the expensive part. In my research, this mattered a lot because satellite data processing could become slow quickly. I improved one workflow with C++ multithreading after measuring the processing time and understanding where parallelism would help.

### How do you prefer to drive documentation for your products?

I prefer documentation that is close to the work: README files, setup notes, examples, comments where the logic is not obvious, and short explanations of design decisions. I do not like documentation that only looks formal but does not help the next person run or modify the system. For research work, I also documented methods carefully because results had to be reproducible and explainable.

### Describe your experience with QEMU/KVM, LXC/LXD and cloud computing.

My direct experience with QEMU/KVM and LXC/LXD is limited, so I would be ramping up there. I have used Docker, Linux environments, AWS-based teaching/course workflows, and cloud-adjacent data pipelines. I understand the purpose of virtualization and containerization, and I am interested in learning LXD and cloud-init more deeply because they connect directly to reproducible Linux provisioning.

### How would you describe your experience in Linux system fundamentals such as networking, storage, and security?

I have practical working knowledge rather than deep systems-specialist experience. I have worked with Linux filesystems, shell tools, environments, permissions, package setup, networking basics for backend/API development, Docker workflows, and database-backed services. Storage became important in my research because I worked on efficient representation and retrieval of large satellite datasets. I would like to grow deeper in Linux networking and security.

### How do you think about software quality?

I think software quality is partly correctness, partly maintainability, and partly honesty. Code should do what it claims, fail in understandable ways, be testable, and be readable enough that another engineer can change it safely. In research software, I learned that a result can look impressive but still be misleading if the data split, evaluation, or assumptions are wrong.

### Describe a case where it was very difficult to test code you were writing, but you found a reliable way to do it.

In my DEM super-resolution research, testing was difficult because random train/test splits could give overly optimistic results. The model could perform well on nearby terrain patterns without really generalizing. I addressed this by thinking more carefully about validation strategy and using terrain-aware metrics such as RMSE, slope, TRI, TPI, and wavelet-based errors. That made the evaluation less convenient but more trustworthy.

### What would you like to achieve in career development and skills development?

I want to grow from an early-career engineer into someone who can own reliable production systems. Technically, I want to deepen my Linux systems knowledge, cloud infrastructure, testing discipline, and open-source development practices. I also want to keep building strength in Python, performance-aware engineering, and applied AI/software systems.

## Context

### How are you involved in open source software?

Most of my involvement has been as a user and builder on top of open-source tools rather than as a major upstream contributor. I have used Python, Linux, Docker, PyTorch, GDAL, Rasterio, PostgreSQL, and many other open-source tools in research and backend work. I want to move from being mostly a user of open source to contributing more directly.

### Describe any significant contributions to open source, with links where possible.

I do not want to overstate this: I have not yet made major upstream open-source contributions comparable to a long-term maintainer. My public-facing technical work includes my first-author research publication and my own projects. [Add GitHub links if useful.] One reason Canonical interests me is that it would put me closer to real open-source engineering culture.

### What do you think are the key ingredients of a successful open source project?

A successful open-source project needs technical quality, clear documentation, respectful maintainers, predictable review processes, and real users. It also needs a healthy balance between accepting contributions and protecting the project's direction. Good examples and good first issues matter because they turn interested users into contributors.

### Why do you most want to work for Canonical?

I am interested in Canonical because it works on infrastructure that developers and companies depend on every day, especially Ubuntu, cloud images, cloud-init, LXD, and cloud tooling. I like work where correctness and reliability matter more than hype. The cloud-init side is especially interesting to me because it is a practical layer between Linux, cloud platforms, and real deployment workflows.

### Which other companies are building the sort of products you would like to work on?

Companies I would put in a similar technical area include Red Hat/IBM, SUSE, AWS, Google Cloud, Microsoft Azure, HashiCorp, and VMware/Broadcom. They all work on some combination of Linux, cloud infrastructure, automation, virtualization, or developer operations.

### What do you think Canonical needs to improve in its engineering and products?

From an outside perspective, I think Canonical could improve the onboarding path for new contributors across its infrastructure projects. The ecosystem is powerful, but for someone new, it can be hard to know where to start: cloud-init, MAAS, LXD, snaps, Ubuntu Pro, MicroCloud, and so on. Clearer learning paths, architecture maps, and beginner-to-intermediate contribution guides could help more developers become serious contributors.

### What do you think is the biggest opportunity for Canonical in this arena?

The biggest opportunity is to make Ubuntu the most reliable and consistent operating system layer across public cloud, private cloud, and edge environments. Cloud-init is already central to repeatable cloud instance initialization, and Canonical can connect that with Ubuntu Pro, LXD, MAAS, and MicroCloud to give teams a secure and reproducible way to run Linux everywhere.

### Who do you think are key competitors to Canonical? How do you think Canonical should plan to win that race?

Key competitors include Red Hat/IBM, SUSE, the major public cloud providers' own Linux images and tooling, and infrastructure automation platforms. Canonical can win by making Ubuntu the easiest serious choice: secure by default, excellent documentation, consistent cloud behavior, strong performance, fast issue response, and a welcoming open-source development process.

