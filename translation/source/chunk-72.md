# Chapter 18: Microservices Architecture (continued)

## Style Specifics (continued)

### Communication

In microservices, architects and developers struggle to find the appropriate service granularity, which affects both data isolation and communication. Finding the correct communication style helps teams keep services decoupled, yet still coordinate them in useful ways.

Fundamentally, architects must decide on synchronous or asynchronous communication. Synchronous communication requires the sender to wait for a response from the receiver. Microservices architectures typically utilize protocol-aware heterogeneous interoperability when communicating to and between services. Let’s break that complicated term down into its parts to better understand what it means and why it’s important:

**Protocol-aware:** Because microservices don’t include a centralized integration hub, each service needs to know how to call other services. Thus, architects commonly standardize on how particular services call each other: a certain level of REST, message queues, and so on. That means that services must know (or discover) which protocol to use to call other services.

**Heterogeneous:** Because microservices is a distributed architecture, each service could be written in a different technology stack. Heterogeneous indicates that microservices fully supports polyglot environments, in which different services use different platforms.

**Interoperability:** Describes services calling one another. While architects in microservices try to discourage transactional method calls, services commonly call other services via the network to collaborate and exchange information.

> **Enforced Heterogeneity**
>
> A well-known architect who was a pioneer in the microservices style was the chief architect at a startup, building personal-information management software for mobile devices. Because mobile is such a fast-moving problem domain, the architect wanted to ensure that none of the development teams would accidentally create coupling points that could hinder their ability to move independently. It turned out that the teams had a wide mix of technical skills, so the architect mandated a new rule: each development team had to use a different technology stack. If one team was using Java and the other was using .NET, it would be impossible for them to share classes accidentally!
>
> This approach is the polar opposite of most enterprise governance policies, which insist on standardizing on a single technology stack. In the microservices world, the goal isn’t to create the most complex ecosystem possible, but to choose the correct scale of technology for the narrow scope of the problem. Not every service needs an industrial-strength relational database, and forcing one on a small team is more likely to slow them down than to benefit them. This concept leverages the highly decoupled nature of microservices.

For asynchronous communication, architects often use events and messages, similar to what we described in event-driven architecture in Chapter 15.

### Choreography and Orchestration

Choreography utilizes the same communication style as EDA. Choreographed architectures have no central coordinator, respecting the bounded context philosophy and making it natural to implement decoupled events between services.

In choreography, each service calls other services as needed, without a central mediator. For example, consider the scenario shown in Figure 18-7. The user requests details about another user’s wish list. Because the `CustomerWishList` service doesn’t contain all the information it needs, it makes a call to `CustomerDemographics` to retrieve the missing information, then returns the result to the user.

> **Figure 18-7.** Using choreography in microservices to manage coordination

Because microservices architectures don’t include a global mediator like other service-oriented architectures, if an architect needs to coordinate across several services, they can create their own localized mediator (usually called an orchestration service).

In Figure 18-8, the developers create a service whose sole responsibility is coordinating calls. For instance, the user calls the `ReportCustomerInformation` mediator, which calls all necessary other services to get the requested information.

> **Figure 18-8.** Using orchestration in microservices

The First Law of Software Architecture suggests that neither of these solutions is perfect—each has trade-offs. Choreography preserves the highly decoupled philosophy of microservices to reap its maximum benefits. However, it also makes common problems like error handling and coordination more complex.

Consider an example with a more complex workflow. In Figure 18-9, the first service called must coordinate across a wide variety of other services, basically acting as a mediator in addition to its other domain responsibilities. This is called the Front Controller pattern, where a nominally choreographed service becomes a more complex mediator for some problem. The downside to this pattern is that the service taking on multiple roles adds complexity.

> **Figure 18-9.** Using choreography for a complex business process

Alternatively, architects may choose to use orchestration for complex business processes, illustrated in Figure 18-10. The architect builds a mediator service to coordinate the business workflow creating coupling between these services, but also allowing the architect to focus coordination into a single service, leaving the others less affected. Domain workflows are often inherently coupled, so the architect’s job entails finding a way to represent that coupling that best supports the goals of both the domain and the architecture.

> **Figure 18-10.** Using orchestration for a complex business process

### Transactions and Sagas

Architects aspire to extreme decoupling in microservices, but often encounter the problem of how to coordinate transactions across services. Because microservices encourages the same level of decoupling in the databases as in the architecture, the atomicity that was trivial in monolithic applications becomes a problem in distributed ones.

Building transactions across service boundaries violates the core decoupling principle of microservices, and also creates the worst kind of dynamic connascence, Connascence of Values (see “Connascence” on page 49). The best advice we can offer architects who want to do transactions across services is: don’t! Fix the service granularity instead. If you’re finding that you need to wire your microservices architecture together with transactions, that’s a sign that your design is too granular.

> **Tip:** Try to avoid transactions that span multiple microservices—fix the service granularity instead!

In keeping with the “it depends” rule, there are always exceptions. For example, a situation could arise where two different services need vastly different architecture characteristics that require distinct service boundaries, yet still need transactional coordination. The architect in that case could, after considering the trade-offs carefully, leverage certain transactional patterns to orchestrate transactions.

Distributed transactions in microservices are usually handled by what is known as a Saga pattern. In literature, a saga is an epic story describing a long sequence of events that leads to some sort of heroic conclusion, hence the name of this transactional pattern.

In Figure 18-11, a service acts as a mediator across multiple service calls to coordinate a transaction. The mediator calls each part of the transaction, records success or failure, and coordinates the results. If everything goes as planned, all the values in the services and their contained databases update synchronously. If there’s an error condition and one part of the transaction fails, the mediator must ensure that no part of the transaction succeeds. Consider the situation shown in Figure 18-12.

> **Figure 18-11.** The Saga pattern in microservices architecture

If the first part of the transaction succeeds but the second part fails, the mediator must send a request to all other participating services of the transaction that were successful and tell them to undo the previous request. This style of transactional coordination is called a compensating transaction framework. Developers usually implement this pattern by having each request from the mediator enter a `pending` state until the mediator indicates overall success. However, juggling asynchronous requests can become complex, especially if new requests appear that are contingent on pending transactional state. Regardless of the protocol used, compensating transactions create a lot of coordination traffic at the network level.

> **Figure 18-12.** Saga pattern compensating transactions for error conditions

> **Tip:** It’s sometimes necessary for a few transactions to cross services; however, if it’s the dominant feature of the architecture, then microservices is likely not the right choice!

Managing transactions in microservices is complicated, and you can dive much deeper. We’ve identified eight different transactional Saga patterns to solve a variety of scenarios, which you can find in Chapter 12 of our book *Software Architecture: The Hard Parts* (O’Reilly, 2021), coauthored with Pramod Sadalage and Zhamak Dehghani.
