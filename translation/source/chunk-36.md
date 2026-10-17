# Chapter 11: The Modular Monolith Architecture Style

Thanks to the widespread adoption of domain-driven design (DDD), as well as increased focus on domain partitioning, the modular monolith architectural style has gained so much popularity since we wrote the first edition of this book in 2020 that we decided to add a chapter to the second edition describing (and rating) it.

## Topology

As the name suggests, the modular monolith architecture style is a monolithic architecture. As such, it’s deployed as a single unit of software: a web archive (WAR) file, a single assembly in .NET, an enterprise archive (EAR) file in the Java platform, and so on. Because modular monolith is considered a domain-partitioned architecture (one organized by business domains rather than technical capabilities), its isomorphic shape is defined as a single deployment unit with functionality grouped by domain area. Figure 11-1 illustrates the typical topology for modular monolith.

To get a sense of the nature of modular monolith’s domain focus, consider the traditional layered architecture (described in Chapter 10). Its components are defined and organized by their technical capabilities: Presentation, Business, and Persistence layers, and so on. For example, the presentation logic for maintaining customer profile information might be represented by a component with the namespace `com.app.presentation.customer.profile`. The third node in the namespace represents the layer’s technical concern (in this case, the Presentation layer).

Figure 11-1. With the modular monolith architecture style, functionality is grouped by domain area

Conversely, modular monolith components are primarily organized by domain. As such, in a modular monolith architecture, the same customer profile maintenance component would be represented by the namespace `com.app.customer.profile`. Here, the third node of the namespace refers to a domain concern rather than a technical one. Depending on the complexity of the component, the namespace might further be divided by technical concern after the domain concern, such as `com.app.customer.profile.presentation` or `com.app.customer.profile.business`.

## Style Specifics

Domains (or subdomains, in some cases) are called modules in this architectural style. Modules can be organized in one of two ways. The simplest architecture is a monolithic structure, where all of the modules and corresponding logical components are contained within the same code base, delineated by the namespace or directory structure they are contained in. A slightly more complex option is the modular structure, where each module is represented as an independent, self-contained artifact (such as a JAR or DLL file), and the modules are combined into one monolithic unit of software during deployment.

As with everything in software architecture, the choice between these two structural options depends on many factors and trade-offs. The following sections outline both and discuss their corresponding trade-offs.

### Monolithic Structure

In the monolithic structure, all of the modules representing the system are contained in a single source-code repository. All the code associated with each module is deployed as a single unit when delivering or releasing the software. This structural option is illustrated in Figure 11-2. Each module is represented by a separate high-level directory containing the components and any subdomains that make up that module.

Figure 11-2. An example of the monolithic structure option

The following namespaces illustrate what a modular monolith might look like for the architecture shown in Figure 11-2:

```text
com.orderentry.orderplacement
com.orderentry.inventorymanagement
com.orderentry.paymentprocessing
com.orderentry.notification
com.orderentry.fulfillment
com.orderentry.shipping
```

This is the simplest option for the modular monolith: all of the system’s source code is located in one place and is thus more easily maintained, tested, and deployed. However, strict governance is needed (see “Governance” on page 172) to maintain the boundaries of each module. Although this structural option is simple, developers have a tendency to reuse too much code across modules, as well as allowing too much communication between modules (see “Module Communication” on page 168). These practices can turn a well-architected modular monolith into an unstructured Big Ball of Mud.

### Modular Structure

With the modular structure, modules are represented as self-contained artifacts (such as JAR and DLL files), then put together into a single deployment unit during deployment. Figure 11-3 illustrates this option using JAR files in the Java platform.

Figure 11-3. An example of the modular structure option using JAR files

The advantage of this structure is that each module is self-contained, allowing teams to work on separate modules (see “Team Topology Considerations” on page 174), many times even within the team’s own dedicated source code repository for those modules. This option works well when the modules are largely independent of other modules. It also works well for larger, more complex systems where each module requires a different kind of expertise or business knowledge. With the modular structure option, developers are less apt to reuse code too much or to have modules communicate too much with one another (see “Module Communication” on page 168). This option also tends to produce cleaner boundaries between modules and better overall separation of concerns.

However, this structural option loses its effectiveness when modules that are dependent on one other need to communicate. Where this is the case, the monolithic structure approach is more effective.

### Module Communication

Communication between modules is never a good thing in this architectural style, but we do acknowledge that in many cases it’s necessary. For instance, in the architecture shown in Figure 11-2, the `OrderPlacement` module must communicate with the `InventoryManagement` module to have it adjust the inventory for the item ordered and perform any additional processing (for example, to order more stock if the inventory is too low). It also has to communicate with the `PaymentProcessing` module to apply payment for an order. Two primary options exist for communicating between modules, which we describe in the following sections.

#### Peer-to-peer approach

The most straightforward solution is simple peer-to-peer communication between modules. With this approach, a class file in one module instantiates a class in another module and invokes the necessary method(s) in that class to perform the operation (see Figure 11-4).

Figure 11-4. Peer-to-peer communication between modules

One issue with the monolithic approach is that it’s too convenient for developers to instantiate any class contained within another module. This makes it easy to go from a well-structured architecture to the Big Ball of Mud antipattern (see Figure 9-1).

With the modular structure, however, the classes contained in another module may be located in separate, external artifacts (JARs or DLL files) rather than a separate directory in the source code repository. A module that communicates with other modules won’t compile unless it has the class references, which means the developer has to form a compile-time dependency between those modules. The usual response to this issue is to create a shared interface class between those modules (in a separately shared JAR or DLL file) so that each module can compile independently of other modules. Either way, too much communication between modules using the modular structure approach results in the DLL Hell antipattern (or, in the Java platform, the JAR Hell antipattern).

#### Mediator approach

The mediator approach decouples modules by using a mediator component to form an abstraction layer between modules. The mediator acts as an orchestrator, accepting requests and delivering them to the appropriate modules. Figure 11-5 illustrates this approach.

Figure 11-5. The mediator decouples modules, so they don’t have to communicate with each other

The astute reader will observe that, while the mediator approach decouples modules, each module is effectively coupled to the mediator. This approach doesn’t remove all coupling and dependencies, but it does simplify the architecture and keep the modules independent from each other. Note that it is the mediator, not the dependent modules, that needs some sort of API or interface to invoke the functionality in other modules.
