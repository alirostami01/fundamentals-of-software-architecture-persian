# Chapter 9: Foundations (continued)

## Architecture Partitioning (continued)

The other architectural variation in Figure 9-3 is domain partitioning, a modeling technique for decomposing complex software systems that organizes components by domain rather than technical capabilities. Domain partitioning was inspired by Eric Evans’s book Domain-Driven Design. In DDD, the architect identifies domains or workflows, independent and decoupled from each other. The microservices architecture style is based on this philosophy.

A modular monolith architecture is partitioned around domains or workflows, rather than technical capabilities. Because components often nest within one another, each component in the domain-partitioned architecture shown in Figure 9-3 (for example, `CatalogCheckout`) may use a persistence library and have a separate layer for business rules, but the top-level partitioning will still revolve around domains.

> SIDEBAR: Conway’s Law

Back in the late 1960s, Melvin Conway made an observation that has become known as Conway’s Law:

> > Organizations which design systems…are constrained to produce designs which are copies of the communication structures of these organizations.

Paraphrased, this law suggests that when a group of people designs some technical artifact, the structures of their design will replicate how those people communicate. People at all levels of organizations see this law in action, and they sometimes base decisions on it. For example, while it’s common for organizations to partition workers based on technical capabilities, this is an artificial separation of common concerns that can hamper collaboration.

A related observation, coined by Jonny Leroy of Thoughtworks, is the Inverse Conway Maneuver, which suggests evolving the structures of teams and organizations together to promote the desired architecture. This consideration has since become universally known as team topologies.

Organizations have begun to realize that team topologies can have a significant impact on many important facets of their business, including software architecture. In the upcoming style-focused chapters, we discuss each architecture style’s effect on these team types.
> END SIDEBAR

One of the fundamental distinctions between architecture patterns is what type of top-level partitioning each supports. In the style-specific chapters that follow, we cover this distinction for each individual pattern. Top-level partitioning also has a huge impact on whether the architect decides to initially identify components technically or by domain.

Architects using technical partitioning organize the components of the system by their technical capabilities: presentation, business rules, persistence, and so on. One of the organizing principles of the layered architecture is separation of technical concerns, which creates useful levels of decoupling. For example, if the Service layer is only connected to the Persistence layer below and the Business Rules layer above, then changes in persistence will potentially affect only those layers. This decoupling reduces the potential for rippling side effects on dependent components.

It’s certainly logical to organize systems using technical partitioning, but, like all things in software architecture, there are some trade-offs. The separation enforced by technical partitioning enables developers to find certain categories of the code base quickly, since it is organized by capabilities, but most realistic software systems require workflows that cut across technical capabilities.

In the technically partitioned architecture shown in Figure 9-4, consider the common business workflow of `CatalogCheckout`. The code to handle `CatalogCheckout` in the technically partitioned architecture appears in all the layers. In other words, the domain is smeared across the technical layers.

Figure 9-4. Where domains/workflows appear in technically partitioned and domain-partitioned architectures

Contrast this with the domain-partitioned architecture shown in Figure 9-4, in which the architects have built top-level components around workflows and domains. Each component may have subcomponents, including layers, but the top-level partitioning focuses on domains, which better reflects the kinds of changes that most often occur on projects.

Neither of these styles is more correct than the other. (Refer to the First Law of Software Architecture.) That said, we have observed a decided industry trend over the last few years toward domain partitioning for both monolithic and distributed (for example, microservices) architectures. As we’ve noted, this is one of the first decisions an architect must make.

### Kata: Silicon Sandwiches—Partitioning

Consider the case of one of our example katas, “Kata: Silicon Sandwiches” on page 71. Let’s start by considering the first of two possibilities for Silicon Sandwiches: domain partitioning, shown in Figure 9-5.

Figure 9-5. A domain-partitioned design for Silicon Sandwiches

In Figure 9-5, the architect has designed around domains (workflows), creating discrete components for `Purchase`, `Promotion`, `MakeOrder`, `ManageInventory`, `Recipes`, `Delivery`, and `Location`. Within many of these components reside subcomponents to handle both common and local variations types of customization.

Figure 9-6. A technically partitioned design for Silicon Sandwiches

An alternative design isolates the common and local parts into their own partitions, as illustrated in Figure 9-6. `Common` and `Local` represent top-level components, while `Purchase` and `Delivery` remain to handle the workflow.

Which is better? It depends! Each kind of partitioning offers different advantages and drawbacks.

#### Domain partitioning

Domain-partitioned architectures separate top-level components by workflows and/or domains.

**Advantages:**

- Modeled more closely on how the business functions rather than on an implementation detail

- Easier to build cross-functional teams around domains

- Aligns more closely to the modular monolith and microservices architecture styles

- Message flow matches the problem domain

- Easy to migrate data and components to a distributed architecture

**Disadvantage:**

- Customization code appears in multiple places

#### Technical partitioning

Technically partitioned architectures separate top-level components based on technical capabilities rather than discrete workflows. This may manifest as layers inspired by Model-View-Controller separation or some other ad hoc technical partitioning. The architecture pictured in Figure 9-6 separates its components based on customization.

**Advantages:**

- Clearly separates customization code.

- Aligns more closely to the layered architecture pattern.

**Disadvantages:**

- Higher degree of global coupling. Changes to the `Common` or `Local` component will likely affect all the other components.

- Developers may have to duplicate domain concepts in both the Common and Local layers.

- Typically, higher coupling at the data level. In a system like this, the application architects and the data architects would likely collaborate to create a single database, including customization and domains. That in turn would create difficulties in untangling the data relationships later, if the architects eventually want to migrate this architecture to a distributed system. Many other factors contribute to choosing an architecture style, as we cover in Part II.

## Monolithic Versus Distributed Architectures

As you learned in Part I, architecture styles can be classified into two main types: monolithic (single deployment unit of all code) and distributed (multiple deployment units connected through remote access protocols). While no classification scheme is perfect, distributed architectures all share a common set of challenges and issues not found in the monolithic architecture styles, making this classification scheme a good separation between the various architecture styles.

In Part II of this book, we describe the following architecture styles in detail:

**Monolithic:**

- Layered architecture (Chapter 10)

- Pipeline architecture (Chapter 12)

- Microkernel architecture (Chapter 13)

**Distributed:**

- Service-based architecture (Chapter 14)

- Event-driven architecture (Chapter 15)

- Space-based architecture (Chapter 16)

- Service-oriented architecture (Chapter 17)

- Microservices architecture (Chapter 18)

Distributed architecture styles, although much more powerful in terms of performance, scalability, and availability than monolithic architecture styles, have significant trade-offs. The first group of issues facing all distributed architectures are described in the “fallacies of distributed computing”, first listed by L. Peter Deutsch and other colleagues from Sun Microsystems in 1994. A fallacy is something false that someone believes or assumes to be true. All eight of the fallacies of distributed computing apply to distributed architectures today. The following sections describe each fallacy.
