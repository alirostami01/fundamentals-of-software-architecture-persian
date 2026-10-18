# Chapter 8: Component-Based Thinking (continued)

## Component Coupling (continued)

### The Law of Demeter

Most architects are told to strive for loose coupling in system design. Less coupling between components or services makes a system more maintainable, easier to test, and less risky to deploy. It also increases the system’s overall reliability, because changes impact fewer components, allowing fewer opportunities for error.

One technique for creating loosely coupled systems is called the Law of Demeter, otherwise known as the Principle of Least Knowledge. In Greek mythology, the goddess Demeter produced all the grain for the entire world, but she had no idea what people did with it (feeding livestock, making bread, and so on). Demeter was effectively decoupled from the rest of the world.

The Law of Demeter states: a component or service should have limited knowledge of other components or services. While this may sound simplistic and obvious, it’s not. Let us show you what we mean.

Consider the components and their corresponding communications illustrated in Figure 8-14. Upon accepting a customer’s order, the `Order Placement` component must tell the `Inventory Management` component to decrement the inventory. If the stock goes down too low, the `Order Placement` component must do two things: tell the `Supplier Ordering` component to order more stock from the supplier, and tell the `Item Pricing` component to adjust the price based on the limited supply available. Finally, once all this is done, the `Order Placement` component tells the `Email Notification` component to email the customer with the order details.

Figure 8-14. The `Order Placement` component is highly coupled to the rest of the system because it has too much knowledge

Notice that, in this architecture, the `Order Placement` component is highly coupled to the other components. While it doesn’t have the responsibility to perform those actions, it does have the knowledge that these actions need to occur—and more knowledge means tighter coupling.

The idea behind the Law of Demeter is to limit each component’s knowledge about the rest of the system. In Figure 8-14, the `Order Placement` component knows that the inventory must be decremented, more stock may need to be ordered, the item price may need to be adjusted, and an email must be sent to the customer. (That’s a lot of knowledge!) But what if that knowledge could be distributed to other components? If so, then the architect can effectively decouple that component from the rest of the system.

To see how the Law of Demeter can be applied to reduce component coupling, refer to the system in Figure 8-14. If the architect added another component between `Order Placement` and `Inventory Management` to defer that knowledge that inventory must be decremented, the `Order Placement` component would still have the same efferent (outgoing) coupling level. Therefore, that coupling point needs to remain as is.

However, what about the knowledge that, if the supply goes down too low, the system must order more stock and adjust the item price? Both of those pieces of knowledge can be deferred to the `Inventory Management` component, thereby reducing the coupling level of the `Order Placement` component. Figure 8-15 illustrates the resulting architecture after applying the Law of Demeter. Removing the knowledge that certain functions need to happen makes the `Order Placement` component less coupled to the rest of the system.

Figure 8-15. The `Order Placement` component is less coupled to the system when it has less knowledge

The astute reader will observe that, while applying the Law of Demeter reduced the coupling level of the `Order Placement` component, it also increased the coupling level of the `Inventory Management` component. Applying the Law of Demeter does not necessarily reduce the system-wide level of coupling; rather, it usually redistributes that coupling to different parts of the system.

## Case Study: Going, Going, Gone—Discovering Components

If a team has no special constraints and is looking for a good general-purpose component decomposition, the Actor/Actions approach works well as a generic solution.

If the architect applies the Actor/Action approach to Going, Going, Gone (GGG), they’ll find that this system has three main roles: the bidder, the auctioneer, and the system—a frequent participant in this modeling technique for internal actions. The roles interact with the system using the following main actions:

`Bidder`

- View live video stream.
- View live bid stream.
- Place a bid.

`Auctioneer`

- Enter live bids into system.
- Receive online bids.
- Mark item as sold.

`System`

- Start auction.
- Make payment.
- Track bidder activity.

Given these actions, the architect can build a set of starter components for GGG and then iterate on it. One such solution appears in Figure 8-16.

Figure 8-16. Initial set of components for Going, Going, Gone

In Figure 8-16, each role and action maps to a component. The components may need to collaborate to share information. These are the components we identified for this solution:

- `Video Streamer`: Streams a live auction to users.

- `Bid Streamer`: Streams bids to users as they occur. Both `Video Streamer` and `Bid Streamer` offer bidders a read-only view of the auction.

- `Bid Capture`: This component captures bids from the auctioneer and bidders.

- `Bid Tracker`: Tracks bids and acts as the system of record.

- `Auction Session`: Starts an auction. When the bidder wins and the auction for that item ends, this component triggers the payment and resolution steps, including notifying bidders of the next item up for bid.

- `Payment`: A third-party payment processor for credit card payments.

After the initial round of component identification (see Figure 8-6), the architect analyzes the previously identified architecture characteristics to determine if any of them will change the design of the component. For example, the current design features a `Bid Capture` component to capture bids from both bidders and the auctioneer. This makes sense functionally: bids from anyone can be captured and handled the same way. But what previously identified architecture characteristics does bid capture call for? The auctioneer doesn’t need the same level of scalability or elasticity as the bidders, who could potentially number in the thousands.

By the same token, the auctioneer might need certain previously identified architecture characteristics more than other parts of the system do—like reliability (ensuring connections don’t drop) and availability (ensuring the system stays up). For example, while it would be bad for business if a bidder can’t log in to the site or suffers from a dropped connection, it would be disastrous if either of those things were to happen to the auctioneer.

To support the bidders’ and auctioneer’s different levels of need for the same architecture characteristics, the architect decides to split the `Bid Capture` component into two components: `Bid Capture` and `Auctioneer Capture`. The updated design appears in Figure 8-17.

The architect creates a new component for `Auctioneer Capture`. They also update the information links from the `Auctioneer Capture` to both `Bid Streamer` (to show the online bidders the live bids) and `Bid Tracker` (to manage the bid streams). `Bid Tracker` is now the component that will unify two very different information streams: the auctioneer’s single stream of information and the multiple streams from bidders.

Figure 8-17. Revised components of the GGG case study

The design shown in Figure 8-17 is unlikely to be the final design. More requirements must be uncovered: how people will register new accounts, how payment functions will be administered, and so on. However, this design provides a good starting point for iterating further.

This is one possible set of components to solve the GGG problem—but it’s not necessarily the best nor the only one. There are few software systems that can be implemented in only one way. Every design has different sets of trade-offs. As an architect, don’t obsess over finding the “one true design,” because there are many that will suffice. Try to assess the trade-offs between different design decisions as objectively as possible, and choose the one that has the “least worst” set of trade-offs.
