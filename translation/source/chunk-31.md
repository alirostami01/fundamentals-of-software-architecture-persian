# Chapter 9: Foundations (continued)

## Monolithic Versus Distributed Architectures (continued)

### Fallacy #1: The Network Is Reliable

Figure 9-7. The network is not reliable

Developers and architects alike assume that the network is reliable, but it is not. While networks have become more reliable over time, the fact of the matter is that networks still remain generally unreliable. This is significant for all distributed architecture styles, because they rely on the network for communicating to, from, and between services. As illustrated in Figure 9-7, `Service B` may be totally healthy, but `Service A` cannot reach it due to a network problem. Even worse, `Service A` might request that `Service B` process some data, but receive no response because of a network issue. This is why things like timeouts and circuit breakers exist between services. The more a system relies on the network (as microservices architectures notably do), the more potential it has to become unreliable.

### Fallacy #2: Latency Is Zero

Figure 9-8. Latency is not zero

As Figure 9-8 shows, when a local call is made to another component via a method or function call, the time to access that component (`t_local`) is measured in nanoseconds or microseconds. However, when that same call is made through a remote access protocol (such as REST, messaging, or RPC), the time (`t_remote`) is measured in milliseconds and thus will always be greater than `t_local`. Latency, in any distributed architecture, is not zero—yet most architects ignore this fallacy, insisting that they have fast networks. Ask yourself: do you know what the average round-trip latency is for a RESTful call in your production environment? Is it 60 milliseconds? Is it 500 milliseconds?

When considering using any distributed architecture, particularly microservices, architects must know this latency average. It is the only way of determining whether a distributed architecture is feasible, due to the fine-grained nature of the services and the amount of communication between them.

For example, say we assume an average of 100 ms of latency per request. Chaining service calls together to perform a particular business function adds 1,000 ms to the request! Knowing the average latency is important, but knowing the 95th to 99th percentile latency is even more important. While the system’s average latency might be only 60 ms (which is good), the 95th percentile might be 400 ms! It’s usually this “long tail” latency that will kill performance in a distributed architecture. In most cases, a network administrator can provide latency values (see “Fallacy #6: There Is Only One Administrator” on page 148).

### Fallacy #3: Bandwidth Is Infinite

Figure 9-9. Bandwidth is not infinite

Bandwidth is usually not a concern in monolithic architectures, because once a business request goes into a monolith, little or no bandwidth is required to process it. However, as shown in Figure 9-9, once a system is broken apart into smaller deployment units (services) in a distributed architecture, such as microservices, communication to and between these services uses significant bandwidth. This slows the network, impacting latency (fallacy #2) and reliability (fallacy #1).

To illustrate the importance of this fallacy, consider the two services shown in Figure 9-9. Let’s say `Service A` manages the wish list items for the website, and `Service B` manages the customer profiles. Whenever a request for a wish list comes into `Service A`, `Service A` needs the customer name for the response contract for the wish list. To get the name, it must make an interservice call to `Service B`. `Service B` returns 45 attributes, totaling 500 KB, to `Service A`, which only needs the name (200 bytes). This may not sound significant, but requests for the wish list items happen about 2,000 times a second. This means that `Service A` is calling `Service B` 2,000 times a second. At 500 KB for each request, each interservice call takes 1 GBps of bandwidth!

This form of coupling, called stamp coupling, consumes significant amounts of bandwidth in distributed architectures. If `Service B` were to pass back only the 200 bytes of data that `Service A` needs, it would use only 400 Kbps in total.

Stamp coupling can be resolved by:

- Creating private RESTful API endpoints

- Using field selectors in contracts

- Using GraphQL to decouple contracts

- Using value-driven contracts with consumer-driven contracts

- Using internal messaging endpoints

Regardless of the technique used, the best way to address this fallacy in a distributed architecture is to ensure that services or systems transmit only the necessary data.

### Fallacy #4: The Network Is Secure

Figure 9-10. The network is not secure

Most architects and developers get so comfortable using virtual private networks (VPNs), trusted networks, and firewalls that they tend to forget about this fallacy of distributed computing—but the network is not secure. As shown in Figure 9-10, each and every endpoint to each distributed deployment unit must be secured against unknown or bad requests. The surface area for threats and attacks increases by magnitudes when moving from a monolithic to a distributed architecture, making security much more challenging. Securing every endpoint, even in interservice communication, is another reason performance tends to be slower in synchronous, highly distributed architecture styles, such as microservices and service-based architectures.

### Fallacy #5: The Topology Never Changes

Figure 9-11. The network topology always changes

Fallacy #5, as shown in Figure 9-11, refers to the overall network topology, including all of its routers, hubs, switches, firewalls, networks, and appliances. Architects assume that the topology is fixed and never changes. Of course it changes. It changes all the time. What is the significance of this fallacy?

Suppose you come into work on a Monday morning and everyone is running around like crazy, because services keep timing out in production. You work with the teams, frantically trying to figure out why this is happening. No new services were deployed over the weekend. What could it be? After several hours, you discover that a supposedly “minor” network upgrade at two o’clock that morning invalidated all of the system’s latency assumptions, triggering timeouts and circuit breakers.

Architects must be in constant communication with operations and network administrators about what is changing and when so that they can make adjustments to avoid such surprises. This may seem obvious and easy, but it is neither. As a matter of fact, this fallacy leads directly to the next fallacy.

### Fallacy #6: There Is Only One Administrator

Figure 9-12. There are many network administrators, not just one

Architects fall into this fallacy all the time: assuming they only need to collaborate and communicate with one administrator. As Figure 9-12 shows, there are dozens of network administrators in a typical large company. With whom should the architect talk about latency or topology changes? This fallacy points to the complexity of distributed architecture and the amount of coordination that must happen to get everything working correctly. A monolithic application, with its single deployment unit, doesn’t require this level of communication and collaboration.

### Fallacy #7: Transport Cost Is Zero

Figure 9-13. Remote access costs money

Many software architects confuse this fallacy, shown in Figure 9-13, with fallacy #2 (latency is zero). Transport cost here refers not to latency, but to the actual monetary cost of making a “simple RESTful call.” Architects incorrectly assume that the necessary and sufficient infrastructure is already in place for making a simple RESTful call or breaking apart a monolithic application. It is usually not. Distributed architectures cost significantly more than monolithic architectures, primarily due to increased needs for hardware, servers, gateways, firewalls, new subnets, proxies, and so on.

We encourage architects embarking on a distributed architecture to analyze their current server and network topology with regard to capacity, bandwidth, latency, and security zones, to avoid getting surprised by this fallacy.

### Fallacy #8: The Network Is Homogeneous

Figure 9-14. The network is not homogeneous

Most architects and developers assume that a network is homogeneous, as shown in Figure 9-14—that it’s made up of network hardware from only one vendor. Nothing could be further from the truth. Most companies’ infrastructures have multiple network-hardware vendors.

So what? The significance of this fallacy is that not all of those heterogeneous hardware vendors play together well. Does Juniper Networks hardware integrate seamlessly with Cisco Systems hardware? Most of it works, and networking standards have evolved over the years, making this less of an issue. However, not all situations, loads, and circumstances have been fully tested, so network packets do occasionally get lost. This in turn affects network reliability and assumptions and assertions about latency and bandwidth. In other words, this fallacy ties back into all of the other fallacies, forming an endless loop of confusion and frustration when dealing with networks (which is inescapable when using distributed architectures).
