# Chapter 10: Layered Architecture Style

The layered architecture style, also known as n-tiered, is one of the most common architecture styles. It’s the de facto standard for many legacy applications because of its simplicity, familiarity, and low cost.

The layered architecture style can fall into several architectural antipatterns, including the Architecture by Implication and the Accidental Architecture antipatterns. When developers or architects “just start coding,” unsure which architecture style they are using, chances are good that they’re implementing the layered architecture style.

## Topology

Components within the layered architecture style are organized into logical horizontal layers, as shown in Figure 10-1, with each layer performing a specific role within the application (such as presentation logic or business logic). Although there are no specific restrictions in terms of the number and types of layers that must exist, most layered architectures consist of four standard layers: Presentation, Business, Persistence, and Database. Some architectures combine the Business and Persistence layers, particularly when the persistence logic (such as SQL or HSQL) is embedded within the Business layer components. Smaller applications may have only three layers, whereas larger and more complex business applications may contain five or more.

Figure 10-1. Standard logical layers within the layered architecture style

Figure 10-2 illustrates topology variants from a physical layering (deployment) perspective. The first variant combines the Presentation, Business, and Persistence layers into a single deployment unit, with the Database layer typically represented as a separate external physical database (or filesystem). The second variant physically separates the Presentation layer into its own deployment unit, with the Business and Persistence layers combined into a second deployment unit. Again, with this variant, the Database layer is usually physically separated through an external database or filesystem. A third variant combines all four standard layers into a single deployment, including the Database layer. This variant might be useful for smaller applications with an internally embedded database or an in-memory database, such as mobile device applications. Many on-premises (on-prem) products are built and delivered to customers using this third variant.

Figure 10-2. Physical topology (deployment) variants

Each layer has a specific role and responsibility, and forms an abstraction around the work that needs to be done to satisfy a particular business request. For example, the Presentation layer is responsible for handling all UI and browser communication logic, whereas the Business layer is responsible for executing specific business rules associated with the request. The Presentation layer doesn’t need to know or worry about how to get customer data; it only needs to display that information on a screen in a particular format. Similarly, the Business layer doesn’t need to be concerned about how to format customer data for display on a screen or even where that data is coming from; it only needs to get the data from the Persistence layer, perform business logic against it (such as calculating values or aggregating data), and pass that information up to the Presentation layer.

This separation of concerns within the layered architecture style makes it easy to build effective role and responsibility models. Components within a specific layer are limited in scope, dealing only with the logic that pertains to that layer. For example, components in the Presentation layer only handle presentation logic, whereas components residing in the Business layer only handle business logic. This allows developers to leverage their particular technical expertise to focus on the technical aspects of the domain (such as presentation logic or persistence logic). The trade-off of this benefit, however, is a lack of overall holistic agility (the entire system’s ability to respond quickly to change).

The layered architecture is a technically partitioned architecture (as opposed to domain-partitioned architecture). This means, as you learned in Chapter 9, that components are separated by their technical role in the architecture (such as presentation or business) rather than by domain (such as customer). As a result, any particular business domain is spread throughout all of the layers of the architecture. For example, the domain of “customer” is contained in the Presentation layer, Business layer, Rules layer, Services layer, and Database layer, making it difficult to apply changes to that domain. As a result, a DDD approach does not fit particularly well with the layered architecture style.

## Style Specifics

Layers in this architectural style encapsulate specific areas of technical responsibility, but the layers themselves may exhibit other characteristics.

### Layers of Isolation

Each layer can be either closed or open. If a layer is closed, then as a request moves from the top layer down to the bottom layer, the request cannot skip any layers. It must go through the layer immediately beneath to get to the next layer (see Figure 10-3). For example, in an architecture where all the layers are closed, a request originating from the Presentation layer must first go through the Business layer and then to the Persistence layer before finally making it to the Database layer.

Figure 10-3. Closed layers within a layered architecture

Notice that in Figure 10-3 it would be much faster and easier for the Presentation layer to access the database directly for simple retrieval requests, bypassing any unnecessary layers (what used to be known in the early 2000s as the Fast-Lane Reader pattern). For this to happen, the Business and Persistence layers would have to be open, allowing requests to bypass other layers. Which is better—open layers or closed layers? The answer to this question lies in a key concept known as layers of isolation.

The layers of isolation concept means that changes made in one layer of the architecture generally don’t impact or affect components in other layers, provided the contracts between those layers remain unchanged. Each layer is independent of the other layers, with little or no knowledge of their inner workings. However, to support layers of isolation, layers involved with the major flow of a request have to be closed. If the Presentation layer can access the Persistence layer directly, then changes made to the Persistence layer would impact both the Business layer and the Presentation layer, producing a very tightly coupled application with layer interdependencies between components. This makes a layered architecture very brittle, as well as difficult and expensive to change.

Using layers of isolation also allows any layer in the architecture to be replaced without impacting any other layer (again, assuming well-defined contracts and the use of the Business Delegate pattern).[^1] For example, you can leverage layers of isolation to replace your older UI framework with a newer one, all within the Presentation layer.

> [^1]: Business Delegate is a pattern designed to reduce coupling between business services and the user interface. Business delegates act as adapters to invoke business objects from the presentation tier.
