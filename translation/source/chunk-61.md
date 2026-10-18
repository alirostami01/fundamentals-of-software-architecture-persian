# Chapter 16: Space-Based Architecture Style

Most web-based business applications follow the same general request flow: a request from a browser hits the web server, then an application server, then finally the database server. While this typical request flow works for a small set of concurrent users, bottlenecks start appearing as the concurrent user load increases: first at the web-server layer, then at the application-server layer, and finally at the database-server layer.

The usual response when increased user load causes bottlenecks is to scale out the web servers. This is relatively easy and inexpensive, and sometimes it works. However, in most cases of high user load, scaling out the web-server layer just moves the bottleneck down to the application server. Scaling application servers can be more complex and expensive than scaling web servers, and doing so usually just moves the bottleneck down to the database server, which is even more difficult and expensive to scale. Even if you can scale the database, what you eventually end up with is a triangle-shaped topology, with the widest part of the triangle being the web servers (easiest to scale) and the smallest part being the database (hardest to scale), as illustrated in Figure 16-1.

In any high-volume application with a large concurrent user load, the database will usually be the final limiting factor in how many transactions the application can process concurrently. While various caching technologies and database-scaling products can help, scaling out a normal application for extreme loads remains a very difficult proposition.

Figure 16-1. Scalability limits within a traditional web-based topology

The space-based architecture style is specifically designed to address problems involving high scalability, elasticity, and concurrency. It is also a useful architecture style for applications that have variable and unpredictable concurrent user volumes. It’s often better to solve extreme and variable scalability architecturally, rather than try to scale out a database or retrofit caching technologies into an architecture that can’t scale as well.

## Topology

Space-based architecture gets its name from the concept of tuple space, the technique of using multiple parallel processors that communicate through shared memory. Space-based systems achieve high scalability, elasticity, and performance by replacing the central database as a synchronous constraint in the system with replicated in-memory data grids.

Application data is kept in-memory and replicated among all the active processing units. When a processing unit updates data, it asynchronously sends that data to the database through a data pump, usually via messaging with persistent queues. Processing units start up and shut down dynamically as user load increases and decreases, which addresses variable scalability. Because no central database is involved in the application’s standard transactional processing, the database bottleneck is removed. This allows for near-infinite scalability within the application.

Space-based architecture is a complicated architectural style consisting of many different artifacts that work together to process a single request. Its primary artifacts are:

**Processing units:** Contain the application functionality

**Virtualized middleware:** The collection of infrastructure-related artifacts that are used to manage and coordinate the processing units

**Messaging grid:** Used to manage input requests and session state

**Data grid:** Manages the synchronization and replication of data between processing units

**Processing grid:** Used to manage request orchestration between multiple processing units

**Deployment manager:** Manages the starting and tearing down of processing unit instances as load increases and decreases

**Data pumps:** Asynchronously send updated data to the database

**Data writers:** Perform the updates from the data pumps

**Data readers:** Read database data and deliver it to processing units upon startup

Figure 16-2 illustrates these primary artifacts.

Figure 16-2. Space-based architecture’s basic topology

## Style Specifics

The following sections describe these primary artifacts and how they work in detail.

### Processing Unit

The processing unit (illustrated in Figure 16-3) contains the application logic (or portions of it), usually including web-based components as well as backend business logic. The contents of the processing unit vary based on the type of application. Smaller web-based applications are usually deployed into a single processing unit, whereas larger applications often split their functionality into multiple processing units, based on the application’s functional areas. The processing unit can also contain small, single-purpose services (much like microservices). In addition, the processing unit also contains an in-memory data grid and replication engine, which are usually implemented through such products as Hazelcast, Apache Ignite, and Oracle Coherence (see “Data Grid” on page 288).

Figure 16-3. The processing unit contains the application’s functionality

### Virtualized Middleware

The virtualized middleware, as shown in Figure 16-4, contains various infrastructure-related artifacts and is used to manage and control the processing units. At a minimum, this middleware artifact contains a messaging grid to manage input requests and user session state, a data grid to manage data replication and synchronization, and a deployment manager to start and tear down processing unit instances as they are needed and not needed. Optionally, the virtualized middleware also contains a processing grid in the event two or more processing units need to be orchestrated for a single business request. An architect can add any other infrastructure-related function to the virtualized middleware as needed, such as security functionality, metrics gathering for observability, and so on.

Since no single product can perform all of the functions of the virtualized middleware, it is usually implemented through third-party products such as web servers, caching tools, load balancers, service orchestrators, and deployment managers to manage monitoring, starting, and tearing down the processing units. Each of these middleware artifacts is described in detail in the following sections.

### Messaging Grid

The messaging grid, shown in Figure 16-4, is part of the virtualized middleware and manages input requests and session state. When a request comes into the virtualized middleware, the messaging grid component determines which active processing units are available to receive it, then forwards the request to one of those processing units.

The complexity of the messaging grid can vary, from a simple round-robin algorithm to a more complex next-available algorithm that keeps track of which processing unit is most available. This component is usually implemented using a typical web server with load-balancing capabilities (such as HA Proxy or Nginx).

Figure 16-4. The messaging grid handles requests and session state
