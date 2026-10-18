# Chapter 18: Microservices Architecture (continued)

## Style Specifics (continued)

### Data Isolation

Another requirement of microservices, also driven by the bounded-context concept, is data isolation. Many architecture styles use a single database for persistence. However, microservices tries to avoid all kinds of coupling, including using shared schemas and databases as integration points.

Data isolation is another factor to consider when looking at service granularity. Be wary of the Entity Trap (discussed in “The Entity Trap” on page 115)—don’t simply model services to resemble single entities in a database. Architects are accustomed to using relational databases to unify values within a system, creating a single source of truth, but that’s no longer an option when you’re distributing data across the architecture. So every architect must decide how they want to handle this problem: either identifying one domain as the source of truth for some fact and coordinating with it to retrieve values, or distributing information through database replication or caching.

While this level of data isolation creates headaches, it also provides opportunities. Now that they aren’t forced to unify around a single database, each team can choose the most appropriate database technology for their service’s budget, storage structure type, operational characteristics, process characteristics, and so on. Another advantage of a highly decoupled system is that any team can change course and choose a more suitable database (or other dependency) without affecting other teams, which aren’t allowed to couple to implementation details. (We cover data isolation and database considerations in more detail in “Data Topologies” on page 348.)

### API Layer

Most microservices architectures include an API layer (usually called an API Gateway) between the consumers of the system (either user interfaces or calls from other systems) and the microservices. The API layer can be implemented as a simple reverse-proxy or a more sophisticated gateway containing cross-cutting concerns such as security, naming services, and so on (these are covered in more detail in “Operational Reuse”).

While API layers have many uses, to stay true to the underlying philosophy of this architecture, they should not be used as mediators or orchestrators. All interesting business logic in this architecture should reside inside a bounded context, and putting orchestration or other business logic into a mediator violates that rule. Architects typically use mediators in technically partitioned architectures, whereas microservices is firmly domain partitioned.

> **Tip:** When using an API layer in a microservices architecture, only include request routing and cross-cutting concerns, such as security, monitoring, logging, and so on. Be careful to avoid putting any business-related logic within the API layer.

### Operational Reuse

Given that microservices prefers duplication to coupling, how do architects handle the parts of this architecture that really do benefit from coupling, such as operational concerns like monitoring, logging, and circuit breakers? Traditional service-oriented architecture philosophy was to reuse as much functionality as possible, domain and operational alike. In microservices, however, architects try to split these two concerns.

Once a team has built several microservices, its members start to realize that each microservice has common elements that benefit from similarity. For example, if an organization allows each service team to implement monitoring independently, how can it ensure that each team does so? And how does the organization handle concerns like upgrades—does each team become responsible for upgrading to the new version of the monitoring tool, and how long will that take? The Sidecar pattern offers a solution to this problem (Figure 18-2).

> **Figure 18-2.** The Sidecar pattern in microservices

In Figure 18-2, the common operational concerns (circuit breaker, logging, monitoring) appear within each service as separate components, each of which can be owned by individual teams or by a shared infrastructure team. The `Sidecar` component handles all the operational concerns that benefit from coupling, so when it comes time to upgrade the monitoring tool, the shared infrastructure team can update the sidecar, and each microservice will receive the new functionality (see “Team Topology Considerations” on page 353).

When each service includes a common `Sidecar` component, the architect can build a service mesh to allow teams unified control of these common concerns across the architecture. The sidecar components connect to form a consistent operational interface across all microservices, as shown in Figure 18-3.

> **Figure 18-3.** The service plane connects the sidecars in a service mesh

In Figure 18-3, each sidecar wires into the service plane. A service plane is integration software (usually in the form of a product such as Istio) that connects each sidecar using a consistent interface, thus forming the service mesh.

Each service forms a node in the overall mesh, as shown in Figure 18-4. The service mesh forms a console that allows teams to globally control operational coupling, such as monitoring levels, logging, and other cross-cutting operational concerns.

> **Figure 18-4.** The service mesh forms a holistic view of the operational aspect of microservices

Architects use service discovery as a way to build elasticity into microservices architectures. Service discovery is a way of automatically detecting and locating services within a network. When a request comes in, rather than invoking a single service, it goes through a service discovery tool, which can monitor the number and frequency of requests and spin up new instances of services to handle scale or elasticity concerns. Architects often include service discovery in the service mesh, making it part of every microservice. The API layer is often used to host service discovery, allowing a single place for user interfaces or other calling systems to find and create services in an elastic, consistent way.

### Frontends

Microservices favors decoupling, which would ideally encompass the user interfaces as well as backend concerns. In fact, the original vision for microservices included UI as part of the bounded context, faithful to the bounded-context principle in DDD. However, the practicalities of the partitioning required by web applications (and other external constraints) make that a difficult goal. That’s why we commonly see two UI styles for microservices architectures.

The first style, shown in Figure 18-5, is the monolithic frontend, which features a single UI that calls through the API layer to satisfy user requests. This frontend could be a rich desktop, mobile, or web application. For example, many web applications now use a JavaScript web framework to build a single UI.

> **Figure 18-5.** Microservices architecture with a monolithic user interface

The second UI option is micro-frontends, shown in Figure 18-6.

> **Figure 18-6.** Micro-frontend pattern in microservices

The micro-frontend approach uses components at the UI level to create a synchronous level of granularity and isolation in the UI and the backend services, thus forming relationships between the UI components and corresponding backend services.

To learn more about micro-frontends, we highly recommend the book *Building Micro-Frontends*, 2nd Edition, by Luca Mezzalira (O’Reilly, 2025).
