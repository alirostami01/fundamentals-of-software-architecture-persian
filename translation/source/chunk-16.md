# Chapter 5: Identifying Architectural Characteristics

To create an architecture or determine the validity of an existing architecture, architects must analyze two things: architectural characteristics and domain. As you learned in Chapter 4, identifying the correct architectural characteristics (“-ilities”) for a given problem or application requires not only understanding the domain problem, but collaborating with stakeholders to determine what is truly important from a domain perspective.

There are at least three places to uncover what architectural characteristics a project needs: the domain concerns, the project requirements, and your implicit domain knowledge. In addition to generic implicit architectural characteristics, such as security and modularity, we’ve noted that some domains also include implicit architectural characteristics. For example, an architect working on medical software that reads from diagnostics equipment should already understand the importance of data integrity and the potential consequences of losing messages. Architects who work in that domain internalize data integrity, so it becomes implicit in every solution they design.

## Extracting Architectural Characteristics from Domain Concerns

Most architectural characteristics come from listening to key domain stakeholders and collaborating with them to determine what is important from a business perspective. While this may seem straightforward, the problem is that architects and domain stakeholders speak different languages. Architects talk about scalability, interoperability, fault tolerance, learnability, and availability; domain stakeholders talk about mergers and acquisitions, user satisfaction, time to market, and competitive advantage. What happens is a “lost in translation” problem where the architect and domain stakeholder don’t understand each other. Architects have no idea how to create an architecture to support user satisfaction, and domain stakeholders don’t understand why architects focus so much on the application’s availability, interoperability, learnability, and fault tolerance.

Fortunately, it’s possible to “translate” from domain concerns into the language of architectural characteristics. Table 5-1 shows some of the more common domain concerns and the corresponding “-ilities” that support them. Understanding the key domain goals allows an architect to translate those domain concerns to “-ilities,” which then forms the basis for correct and justifiable architecture decisions. For example, is the domain concern of time to market more important than scalability, or should the architect focus on fault tolerance, security, or performance? Perhaps the system requires all these characteristics combined.

Table 5-1. Translating domain concerns into architectural characteristics

| Domain concern | Architectural characteristics |
|---|---|
| Mergers and acquisitions | Interoperability, scalability, adaptability, extensibility |
| Time to market | Agility, testability, deployability |
| User satisfaction | Performance, availability, fault tolerance, testability, deployability, agility, security |
| Competitive advantage | Agility, testability, deployability, scalability, availability, fault tolerance |
| Time and budget | Simplicity, feasibility |

## Composite Architectural Characteristics

When translating domain concerns into architectural characteristics, one common pitfall is making false equivalences, such as equating agility solely with time to market. Agility is an example of a composite architectural characteristic: one that has no single objective definition but rather is composed of other measurable things. There’s no measure for agility, so architects must ask: what is agility composed of? It includes things like deployability, modularity, and testability, all of which are measurable.

A common antipattern arises when architects focus narrowly on just one part of a composite, often for convenience. This is like forgetting to put the flour in the cake batter. For example, a domain stakeholder might say something like, “Due to regulatory requirements, it is absolutely imperative that we complete end-of-day fund pricing on time.”

An ineffective architect might respond by focusing solely on performance, because that seems to be the primary focus of the domain concern. However, that approach will fail, for many reasons:

- It doesn’t matter how fast the system is if it isn’t available when needed.

- As the domain grows and more funds are created, the system must be able to scale to finish end-of-day processing in time.

- The system must not only be available, it must also be reliable so that it doesn’t crash as end-of-day fund prices are being calculated.

- What happens if the system crashes while end-of-day fund pricing is 85% complete? It must be able to recover and restart the pricing where it left off.

- Finally, the system may be fast, but are the fund prices being calculated correctly?

So, in addition to performance, this architect must focus equally on availability, scalability, reliability, recoverability, and auditability.

Many business goals start as composite architectural characteristics. Decomposing them, and giving the resulting characteristics objective definitions, is part of the architects’ job. (We’ll see the importance of this in Chapter 6.)

## Extracting Architectural Characteristics

Most architectural characteristics come from explicit statements in some form of requirements document. For example, lists of domain concerns commonly include explicit numbers of expected users and scale. Other characteristics come from architects’ inherent domain knowledge (one of many reasons every architect should know their domain).

For example, suppose you’re an architect designing an application that handles class registration for university students. To make the math easy, assume that the school has 1,000 students and 10 hours for registration. Should you make the implicit assumption that the students will distribute themselves evenly over those 10 hours, and design the system to handle a consistent scale? Or, based on your knowledge of university students’ habits and proclivities, should you design a system that can handle all 1,000 students attempting to register in the last 10 minutes?

Anyone who understands how much students stereotypically procrastinate knows the answer to this question! Rarely will details like this appear in requirements documents—yet they inform design decisions.

> SIDEBAR: The Origin of Architecture Katas

Over a decade ago, Ted Neward, a well-known architect, devised architecture katas, a clever method to allow nascent architects a way to practice deriving architectural characteristics from domain-targeted descriptions. The word kata derives from Japanese, where it refers to an individual martial arts training exercise that emphasizes proper form and technique.

> > How do we get great designers? Great designers design, of course.
> > —Fred Brooks

Big architectural projects take time, and it’s common for architects to design perhaps half a dozen systems in their careers. So how are we supposed to get great architects? The key is giving aspiring architects opportunities to practice their craft. To provide a curriculum, Ted created the first architecture katas site, which your authors Neal and Mark adapted and updated on the companion site for this book at fundamentalsofsoftwarearchitecture.com. True to their original purpose, architecture katas provide a useful laboratory for aspiring architects.

> END SIDEBAR

### Working with Katas

The basic premise is that each kata exercise provides a problem, stated in domain terms, a set of requirements, and some additional context (things that might not appear in the requirements, yet could influence the design). Small teams work on a design (consisting of architectural characteristics analysis and diagrams) for a set time. Then the groups share their results and vote on who came up with the best architecture.

Each kata has predefined sections:

- Description: The overall domain problem the system is trying to solve.

- Users: The expected number and/or types of users of the system.

- Requirements: Domain requirements (as expected from domain users and experts).

- Additional context: The authors updated the kata format on the previously mentioned site with an additional context section with important considerations, making the exercises more realistic.

We encourage readers to use the site to do their own kata exercise. Anyone can host a brown-bag lunch where a team of aspiring architects can solve a problem.

An experienced architect can evaluate the design and trade-off analysis, discussing missed trade-offs and alternative designs either on the spot or after the fact. The designs won’t be elaborate because the exercise is timeboxed.

Next, we’ll use an architecture kata to illustrate how architects derive architectural characteristics from requirements. Welcome to the Silicon Sandwiches kata.
