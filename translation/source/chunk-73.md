# Chapter 18: Microservices Architecture (continued)

## Data Topologies

As we’ve discussed throughout this chapter, data plays a critical role in microservices architectures. As a matter of fact, microservices is the only architectural style that requires architects to break apart data. While it’s possible (if not always effective) to use a monolithic database in other distributed architectures, it’s simply not an option in microservices. Neither are domain databases, as we discuss in “Data Topologies” on page 215 and also in “Data Topologies” on page 268. This is due to the fine-grained nature of microservices, bounded context, and the large number of services found in most microservices ecosystems.

To illustrate why a monolithic database isn’t feasible in microservices, consider a scenario where 60 services share the same database. The first issue that arises will be about controlling change within the architecture. As Figure 18-13 illustrates, changing the structure of that database (such as by changing a column name or dropping a table) would require corresponding changes to all 60 services using that data. Imagine trying to coordinate the maintenance, testing, and release of five dozen separately deployed services while at the same time releasing the database changes! This task would be daunting, to say the least, and would likely end in disaster.

> **Figure 18-13.** Controlling change with a monolithic database is a very challenging task

Perhaps the biggest issue with combining a monolithic data topology with microservices is that it breaks the entire notion of a physical bounded context. Recall that the bounded context includes all functionality required to execute a particular business function or subdomain, including the database and corresponding data structures. If every service shares the same database and data structures, the bounded context goes away.

Another issue with monolithic data is about scalability and elasticity. While many operational tools and products automatically monitor concurrent load and adjust the number of service instances to address increases, there aren’t many databases that scale accordingly. This imbalance can cause overall responsiveness issues and request timeouts. Managing the database connections, which are typically located in each service instance, is another concern. As the number of services and service instances increase, the services can quickly run out of available database connections, resulting in further connection waits and request timeouts.

Last, if the database becomes unavailable due to a crash, planned maintenance, or backups, the entire microservices ecosystem goes down—as would any architectural style using a monolithic database. While not as extreme, a domain-based database topology can suffer from the same issues of scalability, database connection pool management, availability, and fault tolerance.

For these reasons, the standard database topology for microservices is the Database-per-Service pattern. With this database topology, each microservices owns its own data, which is contained as tables within a separate database or schema, as illustrated in Figure 18-14.

> **Figure 18-14.** The Database-per-Service pattern is the typical database topology for microservices

This topology preserves the bounded context, making it easier for architects to control change. Because other services that need data must request it from the owning service through some sort of contract, they are decoupled from the data’s internal structure. Changing the database structure only affects the owning service within the bounded context. This allows architects the freedom to change the database type (such as from a relational database to a document database) without affecting other services.

The Database-per-Service topology also provides excellent scalability, elasticity, availability, and fault tolerance, architectural characteristics that all suffer under the monolithic or domain-based database topologies. Furthermore, managing connections to the database within a bounded context is much easier than with a monolithic or domain-based database.

While the Database-per-Service topology is widely used within microservices, it does have its drawbacks. For example, what if two or more services write to the same database table? What if a service outside of the bounded context must query the database directly, for performance reasons? In these cases (which tend to be fairly common), it is possible for a couple of services to share a database, as shown in Figure 18-15. We recommend that no more than five or six services share a single database (or schema). Any more than that and you’ll start to experience the same issues with change control, scalability, elasticity, availability, fault tolerance, and so on.

> **Figure 18-15.** It’s possible to share data between a few microservices

The box around the services and database in Figure 18-15 denotes the bounded context. Just because services share a database doesn’t mean there is no bounded context; it just means the architect has formed a broader bounded context. For example, they may have valid reasons for breaking payment processing apart into different payment types (such as credit card, gift card, PayPal, rewards points, and so on), but these individual services still need to update and access the same data. Similarly, an architect may break up a single shipping service into separately deployed services, one for each shipping method, but those services will all still require updates from and access to the same data.

The primary trade-off of sharing data between microservices within a broader bounded context is controlling database changes. When the database schema changes, the architect must now coordinate the change and deployment of multiple services, making database changes riskier and less agile. There might also be negative consequences for scalability, elasticity, and fault tolerance, depending on the business problem and the situation.

## Cloud Considerations

While microservices can certainly be deployed in on-prem systems, particularly with the popularity of service orchestration platforms such as Kubernetes and Cloud Foundry, this architectural style is very well suited for cloud-based deployments—so much so that microservices is sometimes referred to as a “cloud-native” architecture. On-demand provisioning of virtual machines, containers, and databases, combined with the services-based approach found in cloud environments (such as AWS), fits well with the microservices architectural style.

The attentive reader might wonder why we didn’t include serverless as an architecture style. Serverless refers to a cloud-computing model where functions are triggered upon request, allocating necessary machine resources on an on-demand basis. Serverless functions include such artifacts as AWS Lambdas, Google cloud functions, and Azure cloud functions. We believe that serverless is not an architectural style, but a deployment model of the microservices architectural style.

Recall from earlier in the chapter that a microservice is defined as a single-purpose, separately deployed unit of software that does one thing really well (hence the prefix micro). As such, microservices tends to be relatively finer-grained than services in other architectural styles. This also essentially describes a serverless function, which is why we consider serverless part of microservices.

That said, microservices in cloud environments does not have to be deployed as serverless functions; it can be deployed as containerized services just as easily. Most cloud vendors have adopted Kubernetes (or some form of the Kubernetes platform), allowing developers to deploy containerized microservices as easily as serverless ones.
