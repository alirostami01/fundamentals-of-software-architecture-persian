# Chapter 15: Event-Driven Architecture Style (continued)

## Style Specifics

The following sections describe EDA in more detail, including some considerations, patterns, and hybrids of this complex architectural style.

### Events Versus Messages

Event-driven architecture leverages events to pass and process information. But is an event really that different from a message? Turns out, yes, it really is.

An event broadcasts to other event processors that something has already happened: “I just placed an order.” A message, however, is more of a command or query, such as “apply the payment for this order” or “give the shipping options for this order.” This is not a subtle difference. When we talk about event processing, we mean reacting to something that has already happened, whereas a message describes something that needs to be done. In our example, it’s clear that “I just placed an order” is an event because it does not describe what processing needs to occur, as a message would. This illustrates EDA’s decoupled nature.

The second main difference between an event and a message is that an event typically does not require a response from the receiver, whereas a message usually does. This reduces back-and-forth communication between event processors, further decoupling them from one another.

Another major difference between events and messages is that an event is typically broadcast to multiple event processors, whereas a message is almost always directed to one event processor. In our simple order-processing example, several event processors are interested in and respond to the `order created` event, whereas only one event processor responds to the message `apply payment`. Events typically use a publish and subscribe (one-to-many) form of communication, whereas messages typically use a point-to-point (one-to-one) form of communication.

A final difference between events and messages is the physical artifact that represents the communication channel. Events use a topic, stream, or notification service so that multiple event processors can subscribe to the channel and listen for the event. Messaging typically uses a queue or messaging service to guarantee that only one type of event processor will receive that message.

Event-driven architecture mostly uses events (hence its name), but it can use messages on occasion, such as requesting data from another event processor (see “Data Topologies” on page 268 and “Request-Reply Processing” on page 256). Later in this chapter, we’ll show you mediated event-driven architecture (see “Mediated Event-Driven Architecture” on page 258), which uses messages to control the processing order of events.

Can you pick out which of the following choices are events and which are messages?

- “Adventurous Air Flight 6557, turn left, heading 230 degrees.”

- “In other news, a cold front has moved into the area.”

- “OK, class, turn to page 145 in your workbooks.”

- “Hi, everyone! Sorry I’m late for the meeting.”

Let’s look at these one by one:

**“Adventurous Air Flight 6557, turn left, heading 230 degrees.”**

This is a message because it’s a command (something that needs to be done) and because it’s directed toward one target, the pilot, even though several other pilots may hear the message.

**“In other news, a cold front has moved into the area.”**

This is an event: it’s being broadcast to multiple people, it describes something that has already happened, and the news broadcaster is not expecting a reply. (There are, however, some messages that don’t require a reply either.)

**“OK, class, turn to page 145 in your workbooks.”**

This one is a little tricky. Turns out this is a message, even though it’s being broadcast to multiple students. It’s a command to do something, not something that has already happened (which would make it an event). This illustrates an important point about the difference between an event and a message: broadcasting a command (such as turning to page 145 in the workbooks) through a publish-and-subscribe channel doesn’t turn it into an event.

**“Hi, everyone! Sorry I’m late for the meeting.”**

This is an event, because this person being late for the meeting has already happened. It’s also being broadcast to multiple people, and no response is expected.

### Derived Events

Derived events are a critical and necessary part of EDA. They are created and triggered by event processors after the initiating event is received. An event processor can trigger more than one derived event, based on its processing.

Consider the derived events triggered when the `Payment` event processor charges a customer’s credit card for a purchase in Figure 15-3. As illustrated in Figure 15-4, charging a credit card involves checking for possible fraud (processed by the `Fraud Detection` event processor) and checking the credit card balance (processed by the `Credit Limit` event processor). EDA can leverage a single event (`creditcard charged`) to do both activities at the same time.

Figure 15-4. Derived events are generated in response to the initiating event

Notice how many derived events this single action generates. In the `Fraud Detection` event processor, it triggers two possible derived events: one if the processor detects fraud, another if no fraud is detected. Both of these derived events are necessary, because different event processors might take further actions depending on the outcome of the fraud detection.

Now look at the derived events from the `Credit Limit` event processor. First, a `limit okay` derived event indicates to the rest of the system there is no risk for this purchase and that the customer has plenty of credit available. As a matter of fact, this particular event could also store in its event payload the amount of credit the customer has left, which might be of interest to downstream event processors. Second, the `limit warning` derived event, warning that the card’s balance is close to the credit limit, might be of interest to other downstream event processors—for instance, the `Notification` event processor, which could notify the customer that they are close to their credit limit. Last, the fatal `limit exceeded` derived event is of interest to several event processors, including `Notification`, `Decline Purchase`, and perhaps a marketing-based `Extend Credit Limit` event processor that automatically extends the customer’s credit limit to allow the purchase.

This illustrates that more than one derived event can be triggered from an event processor. However, be careful not to get trapped in the Swarm of Gnats antipattern, where a processing unit sends out too many fine-grained events (see “The Swarm of Gnats Antipattern” on page 246).

### Triggering Extensible Events

In EDA, it’s usually a good practice for each event processor to advertise what it has done to the rest of the system, regardless of whether or not any other event processor cares about what that action was.

When no event processors care about or respond to the event, we call it an extensible derived event because it nevertheless provides support for architectural extensibility by providing a built-in “hook” in case processing that event requires additional functionality. For example, suppose that, as part of a complex event process (as illustrated in Figure 15-5), the `Notification` event processor generates an email that it sends to a customer, notifying them of a particular action. It then advertises that it has sent the email to the rest of the system through a new derived event (`email sent`). Since no other event processors are currently listening or responding to that event, the message simply disappears (or is ignored, in the case of event streaming). That might seem like a waste of resources, but it’s not. Suppose the business decides to analyze all emails sent to customers. The team can add a new `Email Analyzer` event processor to the overall system with minimal effort and with no changes to other event processors, because the email information is already available via the `email sent` derived event.

Figure 15-5. `Notification` event is sent, but ignored and not used
