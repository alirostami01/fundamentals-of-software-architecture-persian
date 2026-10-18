# Chapter 7: The Scope of Architectural Characteristics

Software architects’ thinking must evolve with our ecosystem, and nowhere is that more apparent than in scoping architectural characteristics. Many of the outdated frameworks for determining architectural characteristics had a fatal flaw: assuming one set of architectural characteristics for the entire system. While that is sometimes still true, many modern architectures, like microservices, contain different architectural characteristics at the service and system levels.

The scope of architectural characteristics is a useful measure for architects, especially in determining the most appropriate architecture style to use as a starting point for implementation. When we were writing our book Building Evolutionary Architectures, we needed a technique to measure the structural evolvability of particular architecture styles. None of the existing measures offered the correct level of detail. The section “Structural Measures” on page 83 discusses a variety of code-level metrics that allow architects to analyze structural aspects of an architecture—but none of these metrics reflects scope. They reveal low-level details about the code, but can’t evaluate dependent components outside the code base (such as databases) that affect many architectural characteristics, especially operational ones. No matter how much effort an architect puts into designing a code base to be performant or elastic, if the system’s database doesn’t match those characteristics, their effort won’t be successful.

Failing to find a good measure of scope, we developed one. We call it architecture quantum.

## Architectural Quanta and Granularity

Component-level coupling isn’t the only thing that binds software together. Many business concepts bind parts of the system together semantically, creating functional cohesion. To design, analyze, and evolve software successfully, architects and developers must consider all the coupling points that could break.

> SIDEBAR: Plurals for Latin-Derived Technical Terms

Quantum originates in Latin, which means that the plural ends with an a. If you have more than one quantum, you have quanta—like the more common data, also derived from Latin. Architects rarely discuss a single datum. The Chicago Manual of Style usage guide notes: “Though originally this word was a plural of datum, it is now commonly treated as a mass noun and coupled with a singular verb” (18th edition, 2024, p. 336).
> END SIDEBAR

Many science-literate architects know of the concept of a quantum from physics, where it refers to the smallest possible amount of something—usually energy. The word quantum derives from Latin, meaning “how great” or “how much.” In general usage, it tends to mean “small, unbreakable thing,” which is how we define an architecture quantum. Another common informal definition of architecture quantum is “the smallest part of the system that runs independently.” For example, microservices often form architecture quanta, which exemplifies this definition: a service can run independently within the architecture, including its own data and other dependencies.

An architecture quantum establishes the scope for a set of architectural characteristics. It features:

- Independent deployment from other parts of the architecture

- High functional cohesion

- Low external implementation static coupling

- Synchronous communication with other quanta

This definition contains several parts. Let’s break them down:

- Establishes the scope for a set of architectural characteristics: Architects use the architecture quantum as a boundary delineating a set of architectural characteristics, particularly operational ones. Because it is independently deployable and has high functional cohesion (discussed next), the architecture quantum provides a useful measure of architecture modularity.

- Independently deployable: An architecture quantum includes all the necessary components to function independently from other parts of the architecture. For example, if an application uses a database, that database is part of the quantum, because the system won’t function without it. This requirement means that virtually all legacy systems that are deployed using a single database, by definition, form a quantum of one. However, in the microservices architecture style, each service includes its own database (part of the bounded context driving philosophy, described in detail in Chapter 18). This creates multiple quanta within that architecture, because each service has its own architectural characteristics scope.

- High functional cohesion: Cohesion in component design refers to how unified the contained code is in its purpose. For example, a Customer component, with properties and methods all pertaining to a Customer entity, exhibits high cohesion. A Utility component with a random collection of miscellaneous methods would not. High functional cohesion implies that an architecture quantum does something purposeful. This distinction matters little in traditional monolithic applications with a single database, where the cohesion is essentially the entire system. However, in distributed architectures like event-driven or microservices, architects are more likely to design each service to match a single workflow (a bounded context, as described in “Domain-Driven Design’s Bounded Context”), so that service would exhibit high functional cohesion.

> SIDEBAR: Domain-Driven Design’s Bounded Context

Eric Evans’s book Domain-Driven Design (Addison-Wesley Professional, 2003) has deeply influenced modern architectural thinking. Domain-driven design (DDD) is a modeling technique that allows architects to decompose complex problem domains in an organized way. DDD defines a bounded context, where everything related to a portion of the domain is visible internally but opaque to other bounded contexts.

Before DDD, architects sought to reuse code holistically across common entities within the organization. But they found that creating common shared artifacts causes a host of problems, such as tight coupling, more difficult coordination, and increased complexity. The bounded-context concept recognizes that each entity works best within a localized context. Thus, instead of creating a unified Customer class across the entire organization, each problem domain can create its own Customer class and reconcile the differences at communication points with other domains.
> END SIDEBAR

To clarify the next parts of the definition, we need to make some finer distinctions about the types of coupling:

- Semantic coupling: Semantic coupling describes the natural coupling of the problem for which an architect is building a solution. For example, an order-processing application’s inherent coupling includes things like inventory, catalogs, shopping carts, customers, and sales. The nature of the problem that motivates building a software solution defines this coupling. Architects have few techniques that prevent changes to the domain from rippling out through the system: a change to the domain (and therefore the semantics) means we’re changing the requirements for the system. While architects can adapt to that, no magical architecture pattern prevents changing the core problem from affecting the architecture.

- Implementation coupling: Implementation coupling describes how an architect and team decide to implement particular dependencies. In an order-processing application, the team must consider a variety of constraints in setting domain boundaries. For example, should all the data reside in a single database, or should some of it be split apart for better scalability or availability? Should we build a monolith or a distributed architecture? The answers to these questions have little effect on the system’s semantic coupling, but greatly affect architectural decisions.

- Static coupling: Static coupling refers to the “wiring” of an architecture—how services depend upon one another. Two services are part of the same architecture quantum if they both depend on the same coupling point. For example, let’s say that two microservices, Catalog and Shipping, need to share address information, so they both create a dependency to a shared component. Because both services are coupled to that dependency, they are part of the same architecture quantum.

Here’s an easy way to think about coupling in software architecture: two things are coupled if changing one might break the other. Static coupling defines the scope dependencies in an architecture. For example, if several services use the same relational database, they are part of the same quantum.

- Dynamic coupling: Dynamic coupling describes the forces involved when architecture quanta must communicate with each other. For example, when two services are running, they must communicate to form workflows and perform tasks within the system. Architects must consider the trade-offs when communicating between services in a distributed architecture, which is discussed in detail in Chapter 15.

With these definitions in hand, we can complete our architecture quantum definition:

- Low external implementation static coupling: The level of implementation coupling between architecture quanta should be low. This characteristic is also derived from the DDD philosophy of low coupling between bounded contexts. Quanta form the operational building blocks of architecture that sit one level of abstraction higher than components. They often overlap with service boundaries. This goal reflects architects’ general preference for loose coupling between different parts of the architecture.

In general, tight coupling is desirable when high cohesion is required, such as within a service or subsystem. We call an architecture “brittle” when a single implementation change can cause unexpected rippling side effects that break many other (ostensibly unrelated) things. The broader the scope of the system’s coupling, the more loose coupling helps to make the architecture less brittle. For example, an architect might rename a field in a service call from State to StateCode, thinking it will only affect one caller, only to discover that many other dependencies have just broken unexpectedly.

> TIP: Higher coupling is allowed for narrower scopes; the broader the scope, the looser the coupling should be.
