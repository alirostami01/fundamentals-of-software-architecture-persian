# Chapter 19: Choosing the Appropriate Architecture Style (continued)

## Decision Criteria (continued)

**Domain/architecture isomorphism:** Architecture isomorphism is a fancy term for the generic “shape” of an architecture—in other words, the way its components depend on each other within the overall topology. The word isomorphism means “a map that preserves sets and relations among elements”; it derives from the Greek isos, meaning “equal,” and morph, meaning “form” or “shape.”

Architects think about the generic shape of the architecture when considering how suitable it is. For example, consider the differences between the two architecture isomorphism diagrams for the layered and modular monolith architectural styles shown in Figure 19-1. The internal shape of each architecture is apparent: separation by layers versus by domains.

> **Figure 19-1.** Comparison between the isomorphic representations of layered and modular monoliths

The difference between monolithic and distributed is similarly clear from isomorphic drawings, as illustrated in Figure 19-2. Here, the distribution of core components makes the macro-level structure of the architecture clear.

> **Figure 19-2.** Comparing isomorphic representations of monolithic and distributed architecture styles

Some problem domains match the topology of the architecture. For instance, the microkernel architecture style is perfectly suited to systems that require customizability—the architect can design customizations as plug-ins. For another example, a system designed for genome analysis, which requires a large number of discrete operations, might be a good fit for space-based architecture, which offers a large number of discrete processors.

Similarly, some problem domains may be particularly ill-suited for certain architecture styles. Highly scalable systems struggle with large monolithic designs, because it’s difficult for a highly coupled code base to support a large number of concurrent users. A problem domain that includes a huge amount of semantic coupling would match poorly with a highly decoupled, distributed architecture: for instance, an insurance application consisting of multipage forms, each based on the context of previous pages, is a highly coupled problem. It would be difficult to model in a decoupled architecture like microservices. An intentionally coupled architecture like service-based architecture would suit this problem better.

Taking all these things into account, you must make several determinations in choosing an architecture style:

**Monolith versus distributed?** Will a single set of architecture characteristics suffice for the design, or do different parts of the system need differing architecture characteristics? A single set implies that a monolith would be suitable (although other factors may suggest a distributed architecture); different sets of architecture characteristics imply a distributed architecture. The concept of architecture quantum (Chapter 7) is useful in making this determination.

**Where should data live?** If the architecture is monolithic, architects commonly assume it will use a single relational database, or perhaps a few of them. In a distributed architecture, you must decide which services should persist data, which also implies thinking about how data will flow through the architecture to build workflows. Consider both structure and behavior when designing architecture, and don’t be afraid to iterate on your design to find better combinations.

**Should services communicate synchronously or asynchronously?** Once you’ve determined where data should live, the next design consideration is communication between services—should it be synchronous or asynchronous? Synchronous communication is often more convenient, but it can mean trading off on scalability, reliability, and other desirable characteristics. Asynchronous communication can provide unique benefits in terms of performance and scale, but also plenty of headaches around data synchronization, deadlocks, race conditions, debugging, and so on. (We cover many of these issues in Chapter 15.)

Because synchronous communication presents fewer design, implementation, and debugging challenges, we recommend defaulting to synchronous when possible, and using asynchronous communication only when necessary.

> **Tip:** Use synchronous communication by default, asynchronous when necessary.

The output of this design process is an architecture topology that encompasses the chosen architecture style (and any hybridizations), Architectural Decision Records (ADRs) about the parts of the design that require the most effort, and architecture fitness functions to protect important principles and operational architecture characteristics.

## Monolith Case Study: Silicon Sandwiches

In the Silicon Sandwiches architecture kata in Chapter 5, after our architecture characteristics analysis, we determined that a single quantum was sufficient to implement the system. Since we were looking at a simple application without a huge budget, the simplicity of a monolith was appealing.

However, we created two different component designs for Silicon Sandwiches: one domain partitioned, and another technically partitioned—you might want to flip back to Chapter 5 if you want a refresher. In this chapter, we return to those simple solutions to create designs for each option and discuss their trade-offs. We’ll begin with a monolithic architecture.

### Modular Monolith

A modular monolith builds domain-centric components with a single database, deployed as a single quantum; the modular monolith design for Silicon Sandwiches appears in Figure 19-3.

This is a monolith with a single relational database, implemented with a single web-based UI (with careful design considerations for mobile devices) to keep overall cost down. Each of the domains we identified appears as a component. If time and resources are sufficient, consider separating the tables and other database assets in the same way as the domain components, which would make it much easier to migrate this architecture to a distributed architecture if future requirements warrant it.

> **Figure 19-3.** A modular monolith implementation of Silicon Sandwiches

Because the architecture style itself doesn’t inherently handle customization, that feature should become part of the domain design. In this case, the architect designs an `Override` endpoint, where developers can upload individual customizations. Correspondingly, they must ensure that every domain component references the `Override` component for each customizable characteristic. (Checking this would be a perfect job for an architectural fitness function.)

### Microkernel

One of the architecture characteristics we identified in Silicon Sandwiches was customizability. Figure 19-4 uses domain/architecture isomorphism to show how this could be implemented using a microkernel architecture.

> **Figure 19-4.** A microkernel implementation of Silicon Sandwiches

In Figure 19-4, the core system consists of the domain components and a single relational database. As in the modular monolith design, careful synchronization between the domains and the data design will facilitate migrating the core to a distributed architecture in the future. Each customization appears in a plug-in; the common ones appear in a single set of plug-ins (with a corresponding database) and a series of local ones, each with its own data. Because none of the plug-ins need to be coupled to the other plug-ins, they can each maintain their data and remain decoupled.

The other unique element of this design is that it utilizes the Backends for Frontends (BFF) pattern, making the API layer a thin microkernel adapter in addition to the core architecture. The API layer supplies general information from the backend, which the BFF adapters translate into a suitable format for the frontend device. For example, the BFF for iOS takes the generic backend output and customizes the data format, pagination, latency, and other factors to fit what the iOS native application expects. Building each BFF adapter allows for the richest possible user interfaces and makes it possible to expand the architecture to support other devices in the future—one of the benefits of the microkernel style.

Communication within either of these two Silicon Sandwich architectures can be synchronous, since the architecture doesn’t require extreme performance or elasticity requirements, and none of the operations will be lengthy.
