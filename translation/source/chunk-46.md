# Chapter 14: Service-Based Architecture Style (continued)

## Data Topologies

Service-based architectures offer architects many choices of database topology, further illustrating their flexibility. This style is unique in being a distributed architecture that can effectively support a monolithic database. However, that single monolithic database could be broken apart into separate databases, even going as far as to create a domain-scoped database to match each domain service (similar to microservices). If using multiple separate databases, the architect must make sure that no other domain service needs the data in each database, which might incur interservice communication between domain services. It’s usually preferable to share data rather than call another domain service in this architectural style. These database variants are illustrated in Figure 14-5.

Figure 14-5. Service-based architecture database topologies

Although this architectural style supports a monolithic database, schema changes to the database table can, if not done properly, affect every domain service. This makes changing the database a very costly, risky task that demands a great deal of effort, coordination, and overall reliability.

In a service-based architecture, the shared class files representing the database table schemas (called entity objects) usually reside in a custom shared library used by all of the domain services, such as a JAR or DLL file. These shared libraries can also contain SQL code. Creating a single shared library of all of the entity objects is the least effective way to implement a service-based architecture. Any change to the database table structures also requires changing that library of the corresponding entity objects, which means changing and redeploying every service, regardless of whether it actually accesses the changed table. Shared library versioning can help address this issue, but it’s still difficult to know which services the table change will affect without doing detailed manual analysis. This scenario, which is considered an antipattern in service-based architecture, is illustrated in Figure 14-6.

Figure 14-6. Using a single shared library for database entity objects impacts all services when a change occurs and is considered an antipattern in service-based architecture

One way to mitigate the impact and risk of database changes is to logically partition the database and represent that logical partitioning through separate shared libraries. Notice that in Figure 14-7, the database is logically partitioned into five separate domains: common, customer, invoicing, order, and tracking. The domain services use five corresponding shared libraries that match the logical partitions in the database. Using this technique, any changes the architect makes to a table within a particular logical domain (in this case, `Invoicing`) would match the corresponding shared library containing the entity objects (and possibly SQL as well). The only services affected would be those using that shared library. No other services would be affected by this change, so there would be no need to retest and redeploy them.

Figure 14-7. Using multiple shared libraries for database entity objects

In Figure 14-7, the database contains a `Common` domain and a corresponding `common_entities_lib` shared library, which is used by all services. This is relatively common.

> **Tip:** To better control database changes within a service-based architecture, make the logical partitioning in the database as fine-grained as possible—while still maintaining well-defined data domains. Since these tables are common to all services, changing them requires coordinating all services that access the shared database. One way to mitigate the potential rippling side effects of changes to these tables (and to their corresponding entity objects and domain services) is to lock the common entity objects in the version control system (if available) and allow only the database team to make changes. This helps control change and emphasizes the significance of making changes to the common tables used by all services.

## Cloud Considerations

Being a distributed architecture, the service-based style works well in cloud environments, even though its domain services are typically coarse-grained. Due to their large scope, domain services are typically implemented as containerized services rather than as serverless functions, and they can easily leverage cloud file storage, database, and messaging services.

## Common Risks

While interservice communication is typical with microservices, it’s something architects try to avoid in the service-based architectural style. Ideally, domains should be as independent as possible, with coupling focused only at the database level. Too much communication between domain services is a good indication that either the architect didn’t partition the domains correctly or this isn’t the right architectural style for the problem they are solving.

Another common risk is creating too many domain services. The practical upper limit is around 12. Any more than that is likely to start causing issues with testing, deployment, monitoring, and database connections and changes.

## Governance

In addition to the common structural and operational architectural governance techniques discussed throughout this book, such as cyclomatic complexity, scalability, responsiveness, and so on, architects can apply specific governance tests to ensure the structural integrity of a service-based architecture.

Because domain services should be as independent as possible, the first aspect of governing this style is ensuring that changes don’t span across multiple domain services. If they do, that’s a good indication that the domain boundaries aren’t appropriately defined, or that service-based is not the most appropriate architectural style for the problem.

When interservice communication is unavailable, architects can also govern the amount of communication between domain services. There are certainly situations and workflows where one domain service must communicate with another: for example, an `OrderProcessing` domain might need to communicate with a `Customer Notification` domain to email order status information to the customer. For the most part, though, domain services should be largely independent from each other, with orchestration taking place at the UI or API Gateway level.

## Team Topology Considerations

Since service-based architectures are domain partitioned, they work best when teams are also aligned by domain area (such as cross-functional teams with specialization). When a domain-based requirement comes along, a domain-focused cross-functional team can work together on that feature within a specific domain service, without interfering with other teams or services. Conversely, technically partitioned teams (such as UI teams, backend teams, database teams, and so on) do not work well with this architectural style because of its domain partitioning. Assigning domain-based requirements to a technically organized team requires a level of interteam communication and collaboration that proves difficult in most organizations.

Here are some considerations for architects with regard to aligning a service-based architecture with the specific team topologies outlined in “Team Topologies and Architecture” on page 151:

**Stream-aligned teams:** If domain boundaries are properly aligned, stream-aligned teams work well with this architectural style, particularly when their streams are focused on a specific domain. However, service-based architecture becomes more challenging when streams cross the boundaries defined by the domain services. In this case, the architect should analyze the boundaries and granularity of the domain services and either realign them to the streams or choose a different architectural style.

**Enabling teams:** Service-based architecture is not as effective when paired with the enabling team topology as other distributed architectures are, due to the coarse-grained nature of its domain services. However, an architect can increase this style’s modularity by carefully identifying and creating appropriate components within each domain service. Specialists and cross-cutting team members can then make suggestions and perform experiments based on those components.

**Complicated-subsystem teams:** Complicated-subsystem teams can leverage this architecture style’s domain-level and subdomain-level modularity to focus on complicated domain or subdomain processing, independent of other team members (and services).

**Platform teams:** Service-based architecture’s high degree of modularity helps teams leverage the benefits of the platform team topology by utilizing common tools, services, APIs, and tasks.
