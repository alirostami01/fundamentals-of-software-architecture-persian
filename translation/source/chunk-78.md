# Chapter 19: Choosing the Appropriate Architecture Style (continued)

## Distributed Case Study: Going, Going, Gone

The Going, Going, Gone (GGG) kata from Chapter 8 presents some more interesting architectural challenges. Based on the component analysis in “Case Study: Going, Going, Gone—Discovering Components” on page 125, we know that different parts of this architecture need different characteristics. For example, the need for availability and scalability will differ between roles like auctioneer and bidder.

The system requirements for GGG also explicitly state some ambitious expectations for scale, elasticity, performance, and other tricky operational architecture characteristics. The architecture pattern should allow for a high degree of customization at a fine-grained level. Of the candidate distributed architectures, low-level event-driven architecture and microservices are the two that best match most of the required architecture characteristics. Of the two, microservices is better at supporting variation among operational architecture characteristics. (Purely event-driven architectures typically separate pieces not by their architecture characteristics, but by whether they use orchestrated or choreographed communication.)

Achieving the stated performance goal would be a challenge in microservices, but the best way to address any weak point of an architecture is by designing to accommodate it. For example, while microservices by its nature offers a high degree of scalability, it often develops specific performance issues caused by too much orchestration or too aggressive data separation, among other issues.

> **Figure 19-5.** A microservices implementation of Going, Going, Gone

In Figure 19-5, each identified component becomes a service in the architecture, matching components with service granularity. GGG has three distinct user interfaces:

**Bidder:** The numerous bidders for the online auction.

**Auctioneer:** One per auction.

**Streamer:** A service responsible for streaming video and bids to the bidders. This is a read-only stream, which allows for optimizations that wouldn’t be available if updates were necessary.

The following services appear in this design for the GGG architecture:

- **`Bid Capture`:** Captures online bidder entries and asynchronously sends them to `Bid Tracker`. This service needs no persistence because it acts as a conduit for the online bids.

- **`Bid Streamer`:** Streams the bids back to online participants in a high-performance, read-only stream.

- **`Bid Tracker`:** Tracks bids from both `Auctioneer Capture` and `Bid Capture`, unifying these two information streams and ordering the bids in as close to real time as possible. Both inbound connections to this service are asynchronous, allowing the developers to use message queues as buffers to handle very different message flow rates.

- **`Auctioneer Capture`:** Captures bids for the auctioneer. The analysis in “Case Study: Going, Going, Gone—Discovering Components” on page 125 showed that the architecture characteristics of `Bid Capture` and `Auctioneer Capture` are quite different, leading us to separate them.

- **`Auction Session`:** Manages the workflow of individual auctions.

- **`Payment`:** Third-party payment provider that handles payment information after `Auction Session` completes the auction.

- **`Video Capture`:** Captures the video stream of the live auction.

- **`Video Streamer`:** Streams the auction video to online bidders.

We were careful to identify both synchronous and asynchronous communication styles in this architecture. The choice of asynchronous communication was primarily to accommodate operational architecture characteristics varying between services. For example, if the `Payment` service can only process a new payment every 500 ms, and a large number of auctions end at the same time, using synchronous communication between the services would cause timeouts and other reliability headaches. Message queues add reliability to a critical but fragile part of the architecture.

> **Figure 19-6.** The quantum boundaries for GGG

In the final analysis, this design resolved to five quanta, identified in Figure 19-6, roughly corresponding to the services: `Payment`, `Auctioneer`, `Bidder`, `Bidder Streams`, and `Bid Tracker`. Multiple instances are indicated in the diagram by stacks of containers. Using quantum analysis at the component-design stage made it easier to identify service, data, and communication boundaries.

Note that this isn’t the “correct” design for GGG, and it’s certainly not the only one. We don’t even suggest that it’s the best possible design—but it seems to have the *least worst* set of trade-offs. Choosing microservices, then using events and messages intelligently, allows this architecture to get the most out of a generic architecture pattern while still building a foundation for future development and expansion.
