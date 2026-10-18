# Chapter 15: Event-Driven Architecture Style (continued)

## Style Specifics (continued)

### Event Payload (continued)

#### Key-based event payload

A key-based event payload is an event payload that contains only a key identifying the context for the event (such as an order ID or customer ID). With key-based event payloads, the event processors responding to the event must query a database to retrieve the information they need to process the event.

When a customer places an order, the `Order Placement` event processor inserts the order into the database and triggers a key-based event called `order_placed`. This event contains a single key value containing the order ID in simple JSON:

```json
{ "order_id": "123" }
```

One of the main disadvantages of key-based event payloads is that each event processor responding to the event must query the database to get the information it needs to process the order. For instance, when the `Payment` event processor responds to the event, it must query the database for the order information it needs to process payment. The `Inventory` event processor also responds simultaneously to the event, so it must also query the database to retrieve the item ID and quantity. This can detract from responsiveness, performance, and scalability, and can overwhelm a database, particularly in a highly parallel and asynchronous architecture such as event-driven architecture. (See “Data Topologies” on page 268 for ways to mitigate this risk.) Key-based event payloads also present a challenge if the required data is not easily accessible (such as if it lies within the bounded context of another event processor). Figure 15-12 illustrates this technique.

Figure 15-12. With key-based event payloads, only the context key is contained in the event

However, using key-based event payloads carries many advantages, some of which may outweigh the performance and scalability issues. The first main advantage is better overall data consistency and data integrity, thanks to having a single system of record. Because data about the event is located in only one place (the database), key-based event payloads can handle changes to the data during event processing much more easily than data-based event payloads.

The second main advantage is that because the contract in key-based event payloads is so simple and rarely changes, architects typically implement it through loose, schema-less JSON or XML. Therefore, key-based event payloads don’t have the same issues with contract change management, versioning, and communication and deprecation strategies that data-based event payloads tend to have.

Another advantage of key-based event payloads: they don’t have the same stamp coupling and bandwidth issues as data-based event payloads. Because there’s no opaque data associated with the event, contracts are simple, small, and utilize minimal bandwidth. Thus, they tend to perform faster, from a network and message broker perspective, than data-based event payloads.

#### Trade-off summary

Choosing between a data-based event payload versus a key-based data payload requires careful trade-off analysis. Remember, it’s not an all-or-nothing proposition: each type of event can use a different payload type. Table 15-1 summarizes the trade-offs associated with data-based and key-based event payloads.

Table 15-1. Data-based versus key-based event payloads

| Criteria | Data-based payloads | Key-based payloads |
|---|---|---|
| Performance and scalability | Good | Bad |
| Contract management | Bad | Good |
| Stamp coupling | Bad | Good |
| Bandwidth utilization | Bad | Good |
| Restricted database access | Good | Bad |
| Overall system fragility | Bad | Good |

Notice that the overall trade-off between these two options boils down to scalability and performance versus contract management and bandwidth utilization. Ask which one is more important for each particular event. Some event processing requires extreme levels of scale and performance, in which case a data-based event payload would be a better choice; some event processing data will undergo frequent change, in which case a key-based event payload might be more appropriate.

As with most things in software architecture, architects’ choices lie on a spectrum, not a simple binary. That’s why it’s important to be careful to avoid triggering what are known as anemic events.

#### Anemic events

An anemic event is a derived event with a payload that doesn’t contain enough information to help the event processor make decisions, and lacks the necessary context for further downstream processing.

Figure 15-13 illustrates an anemic derived event. In this example, a customer has updated some information in their user profile. Once that information is updated in the database, the `Customer Profile` event processor triggers a `profile_updated` event, using a key-based event payload that passes only the customer ID as its key-based data.

The three services responding to this event receive only the customer ID and the context that the customer’s profile was changed. The first service (`Service 1`) has no idea what data was changed in the profile: name, address, some other critical information? Unfortunately, querying the database cannot answer this question, so `Service 1` has no idea how to respond or what action to take. `Service 2` responds to the `profile_updated` event, but going only by the key, does not know if it needs to perform any additional processing. Finally, `Service 3` responds to the same event, but has no idea what the prior values were and therefore cannot perform its processing. All three of these event processors need to respond in some way to the customer updating their profile but can’t, due to a lack of information. These are anemic events: events that do not include additional information to further process the event.

Figure 15-13. An anemic event lacks enough context to process the event

To avoid anemic events such as this one, include the updated customer information as well as the prior values, since most databases typically don’t reflect that information.

This is an example of the spectrum of event payload granularity. On the extreme left side of the spectrum sit key-based event payloads, where only the key is contained within the event. While this has merit when creating or deleting an order, it doesn’t work well when a customer updates an order. On the far right side of the spectrum is the data-based event payload, where all the data is included, whether it’s needed or not. This is where stamp coupling rears its ugly head. The customer-profile-update scenario fits somewhere between these extremes because it provides the right level of information, thus avoiding the anemic derived event problem.
