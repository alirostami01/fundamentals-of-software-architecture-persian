# Chapter 15: Event-Driven Architecture Style (continued)

## Governance

A majority of the governance associated with EDA is nonstructural and requires observability in the form of logs as part of an overall governance mesh. Depending on the infrastructure and environment, some governance metrics associated with EDA may need to be manually collected.

The two main areas of governance in this style are static coupling through contract management, and dynamic coupling through synchronous calls. Both of these aspects are considered structural decay in EDA, so it’s important to keep an eye on them.

From a static coupling perspective, architects can set up governance around things like the rate of change of event payload contracts and overall stamp coupling. Changing contracts can be very risky in EDA because of its decoupled nature. Changing an event contract, particularly one with no associated schema, can break a downstream event processor. This is a particular risk in EDA because it’s so difficult to test nondeterministic end-to-end event flows.

Stamp coupling (see “Event Payload” on page 240) can be governed by continually recording and observing which fields in an event contract are not being used by event processors responding to the event. Observing these unused fields can help trim down contract size, reduce bandwidth, and help manage stamp coupling and corresponding unnecessary changes to event processors.

From a dynamic coupling standpoint, architects can write automated fitness functions to observe and track synchronous communication between event processors through logs and other observable means (such as source code annotations or use of standard synchronous custom-identifier libraries). Any synchronous communication in an event-driven architecture should be tracked and discussed to ensure that it is necessary, particularly if using a domain or dedicated database topology.

## Team Topology Considerations

EDA is largely considered a technically partitioned architecture due to the many artifacts that make up each domain: multiple event processors, event channels, message brokers, and possibly databases, depending on the database topology. Nevertheless, it can work well when teams are aligned within domain areas (such as cross-functional teams with specialization). That said, specific types of team topologies (see “Team Topologies and Architecture” on page 151) might find EDA challenging.

Here are some considerations regarding the alignment between these specific team topologies and EDA:

**Stream-aligned teams:** Depending on the size of the system, stream-aligned teams might find themselves struggling to implement domain-based changes, due to the decoupled nature of event processors. Because domains and subdomains in EDA are typically implemented with multiple event processors and derived events, stream-aligned teams might find it a challenge to understand all of these moving parts. For example, adding a step to the order-placement workflow might require changing multiple event processors, as well as restructuring how (and when) the existing derived events are triggered. The larger and more complex the event-driven architecture, the less effective stream-aligned teams will be.

**Enabling teams:** Because of the integration required between event processors based on derived events and their contracts, enabling teams don’t work well in event-driven architectures. Experimentation and efficiency by enabling teams within a stream can disrupt a stream-aligned team’s understanding and management of an overall event flow, and usually requires too much coordination between stream-aligned teams and enabling teams.

**Complicated-subsystem teams:** Complicated-subsystem teams work well with EDA due to its decoupled, asynchronous nature. Complex processing can be easily isolated through separate event processors, and the complicated-subsystem team can focus on those, leaving less complicated processing to the stream-aligned teams. Because event processors are highly dynamically decoupled, stream-aligned teams only need to coordinate with complicated-subsystem teams for static event-payload contracts and derived events.

**Platform teams:** In EDA, developers can leverage the benefits of the platform-teams topology by utilizing common tools, services, APIs, and tasks, primarily due to EDA’s technical partitioning. This is especially true if teams treat the infrastructure-related parts of EDA (such as the message brokers, event hubs, event buses, and other event-channel artifacts) as platform related.

## Style Characteristics

A one-star rating in the characteristics ratings table in Figure 15-39 means the specific architecture characteristic isn’t well supported in the architecture, whereas a five-star rating means it’s one of that style’s strongest features. Definitions for each characteristic identified in the scorecard can be found in Chapter 4.

Event-driven architecture is primarily a technically partitioned architecture, in that any particular domain is spread across multiple event processors and tied together through brokers, contracts (event payload), and topics. Changes to a particular domain usually impact multiple event processors and other messaging artifacts, so EDA is not generally considered domain partitioned.

Figure 15-39. EDA characteristics ratings

The number of quanta within EDA can vary from one to many, depending on the database interactions within each event processor and whether the system uses request-reply processing. Even though communication in an EDA relies on asynchronous calls, if multiple event processors share a single database instance, they would all be contained within the same architectural quantum. The same is true for request-reply processing: even though the communication between the event processors is still asynchronous, if a response is needed right away from the event consumer, it ties those event processors together synchronously, forming a single quantum.

For example, imagine that one event processor sends a request to another event processor to place an order. The first event processor must wait for an order ID from the other event processor to continue. If the second event processor (the one that places the order and generates an order ID) is down, the first event processor cannot continue. This means they are part of the same architecture quantum and share the same architectural characteristics, even though they are both sending and receiving asynchronous messages.

Event-driven architecture rates very high (4 to 5 stars) for performance, scalability, and fault tolerance, its primary strengths. Its high performance is achieved by combining asynchronous communications with highly parallel processing. High scalability is realized through the programmatic load balancing of event processors (also called competing consumers and consumer groups). As the request load increases, additional event processors can be programmatically added to handle the additional requests. The reason we only gave it four stars (rather than five) is because of the database (see Chapter 16, on space-based architectures, for an example of a five-star rating for these characteristics). EDA achieves fault tolerance through its decoupled, asynchronous event processors, which provide eventual consistency and processing of event workflows. If other downstream processors are unavailable, as long as the user interface or an event processor making a request does not need an immediate response, the system can process the event at a later time.

EDA rates relatively low on overall simplicity and testability, mostly due to its nondeterministic and dynamic event flows. In request-based models, deterministic flows are relatively easy to test because their paths and outcomes are generally known. Such is not the case with the event-driven model. Sometimes architects just don’t know how event processors will react to dynamic events or what messages they might produce. These are known as nondeterministic workflows. These systems’ “event tree diagrams” can be extremely complex, generating hundreds or even thousands of scenarios, making it very difficult to govern and test.

Finally, EDAs are highly evolutionary, hence the five-star rating. Adding new features through existing or new event processors is relatively straightforward. By providing hooks via triggered derived events, the event and its corresponding data are already available for other processing, so no changes are required in the infrastructure or existing event processors to add that new functionality

EDA’s disadvantages include difficulty controlling the overall workflow associated with an initiating event. Event processing is very dynamic due to changing conditions, and it’s difficult to know when the business transaction based on the initiating event has been completed.

Error handling is also a big challenge with EDA. Because there is typically no mediator monitoring or controlling the business transaction (except with the mediator topology), if a failure occurs, other services will be unaware of the crash. The business process based on that initiating event gets stuck and is unable to move without some sort of automated or manual intervention, even as all other processes move along without regard for the error. For example, if the `Payment` event processor in our ordering system crashes and does not complete its assigned task, the `Inventory` event processor still adjusts the inventory, and all other further event processors react as though everything is fine.

Restarting a business transaction (recoverability) is very difficult to do in EDA. Because other actions have been taken asynchronously through the processing of the initiating event, many times it’s simply not feasible to resubmit the initiating event.
