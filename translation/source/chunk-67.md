# Chapter 17: Orchestration-Driven Service-Oriented Architecture

Architecture styles make sense to architects in the context of the era when they evolved, but lose relevance in later eras, much like art movements. Orchestration-driven service-oriented architecture (SOA) exemplifies this tendency. The external forces that often influence architecture decisions, combined with a logical but ultimately disastrous organizational philosophy, doomed this architecture to irrelevance. However, it provides a great example of how a particular organizational idea can make logical sense yet hinder the most important parts of the development process. It illustrates one of the dangers of ignoring our First Law: everything in software architecture is a trade-off.

## Topology

The topology of orchestration-driven SOA is shown in Figure 17-1.

Not all examples of this style of architecture have these exact layers, but they all follow the same idea of establishing a taxonomy of services within the architecture, each layer with a specific, well-defined responsibility.

Service-oriented architecture is a distributed architecture. The exact demarcation of boundaries isn’t shown in Figure 17-1 because it varies based on organization and tools: some of the parts of the taxonomy may exist inside an application server. Orchestration-driven SOA centers on a specific taxonomy of services, with different technical responsibilities within the architecture and roles dedicated to specific layers.

Figure 17-1. Topology of orchestration-driven service-oriented architecture

## Style Specifics

Orchestration-driven SOA is mostly of historical interest to current-day architects; the lessons learned from building these architectures are an important part of the field’s evolution. However, architects still find parts of it relevant in some integration architecture scenarios.

Service-oriented architecture appeared in the late 1990s, just as small companies of all kinds were growing into enterprises at a breakneck pace, merging with smaller companies, and requiring more sophisticated IT to accommodate this growth. However, computing resources were scarce, precious, and commercial. Distributed computing had just become possible and necessary, and many companies needed its scalability and other beneficial characteristics.

Many external drivers forced architects in this era toward distributed architectures with significant system constraints. Before open source operating systems were thought reliable enough for serious work, operating systems were expensive and licensed per machine. Similarly, commercial database servers came with Byzantine licensing schemes, which sometimes caused application-server vendors (which offered database connection pooling) to react by battling with database vendors. Given that so many resources were expensive at scale, architects adopted a common philosophy of reusing as much as possible.

These technical concerns wedded with organizational concerns about duplication of both information and workflows—because of frequent mergers and growth, organizations struggled with the variety and inconsistencies between core business entities. This made the goals of SOA attractive. Consequently, architects embraced reuse in all forms as the dominant philosophy in this architecture, the side effects of which we cover in “Reuse…and Coupling” on page 320. This style of architecture also exemplifies how far architects can push the idea of technical partitioning, which can have good motivations but leads to bad consequences when taken to extremes.

> **Why So Many Service Names?**
>
> Architects are often confused by the multitude of things in software architecture called services. We cover three different “services” styles even in this book: SOA in this chapter, microservices in Chapter 18, and service-based architectures in Chapter 14. Part of the problem is the inflexibility of language to describe architectures. The other part lies in the constant evolution of the software-development ecosystem. Service is a nice generic name for something that provides a, well, service, so architects tend to reuse the name. As styles evolve, we change what we mean by service. For example, an entity service in an orchestration-driven SOA is different in virtually every way from a service in a microservices architecture (which is distinct from a service-based architecture). As annoying as it is, architects must often parse the context when the word service appears in a name; the term itself has suffered from semantic diffusion.

### Taxonomy

The driving philosophy behind this architecture is a specific type of abstraction and enterprise-level reuse. Many large companies were annoyed at how much they had to continually rewrite software. They arrived at a strategy that seemed to solve that problem gradually by creating a strict service taxonomy, with well-defined layers and corresponding responsibilities. Each layer of the taxonomy supports the dual goals of ultimate abstraction and reuse.

#### Business services

Business services sit at the top of this SOA and provide the entry point for business processes. For example, services like `ExecuteTrade` or `PlaceOrder` represent the correct scope of behavior for these services. One litmus test common at the time was: can an architect answer “yes” to the question “Are we in the business of…” for each of these services? If so, then the service is at the appropriate level of granularity. However, while a developer might need a method like `CreateCustomer` to carry out a business process like `ExecuteTrade`, `CreateCustomer` is at the wrong level of abstraction for a business service. The company isn’t in the business of creating customers, but it needs to create customers in order to execute trades.

These service definitions contain no code—just input, output, and sometimes schema information. Business users and/or analysts define these service signatures, hence the name business services.

#### Enterprise services

The enterprise services contain fine-grained shared implementations. Typically, a team of developers builds atomic behavior around particular business domains, such as `CreateCustomer` or `CalculateQuote`, and transactional entities, such as `Customer`, `Order`, and `Lineitem`. These enterprise services are the building blocks that make up the business services, tied together via the orchestration engine.

It is worth noting the abstraction differences between business and enterprise services. While business services are quite coarse-grained, enterprise services are fine-grained and meant to capture different types of abstractions, workflows, and entities. The architect’s goal in creating enterprise services is to create perfectly encapsulated building blocks of isolated business functionality that can be freely composed into more complex business workflows.

While that’s a laudable goal, architects find that the ideal sweet spot of abstraction between all these forces is elusive at best and likely impossible because of numerous competing trade-offs. Ultimately, like other technically partitioned architectures, this architecture attempts a strict separation of responsibility, which flows from the imperative of reuse. The idea is that if developers can build fine-grained enterprise services at just the correct level of granularity, the business won’t have to rewrite that part of the business workflow again. Gradually, the business will build up a collection of reusable assets in the form of reusable enterprise services—in theory, anyway.

Unfortunately, the dynamic nature of reality and the evolutionary impact of the software development ecosystem defy these attempts. Business components aren’t like construction materials, where solutions last decades. Markets, technology changes, engineering practices, and a host of other factors confound attempts to impose stability on the software world.
