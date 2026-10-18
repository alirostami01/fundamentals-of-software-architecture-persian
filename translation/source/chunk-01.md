<!-- Source chunk 01 | Book: Fundamentals of Software Architecture, 2e (Richards & Ford) -->
<!-- PDF pages 24-29 (Chapter 1: Introduction, through the First Law) | words: 882 -->

CHAPTER 1
Introduction
So you’re interested in software architecture. Perhaps you’re a developer who wants
to move to the next career step, or perhaps you are a project manager who wants
to understand what happens when software architectures work. You may also be an
“accidental architect”: someone who makes architecture decisions (defined below)
but doesn’t have the title of “software architect"…yet.
Why delve into the realm of software architecture? Perhaps you have experience with
lots of projects and want to understand more deeply how the larger parts of systems
fit together, along with the numerous trade-offs. If so, software architecture is an
obvious next career step.
This book is designed for all of you. It provides an overview of the extremely
multifaceted job of “software architect. ”
Software architects must understand and analyze software systems deeply, in all their
complexity, and must make important trade-off decisions, sometimes with incomplete information. Many software developers worried that generative AI might slowly
replace them are considering moving to software architecture, a role much harder
to replace. Software architects make exactly the kinds of decisions that AI cannot,
evaluating trade-offs within complex, changing contexts.
Architecture, like much art, can only be understood in context. Architects base
their decisions on the realities of their environment. For example, one of the major
goals of late-20th-century software architecture was to use shared infrastructure and
resources as efficiently as possible, because operating systems, application servers,
database servers, and so on were all commercial and very expensive.
In 2002, trying to build an architecture like microservices would have been inconceivably expensive. Imagine strolling into a 2002 data center and telling the head of
operations, “Hey, I have a great idea for a revolutionary style of architecture, where
each service runs on its own isolated machinery with its own dedicated database.
I’ll need 50 Windows licenses, another 30 application-server licenses, and at least
50 database server licenses. ” We can only build such architectures today because of
the advent of open source and the updated engineering practices of the DevOps
revolution. All architectures are products of their context—keep that in mind as you
read this book.
Defining Software Architecture
So what is software architecture? Figure 1-1 illustrates how we like to think about
software architecture. This definition has four dimensions. The software architecture
of a system consists of an architecture style as the starting point, combined with the
architecture characteristics it must support, the logical components to implement its
behavior, and finally the architecture decisions justifying it all. The system’s structure
is denoted by the heavy black lines supporting the architecture. We’ll walk quickly
through these dimensions in the order in which architects analyze them, and subsequent chapters will provide more details.
Figure 1-1. Architecture consists of the system’s structure, combined with architecture
characteristics (“-ilities”), logical components, architecture styles, and decisions
Architecture characteristics (see Figure 1-2) define the capabilities of a system (commonly abbreviated as “-ilities”) and the criteria for its success: in short, what the
system should do. Architecture characteristics are so important that we’ve devoted
several chapters in this book to understanding and defining them.
Figure 1-2. “ Architecture characteristics” refer to the “-ilities” that the system must
support
While architectural characteristics define a system’s capabilities, logical components
define its behavior. Designing logical components is one of the key structural activities for architects. In Figure 1-3, the logical components form the domains, entities,
and workflows of the application.
Figure 1-3. Logical components structure the behavior of the system
Once an architect has analyzed the architectural characteristics and logical components the system needs (both described in detail later), they know enough to choose
an appropriate architecture style as a starting point for implementing their solution
Figure 1-4.
Figure 1-4. Choosing an architectural style involves finding the easiest implementation
path for a given set of requirements
The fourth dimension that defines software architecture is architecture decisions,
which define the rules for how a system should be constructed. For example, an
architect might make a decision that only the Business and Services layers within
a layered architecture can access the database (see Figure 1-5 ), restricting the Presentation layer from making direct database calls. Architecture decisions form the
constraints of the system and direct the development teams on what is and what isn’t
allowed.
Figure 1-5. Architecture decisions are rules for constructing systems
We discuss architecture decisions and how to document them concisely in Chapter 21.
Laws of Software Architecture
As your two authors set out to write the first edition of this book, we had an
ambitious goal: we hoped to find things that seemed universally true about software
architecture and codify them as “laws” of software architecture. As we wrote, we
kept our eyes peeled for things we could capture; we had hoped to find maybe 10 or
15. To our surprise, we ended up identifying just two laws in the first edition, and
uncovered one more while writing the second edition. True to our original intent,
these three laws seem pretty universal and inform many important perspectives for
working software architects.
We learned the First Law of Software Architecture by constantly stumbling across it,
and we think it gets to the heart of why these universal truths seem so elusive:
Everything in software architecture is a trade-off.
—First Law of Software Architecture
