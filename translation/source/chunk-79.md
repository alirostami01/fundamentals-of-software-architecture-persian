# Chapter 20: Architectural Patterns

We distinguish between architectural styles and architectural patterns in Chapter 9: to recap, styles are named topologies that architects distinguish by differences in topologies, physical architectures, deployments, communication styles, and data topologies. Architecture patterns, inspired by the often-mentioned book *Design Patterns*, are contextualized solutions to problems.

It’s important to distinguish between architecture patterns and “best practices” (discussed in more depth in Chapter 21). Calling something a “best practice” implies that the architect has a clear duty, anytime a particular situation arises, to utilize that practice. Calling it a better practice would at least brook some argument, but no—we call it the best practice, allowing architects to shut off their brains and always follow the same solution.

It’s also important to distinguish between patterns and solutions. Many tools, frameworks, libraries, and other software-development artifacts encapsulate one or more patterns—depending on how they are implemented, with differing degrees of fidelity and intermingling with other patterns. Focus on identifying the most appropriate pattern first, then choose the most appropriate implementation for it.

We provide a smattering of representative patterns in this chapter to contrast and provide context for the styles we’ve introduced in Part II of this book. Our first example, an architecture reuse pattern, clarifies the difference between patterns and implementations.

## Reuse

The split between domain coupling and operational coupling is a common architectural concern in distributed architectures such as microservices.

### Separating Domain and Operational Coupling

One of the design goals of microservices architectures is a high degree of decoupling, often manifested in the advice: “duplication is preferable to coupling.”

Let’s say that two services need to pass information about customer profiles back and forth, but the architecture’s domain-driven bounded context insists that implementation details should remain private to each service. A common solution is to give each service its own internal representations of entities such as `Profile`, then passing that information in loosely coupled ways, such as name-value pairs in JSON. This lets each service change its internal representation—including the technology stack—at will, without breaking the integration. Developers generally frown on duplicating code, which can cause issues with synchronization, semantic drift, and more, but some things are worse than duplication…and in microservices, that includes coupling.

Architects who design microservices generally resign themselves to the reality that sometimes they have to duplicate implementations to preserve decoupling. But what about capabilities that benefit from high coupling? Each service should have certain common operational capabilities, such as monitoring, logging, authentication and authorization, and circuit breakers. However, allowing each team to manage these dependencies often descends into chaos.

For example, consider a company trying to choose one standard monitoring solution for all of its services to make it easier to operationalize them. The architect decides to make each team responsible for implementing monitoring for its service: the `Payment` service team, the `Inventory` service team, and so on. But how can the operations team be sure that each team actually did this? Also, what about issues such as unified upgrades? If the standardized monitoring tool needs an upgrade across the organization, how should the teams all coordinate that?

#### Hexagonal architecture

In the Hexagonal architecture pattern, shown in Figure 20-1, the domain logic resides in the center of the hexagon, which is surrounded by ports and adapters connected to other parts of the ecosystem (in fact, this pattern is alternately known as the Ports and Adapters pattern). A visual representation of this pattern appears in Figure 20-1.

> **Figure 20-1.** The Hexagonal architecture pattern

Sharp-eyed readers may notice that only four of the hexagon’s six sides are used. This pattern’s creator, Alistair Cockburn, initially drew it as a hexagon and called it the Hexagonal architecture pattern. He almost instantly regretted it, since the name Ports and Adapters is more descriptive, but it was too late. Too many architects thought “Hexagonal” sounded cool, so the name stuck.

Mistaking the pattern for the implementation is a common hazard, and this is a good example. The Hexagonal architecture has a potentially serious flaw when used to describe microservices, but only for those who understand the pattern’s original intent. Hexagonal architecture predates modern microservices, but there are many similarities between them. There’s also one significant difference: data fidelity. Hexagonal architecture treats the database as just another adapter that can be plugged in. It didn’t include the data schema as business logic, because of the misperception (which was common at the time that the Hexagonal pattern name was coined) that the database was an entirely separate piece of machinery. Eric Evans had the insight to correct this mistake in his book *Domain-Driven Design* by recognizing that, regardless of where they reside, database schemas must change to reflect the system’s business logic.

This makes the Hexagonal pattern a constant source of confusion among architects. Whenever someone uses it, are they describing the separation of operational and domain concerns, or are they referring to the literal pattern, which would isolate the data and therefore violate a core microservices design principle? Using the pattern name as shorthand for “separation of domain and operational concerns” is fine, as long as it isn’t misleading in context. However, architects today have no need for this implementation. We now have a more suitable mechanism to implement the Hexagonal pattern: the Service Mesh pattern.

#### Service Mesh

Back in “Operational Reuse” on page 334, we described the common architectural approach to separation of technical concerns from domain concerns: using the Sidecar and Service Mesh patterns.

The Sidecar pattern isn’t just a way to decouple operational capabilities from domains—it’s an orthogonal reuse pattern to address a specific kind of coupling (see “Orthogonal Coupling” on page 374). Often, architectural solutions require several types of coupling, such as our current example of domain versus operational coupling. An Orthogonal Reuse pattern presents a way to reuse some aspect represented by one or more concerns in the architecture that doesn’t fit within the preferred hierarchical organization. For example, microservices architectures are organized around domains, but operational coupling requires cutting across those domains. A sidecar allows an architect to isolate those concerns in a cross-cutting, but consistent, layer through the architecture.

> **Orthogonal Coupling**
>
> In mathematics, two lines are orthogonal if they intersect at right angles, which also implies independence. In software architecture, two parts of an architecture may be orthogonally coupled: they may have two distinct purposes that must still intersect to form a complete solution. The obvious example from this chapter is an operational concern such as monitoring, which is necessary but independent from domain behavior, like catalog checkout. Recognizing orthogonal coupling allows architects to find the intersection points that cause the least entanglement between concerns.

While the Sidecar pattern offers a nice abstraction, it has trade-offs like all other architectural approaches, as shown in Table 20-1.

**Table 20-1.** Trade-offs for the Sidecar and Service Mesh patterns

| Advantages | Disadvantages |
|---|---|
| Offers a consistent way to create isolated coupling | Must implement a sidecar per platform |
| Allows consistent infrastructure coordination | Sidecar component may grow large/complex |
| Ownership per team, centralized, or some combination | Implementation “drift” between independent teams |

Both the Hexagonal and Service Mesh patterns illustrate ways to implement the reuse pattern to separate domain from operational concerns. The Hexagonal implementation is general purpose, while the Service Mesh is well suited to microservices and other distributed architectures. The key for architects is to identify the pattern first—separation—and then decide how best to implement it in their architecture.
