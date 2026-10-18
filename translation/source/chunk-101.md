# Chapter 26: Architectural Intersections

So far in this book, we’ve shown how to identify the critical characteristics an architecture must support, how to select the most appropriate architectural style for those characteristics and for the business problem, how to make effective architecture decisions, and how to lead and guide development teams through implementing the architecture. However, for an architecture to work, it must also be aligned with other facets of the technical and business environment. We call these alignments the *intersections of architecture*.

In this chapter, we discuss several important intersections that arise when creating or validating a software architecture:

- ***Implementation*:** Is the implementation aligned with architectural concerns surrounding operational characteristics, architectural constraints, and the internal structure of the architecture?
- ***Infrastructure*:** Do the infrastructure and the way the architecture is deployed align with the operational concerns of the architecture, such as scalability, responsiveness, fault tolerance, and availability?
- ***Data topologies*:** One widely ignored alignment is that between the intersection of architecture and data topologies and data type. The data topology (monolithic, domain databases, and database per service) must properly align with the architectural style for the system to work.
- ***Engineering practices*:** Does the way the development team creates, maintains, and tests software match the corresponding architecture? Does the deployment pipeline match the architectural style?
- ***Team topologies*:** The way teams are organized can significantly impact the architecture, and vice versa. If the team structure is not properly aligned with the architecture, development teams will usually struggle, finding even the simplest of changes challenging.
- ***Systems integration*:** What other systems or services does the architecture need to communicate with? Not paying attention to this particular intersection can have devastating results in terms of maintenance, reliability, and operational characteristics such as scalability, responsiveness, and availability.
- ***The enterprise*:** Is the architecture aligned with the frameworks, practices, guiding principles, and standards across the organization and the enterprise?
- ***The business environment*:** Is the architecture properly aligned with the business environment and the problem domain? Too often architects ignore this important intersection, and as a result the architecture fails to meet the goals or needs of the business.
- ***Generative AI*:** How does the increasing use of large language models (LLMs) impact the architecture? This intersection is quickly becoming an important one as more companies leverage generative AI within their systems.

The following sections describe these intersections in more detail.

## Architecture and Implementation

The First Law of Software Architecture also happens to be software architects’ most common response to any question: “It depends.” Perhaps the second most common response is, “That’s an implementation detail.” When a software architecture fails to achieve its goals, this second response is often to blame.

For an architecture to work properly, its *implementation*—that is, its source code—must be aligned with its design to address three things: the architecture’s operational concerns (such as fault tolerance, responsiveness, scalability, and so on), internal structure, and constraints. This section addresses each of the three in turn.

### Operational Concerns

*Operational concerns* are the architectural characteristics we focused on in Part I of the book, which form the foundation of any software architecture, and which the architecture must support in order to solve the business problem at hand. Architectural characteristics are what drive architectural decisions (as discussed in Chapter 21).

So what does it mean for the architecture and the implementation to fall out of alignment in how they address the system’s operational concerns? Let’s say you’re an architect working on a new order-entry system that needs to support anywhere from several thousand to half a million concurrent customers. You choose a microservices architecture style, based on the star ratings found in “Style Characteristics” on page 354 in Chapter 18, which is appropriate based on this system’s high scalability and elasticity needs. However, during *implementation*, the development team observes that, because the services’ bounded contexts are so tightly formed (see “Bounded Context” on page 331 in Chapter 18), the `Order Placement` service cannot access the inventory database directly. Instead, it must synchronously call the `Inventory` service to get the current inventory for any item a customer is interested in buying. Not only does this synchronous call tightly couple the two services, it greatly slows the system’s responsiveness.

The development team decides to use an *in-memory replicated cache* between these services, as shown in Figure 26-1: data resides in the *internal memory* of each service instance, and is always kept in sync behind the scenes through caching. Caching products for this purpose include Apache Ignite and Hazelcast. Here, the `Inventory` service would have a writable in-memory cache containing the item IDs and current inventory counts; each instance of the `Order Placement` service would have a replicated read-only version of that cache in its internal memory. Using an in-memory replicated cache decouples the services and *significantly* improves responsiveness.

> **Figure 26-1.** The development team decided to use in-memory replicated caching between services, resulting in out-of-memory conditions when scaling the services

After production release, as the number of concurrent users grows, more instances of each service are needed to handle the load. The system crashes when the load reaches about 80,000 concurrent customers because the internal cache’s memory requirements are too high, causing out-of-memory conditions in all of the virtual machines.

In this scenario, the architecture and its implementation are misaligned. While the architecture focuses on supporting high levels of *scalability* and *elasticity*, the implementation focuses on *responsiveness* and *service decoupling*. Both teams made good decisions, but in service of different goals.

### Structural Integrity

You learned in Chapter 8 that logical components are the building blocks of any system and form its *logical architecture*. They are usually represented through the directory structures in the source-code repository (or namespaces, depending on the programming language). Since the logical architecture describes how the system works and what parts of the system interact with other parts, it’s critical that the structure of the source code matches that of the logical architecture.

Without proper guidance, knowledge, and governance, it’s easy for developers to ignore the system’s logical architecture and start creating directory structures and namespaces as they please, without regard for their impact on the system’s integrity. This misalignment results in architectures that are difficult to maintain, test, and deploy, and as a result become less reliable and harder to evolve or adapt to new features, such as the logical architecture illustrated in Figure 26-2.

> **Figure 26-2.** An example of an internal logical architecture that lacks governance and alignment

To ensure that the structure of the source code matches the logical architecture, we recommend using automated governance tools, such as ArchUnit for the Java platform, ArchUnitNet and NetArchTest for the .NET platform, PyTestArch for Python, or TSArch for TypeScript and JavaScript. These automated tools, coupled with good communication and collaboration between the architect and the development team, create implementations that are properly aligned with the architecture, as shown in Figure 26-3.

> **Figure 26-3.** An example of an internal logical architecture based on proper governance and alignment

Compare Figure 26-2 with Figure 26-3. Notice how the architecture in Figure 26-3 is much more maintainable, testable, deployable, reliable, adaptable, and extensible than that of the misaligned architecture shown in Figure 26-2. This comparison illustrates the importance of this type of implementation alignment.
