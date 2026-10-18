<!-- Source chunk 07 | PDF pages 52-57 | Chapter 2: Analyzing Trade-Offs (topic vs queue example), Understanding Business Drivers | words: 1224 -->

Analyzing Trade-Offs
Thinking like an architect is about seeing trade-offs in every solution, technical or
otherwise, and analyzing those trade-offs to determine the best solution. The reason
this is one of the critical activities of an architect (and hence part of architectural
thinking) is exemplified through the following quote by Mark (one of your authors):
Architecture is the stuff you can’t Google or ask an LLM about.
—Mark Richards
Everything in architecture is a trade-off, which is why the famous answer to every
architecture question in the universe is “It depends. ” While this answer might be
annoying, it is unfortunately true. Y ou cannot Google the answer or ask an AI engine
or large language model (LLM) whether REST or messaging would be better for your
system or whether microservices is the right architecture style for your new product,
because the answer does depend. It depends on the deployment environment, business drivers, company culture, budgets, time frames, developer skill set, and dozens
of other factors. Everyone’s environment, situation, and problem will be different.
That’s why architecture is so hard. To quote Neal, your other author:
There are no right or wrong answers in architecture—only trade-offs.
—Neal Ford
For example, consider an item auction system ( Figure 2-8 ) where online bidders
bid on items up for auction. The Bid Producer service generates a bid from the
bidder and then sends that bid amount to the Bid Capture, Bid Tracking, and Bid
Analytics services.
Figure 2-8. Auction system example of a trade-off—queues or topics?
For the asynchronous behavior in this system, an architect could use queues in a
point-to-point messaging fashion, or use a topic in a publish-and-subscribe messaging fashion. Which one should they choose? They can’t Google the answer. Architectural thinking requires them to analyze the trade-offs associated with each option and
select the best (or least worst) option given the specific situation.
The two messaging options for the item auction system are shown in Figure 2-9 ,
which illustrates using topics in a publish-and-subscribe messaging model, and Figure 2-10, which depicts using queues in a point-to-point messaging model.
Figure 2-9. Using a topic for communication between services
Figure 2-10. Using queues for communication between services
The clear advantage (and seemingly obvious solution) to this problem in Figure 2-9 is
architectural extensibility. The Bid Producer service only requires a single connection
to a topic. Compare that to the queue solution in Figure 2-10 , where the Bid Pro
ducer needs to connect to three different queues. If a new service called Bid History
were to be added to this system (to provide each bidder with a history of all of their
bids), no changes would be needed to the existing services or infrastructure. The new
Bid History service could simply subscribe to the topic that already contains the bid
information.
However, with the queue option shown in Figure 2-10 , the Bid History service
would require a new queue, and the Bid Producer would need to be modified
to add an additional connection to the new queue. The point here is that using
queues means that adding new bidding functionality requires significant changes to
the services and infrastructure, whereas with the topic approach, no changes to the
existing infrastructure are needed. Also, the Bid Producer is less coupled in the topic
option, where the Bid Producer doesn’t know how the bidding information will be
used or by which services. In the queue option, the Bid Producer knows exactly how
the bidding information will be used (and by whom), and hence is more coupled to
the system.
So far, this trade-off analysis seems to make it clear that the topic approach using the
publish-and-subscribe messaging model is the obvious and best choice. However, to
quote Rich Hickey, the creator of the Clojure programming language:
Programmers know the benefits of everything and the trade-offs of nothing. Architects
need to understand both.
—Rich Hickey
Thinking architecturally means not only looking at the benefits of a given solution,
but also analyzing the associated negatives, or trade-offs. Continuing with the auction
system example, a software architect would analyze the negatives of the topic solution
as well as the positives. In Figure 2-9, you can see that with a topic, anyone can access
bidding data, which introduces a possible issue with data access and data security.
However, in the queue model illustrated in Figure 2-10, the data sent to the queue can
only be accessed by the specific consumer receiving that message. If a rogue service
was to listen in on a queue, the corresponding service would not receive those bids,
and a notification would immediately be sent about the loss of data (and possible
security breach). In other words, it is very easy to wiretap a topic, but not a queue.
In addition to the security issue, the topic solution in Figure 2-9 only supports
homogeneous contracts. All services that receive the bidding data must accept the
same data contract and set of bidding data. In the queue option, each consumer can
have its own contract, specific to the data it needs. For example, suppose the new Bid
History service requires the current asking price along with the bid, but no other
service needs that information. In this case, the contract would need to be modified,
impacting all other services using that data. In the queue model, this would be a
separate channel, and thus a separate contract that does not impact any other service.
Another disadvantage of the topic model is that it does not support monitoring
the number of messages in the topic, so it can’t support autoscaling capabilities.
However, with the queue option, each queue can be monitored individually and programmatic load balancing can be applied to each bidding consumer so that each can
be automatically scaled independently. Note that this trade-off is technology specific:
the Advanced Message Queuing Protocol (AMQP) can support programmatic load
balancing and monitoring because of the separation between an exchange (what the
producer sends to) and a queue (what the consumer listens to).
Given this fuller trade-off analysis, which is the better option?
It depends! Table 2-1 summarizes these trade-offs.
Table 2-1. Trade-offs for topics
Topic advantages Topic disadvantages
Architectural extensibility Data access and data security concerns
Service decoupling No heterogeneous contracts
Monitoring and programmatic scalability
Again, everything in software architecture has trade-offs: advantages and disadvantages. Thinking like an architect means analyzing these trade-offs, then asking questions like: “Which is more important: extensibility or security?” An architect’s choice
will always depend on the business drivers, environment, and a host of other factors.
Understanding Business Drivers
Thinking like an architect also means understanding the business drivers required
for the success of the system and translating those requirements into architecture
characteristics such as scalability, performance, and availability. This is a challenging
task that requires the architect to have some business-domain knowledge and healthy,
collaborative relationships with key business stakeholders. We’ve devoted four chapters in the book to this specific topic: in Chapter 4 , we define various architecture
characteristics. In Chapter 5 , we describe ways to identify and qualify architecture
characteristics. In Chapter 6 , we describe how to measure each characteristic to
ensure the business needs of the system are met. And finally, in Chapter 7 we discuss
the scope of architectural characteristics and how they relate to coupling.
