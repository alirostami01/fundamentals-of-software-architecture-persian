# Chapter 15: Event-Driven Architecture Style (continued)

## Style Specifics (continued)

### Preventing Data Loss

Architects dealing with asynchronous communications are always concerned with data loss: when an event or message gets dropped or never makes it to its final destination. Fortunately, there are basic out-of-the-box techniques to prevent data loss.

Architects can implement event channels in a variety of ways. Most event-driven architectures use the Advanced Message Queuing Protocol (AMQP) for triggering and responding to events. Examples of AMQP brokers include Amazon SNS (Simple Notification Service), RabbitMQ, Solace, and Azure Event Hubs. With AMQP, events are published to an exchange. The exchange uses the binding rules set by the consuming event processors to forward the event to a queue for each event processor that subscribes to that event. AMQP brokers can also leverage what is known as the Event Forwarding pattern to prevent data loss, a technique we describe in this section.

Another event channel implementation is the Jakarta Messaging API (formerly Java Message Service or JMS), which uses topics rather than the two-step forwarding process queues use. Nevertheless, Jakarta Messaging can still leverage the Event Forwarding pattern to prevent data loss, provided that the event processors responding to an event are configured as durable subscribers. A durable subscriber is one that is guaranteed to receive an event. If the event processor is down or otherwise unavailable, the JMS topic stores the event until the subscribing event processor becomes available.

Another possible event-channel implementation is event streaming using Kafka as an event broker (the software product containing the queues and topics). The techniques for preventing data loss within event streaming are very different from those used for the Event Forwarding pattern described in this section. Refer to the Kafka website for more information about preventing data loss when using this kind of streaming event broker.

Consider a typical scenario in which event processor `A` asynchronously publishes an event to a message broker, which eventually goes to an AMQP queue or JMS topic. Event processor `B` responds to the event and inserts the data from the payload into a database. As illustrated in Figure 15-20, there are three ways data loss can occur in this scenario:

1. While event processor `A` is publishing the event, it crashes before an acknowledgment from the event broker can be sent; alternately, the event broker sends an acknowledgment to event processor `A`, but then crashes before the event is accepted by another event processor.

2. Event processor `B` accepts the event from the queue but crashes before it can process the event.

3. Event processor `B` is unable to persist the message to the database due to a data error.

Each of these areas of data loss can be mitigated through the Event Forwarding pattern.

Figure 15-20. Places where data loss can happen within an event-driven architecture

With the first issue, the event never makes it to the queue or the broker fails before the event is read. To address this, use persistent message queues along with synchronous send. Persisted message queues support guaranteed delivery: when the event broker receives the event, not only does it store the event in memory for fast retrieval, it also persists the event in some sort of physical data store (such as a filesystem or database). If the event broker goes down, the event is physically stored on disk, so it will still be available for processing when the event broker comes back up. Synchronous send does a blocking wait in the event processor, stopping it from triggering the event until the broker acknowledges that it has persisted the event to the database. These two basic techniques prevent data loss between the event producer and the queue, because the event is either still with the event producer or persisted within the queue.

A basic messaging technique called client acknowledge mode can address the second issue, where event processor `B` de-queues the next available event and crashes before it can process the event. By default, when an event is read from a queue, it is immediately removed from that queue (this is called auto acknowledge mode). Client acknowledge mode keeps the event in the queue and attaches the client ID to it so that no other consumers can read or process the event. With this mode, if event processor `B` crashes, the event is still preserved in the queue, preventing message loss.

The third issue, in which event processor `B` is unable to persist the event to the database due to some data error, can be addressed with ACID transactions via a database commit. Once the event processor issues a database commit, the data is guaranteed to be persisted in the database. Last participant support (LPS) removes the event from the persisted queue by acknowledging that all processing has been completed and that the event has been persisted. This guarantees that the event has not been lost in transit from event processor `A` to the database. These techniques are illustrated in Figure 15-21.

Figure 15-21. Preventing data loss within an event-driven architecture

### Request-Reply Processing

So far in this chapter, we’ve dealt with asynchronous requests that don’t need an immediate response from the event consumer. But what about event processors that need information back immediately from another event processor—for example, waiting for some sort of confirmation ID or acknowledgment before triggering an event? This scenario requires synchronous communication to complete the request.

In EDA, synchronous communication is typically accomplished through request-reply messaging (sometimes referred to as pseudosynchronous communications). Each event channel within request-reply messaging consists of two queues: a request queue and a reply queue. The message producer making the initial request for information asynchronously sends data to the request queue, and then returns control to the message producer. The message producer then does additional processing, and eventually waits on the reply queue for the response. The message consumer receives and processes the message, then sends the response to the reply queue. The event producer receives the message with the response data. This basic flow is illustrated in Figure 15-22.

Figure 15-22. Request-reply message processing

There are two primary ways to implement request-reply messaging. The first (and most common) technique is to put a correlation ID (CID) field in the message header of the reply message, usually set to the message ID of the original request message (simply called ID in Figure 15-23). It works like this:

1. The event producer sends a message to the request queue and records the unique message ID (ID 124). Notice that the CID in this case is `null`.

2. The event producer does a blocking wait on the reply queue with a message filter (also called a message selector), where the CID in the message header equals the original message ID (124). There are two messages in the reply queue: ID 855 with CID 120, and ID 856 with CID 12Neither of these messages will be picked up, because neither correlation ID matches what the event consumer is looking for (CID 124).

3. The event consumer receives the message (ID 124) and processes the request.

4. The event consumer creates the reply message containing the response and sets the CID in the message header to the original message ID (124).

5. The event consumer sends the new message ID (857) to the reply queue.

6. The event producer receives the message, because the CID (124) matches the message selector from step 2.

Figure 15-23. Request-reply message processing using a correlation ID

The other way to implement request-reply messaging is to use a temporary queue for the reply queue. A temporary queue is dedicated to a specific request, created when the request is made, and deleted when the request ends. This technique, as illustrated in Figure 15-24, does not require a correlation ID, because the temporary queue is a dedicated queue only known to the event producer for that specific request. The temporary queue technique works as follows:

1. The event producer creates a temporary queue (or one is automatically created, depending on the message broker) and sends a message to the request queue, passing the name of the temporary queue in the reply-to header (or some other agreed-upon custom attribute in the message header).

2. The event producer does a blocking wait on the temporary reply queue. No message selector is needed because any message sent to this queue belongs solely to the event producer that sent the original message.

3. The event consumer receives the message, processes the request, and sends a response message to the reply queue named in the reply-to header.

4. The event processor receives the message and deletes the temporary queue.

Figure 15-24. Request-reply message processing using a temporary queue

While the temporary queue technique is much simpler, the message broker must create a temporary queue for each request and then delete it immediately. This can significantly slow the broker down and can affect overall performance and responsiveness, particularly for large message volumes and high concurrency. For this reason, we usually recommend using the correlation ID technique.
