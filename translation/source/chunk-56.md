# Chapter 15: Event-Driven Architecture Style (continued)

## Style Specifics (continued)

### Mediated Event-Driven Architecture

So far in this chapter we’ve focused on choreographed EDA, where event processors trigger events through broadcast capabilities, and multiple event processors respond to the event. However, there may be times when an architect wants more control over the processing of an event. In this case, the architect can use an orchestrated form of EDA known as the mediator topology.

The mediator topology addresses some of the shortcomings of the standard choreographed EDA topology we’ve described so far in this chapter. It’s centered on an event mediator, which manages and controls the workflow for initiating events that require coordination between multiple event processors. The architecture components that make up the mediator topology are: an initiating event, an event queue, an event mediator, event channels, and event processors.

Importantly, the mediated topology typically uses messages rather than events (see “Events Versus Messages” on page 232). They are generally commands (such as `ship_order`) rather than events that have happened (such as `order_shipped`).

Like in the choreographed topology, the initiating event is what starts the whole process. However, in the mediator topology (Figure 15-25), an event mediator accepts the initiating event. It only knows the steps involved in processing the event, so it generates corresponding derived messages and sends them to dedicated message channels (usually queues) in a point-to-point fashion. Event processors then listen to the dedicated event channels, process messages, and (usually) respond to the mediator when they have completed their work. Event processors within the mediator topology do not advertise what they’ve done to the rest of the system through additional derived messages.

In most implementations of the mediator topology, there are multiple mediators, each usually associated with a particular domain or grouping of events. This avoids having a single point of failure, which can be an issue with this topology, and increases overall throughput and performance. For example, a customer mediator might handle all customer-related events (such as new customer registrations and profile updates), while an order mediator handles order-related activities (such as adding an item to a shopping cart and checking out).

How architects choose to implement the event mediator usually depends on the nature and complexity of the messages the event mediator is processing. For example, for events requiring simple error handling and orchestration, mediators such as Apache Camel, Mule ESB, or Spring Integration will usually suffice. Message flows and message routes within these types of mediators are typically custom written in programming code (such as Java or C#) to control the event-processing workflow.

However, if the event workflow requires lots of conditional processing and multiple dynamic paths with complex error handling directives, then a mediator such as Apache ODE or the Oracle BPEL Process Manager would be a more appropriate choice. These mediators are based on the Business Process Execution Language (BPEL), an XML-like structure that describes the steps involved in processing an event. BPEL artifacts also contain structured elements used for error handling, redirection, multicasting, and so on. BPEL is a powerful but relatively complex language to learn, so architects usually create mediators using the GUI tools in BPEL’s engine suite.

Figure 15-25. Mediator topology

BPEL is good for complex, dynamic workflows, but it does not work well for event workflows with long-running transactions that involve human intervention throughout the event process. For example, suppose a trade is being placed through a `place_trade` initiating event. The event mediator accepts this event, but during the processing, finds that manual approval is required because the trade is over a certain number of shares. The event mediator now has to stop the event processing, notify a senior trader to get the manual approval, and wait for that approval. In these cases, a Business Process Management (BPM) engine, such as jBPM, would be more appropriate than using an event mediator.

Before choosing what kind of event mediator to implement, it’s important to know the types of events it will process. For complex, long-running events involving human interaction, Apache Camel would be extremely difficult to use and maintain. By the same token, using a BPM engine for simple event flows would waste months of effort on something Apache Camel could accomplish in a matter of days.

Of course, it’s rare to have all events fit neatly into one class of complexity. We recommend classifying events as simple, hard, or complex, and sending every event through a simple mediator, such as Apache Camel or Mule. The simple mediator can handle the event itself or forward it to another, more complex event mediator based on that complexity classification. This mediator delegation model, illustrated in Figure 15-26, ensures that all types of events are handled by the type of mediator that will process them most effectively.

Figure 15-26. Delegating the event to the appropriate type of event mediator

Notice in Figure 15-26 that the `Simple Event Mediator` generates and sends a derived message when the event workflow is simple enough to be handled entirely by the simple mediator. However, when the initiating event is classified as hard or complex, the `Simple Event Mediator` forwards the original initiating event to the corresponding mediators (BPEL or BPM). The `Simple Event Mediator`, having intercepted the original event, may still be responsible for knowing when that event is complete, or it could simply delegate the entire workflow (including client notification) to the other mediators.
