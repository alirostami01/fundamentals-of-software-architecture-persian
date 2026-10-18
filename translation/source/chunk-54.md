# Chapter 15: Event-Driven Architecture Style (continued)

## Style Specifics (continued)

### The Swarm of Gnats Antipattern

Related to anemic events is an antipattern known as the Swarm of Gnats. You probably know gnats as very small, annoying flying insects that buzz around your head, bothering you enough to send you back indoors on a beautiful sunny day. Whereas anemic events are concerned about the granularity of an event payload, the Swarm of Gnats antipattern is concerned about the granularity of the triggered events themselves and with how many derived events are triggered from an event processor. If an architect triggers too many derived events from a single event processor, they risk getting caught up in the Swarm of Gnats antipattern.

Consider the credit card payment example shown in Figure 15-14, where a customer places an order and their credit card is charged to pay for it. When the credit card is charged, the `Payment` event processor triggers a `payment applied` event, and (fortunately) the `Fraud Detection` event processor listens for it. This event processor analyzes each charge to determine whether it’s legitimate or fraudulent. Whatever the outcome, the `Fraud Detection` event processor triggers a `fraud_checked` derived event with the outcome of the fraud check contained in its event payload.

Figure 15-14. An example of an event that is too coarse-grained

Three event processors are interested in the outcome of the credit card fraud check:

- If fraud is detected, the `Credit Card Locking` event processor locks the customer’s credit card to prevent further charges.

- The `Customer Notify` event processor notifies the customer of possible fraud.

- If fraud is not detected, the `Purchase Profile` event processor updates its algorithms.

Unfortunately, when a single `fraud_checked` derived event is triggered, all of these event processors must respond to the event, check the payload for the outcome, and decide whether to take action. Because this derived event is too coarse-grained, all of the event processors must perform additional processing: analyzing the payload of the single derived event to decide whether to take action. If no fraud has been detected, this is a waste of bandwidth and processing power, since only the `Purchase Profile` event processor needed to take any action.

A much more efficient approach would be to trigger two separate derived events (`fraud_detected` and `no_fraud_detected`), as shown in Figure 15-15. Here, the derived events triggered by the `Fraud Detection` event processor provide context outside of the event payload, allowing each event processor to decide whether to respond without having to analyze the event’s internal payload.

Figure 15-15. Triggering multiple events allows for more efficient processing and decision making

In this example, triggering multiple derived events for each outcome allows for better event flow, less churn, and more efficient processing. However, triggering too many derived events results in the Swarm of Gnats antipattern.

The scenario shown in Figure 15-16 illustrates how this antipattern can occur. A customer has recently moved and needs to change their user profile on the website to update their credit card’s bill-to address, ship-to address (where orders will be shipped), and phone number from their old landline to their cell phone. When the customer hits the Submit button for these profile changes, the `Customer Profile` event processor receives the update request, updates the database, and triggers a separate event for each update that contains the necessary information to do any further processing.

Figure 15-16. Triggering too many fine-grained derived events is known as the Swarm of Gnats antipattern

The problem with triggering too many fine-grained, detailed events is that it can saturate and overwhelm the system with derived events all related to the same thing: the customer updated their user profile. This antipattern also tends to proliferate numerous small derived events from other event processors, eventually making it hard for anyone to understand the system’s overall event flows.

To avoid this antipattern, the architect could bundle each individual profile update into a single `profile_updated` derived event for the complete action, containing the before and after data of all updated fields. This more efficient approach is illustrated in Figure 15-17.

Figure 15-17. Combining individual state changes into a single derived event avoids the Swarm of Gnats antipattern

Determining the right level of granularity for derived events can be quite challenging. We recommend focusing on the outcome of the processing or state change to avoid the Swarm of Gnats antipattern and help simplify event flows.

### Error Handling

The Workflow Event pattern of reactive architecture is one way of addressing error handling in an asynchronous workflow. This pattern addresses both resiliency and responsiveness, since it allows the system to handle asynchronous errors without affecting its responsiveness.

The Workflow Event pattern leverages delegation, containment, and repair by using a workflow delegate, as illustrated in Figure 15-18. In this pattern, an event processor asynchronously passes data through a message channel to the event consumer. If the event consumer experiences an error while processing the data, it immediately delegates that error to the `Workflow Processor` service and moves on to the next message in the event queue. This way, the next message is immediately processed, so overall responsiveness remains the same. If the event consumer were to spend time trying to figure out the error, then it would not be processing the next message in the queue—delaying not only the next message, but all other messages waiting in the processing queue.

