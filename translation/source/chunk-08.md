<!-- Source chunk 08 | PDF pages 57-59 | Chapter 2 end: Balancing Architecture and Hands-On Coding, There's More to Architectural Thinking | words: 952 -->

Balancing Architecture and Hands-On Coding
One of the difficult tasks an architect faces is how to balance hands-on coding with
software architecture. We firmly believe that every architect should code and should
maintain a certain level of technical depth (see “Technical Breadth” on page 20).
While this may seem like an easy task, it is sometimes rather difficult to accomplish.
Our first tip for anyone striving to balance hands-on coding with being a software
architect is avoiding the Bottleneck Trap. The Bottleneck Trap antipattern occurs
when an architect takes ownership of code within the critical path of a system
(usually the underlying framework code or some of the more complicated parts)
and becomes a bottleneck to the team. This happens because the architect is not a
full-time developer and therefore must balance development work (like writing and
testing source code) with the architect role (drawing diagrams, attending meetings,
and well, attending more meetings).
One way to avoid the Bottleneck Trap is for the architect to delegate the critical
parts of the system to others on the development team and then focus on coding
a minor piece of business functionality (such as a service or UI screen) one to
three iterations down the road. This has three positive effects. First, the architect
gains hands-on experience by writing production code while avoiding becoming a
bottleneck on the team. Second, the critical path and framework code are distributed
to the development team (where they belong), giving the team ownership and a better
understanding of the harder parts of the system. Third, and perhaps most important,
the architect is writing the same business-related source code as the development
team. This helps them better identify with the development team’s pain points around
processes, procedures, and the development environment (and hopefully work to
improve those things).
Suppose, however, that the architect can’t develop code with the development team.
How can they still remain hands-on and maintain some level of technical depth?
The following are some tips and techniques for architects who want to continue
deepening their technical abilities:
Frequent proofs-of-concept
Doing frequent proofs-of-concept (POCs) requires the architect to write source
code; it also helps validate an architecture decision by taking the implementation
details into account. For example, suppose an architect gets stuck trying to
choose between two caching solutions. One effective way to help make this
decision is to develop a working example in each caching product and compare
the results. This allows the architect to see firsthand the implementation details
and the amount of effort required to develop the full solution. It also allows them
to better compare architectural characteristics between the different caching
solutions, such as scalability, performance, and overall fault tolerance.
Whenever possible, the architect should write the best production-quality code
they can. We recommend this practice for two reasons. First, quite often, “throwaway” proof-of-concept code goes into the source code repository and becomes
the reference architecture or guiding example for others to follow. The last thing
any architect would want is for their sloppy throwaway code to be treated as
representing their typical quality of work. Second, writing production-quality
proof-of-concept code means getting practice at writing quality, well-structured
code, rather than continually developing bad coding practices by creating quick,
sloppy POCs.
Tackle technical debt
Another way architects can remain hands-on is to tackle some technical debt,
freeing the development team to work on the critical functional user stories. Tech
debt is usually low priority, so if the architect doesn’t get the chance to complete
a technical debt task within a given iteration, it’s not the end of the world and
generally won’t impact the success of the iteration.
Fix bugs
Similarly, working on bug fixes within an iteration is another way of maintaining
hands-on coding skills while helping the development team. While certainly not
glamorous, this technique allows the architect to identify issues and weaknesses
within the code base and possibly the architecture.
Automate
Leveraging automation by creating simple command-line tools and analyzers
to help the development team with their day-to-day tasks is another great way
to maintain hands-on coding skills while making the development team more
effective. Look for repetitive tasks the development team performs and automate
them. They’ll be grateful for the automation. Some examples are automated
source validators to help check for specific coding standards not found in other
lint tests, automated checklists, and repetitive manual code-refactoring tasks.
Automation in the form of architectural analysis and fitness functions to ensure
the vitality and compliance of the architecture is another great way to stay
hands-on. For example, an architect can write Java code in ArchUnit in the
Java platform to automate architectural compliance, or custom fitness functions
to ensure architectural compliance while gaining hands-on experience. We talk
about these techniques in Chapter 6.
Do code reviews
A final technique to remain hands-on as an architect is to do frequent code
reviews. While the architect is not actually writing code, this at least keeps
them involved in the source code. Further benefits of code reviews include ensuring compliance with the architecture and identifying mentoring and coaching
opportunities on the team.
There’s More to Architectural Thinking
This chapter forms the foundational aspects of beginning to think like an architect.
However, there’s much more to thinking like an architect than what is described in
this chapter. Thinking like an architect involves understanding the overall structure
of a system (we cover that topic next in Chapter 3), understanding business concerns
and translating those concerns to architectural characteristics (we have four chapters
on that topic), and finally, seeing a system through its logical components— the
building blocks of a system (we discuss that topic in Chapter 8).
