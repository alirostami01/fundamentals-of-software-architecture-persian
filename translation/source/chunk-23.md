# Chapter 7: The Scope of Architectural Characteristics (continued)

## Synchronous Communication

Communication refers to dynamic coupling—when architecture quanta call each other, which is common in distributed architectures. This particularly concerns the family of operational architectural characteristics described in “Operational Architectural Characteristics” on page 59, because they often determine important timing and blocking in distributed architectures.

For example, consider a microservices architecture with a Payment service and an Auction service. When an auction ends, the Auction service sends payment information synchronously to the Payment service. However, let’s say that the Payment service can only handle one payment every 500 ms. What happens when a large number of auctions end at once? The two services have different operational architectural characteristics. The first call will work, but then calls will start failing because the Payment service can’t handle the number of requests—it isn’t as scalable as the Auction service.

We call out synchronous communication here because asynchronous communication has less potential impact. For example, if the Auction service calls the Payment service asynchronously, using a message queue, the queue can act as a buffer to allow the two systems to operate. Of course, if the Auction service continually sends more messages than Payment can handle, it will eventually overflow the message queue. However, when the flood of messages comes in bursts, the queue can hold on to pending messages until the receiver is ready. Synchronous communication is unforgiving in distributed architectures, especially if parts of the architecture have different architectural characteristics. Chapter 15 thoroughly covers the types of communication in event-driven architectures.

The concept of architecture quantum provides a new way to think about scope. In modern systems, architects define architectural characteristics at the quantum level rather than the system level. This provides important information when analyzing a new problem domain.

## The Impact of Scoping

Architects can use the scope of architectural characteristics to help determine appropriate service boundaries illustrated overall in the decision tree in Figure 7-1 and further detailed in the steps.

Figure 7-1. A decision tree that uses architectural characteristics scope to help determine architectural style

### Scoping and Architectural Style

Determining the quantum boundaries of the problem domain helps in choosing an architectural style: is a monolithic architecture or distributed architecture most suitable? Consider the first part of the decision chart shown in Figure 7-2.

Figure 7-2. Choosing an appropriate architectural style based on architectural characteristics

As we discussed in Chapter 4, architects must analyze architectural characteristics and the domain to determine the most appropriate architectural style. Part of this analysis concerns whether the solution needs multiple groups of architectural characteristics. In step one in Figure 7-2, the architect determines if the system can succeed with a single set of architectural characteristics, or if more than one group is required (see “Kata: Going Green” on page 103 for an example).

If the architect determines that a single set of architectural characteristics will suffice, they can choose a monolithic architecture, reducing the number of subsequent choices. If they choose a distributed architecture, the next step is to determine its quantum boundaries, as shown in Figure 7-3.

Figure 7-3. In distributed architectures, architects must choose the appropriate quantum boundaries

We provide some guidelines for determining granularity in Chapter 18. The next step is choosing a persistence mechanism, which concerns both architecture families, shown in Figure 7-4.

Figure 7-4. Both architecture styles generally require persistence of some kind

For monolithic architectures, a single monolithic database is generally suitable. The architecture and database are developed and deployed together, in lockstep. This completes the process—the architect can move on to choosing the most appropriate monolithic style.

Distributed architectures, on the other hand, can use a single database (common in event-driven architectures) or partition the data along the lines of the service granularity (as in microservices architectures). One further step remains: determining what type of communication to use between quanta, synchronous or asynchronous. (We discuss this question in detail in Chapter 15.) Remember that, in some systems, choosing synchronous communication can change the quantum boundaries established through static coupling; the two types of coupling interact frequently.

### Kata: Going Green

Let’s try analyzing a problem by using architecture quantum as a scope for architectural characteristics. The problem, called Going Green, is illustrated in Figure 7-5.

You are working with Going Green (GG), a business that recycles and resells old electronics, such as cell phones. Its system uses both public kiosks and a website, all running the same system. A user can upload their device’s model number and condition, and GG will bid for it. If the user accepts the bid, they can deposit it in the kiosk or, if they go through the website, GG will send them a box to mail it in. Upon receiving the device, GG assesses it and sends the user their payment. GG then estimates the value of the device and either recycles or resells it. Its system also produces reports and other analytics.

Figure 7-5. Requirements overview for Going Green

As you perform your architectural characteristics analysis, you notice three distinct clusters forming, as shown in Figure 7-6.

Figure 7-6. The GG architectural characteristics analysis yields three clusters of capabilities

The public-facing parts of the application need scalability, availability, and agility; the back-office functions need security, data integrity, and auditability; and the assessment part needs maintainability, deployability, and testability (which make up the composite architectural characteristic of agility). Why does the assessment part need a separate set of architectural characteristics? This is a good example of how business drivers intersect with architectural concerns. GG’s business model relies on reselling the highest-value used electronics, and new models come out in a constant stream. The faster they can update their device assessments, the more they can get newer (and therefore more valuable) devices to resell.

Could you design a system that meets all these criteria: scalability, availability, security, data integrity, auditability, maintainability, deployability, and testability? It’s possible…but it would be difficult. These architectural characteristics often counteract one another: for instance, achieving fast deployability is more difficult when you’re also prioritizing back-office concerns like auditability. And the UI requires a vastly different level of scalability than other parts of the system.

Instead of trying to do it all, you can use the clusters of architectural characteristics as your guide to separating quanta. In Figure 7-7, the dotted lines illustrate each architectural quantum. Using characteristic scope as a guide for service granularity is a good first step in determining the most beneficial set of trade-offs. (We explore this topic further in Chapter 18.)

Figure 7-7. This GG architecture captures each set of architectural characteristics as an architectural boundary

## Scoping and the Cloud

Cloud-based resources complicate the picture, because they encapsulate so many of the operational architectural characteristics of a system. Architects must consider at least two scenarios when using cloud-based resources for all or part of an application, depending on the deployment model:

- Using the cloud to host containers: Many development teams use the cloud as an alternate operations center, running (and orchestrating) containers for servers. In such situations, architects must consider the architectural characteristics of the containers and the constraints introduced by the orchestration tool (for example, Kubernetes).

- Using cloud-provider resources as system components: Another flavor of a cloud-based system pieces applications together using the cloud provider’s building blocks, such as triggered functions, databases, and so on. In this case, architects must look at the capabilities the provider advertises (and hopefully maintains) for insights on how to build suitable capabilities for that particular context.

Many of the capabilities we know today as cloud providers’ configuration settings, such as elasticity, were hard-won by the previous generation of architects working on physical systems. Their major concerns have become easier—but we have our own modern set of trade-offs, such as provider availability and heightened security concerns. The details of software architecture change a lot, but the job of analyzing trade-offs remains constant.
