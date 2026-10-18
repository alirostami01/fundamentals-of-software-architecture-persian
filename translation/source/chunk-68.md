# Chapter 17: Orchestration-Driven Service-Oriented Architecture (continued)

## Style Specifics (continued)

### Taxonomy (continued)

#### Application services

Not all services in the architecture require the same level of granularity or reuse as the enterprise services. Application services are one-off, single-implementation services. For example, perhaps one application needs geolocation, but the organization doesn’t want to take the time or effort to make that a reusable service. An application service, typically owned by a single application team, solves that problem.

#### Infrastructure services

Infrastructure services supply operational concerns, such as monitoring, logging, authentication, authorization, and so on. These services tend to be concrete implementations, owned by a shared infrastructure team that works closely with operations. Architects’ philosophy in building this architecture revolves around technical partitioning, so it makes sense that they would build separate infrastructure services.

#### Orchestration engine and message bus

The orchestration engine forms the heart of this distributed architecture, stitching together the business service implementations using orchestration, including features like transactional coordination and message transformation. The orchestration engine defines the relationship between the business and enterprise services, how they map together, and where transaction boundaries lie. It also acts as an integration hub, allowing architects to integrate custom code with package and legacy software systems. This combination of features highlights the modern-day use of tools like enterprise service buses (ESBs). While most architects consider it a bad idea to build an entire architecture around ESBs, they are immensely useful in integration-heavy environments. Where architects must combine an integration hub and orchestration engine, why not use a tool that already includes them? (This points to another important skill to develop as an architect—how to discern the true uses of tools, separate from the hype, both good and bad.)

Because the message bus forms the heart of the architecture, Conway’s Law (see “Conway’s Law” on page 139) correctly predicts that the team of integration architects responsible for this engine tends to become a political force within an organization— and eventually a bureaucratic bottleneck.

While this centralized, taxonomized approach might sound appealing, in practice it has mostly been a disaster. Offloading transaction behavior to an orchestration tool sounds good, but architects struggle to find the correct level of granularity. While they can build a few services wrapped in a distributed transaction, the architecture becomes increasingly complex. Developers must figure out where the appropriate transaction boundaries between services lie as entities become involved in numerous workflows. Despite managers predicting and hoping that organizations could successfully build transactional building blocks as enterprise services, it has proved difficult in practice.

#### Message flow

All requests go through the orchestration engine, where this architecture’s logic resides. Thus, message flow goes through the engine even for internal calls, as shown in Figure 17-2.

Figure 17-2. Message flow with service-oriented architecture

In Figure 17-2, the `CreateQuote` business-level service calls the service bus, which defines the workflow. The workflow consists of calls to both `CreateCustomer` and `CalculateQuote`, each of which also makes calls to application services. The service bus acts as the intermediary for all calls within this architecture, serving as both an integration hub and orchestration engine.

### Reuse…and Coupling

One of the primary goals of the architects who first utilized this architecture was reuse at the service level—the ability to gradually build business behavior that they could incrementally reuse over time. They were instructed to find reuse opportunities as aggressively as possible.

For example, consider the situation illustrated in Figure 17-3. An architect realizes that each of six divisions within an insurance company contains a notion of `Customer`.

Figure 17-3. Seeking reuse opportunities in service-oriented architecture

Therefore, the proper SOA strategy entails extracting the `Customer` parts into a reusable service and then allowing the original services to reference the canonical `Customer` service. This is shown in Figure 17-4: here the architect has isolated all customer behavior into a single `Customer` service, achieving the obvious reuse goals.

Figure 17-4. Building canonical representations in service-oriented architecture

Architects only slowly realized the negative trade-offs of this design. First, when a team builds a system primarily around reuse, it also incurs a huge amount of coupling between components. After all, reuse is implemented via coupling. For example, in Figure 17-4, a change to the `Customer` service ripples out to all the other services. This makes even incremental change risky: each change has a potentially huge ripple effect. That in turn requires coordinated deployments, holistic testing, and other drags on engineering efficiency.

Another negative side effect of consolidating behavior into a single place: consider the case of auto and disability insurance in Figure 17-4. To support a single `Customer` service, each division must include all the details the organization knows about its customers. Auto insurance requires a driver’s license, which is a property of the person, not the vehicle. Therefore, the `Customer` service will have to include details about driver’s licenses that the disability insurance division cares nothing about. Yet the disability insurance team must deal with the extra complexity of a single customer definition. In many ways, DDD’s insistence on avoiding holistic reuse derives from experiences with these kinds of architectures.

Perhaps the most damaging revelation about orchestration-driven SOA is the impracticality of building an architecture so focused on technical partitioning. While this makes sense from a separation and reuse philosophy standpoint, it is a practical nightmare.

For example, developers commonly work on tasks like “add a new address line to `CatalogCheckout`.” Domain concepts like `CatalogCheckout` are spread so thinly throughout this architecture that they were virtually ground to dust. In an SOA, this task could involve dozens of services in several different tiers, plus changes to a single database schema. What’s more, if the current enterprise services aren’t defined at the correct transactional granularity, the developers will either have to change their design or build a nearly identical new service to change the transactional behavior. So much for reuse.

## Data Topologies

Unlike many of the architecture styles we discuss in this book, the data topologies for orchestration-driven SOA aren’t very interesting, given this style’s historical origins. Even though it is a distributed architecture consisting of many parts, it generally uses a single (or a few) relational databases, which was the common practice in all distributed architectures in the late 1990s. Even transactionality was generally relegated to this architecture and away from databases: the message bus often included declarative transactional interactions for each of the entities within the topology, allowing developers, architects, or others to determine transactional behavior independently of the database or even the situational reuse of the entity.

Architects in this era considered data a foreign country. While it is an inevitable part of the plumbing in both SOA and event-driven architectures, back then, they treated it more as an integration point than as part of the problem domain.

> **Really? Declarative Transactions?!?**
>
> Yes, really. One of the “features” of many application servers in the heyday of orchestration-driven SOA was allowing configuration managers to change the transactional scope of individual entities, depending on the transactional context within which they wanted to operate. (This was declared, of course, in XML, given the era and its love for verbose but easy-to-parse configuration formats.) A portion of the declaration of an entity (called `EntityBeans`, a specialized type of JavaBean) determines transactional scope as it participates in workflows, which architects themselves declare to be transactional or not. In turn, the application server interacts with the database to create and manage database transactions that match the desired behavior of the entities and/or workflows.
>
> This has largely failed, for two reasons. First, if a developer doesn’t know what the transactional behavior will be at runtime, it adds considerable complexity to entities and dependencies. This forces developers to create almost identical versions of the entities, differing only in their transactional scope. Second, no matter how much sophistication vendors build into their message buses, edge cases constantly appear where the myriad failure modes prevent the system from cleanly managing transactions, creating tangled messes of inconsistency for humans to untangle. Some complex, multifaceted features of systems (like transactions) cannot be cleanly abstracted away. Too many leaks in the abstraction prevent it from achieving reliability.
