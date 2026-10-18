# Chapter 15: Event-Driven Architecture Style (continued)

## Data Topologies (continued)

### Domain Database Topology

Another possible database topology within EDA is the domain database topology, which groups event processors into various domains, each owning its own database (Figure 15-35).

Figure 15-35. The domain database topology uses a separate database for each domain

The main advantages of the domain database topology over the monolithic database topology, which flow from being domain partitioned, are better fault tolerance, scalability, and change control. In the example shown in Figure 15-35, if the order-processing domain database (the one associated with the `Order Fulfillment` and `Order Shipping` event processors) crashes or becomes unavailable due to maintenance, the order placement domain is still fully operational and can continue to accept orders. The event channel containing the `payment applied` derived event acts as a backpressure point, queuing events until the order-processing database becomes available. The same is true with scalability and change control; each domain database only has to worry about scaling based on its domain’s specific event processors, and only those domain-scoped event processors need to change if the database structure changes.

However, consider the two pieces of information needed by the `Order Placement` event processor: the number of books currently on hand and the shipping options. With the domain database topology, the `Order Placement` event processor can simply query its domain database to get the book inventory, similar to how it retrieved this information with the monolithic database topology. However, it must make a synchronous call to the `Order Shipping` event processor to retrieve the shipping options, thus synchronously coupling these services (see Figure 15-36).

Figure 15-36. Data needed by the Order Placement event processor may require synchronous communication to an event processor in another domain

Architects should try to avoid synchronous coupling in a highly dynamic, decoupled architecture like EDA. Synchronous calls can take a toll on fault tolerance and scalability, negating many of the benefits of using this topology. Always check that the domains remain fairly independent from each other, and minimize synchronous interservice calls as much as possible. If too much synchronous communication between event processors is required, reevaluate the domain boundaries, combine the domains into a single one, or move to a monolithic database topology.

### Dedicated Data Topology

Another viable option within EDA is the dedicated database topology, commonly referred to in the microservices world as the database-per-service pattern. With this database topology, each event processor owns its own dedicated database in a tightly formed bounded context, similar to microservices (see “Data Topologies” on page 348 in Chapter 18). This topology is illustrated in Figure 15-37.

Figure 15-37. The dedicated database topology of EDA uses a separate database for each event processor

Not surprisingly, the dedicated database topology has the highest levels of fault tolerance, scalability, and change control out of all the available topologies. If an event processor or database goes down, the outage is isolated to just that event processor; all other event processors function normally. Databases only need to scale based on the single event processor within its bounded context, making this topology the most scalable of the three discussed in this section. Finally, changes to the database structure only impact the event processor attached to that database.

On the negative side, depending on the database technology stack, this can be a very expensive option. Perhaps the biggest disadvantage, however, is synchronous dynamic coupling between event processors. To illustrate this disadvantage, look again at the two pieces of information the `Order Placement` event processor needs for its processing: book inventory and shipping options. In this topology, the `Order Placement` event processor would need to make synchronous calls to both the `Inventory` event processor and the `Order Shipment` event processor to get the information it needs, forming tight synchronous coupling points throughout the architecture (as shown in Figure 15-38). As with the domain database topology, identify all data-related requirements in each event processor before selecting this database topology option.

Figure 15-38. Data needed by the `Order Placement` event processor may require synchronous communication to other event processors

The dedicated database topology is a good choice when event processors are mostly self-contained, only needing the data within its own bounded context and corresponding database. If event processors are communicating too much (see “Governance” on page 276), the architect should consider moving to the domain or even the monolithic database topology to improve overall performance and scalability. However, if the specific situation involves frequent structural changes to the database, that might warrant a trade-off between these operational characteristics to minimize the number of event processors affected.

## Cloud Considerations

Event-driven architectures work well with cloud-based environments and implementations, primarily due to their highly decoupled nature. EDA can easily leverage the asynchronous services provided by cloud vendors, and the elastic nature of cloud infrastructure and cloud-based services matches its shape. Essentially, cloud-based environments are a good match for EDA.

## Common Risks

One of the main risks associated with EDA is that its nondeterministic event processing can cause side effects: for instance, event processors unexpectedly triggering derived events or not responding to an event when they should. Event workflows can get very complex in an event-driven architecture, and many times it’s difficult to know exactly what will happen when an event is triggered.

Another big risk is having too much static coupling (and hence brittleness) within the event-driven architecture. Although EDA is highly dynamically coupled, event payload contracts (see “Event Payload” on page 240) can also introduce tight static coupling. Changing a contract can be a daunting task, since architects don’t always know which event processors are responding to a particular event. When an event payload contract does change, it may negatively impact several other event processors, adding to the overall brittleness of this architectural style. Key-based event payloads help mitigate this risk, but the risks of this practice include issues with scalability and performance and the possibility of anemic events (see “Event Payload” on page 240).

Watch out for too much synchronous communication between event processors as well. Event-driven architecture gets its superpowers from its highly dynamically decoupled event processors. However, if event processors keep needing to communicate synchronously, it’s a good sign that EDA is not the most appropriate architectural style.

Finally, overall state management is both a risk and a challenge in EDA. It’s good to know when the initiating event has been completely processed, but that can be very hard to determine due to EDA’s nondeterministic, asynchronous parallel event processing. Occasionally an architect can identify the final processing endpoint and have the event processor that accepted the initiating event subscribe to that “ending” event, but in most cases this is hard to determine. As a result, it’s difficult to know when an initiating event has been fully processed, or even its current state.
