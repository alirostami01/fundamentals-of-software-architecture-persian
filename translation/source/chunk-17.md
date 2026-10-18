## Kata: Silicon Sandwiches

- Description: A national sandwich shop wants to enable online ordering in addition to its current call-in service.

- Users: Thousands, perhaps one day, millions.

Requirements:

- Allow users to place an order and, if the shop offers delivery service, select pickup or delivery.

- Give pickup customers a time to pick up their order and directions to the shop (which must integrate with several external mapping services that include traffic information).

- For delivery service, dispatch the driver with the order to the user.

- Provide mobile device accessibility.

- Offer national daily promotions and specials.

- Offer local daily promotions and specials.

- Accept payment online, at the shop, or upon delivery.

Additional context:

- Sandwich shops are franchised, each with a different owner.

- The parent company has near-future plans to expand overseas.

- The corporate goal is to hire inexpensive labor to maximize profit.

Given this scenario, how would you derive architectural characteristics? Each part of the requirement might contribute to one or more aspects of the architecture (and many will not). The architect doesn’t design the entire system here—considerable effort must still go into crafting code to solve the domain design (covered in Chapter 8). Instead, look for things that influence or impact the design, particularly structural.

First, separate the candidate architectural characteristics into explicit and implicit characteristics.

### Explicit Characteristics

Explicit architectural characteristics appear in a requirements specification as part of the necessary design. For example, a shopping website may aspire to support a particular number of concurrent users, which domain analysts specify in the requirements. Consider each part of the requirements to see if it contributes to an architectural characteristic. But first, consider domain-level predictions about expected metrics, as represented in the Users section of the kata.

One of the first details that should catch your eye is the number of users: currently thousands, perhaps one day, millions (this is a very ambitious sandwich shop!). Thus, scalability—the ability to handle a large number of concurrent users without serious performance degradation—is one of the top architectural characteristics. Notice that the problem statement didn’t explicitly ask for scalability, but rather expressed that requirement as an expected number of users. Architects must often decode domain language into engineering equivalents.

You’ll also probably need elasticity—the ability to handle bursts of requests. These two characteristics are often lumped together, but they have different constraints. Scalability looks like the graph shown in Figure 5-1.

> Figure 5-1. Scalability is a measure of the increase of users over time

Elasticity, on the other hand, measures bursts of traffic, as shown in Figure 5-2.

> Figure 5-2. Elastic systems must withstand bursts of users

Some systems are scalable but not elastic. For example, a hotel reservation system’s number of users, absent special sales or events, is probably predictably seasonal. In contrast, consider a concert-ticket booking system. As new tickets go on sale, fervent fans will flood the site, requiring high degrees of elasticity. Often, elastic systems also need scalability: the ability to handle bursts and high numbers of concurrent users.

Elasticity does not appear in the Silicon Sandwiches requirements, but you should still identify it as an important consideration. Requirements sometimes state architectural characteristics outright, but others lurk inside the problem domain. Is a sandwich shop’s traffic consistent throughout the day, or does it get bursts of traffic around mealtimes? Almost certainly the latter, so identify this potential architectural characteristic.

Next, consider each of these business requirements in turn to see if it calls for architectural characteristics:

REQ: Users place their order, and, if the shop offers delivery service, select pickup or delivery.

No special architectural characteristics seem necessary to support this requirement.

REQ: Pickup customers are given a time to pick up their sandwich and directions to the shop (which must provide the option to integrate with external mapping services that include traffic information).

External mapping services imply integration points, which may impact aspects such as reliability. For example, say a developer builds a system that relies on a third-party system. If those calls fail, it impacts the reliability of the calling system. Conversely, be wary of overspecifying architectural characteristics. What if the external traffic service is down? Should the Silicon Sandwiches site fail, or should it just offer slightly less efficiency without traffic information? Architects should always guard against building unnecessary brittleness or fragility into designs.

REQ: For delivery service, dispatch the driver with the order to the user.

No special architectural characteristics seem necessary to support this requirement.

REQ: Provide mobile device accessibility.

This requirement will primarily affect the user experience (UX) design of the application, and points toward building either a portable web application or several native web applications. Given the budget constraints and simplicity of the application, it would likely be overkill to build multiple applications, so the design points toward a mobile-optimized web application. Thus, you may want to define some specific performance-related architectural characteristics to optimize page load time and other mobile-sensitive characteristics.

You shouldn’t act alone in situations like this. Collaborate with UX designers, domain stakeholders, and other interested parties to vet such decisions. For example, the business may require some behavior that’s only possible if you build native applications.

REQ: Offer national daily promotions and specials; offer local daily promotions and specials.

Both of these requirements specify customizability across both promotions and specials. Requirement 1 also implies customized traffic information based on the user’s address. Based on both of these requirements, you might consider customizability as an architectural characteristic. For example, the microkernel architectural style (covered in Chapter 13) supports customized behavior extremely well by defining a plug-in architecture. In this case, the default behavior appears in the core, and developers write the optional location-based custom parts as plug-ins. However, a traditional design can also accommodate this requirement via design patterns (such as the Template Method). This conundrum is common in architecture and requires architects to constantly weigh trade-offs between competing options. We discuss particular trade-offs in more detail in “Design Versus Architecture and Trade-Offs” on page 76.

REQ: Accept payment online, at the shop, or upon delivery.

Online payments imply a need for security, but nothing in this requirement suggests a particularly high level of security beyond what’s implicit. Architects can handle security with either design or architecture, making it a minimal architectural characteristics concern in this application.

REQ: Sandwich shops are franchised, each with a different owner.

This requirement may impose cost restrictions on the architecture. Check the feasibility, applying constraints like cost, time, and staff skill sets, to see if a simple or sacrificial architecture is warranted.

REQ: The parent company has near-future plans to expand overseas.

This requirement implies internationalization (often abbreviated as “i18n”). Many design techniques exist to handle this requirement, which shouldn’t require special structure to accommodate. This will, however, certainly drive UX decisions.

REQ: The corporate goal is to hire inexpensive labor to maximize profit.

This requirement suggests that usability will be important, but it, too, is more concerned with design than architectural characteristics.

The third architectural characteristic we can derive from the preceding requirements is performance: no one wants to buy from a sandwich shop that has poor performance, especially at peak times. However, performance is a nuanced concept. What kind of performance should you design for? (We cover the various nuances of performance in Chapter 6.)

It’s also important to define performance numbers in conjunction with scalability numbers. In other words, establish a baseline of performance without a particular scale, and determine an acceptable level of performance given a certain number of users. Quite often, architectural characteristics interact, forcing architects to define them in relation to one another.
