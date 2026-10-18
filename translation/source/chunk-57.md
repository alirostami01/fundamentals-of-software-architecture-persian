# Chapter 15: Event-Driven Architecture Style (continued)

## Style Specifics (continued)

### Mediated Event-Driven Architecture (continued)

To examine how the mediator topology works, let’s consider the same retail order entry system that we described in the section on choreographed topology, but this time using the mediator topology. The mediator knows the steps required to process this particular event. The mediator component’s internal event flow is illustrated in Figure 15-27.

Figure 15-27. Mediator steps for placing an order

In keeping with the prior example, the same initiating event (`place order`) is sent to the event mediator via a dedicated queue for processing. The `Customer` mediator picks up this initiating event and begins generating derived messages, based on the flow in Figure 15-27. The events shown in steps 2, 3, and 4 are all done concurrently and serially, between steps. In other words, step 3 (fulfill order) must be completed and acknowledged before the customer can be notified that the order is ready to be shipped in step 4 (ship order).

Once it receives the initiating event, the `Customer` mediator generates a `create order` derived message, which it sends to the `order placement` queue (see Figure 15-28). The `Order Placement` event processor accepts the message and validates and creates the order, and sends the mediator an acknowledgment and the order ID in return. At this point, the mediator might send that order ID to the customer, indicating that the order was placed, or it might have to continue until all the steps are complete (this would depend on specific business rules about order placement).

Figure 15-28. Step 1 of the mediator example

Now that step 1 is complete, the mediator moves to step 2 (see Figure 15-29) and generates three derived messages at the same time: `email customer`, `apply payment`, and `adjust inventory`. It sends all three to their respective queues. All three event processors receive these messages, perform their respective tasks, and notify the mediator that their processing is complete. The mediator must wait until it receives acknowledgment from all three parallel processes before moving on to step 3. If an error occurs in one of the parallel event processors, the mediator can take corrective action (more about that later in this section).

Figure 15-29. Step 2 of the mediator example

Once the mediator gets a successful acknowledgment from all of the event processors in step 2, it can move to step 3 to fulfill the order (see Figure 15-30). Once again, both of these messages (`fulfill order` and `order stock`) can occur simultaneously. The `Order Fulfillment` and `Warehouse` event processors accept the messages, perform their work, and return an acknowledgment to the mediator.

Figure 15-30. Step 3 of the mediator example

The mediator moves on to step 4 (see Figure 15-31) to ship the order. This step generates two derived messages: a `ship order` message, and another `email customer` message with specific information about what to do (notify the customer that the order is ready to be shipped).

Figure 15-31. Step 4 of the mediator example

Finally, the mediator moves to step 5 (see Figure 15-32) and generates another contextual `email customer` message to notify the customer that the order has been shipped. This ends the workflow. The mediator marks the initiating event flow complete and removes all state associated with the initiating event.

Figure 15-32. Step 5 of the mediator example

In this topology, unlike the choreographed topology, the mediator component has knowledge of and control over the workflow. It can maintain event state and manage error handling, recoverability, and restart capabilities. For example, suppose in our example that the payment was not applied because the credit card has expired. When the mediator receives this error condition, it knows that the order cannot be fulfilled (step 3) until payment is applied, so it stops the workflow and records the state of the request in its own persistent datastore. Once payment is eventually applied, the workflow can be restarted from where it left off (in this case, the beginning of step 3).

While the mediator topology addresses the issues associated with the choreographed topology, it has its own disadvantages. First of all, it is very difficult to declaratively model the dynamic processing that occurs within a complex event flow. As a result, many workflows within the mediator topology only handle general processing, but use a hybrid model that combines the mediator and choreographed topologies to address the dynamic nature of complex event processing, such as out-of-stock conditions or other nontypical errors. Furthermore, although the event processors can easily scale in the same manner as the choreographed topology, the mediator must scale as well—something that occasionally produces a bottleneck in the overall event-processing flow. Event processors are not as highly decoupled in the mediator topology as they are in the choreographed topology. Finally, performance is not as good in this topology, because the mediator controls event processing.

The trade-off between the choreographed and mediator topologies essentially comes down to weighing workflow control and error handling capability against high performance and scalability. Although performance and scalability are still good within the mediator topology, they are not as high as with the choreographed topology.

## Data Topologies

With all this talk of events and event processing, it’s easy to forget about the data side of EDA. Database topologies are a unique and interesting aspect of this architectural style. It offers many options, each with significant trade-offs that can have a big impact on the overall architecture. To describe the different database topologies within EDA, we’ll use a simplified version of the example we showed in Figure 15-3 (see Figure 15-33).

When a customer places an order, the `Order Placement` event processor creates the order, then triggers an `order placed` event, to which both the `Payment` and `Inventory` event processors respond. Once the payment has been applied, the `Order Fulfillment` event processor helps the order packer prepare the order, then triggers an `order fulfilled` event. The `Shipping` event processor responds to the `order fulfilled` event by shipping the order to the customer, completing the processing and fulfilling the customer’s request.

Figure 15-33. A simplified example of the example order-entry system using EDA

One complication of EDA is that the `Order Placement` event processor needs to know two pieces of information: how many items are currently in stock, and what shipping options are available based on the customer’s location. How it gets this information will depend on the type of database topology the architecture uses. Let’s look at each database topology option to see its significant trade-offs.

### Monolithic Database Topology

The first, and perhaps most common, database topology used within EDA is the single monolithic database topology. With this topology, all data is available to all event processors through a central database.

The main benefit of the monolithic database topology is that any event processor can query the data it needs directly from the database, without having to synchronously communicate with any other event processors. This is a significant advantage, since event-driven architectures rely on highly decoupled event processors communicating through asynchronous communications. In Figure 15-34, the `Order Placement` event processor can simply query the central monolithic database to retrieve the number of items currently in stock and the customer’s shipping options.

Figure 15-34. With the monolithic database topology, data is available directly from the database

While the monolithic database topology supports decoupling and limits communication between event processors, it carries with it some messy disadvantages, the first of which is fault tolerance. If the central monolithic database crashes or goes down for maintenance, all event processors become unavailable.

The second issue is scalability. Because event-driven architectures use asynchronous communication, each event processor can scale independently of the others. The event channel essentially acts as a backpressure point so that individual event processors can scale as necessary, regardless of whether other event processors scale as well. However, if all the event processors are simultaneously querying and writing to the same database, the database must scale to meet these demands. Many databases are unable to achieve this at high concurrency loads.

The third issue is change control. When the structure of the database changes (such as dropping a column or attribute), multiple event processors are affected and must coordinate, even for a single database change.

Finally, the monolithic database topology necessarily creates a single architectural quantum, due to the shared monolithic database.
