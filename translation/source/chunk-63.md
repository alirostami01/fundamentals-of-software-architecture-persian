# Chapter 16: Space-Based Architecture Style (continued)

## Style Specifics (continued)

### Data Grid (continued)

#### Near-cache considerations

A near-cache is a hybrid caching model bridging in-memory data grids with a distributed cache. In this model (illustrated in Figure 16-8) the distributed cache is referred to as the full backing cache, and each in-memory data grid contained within a processing unit is called a front cache. The front cache always contains a smaller subset of the full backing cache, and uses an eviction policy to remove older items so that newer ones can be added. The front cache has three eviction policy options: a most recently used cache, containing the most recently used items; a most frequently used cache, containing the most frequently used items; or a random replacement eviction policy, which removes items randomly when space is needed. Random replacement is a good eviction policy when there is no clear analysis of the data providing a reason to keep either the latest used or the most frequently used.

Figure 16-8. The near-cache model uses both a front cache and a backing cache

While the front caches are always kept in sync with the full backing cache, the front caches contained within each processing unit are not synchronized between other processing units that share the same data. This means that multiple processing units that share the same data context (such as a customer profile) will likely all have different data in their front caches. This creates inconsistencies in performance and responsiveness between processing units, so we do not recommend using a near-cache model in a space-based architecture.

### Processing Grid

The processing grid, illustrated in Figure 16-9, is an optional component within the virtualized middleware that manages orchestrated request processing when multiple processing units are involved in a single business request. If a request requires coordination between more than one type of processing unit (such as an order-processing unit and a payment-processing unit), the processing grid mediates and orchestrates the request between those two processing units.

Figure 16-9. The processing grid manages orchestration between processing units

Most modern space-based implementations (particularly those with fine-grained services) implement their processing-grid functionality through separate, fine-grained orchestration processing units rather than a single coarse-grained orchestration engine, with each orchestration processing unit handling a single major workflow. For an ecommerce example, let’s say that when a customer places an order, three processing units must coordinate: Order Placement, Payment, and Inventory Adjustment. The architect could create an Order Placement Orchestrator processing unit to orchestrate these three processing units. They might also create separate orchestration processing units for other major workflows, such as handling order returns and replenishing stock.

### Deployment Manager

The `Deployment Manager` component manages the dynamic startup and shutdown of processing-unit instances based on load conditions. This component continually monitors response times and user loads, starts up new processing units when load increases, and shuts down processing units when the load decreases. It is critical to achieving variable scalability (elasticity) within an application. Most cloud-based infrastructures handle this responsibility, as do service-orchestration products such as Kubernetes.

### Data Pumps

A data pump is a way of sending data to another processor, which then updates a database. Space-based architectures need data pumps because processing units do not read from and write to databases directly. Data pumps in space-based architecture are always asynchronous, providing eventual consistency between the in-memory cache and the database. When a processing-unit instance receives a request and updates its cache, that processing unit becomes the owner of the update, and therefore responsible for sending it through the data pump so that the database can be updated eventually.

Data pumps are usually implemented in a space-based architecture using messaging, as shown in Figure 16-10.

Figure 16-10. Data pumps are used to send data to a database

Messaging supports not only asynchronous communication, but also guaranteed delivery, message persistence, and message order, through first-in, first-out (FIFO) queuing. Furthermore, messaging decouples the processing unit and the data writer so that if the data writer is unavailable, processing within the processing units isn’t interrupted.

Most space-based architectures have multiple data pumps. Usually each one is dedicated to a particular domain or subdomain (such as customer or inventory), but they can be dedicated to each type of cache (such as `CustomerProfile`, `CustomerWishlist`, and so on) or to a processing-unit domain (such as `Customer`) that also contains a much larger general cache.

Data pumps usually have contracts, including an action associated with the contract data (add, delete, or update). The contract can be a JSON schema, XML schema, an object, or even a value-driven message (a map message containing name-value pairs). For updates, the data pump’s message payload usually only contains the new data values. For example, if a customer changed a phone number on their profile, only the new phone number would be sent, along with the customer ID and an action to update the data.

### Data Writers

The `Data Writer` component accepts messages from a data pump and updates the database with the information in their payloads (see Figure 16-10). Data writers can be implemented as services, applications, or data hubs (such as Ab Initio). Their granularity can vary, based on the scope of the data pumps and processing units.

A domain-based data writer contains the necessary database logic to handle all updates within a particular domain (such as order processing), regardless of the number of data pumps it is reading from. The system in Figure 16-11 has four different processing units and four different data pumps to represent the customer domains (`Profile`, `WishList`, `Wallet`, and `Preferences`)—but only one data writer. That single customer data writer listens to all four data pumps and contains the database logic (such as SQL) to update customer-related data in the database.

Figure 16-11. Domain-based data writer

Alternatively, each class of processing unit can have its own dedicated `Data Writer` component, as illustrated in Figure 16-12. In this model, each data writer is dedicated to a corresponding data pump and contains only the database processing logic for that particular processing unit (such as `Wallet`). While this model tends to produce a lot of data-writer components, it does provide better scalability and agility because it aligns the processing unit, data pump, and data writer.

Figure 16-12. Dedicated data writers for each data pump
