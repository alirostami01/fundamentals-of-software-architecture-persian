# Chapter 25: Negotiation and Leadership Skills (continued)

## The Software Architect as a Leader

A software architect is also a leader, guiding a development team as they implement the architecture. We maintain that about 50% of being an effective software architect is having good people skills, including facilitation and leadership. In this section, we discuss leadership techniques for software architects.

### The 4 Cs of Architecture

We’ve said many times that change is a constant—and that’s never more true than when the change in question involves things getting more and more complex, whether it’s business processes, technology, or even architecture itself. As you saw in Part III of this book, some architectures are *very* complex. If an architecture needs to support six nines of availability (99.9999%), that’s equivalent to unplanned downtime of about 86 milliseconds a day, or 31.5 seconds of downtime per *year*. This sort of complexity is known as *essential complexity*—in other words, “we have a hard problem.”

It’s easy for architects (and developers) to fall into the trap of adding unnecessary complexity to solutions, diagrams, and documentation. To quote Neal:

> Developers are drawn to complexity like moths to a flame—frequently with the same result.

Figure 25-1 diagrams the major information flows of the backend processing systems at a very large global bank. Is this system *necessarily* complex—in other words, does it *have* to be complex? No one knows, because the architect has *made* it complex. This sort of complexity is called *accidental complexity*: in short, “we have made a problem hard.” Architects sometimes add complexity to prove their worth when things seem too simple, or to guarantee that they are always kept in the loop on decisions or even to maintain job security. Whatever the reason, introducing accidental complexity into something that does not have to be complex is one of the best ways to lose respect and become an ineffective leader and architect.

> **Figure 25-1.** Introducing accidental complexity into a problem

To avoid accidental complexity, we use what we call the *4 Cs* of architecture leadership: *communication*, *collaboration*, *clear*, and *concise*. These factors, as shown in Figure 25-2 (not to be confused with the 4 Cs within the C4 Model of diagramming), work together to create an effective communicator and collaborator on the team.

> **Figure 25-2.** The 4 Cs of architecture

As a leader, facilitator, and negotiator, it’s vital for a software architect to be able to *communicate* *clearly* and *concisely*. It is equally important to be able to *collaborate* with developers, business stakeholders, and other architects. Focusing on the 4 Cs helps an architect gain the team’s respect and helps make them the go-to person on the project for questions, advice, mentoring, coaching, and leadership.

### Be Pragmatic, Yet Visionary

An effective software architect must be pragmatic, yet visionary. Striving for this balance is not as easy as it sounds; it takes a fairly high level of maturity and significant practice to accomplish.

A *visionary* is someone who thinks about or plans the future with imagination or wisdom. Being a visionary means applying strategic thinking to a problem, which is exactly what architects do. Architects plan for the future and make sure the architecture they build remains vital (valid and useful) for a long time. However, architects often become too theoretical in their planning and designs, creating solutions that are too difficult to implement—or even understand.

Now consider the other side of the coin, which is being *pragmatic*. Being pragmatic means dealing with things sensibly and realistically in a way that is based on *practical* rather than *theoretical* considerations. While architects need to be visionaries, they also need to apply practical, realistic solutions. Being pragmatic when creating an architectural solution means accounting for:

- Budget constraints and other cost-based factors
- Time constraints and other time-based factors
- The development team’s skill set and skill level
- The trade-offs and implications of each architecture decision
- The technical limitations of any proposed design or solution

Good software architects strive to balance pragmatism with imagination and wisdom in solving problems (see Figure 25-3).

For example, consider an architect faced with sudden, significant increases in concurrent user load for reasons that are unclear. A visionary might come up with an elaborate way to improve the system’s elasticity by breaking apart the databases and building a complex *data mesh*: a collection of distributed, domain-partitioned databases used to separate analytical data concerns from transactional ones. In theory, this approach *might* be possible, but being pragmatic means applying reason and practicality to the solution. For example, has the company ever used a data mesh before? What are the trade-offs of using a data mesh? Would this solution really solve the problem?

> **Figure 25-3.** Good architects find the balance between being pragmatic and being visionary

Maintaining a good balance between being pragmatic and being visionary is an excellent way to gain respect as an architect. Business stakeholders appreciate visionary solutions that fit within a set of constraints, and developers appreciate having a practical (rather than theoretical) solution to implement.

A pragmatic architect would first look at what factors are limiting the system’s elasticity. Finding and isolating any bottlenecks would be a practical first approach to this problem. Is the database creating a bottleneck with respect to some of the services invoked or other external sources needed? If so, could some of the data be cached to reduce calls to the database?

### Leading Teams by Example

Bad software architects “pull rank,” using their title to get people to do things. Effective software architects get people to do things by leading through example. Again, this is all about gaining the respect of development teams, business stakeholders, and other people throughout the organization (such as the head of operations, development managers, and product owners).

The classic “lead by example, not by title” story involves a captain in command of a sergeant during a military battle. The captain, who is largely removed from the troops, commands all of the troops forward to take a particularly difficult hill. The soldiers, full of doubt, look for confirmation from the lower-ranking sergeant. The sergeant, understanding the situation, nods his head slightly, and the soldiers immediately move forward with confidence to take the hill.

The moral of this story is that rank and title mean very little when it comes to leading people. The computer scientist Gerald Weinberg is famous for saying, “No matter what the problem is, it’s a people problem.” Most people think that solving technical issues has nothing to do with people skills and everything to do with *technical knowledge*. While technical knowledge is certainly necessary, it’s only a part of solving any problem.

Suppose, for example, that an architect is meeting with a team of developers to solve an issue that’s come up in production. One of the developers makes a suggestion, and the architect responds, “Well, *that’s* a dumb idea.” Not only will that developer not make any more suggestions, but now none of the other developers dare to say anything. The architect has just shut down collaboration across the entire team.
