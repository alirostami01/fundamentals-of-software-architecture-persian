# Chapter 14: Service-Based Architecture Style

Service-based architecture is a hybrid variant of the microservices architectural style and is considered one of the most pragmatic styles available, mostly due to its flexibility. Although service-based architecture is distributed, it doesn’t have the same level of complexity and cost as other distributed architectures (such as microservices or event-driven architecture), making it a popular choice for business-related applications.

## Topology

The basic topology of service-based architecture follows a distributed macro-layered structure consisting of a separately deployed user interface; separately deployed, remote, coarse-grained services; and, optionally, a monolithic database.

Although Figure 14-1 illustrates the basic topology of this style, it can vary greatly, including using separate UIs and separate databases. This chapter will describe these topology variants in detail.

Services within this architectural style typically represent a specific domain or subdomain with a system, so they are called domain services. Domain services are generally coarse-grained and represent some portion of the system’s functionality (such as order fulfillment or order shipping). They are typically independent of each other and separately deployed. Services are typically deployed much like any monolithic application would be, so they do not require containerization (although deploying a domain service in a container such as Docker or Kubernetes is certainly an option). When using a single monolithic database, an architect should try to minimize the number of domain services (we recommend no more than 12) to avoid change control, scalability, and fault tolerance issues.

Figure 14-1. Basic topology of the service-based architectural style

Typically, each domain service is deployed as a single instance. However, based on the system’s scalability, fault tolerance, and throughput needs, architects sometimes create multiple instances of a domain service. Doing so usually requires some sort of load-balancing capability between the UI and the domain service so that the UI can be directed to a healthy and available service instance.

Services are accessed remotely from a UI using a remote access protocol, typically REST. Other possibilities include messaging, remote procedure call (RPC), an API layer with a proxy or gateway, or even SOAP. However, in most cases, the UI has an embedded service locator pattern so it can access the services directly; the service locator pattern can also be embedded within an API Gateway or proxy.

The service-based architecture typically uses a centrally shared monolithic database. This allows services to leverage SQL queries and joins just as a traditional monolithic layered architecture would. Because of the small number of domain services typically found in this architectural style, exhausting the available database connections is rarely an issue. Managing database changes, however, can present a challenge. “Data Topologies” on page 215 describes techniques for addressing and managing database changes within a service-based architecture.

## Style Specifics

Because domain services in a service-based architecture are generally coarse-grained, each domain service is typically designed using a layered architectural style consisting of an API Facade layer, a Business layer, and a Persistence layer. Another popular design approach is to partition each domain service into subdomains, similar to the modular monolith architectural style (see Chapter 11). Both approaches are illustrated in Figure 14-2.

Figure 14-2. Domain service design variants

Regardless of its design, a domain service must contain some sort of API access facade that the UI interacts with to execute some sort of business functionality. The API access facade typically takes on the responsibility of orchestrating the business request from the UI.

Let’s consider an example from an ecommerce site with a service-based architecture. A business request comes from the UI: a customer is ordering some items. This single request is received by the API access facade within the `OrderService` domain service. The API access facade internally orchestrates everything that has to happen to fulfill this request: placing the order, generating an order ID, applying the payment, and updating the inventory for each product ordered. In a microservices architecture, completing this request would likely involve orchestrating many separately deployed, remote, single-purpose services. This difference in granularity—between internal class-level orchestration in a service-based architecture and external service orchestration in microservices—points to one of the many significant differences between the two styles.

Because domain services are coarse-grained, regular ACID (atomicity, consistency, isolation, durability) database transactions with standard database commits and rollbacks can ensure database integrity within a single domain service. Compare this to the fine-grained single-purpose services of highly distributed architectures like microservices, which use a distributed transaction technique known as BASE transactions (basic availability, soft state, eventual consistency). Such fine-grained services don’t support the same level of database integrity that ACID transactions in a service-based architecture can support.

To illustrate this point, consider the order checkout process within our example service-based ecommerce site. Suppose the customer places an order, but the credit card they use for payment has expired. Since this payment is an atomic transaction within the same service, the service can remove everything added to the database so far using a standard transaction rollback. The service notifies the customer that the payment cannot be applied.

Now consider this same process in a microservices architecture, with its smaller, fine-grained services. First, the `OrderPlacement` service accepts the request, creates the order, generates an order ID, and inserts the order into the order tables. Once this is done, the `OrderPlacement` service makes a remote call to the `PaymentService`, which tries to apply the payment. If the payment cannot be applied because the credit card is expired, the order cannot be placed. Now the data is in an inconsistent state: the order information has already been inserted, but has not been approved. A separate action known as a compensating update (discussed in Chapter 9) would need to be applied to the `OrderPlacement` service to bring the data to a consistent state.

### Service Design and Granularity

Because domain services are coarse-grained, they allow for better data integrity and consistency, but there’s a big trade-off. In a service-based architecture, changing the order-placement functionality in an `OrderService` would require the team to test and redeploy all of the service’s functionality, including payment processing. In a microservices architecture, however, the same change would only affect a smaller, fine-grained `OrderPlacement` service, requiring no testing or deployment for the `PaymentService`. Furthermore, because a domain service deploys more functionality, there’s more risk that something else might break (including payment processing). With microservices, each service has a single responsibility, so there’s less chance of breaking other functionalities when making changes.

### User Interface Options

The service-based architecture style includes many UI variants, making it very flexible. For example, an architect could break apart the single monolithic UI illustrated in Figure 14-1 into separate UIs, even to the point of matching each domain service. This would increase the system’s overall scalability, fault tolerance, and agility. These UI variants are illustrated in Figure 14-3.

Figure 14-3. Three user-interface variants in a service-based architecture

For example, a typical ordering system could have a UI for customers to place orders, and separate, internal UIs for the order packers to view the items that need to be packed and for customer support.

### API Gateway Options

Thanks to the flexibility of this architectural style, it’s possible to add an API layer consisting of a reverse proxy or API Gateway between the UI and services, as shown in Figure 14-4. This is useful for exposing domain service functionality to external systems, for consolidating shared cross-cutting concerns (such as metrics, security, auditing requirements, and service discovery) and moving them into the API Gateway, and for load-balancing domain services that have multiple instances.

Figure 14-4. Adding an API layer between the UI and the domain services
