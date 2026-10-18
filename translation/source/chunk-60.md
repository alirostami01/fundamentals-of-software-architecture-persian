# Chapter 15: Event-Driven Architecture Style (continued)

## Style Characteristics (continued)

### Choosing Between Request-Based and Event-Based Models

The request-based and event-based models are both viable approaches for designing software systems. However, choosing the right model is essential to success. We recommend choosing the request-based model for well-structured, data-driven requests (such as retrieving customer profile data), when the priority is certainty and control over the workflow. We recommend choosing the event-based model for flexible, action-based events that require high levels of responsiveness and scale, with complex and dynamic user processing.

Understanding the event-based model’s trade-offs also helps in determining the best fit. Table 15-2 lists the advantages and disadvantages of the event-based model of EDA.

Table 15-2. Trade-offs of the event-driven model

| Advantages over request-based | Trade-offs |
|---|---|
| Better response to dynamic user content | Only supports eventual consistency |
| Better scalability and elasticity | Less control over processing flow |
| Better agility and change management | Less certainty over outcome of event flow |
| Better adaptability and extensibility | Difficult to test and debug |
| Better responsiveness and performance |  |
| Better real-time decision making |  |
| Better reaction to situational awareness |  |

## Examples and Use Cases

Any business problem focused on responding to things happening in the system (either internal or external) is a good candidate for EDA. The order-entry system example we’ve used throughout this chapter is a good use case for EDA in that it allows for parallel, decoupled processing of an order. Systems that require high levels of responsiveness, performance, scalability, fault tolerance, and elasticity are also great candidates for EDA.

Another good use case to demonstrate the power and effectiveness of EDA is our ongoing Going, Going, Gone auction-system example, where users bid on items put up for auction until a final bid goes uncontested and the bidder wins that item. In these systems, the number of bidders is usually unknown, requiring both scalability and elasticity—particularly if the auction is timed and the bidding comes to a close. These systems also need high levels of responsiveness. Perhaps the best reason that online bidding systems and EDA are a good match, though, is that EDA regards placing a bid not as a request made to the system, but as an event that has happened.

As Figure 15-40 shows, lots of actions take place in the system when a bidder places a bid. These actions can all be asynchronous, done either at the same time or later, as backend processing (such as the `Bidder Tracker` event processor). When a bidder places a bid, the `Bid Capture` event processor receives that initiating event, determines if it’s higher than the prior bid, and triggers a `bid placed` event. The `Auctioneer` event processor responds to that event and updates the website with the item’s new bid price. Simultaneously, the `Bid Streamer` event processor responds to the same event, streaming the bid out to the website bid history or even to the individual bidders (depending on the UI). Finally, the `Bidder Tracker` event processor responds to the event to persist the bidder and their bid for tracking and auditing purposes.

Figure 15-40. An online bidding system example using EDA

Many other event processors are involved in the workflow of this initiating event, and many other derived events are triggered, but this small part of the system demonstrates a good use of the event-driven architectural style, illustrating responsiveness, fault tolerance, scalability, and elasticity.

Event-driven architecture is a very complicated architectural style, but also a very powerful one. Closely analyze the workflows and processing needed for the business problem to determine if dealing with EDA’s complexity is worthwhile given its superpowers. If a majority of the processing needed is request based, consider the microservices architectural style (discussed in Chapter 18) instead.
