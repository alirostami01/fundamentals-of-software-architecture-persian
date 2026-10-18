# Chapter 14: Service-Based Architecture Style (continued)

## Examples and Use Cases

To illustrate the flexibility and power of the service-based architectural style, we’ll revisit our example of Going Green, a system used to recycle old electronic devices (such as an iPhone or Galaxy cell phone).

Going Green’s processing flow works as follows:

1. The customer asks Going Green (via a website or kiosk) how much money it will pay for an old electronic device (quoting).
2. If satisfied with the quote, the customer sends the device to the recycling company (receiving).
3. Going Green assesses the device’s condition (assessment).
4. If the device is in good working condition, Going Green pays the customer for the device (accounting). During this process, the customer can go to the website at any time to check on the status of the item (item status).
5. Based on the assessment, Going Green either safely destroys the device and recycles its parts, or resells it on a third-party sales platform, such as Facebook Marketplace or eBay (recycling).
6. Going Green periodically runs financial and operational reports on its recycling activity (reporting).

Figure 14-10 illustrates this system as implemented using a service-based architecture. Each of the domain areas we just identified is implemented as a separately deployed, independent domain service. The services that need to scale (and hence would require multiple service instances) are those needing higher throughput (in this case, the customer-facing `Quoting` and `ItemStatus` services). Since the other services don’t need to scale, they only require a single service instance.

Figure 14-10. Going Green’s electronics recycling application using service-based architecture

In this example, the UI applications are separated into domains: Customer Facing, Receiving, and Recycling and Accounting. This separation provides good fault tolerance at the UI level, good scalability, and appropriate security (since external customers have no network path to access internal functionality). Notice, too, that there are two separate physical databases: one for external customer-facing operations, and one for internal operations. This arrangement allows internal data and operations to reside in a separate network zone from the external operations (denoted by the horizontal line). It also provides much better security-access restrictions and data protection—and constitutes a separate architectural quantum). One-way access through the firewall allows internal services to access and update customer-facing information, but not vice versa. Alternatively, depending on the database, teams could also use internal table mirroring and external table synchronization to synchronize the data between the two databases.

Additionally, the `Assessment` service changes constantly, as new products are received or come on the market. With a service-based architecture, these frequent changes are isolated to a single domain service, providing agility, testability, and deployability.

Service-based architecture is a very flexible architectural style that offers domain partitioning and good levels of scalability, agility, fault tolerance, availability, and responsiveness at a fairly low price, compared to other distributed architectures. These factors make it a popular choice.

Service-based architectures also make good “stepping stone” migration targets for other distributed architectures, whether the organization is migrating to another distributed architecture style or creating a new distributed system from scratch. This drives us to our main point:

> **Not every portion of an application needs to be microservices.**
>
> — Mark Richards

Initially moving to or creating a service-based architecture as a “stepping stone” before migrating to the target architectural style allows teams to analyze the domains and decide which portions of the architecture should be microservices. For example, in the Going Green example, the `Recycling` and `Accounting` services don’t need to be broken down any further and should probably remain domain services. However, the `Assessment` service changes frequently and requires high levels of agility, so that service should be broken down into separate services, one for each type of electronic device. If the Going Green team skipped this step and moved straight to a microservices architecture, every piece of functionality would likely end up as a microservice, even if it didn’t need to be one.

These are a few of the many reasons that service-based architectures are a favorite among architects. However, it’s only one of many distributed architectural styles, and understanding all of them is helpful for determining the right fit for a particular business problem. To that end, let’s look at some other distributed architectures.
