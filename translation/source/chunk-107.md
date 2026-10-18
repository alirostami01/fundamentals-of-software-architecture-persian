<!-- Source chunk 107 | PDF pages 513-517 | Chapter 27: Synchronous vs Asynchronous Messaging, First Corollary, sidebox, Second Corollary | words: 1322 -->
# Chapter 27: The Laws of Software Architecture, Revisited (continued)

## First Law: Everything in Software Architecture Is a Trade-Off (continued)

### Synchronous Versus Asynchronous Messaging

Consider the following trade-off analysis: your team is building a distributed architecture to send trade information to both the `Notification` and `Analytics` services, and you’re trying to decide whether to use a *queue* or *topic* to implement this behavior.

The first option is a queue, or a point-to-point communication protocol. As you learned in Chapter 2, the publisher knows who is receiving the message. To reach multiple consumers, the publisher needs to send a message to one queue for each consumer. If the `Trading` service wants to use queues to tell the `Analytics` service and the `Reporting` service about trades, the implementation will appear as in Figure 27-2.

Figure 27-2. Using a queue to pass trade information to `Notification` and `Analytics`

In Figure 27-2, the `Trading` service issues a message to each consumer via a queue. Each consumer has its own queue, and the sender posts a message to each.

Figure 27-3. Using a topic to pass trade information to `Notification` and `Analytics`

The alternative topology uses a *topic* instead, which implements a broadcast rather than point-to-point communication. In Figure 27-3, the `Trading` service posts a single message to a topic. Each consumer subscribes to the topic, and they all receive a notification when a message appears. In this case, the publisher of the message doesn’t know (or care) who the consumers are—in fact, the team can add new consumers anytime without changing the other consumers or the producer.

Both options are viable, so how should you decide? By performing a trade-off analysis, of course.

With queues, every service that the `Trading` service needs to notify will need a separate queue. This is nice if the `Notification` service and the `Analytics` service need different information, since you can send different messages to each queue. The `Trading` service is aware of every system to which it communicates, which makes it harder for another (potentially rogue) service to “listen in.” That’s especially beneficial if security is high on the priority list. Because each queue is independent, you can monitor them separately and even scale them independently if needed. The `Trading` service is tightly coupled to its consumers—it knows exactly how many there are. However, if you need to send messages to the `Compliance` service, you’ll have to rework the `Trading` service to start sending messages to a third queue.

Table 27-2 summarizes the trade-offs of using queues for this project.

Table 27-2. Trade-offs when using a queue

| Advantage | Disadvantage |
|---|---|
| Supports heterogeneous messages for different consumers | Higher degree of coupling |
| Allows independent monitoring of queue depth | Trading service must connect to multiple queues |
| More secure | Requires additional infrastructure |
| Less extensible (must add queues for more consumers) | Good support for extensibility and evolvability |

Let’s do the same exercise for topics. One advantage is clear: topics are extremely extensible. Any new consumer interested in, for example, compliance, can subscribe to that topic without touching any of the existing behavior. However, this advantage has downsides: each consumer must consume the same message from the topic, which can lead to *stamp coupling* (shown in Figure 9-9). And, because every consumer can read the entire message, there are security concerns: *should* everyone be able to read the entire message?

With this perspective in hand, you can make your trade-off table, shown in Table 27-3.

Table 27-3. Trade-offs when using a topic

| Advantage | Disadvantage |
|---|---|
| Low coupling | Homogeneous message for each consumer |
| Trading service generates just one message | Can’t monitor or scale individual consumers |
| More extensible/evolvable | Less secure |
|  | Less scalability options |

Now that you’ve done the trade-off analysis, you need to return to the organizational goals for this solution and see which option is the better fit. If security is more important, you should probably select queues. If the organization is growing rapidly and has other services interested in trades, then extensibility might be a priority, which would lead you to use topics.

### First Corollary: Missing Trade-Offs

Our first law has two corollaries. The first is:

> If you think you’ve discovered something that *isn’t* a trade-off, more likely you just haven’t *identified* the trade-off…yet.
>
> —Corollary 1

The essence of a software architecture decision is trade-off analysis, but what happens when you encounter a decision that seems to not have any trade-offs? Our advice: keep looking!

Consider code reuse. Surely this is a purely beneficial practice, right? The more code the organization can reuse, the less code it must write, saving time and duplication.

Two factors dictate how effective code reuse will be. Architects often discover the first but miss the second. The first factor is *abstraction*: if you can abstract this code and use it from multiple call points, it’s a good candidate for reuse. The second factor is *low volatility*. When a team reuses a module of code that’s always changing, this creates churn in the entire system. Every time the shared code changes, all callers of that code must coordinate around that change. Even if it isn’t a breaking change, the team must still verify that the change hasn’t broken anything. When architectures reuse code inappropriately, teams end up chasing breaking changes all over the architecture. This was one of the key lessons architects as a field learned from the orchestration-driven SOA architecture style (covered in Chapter 17), one of the underlying philosophies of which was to try to reuse as much code as possible. From a practical standpoint, teams working in those architectures were swimming through quicksand: every change had the potential to send unpredictable side effects rippling out through the system.

That’s the hidden trade-off: reusing code effectively requires good abstraction *and* low volatility. This is why the most successful reuse targets in architecture are “plumbing”: technology frameworks, libraries, platforms, and so on. The portion of most applications that changes the fastest is the domain (the motivation for writing the software in the first place), so domain concepts are terrible candidates for reuse. (Notice that this underlies the DDD principle of bounded context—no bounded contexts can reuse any of the implementation details of another bounded context.)

> **Why We Can’t Have Nice Things—Trade-Offs!**
>
> As professional consultants, our clients often make requests like the following: “We like the idea of microservices and distributed architectures that feature high degrees of decoupling because they allow high degrees of agility and fast deployment. However, we also want a high degree of institutional reuse so that teams aren’t constantly rewriting code.”
>
> We have to be the bearers of bad news here: you cannot have both these things, because the way a system implements reuse is via coupling. No organization can have both decoupling *and* a high degree of reuse. The two things are fundamentally incompatible. This is a prime example of how organizations can misunderstand key trade-offs.

### Second Corollary: You Can’t Do It Just Once

It would be nice if an architect could just perform one trade-off analysis—just think *really hard* and decide once and for all to use choreography for all workflows. But there are two problems with trade-off analysis. First, there are often dozens or even hundreds of variables (technical and otherwise) that contribute to the decision: complexity, team experience, budget, team topology, schedule pressure…the list is endless. Subtle differences in those variables can push a particular analysis in one direction or another, making this an ongoing exercise. It’s dangerous for architects to make sweeping, semipermanent decisions based on assumptions that might not be valid for future applications of this solution.

Think of this corollary as job security for architects. We have to keep doing trade-off analysis over and over, even for seemingly similar situations. This reinforces the idea that the real job is trade-off analysis, not making permanent, perfect decisions.