When the `Workflow Processor` service receives an error, it tries to figure out what’s wrong with the message. Perhaps there’s a static, deterministic error? It could analyze the message using some machine-learning or AI algorithms to look for some anomaly in the data. Either way, the workflow processor programmatically (that is, without human intervention) makes changes to the original data to try to repair it, then sends it back to the originating queue. The event consumer sees this updated message as a new one and tries to process it again, hopefully this time with more success.

Of course, the workflow processor can’t always determine what’s wrong with the message. In these cases, it sends the message off to another queue, which is then received by a dashboard on the desktop of a knowledgeable person. This person looks at the message, applies manual fixes, and then resubmits it to the original queue (usually through a reply-to message header variable).

Figure 15-18. The Workflow Event pattern of reactive architecture

Suppose a trading advisor in one part of the country accepts trade orders (instructions on what stock to buy and for how many shares) on behalf of a large trading firm in another part of the country. The advisor batches up the trade orders in what is usually called a basket and asynchronously sends them to a broker across the country, who then purchases the stock. To simplify the example, suppose the contract for the trade instructions must adhere to the following:

```text
ACCOUNT(String),SIDE(String),SYMBOL(String),SHARES(Long)
```

Suppose the large trading firm receives the following basket of Apple (AAPL) trade orders from the trading advisor:

```text
12654A87FR4,BUY,AAPL,1254
87R54E3068U,BUY,AAPL,3122
6R4NB7609JJ,BUY,AAPL,5433
2WE35HF6DHF,BUY,AAPL,8756 SHARES
764980974R2,BUY,AAPL,1211
1533G658HD8,BUY,AAPL,2654
```

The fourth trade instruction (`2WE35HF6DHF,BUY,AAPL,8756 SHARES`) has the word `SHARES` after the number of shares for the trade. When the primary firm processes these asynchronous trade orders without any error handling capabilities, the following error occurs within the `TradePlacement` service:

```text
Exception in thread "main" java.lang.NumberFormatException:
        For input string: "8756 SHARES"
        at java.lang.NumberFormatException.forInputString
        (NumberFormatException.java:65)
        at java.lang.Long.parseLong(Long.java:589)
        at java.lang.Long.<init>(Long.java:965)
        at trading.TradePlacement.execute(TradePlacement.java:23)
        at trading.TradePlacement.main(TradePlacement.java:29)
```

When this exception occurs, because this was an asynchronous request, there is no user to synchronously respond to and fix the error. The `TradePlacement` service can’t do anything, except possibly log the error condition.

Applying the Workflow Event pattern can fix this error programmatically. Because the primary firm has no control over the trading advisor or the trade-order data it sends, it must react to fix the error itself (see Figure 15-19). When the same error occurs (`2WE35HF6DHF,BUY,AAPL,8756 SHARES`), the `TradePlacement` service immediately delegates the error via asynchronous messaging to the `Trade Placement Error` service for error handling, passing it along with the error information about the exception:

```text
Trade Placed: 12654A87FR4,BUY,AAPL,1254
Trade Placed: 87R54E3068U,BUY,AAPL,3122
Trade Placed: 6R4NB7609JJ,BUY,AAPL,5433
Error Placing Trade: "2WE35HF6DHF,BUY,AAPL,8756 SHARES"
Sending to trade error processor <-- delegate the error fixing and move on
Trade Placed: 764980974R2,BUY,AAPL,1211
...
```

The `Trade Placement Error` service, acting as the workflow delegate, receives the error and inspects the exception. Seeing that the issue is with the word `SHARES` in the Number of Shares field, the `Trade Placement Error` service strips off the word `SHARES` and resubmits the trade for reprocessing:

```text
Received Trade Order Error: 2WE35HF6DHF,BUY,AAPL,8756 SHARES
Trade fixed: 2WE35HF6DHF,BUY,AAPL,8756
Resubmitting Trade For Re-Processing
```

The `TradePlacement` service can now process the fixed trade successfully:

```text
...
trade placed: 1533G658HD8,BUY,AAPL,2654
trade placed: 2WE35HF6DHF,BUY,AAPL,8756 <-- this was the original trade in error
```

Figure 15-19. Error handling with the Workflow Event pattern

One consequence of using the Workflow Event pattern is that messages that are sent to a workflow processor and then resubmitted are processed out of sequence. In our trading example, the order of the messages matters, because all trades within a given account must be processed in order (for example, a `SELL` for IBM must occur before a `BUY` for AAPL within the same brokerage account). It would be complex, although not impossible, to maintain the message order within a given context (in this case, the brokerage account number). One way to address this is for the `TradePlacement` service to queue and store the brokerage account number of the erroneous trade. Any trade with that same brokerage account number would be stored in a temporary queue for later processing (in first-in, first-out, or FIFO, order). Once the erroneous trade is fixed and processed, the `TradePlacement` service de-queues the remaining trades for that same account and processes them in order.
