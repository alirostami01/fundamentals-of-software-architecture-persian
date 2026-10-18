# Chapter 15: Event-Driven Architecture Style (continued)

## Style Specifics (continued)

### Asynchronous Capabilities

The event-driven architectural style has a unique characteristic in that it relies primarily on asynchronous communication for both fire-and-forget processing (no response required) and request/reply processing (when a response is required from the event consumer, see “Request-Reply Processing” on page 256). Asynchronous communication can be a powerful technique for increasing a system’s overall responsiveness.

In Figure 15-6, a user is posting a product review on a website. The comment service, in this example. takes 3,000 milliseconds to validate and post that comment. The comment has to go through several parsing engines: a check for unacceptable words, a check to make sure that the comment is not indicating abusive text (such as “slow thinker” or “unable to think clearly”), and finally a context check to make sure the comment is about the product (and not, say, just a political rant).

The top path in Figure 15-6 posts the comment using a synchronous RESTful call. That means 50 ms in network latency for the service to receive the post, 3,000 ms to validate and post the comment, and 50 ms of latency to tell the user that the comment was posted. The total time to post a comment, from the user’s point of view, is thus 3,100 milliseconds. Now look at the bottom path, which uses asynchronous messaging. Here, the user’s total posting time is only 25 ms, as opposed to 3,100 ms. It still takes the system 25 ms to receive the comment and 3,000 ms to post it, for a total of 3,025 ms, but from the end user’s perspective, only 25 ms go by before the system responds that it has accepted the comment (although it hasn’t actually been posted yet).

Figure 15-6. Synchronous versus asynchronous communication

The difference in response time between 3,100 ms and 25 ms is staggering. There is, however, one caveat: on the synchronous top path, the end user gets a guarantee that their comment has been posted. However, on the asynchronous bottom path, the post is only acknowledged, with a future promise that eventually it will be posted. What would happen if the user’s comment includes profanity and the system rejects it? There is no way for it to notify the end user—or is there? If the user must register with the website to post a comment, the system could send them a message indicating a problem with the comment and suggesting how to repair it.

This example illustrates the difference between responsiveness (the time it takes to get information back to the user) and performance (the time it takes to insert the comment into the database). When the user doesn’t need any information back (other than an acknowledgment or a thank-you message), why make them wait? Responsiveness is all about notifying the user that the action has been accepted and will be processed momentarily, whereas performance is about making the end-to-end process faster. On the asynchronous bottom path, the architect did nothing to optimize the way the comment service processes the comment (that’s addressing responsiveness). If the architect took the time to optimize the comment service, perhaps by executing all of the text and grammar parsing engines in parallel, leveraging caching and other similar techniques but still using synchronous communication, they would be instead addressing overall performance.

That was a simple example. What about a more complicated one? This time, let’s look at an online stock trade, where a user is purchasing some stock asynchronously. What if there is no way to notify the user of an error?

While asynchronous communication significantly improves responsiveness, error handling is a big issue. The difficulty of addressing error conditions adds to the complexity of this architecture style. “Error Handling” on page 249 illustrates a pattern of reactive architecture for addressing error-handling challenges: the Workflow Event pattern.

In addition to its responsiveness, asynchronous communication also provides a good level of dynamic decoupling and avoids an antipattern, Dynamic Quantum Entanglement, which occurs when two architectural quanta communicate through synchronous communication. (You probably recall from Chapter 7 that an architectural quantum is a part of the system that can be deployed independently from the rest of the system and is bound through synchronous dynamic coupling, and that architectural characteristics live at the quantum level.) Because these two architectural quanta are now dependent on each other, they essentially become entangled. The dependency turns them into a single architectural quantum. Asynchronous communication can help detangle architectural quanta because it removes that dynamic dependency.

To illustrate this important point, consider the two systems in Figure 15-7. In this example, the `Portfolio Management` system creates a trade order to buy some stock. It synchronously sends this trade order to the `Trade Order` system, which will perform compliance checks and create the trade order. Because the communication between these two systems is synchronous, the `Portfolio Management` system must necessarily block and wait for a trade confirmation number from the `Trade Order` system. These two systems have become entangled and now form a single architectural quantum.

Figure 15-7. These systems form a single architectural quantum due to synchronous dynamic coupling

The significance of this entanglement is that the architectural characteristics now live between these two systems. If the `Trade Order` system becomes unavailable or unresponsive, the `Portfolio Management` system cannot submit the trade order. This also degrades responsiveness: if the `Trade Order` system is slow, the `Portfolio Management` system will be slow too. Scalability also suffers because if the `Portfolio Management` system needs to scale, so does the `Trade Order` system. If it doesn’t or can’t, then the `Portfolio Management` system can’t scale as needed.

An architect can detangle these architectural quanta by replacing the synchronous call with an asynchronous call between the two systems, as illustrated in Figure 15-8.

Figure 15-8. These systems form separate architectural quanta due to their asynchronous dynamic coupling

By using asynchronous communication, the `Portfolio Management` system can send the trade order through a queue or some other asynchronous means, so it doesn’t have to wait for the `Trade Order` system to create the trade order. Once the `Trade Order` system performs its compliance checks and creates the trade order, it can send the confirmation number to the `Portfolio Management` system through a separate, asynchronous channel. Removing this dependency from the two systems’ dynamic coupling allows them to form two separate architectural quanta. If the `Trade Order` system is unavailable or unresponsive, the `Portfolio Management` system can still issue trade orders, knowing that at some point they will be created and confirmation numbers sent back.

### Broadcast Capabilities

Another of EDA’s unique characteristics is its ability to broadcast events without knowing what other processing units (if any) are receiving those events or what processing they will perform in response. As Figure 15-9 shows, this dynamically decouples the event processors from each other.

Figure 15-9. Broadcasting events to other event processors

Broadcast capabilities are an essential part of many patterns, including eventual consistency and complex event processing (CEP). For example, prices for instruments traded on the stock market change frequently. Every time a new ticker price (the current price of a particular stock) is published, many event processors might respond to the new price (such as trade analytics, or buying or selling the stock). However, the event processor that publishes the latest price simply broadcasts it, with no knowledge of how that information will be used. This is known as semantic decoupling in that one event processor has no knowledge of (or dependency on) the actions of other event processors.
