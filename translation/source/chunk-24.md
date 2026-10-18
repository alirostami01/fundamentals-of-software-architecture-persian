# Chapter 8: Component-Based Thinking

In Chapter 3, we introduced the concept of a module as a collection of related code. In this chapter, we dive much deeper into this concept, focusing on the architectural aspect of modularity in terms of logical components—the building blocks of a system.

Identifying and managing logical components is a part of architectural thinking (see Chapter 2), so much so that we call this activity component-based thinking. Component-based thinking is seeing the structure of a system as a set of logical components, all interacting to perform certain business functions. It’s at this level (not the class level) that an architect “sees” the system.

In this chapter, we define logical components within software architecture, how to identify them, and how to arrive at an appropriate level of granularity through analyzing what’s known as cohesion (we define what that means a little later on in this chapter). We also discuss coupling between components and how and why to create loosely coupled systems.

## Defining Logical Components

Think about the floor plan of a typical Western house, as illustrated in Figure 8-1. Notice the floor plan is made up of various rooms (such as a kitchen, bedrooms, bathrooms, a living room, an office, and so on), each serving a different purpose. These rooms represent the building blocks—the components—of the house.

Figure 8-1. The various rooms represent the components of the house

In the same way, the major functions a system performs represent the components of that system, as shown in Figure 8-2. Like the rooms of a house, each component performs a specific function, such as managing inventory, shipping orders, or processing payments. Together they make up the system. Each component contains source code that implements that particular business function.

Figure 8-2. The various major functions represent the components of the system

Logical components in software architecture are usually manifested through a namespace or a directory structure containing the source code that implements that particular functionality. Typically, the leaf nodes of the directory structure or namespace containing source code represent the logical components in the architecture, and higher-level directories or namespace nodes represent the system’s domains and subdomains. In the directory structure illustrated in Figure 8-3, the directory path `order_entry/ordering/payment` represents the `Payment Processing` component, and the path `order_entry/processing/fulfillment` represents the `Order Fulfillment` component. The source code underlying the directories implements these logical components.

Figure 8-3. The leaf nodes of the directory represent the components of the system

An architect can analyze a software system’s directory structures or namespaces to understand its internal structure—in other words, its logical architecture. We describe the differences between logical and physical architectures in the next section.

## Logical Versus Physical Architecture

A logical architecture consists of a system’s logical components (building blocks) and how they interact with one another. It also usually shows their interactions with various actors (users who interact with the system), and may also show a repository (not a database) to clarify where data is used or transferred between components. Figure 8-4 illustrates an example of a logical architecture.

Figure 8-4. Diagram of a logical architecture

A logical architecture diagram doesn’t typically show a user interface, databases, services, or other physical artifacts. Rather, it shows the logical components and how they interact, which should match the directory structures and namespaces that organize the code.

A physical architecture, on the other hand, includes such physical artifacts as services, user interfaces, databases, and so on. Figure 8-5 is an example of a physical architecture diagram.

Figure 8-5. Diagram of a physical architecture

The system’s physical architecture should closely represent one (or more) of the many architectural styles described in Part II of this book: microservices, layered architecture, event-driven architecture, and so on.

Many architects choose to bypass creating a logical architecture and start directly with a physical architecture. However, we advise against this practice, because a physical architecture doesn’t always show where the system’s functionality is and how it all fits together. For example, in a physical architecture, payment-processing functionality may be spread across multiple services, making it difficult to see how it interacts with other parts of the system. Furthermore, a physical architecture doesn’t provide development teams with any guidance on how to build a monolithic or distributed system, or organize its code, resulting largely in unstructured architectures that are hard to maintain, test, and deploy.

Generally, a system’s logical architecture is independent of its physical architecture. In other words, when creating a logical architecture, the focus is more on what the system does, how that functionality is demarcated, and how the functional parts of the system interact, rather than on its physical structure. For example, the architect creating a logical architecture like that shown in Figure 8-4 may not have determined yet whether those components will all go into a monolithic architecture (a single deployment unit) or will be deployed as services (separate deployment units), nor have they necessarily decided what kind of architecture style would be most appropriate.

## Creating a Logical Architecture

Creating a logical architecture involves continuously identifying and restructuring logical components. Component identification works best as an iterative process. It involves producing candidate components, then refining them through a feedback loop, as illustrated in Figure 8-6.

Figure 8-6. The component identification and refactoring cycle

The first activity an architect does in developing a logical architecture is to identify the initial core components, and then assign user stories or requirements to them. After this, they analyze the component’s roles and responsibilities to make sure that the user stories or requirements assigned to it make sense. Then the architect looks at the architectural characteristics the system must support and determines whether any refactoring is needed to possibly break apart or combine the component based on those characteristics. Finally, the architect optionally refines the components based on this analysis. This process is a feedback loop that essentially never stops.

The workflow in Figure 8-6 can be used for greenfield (new) systems or anytime a feature is added to or changed in the system. For example, suppose you need to enable an order-entry system to allow users to pick items up at a store rather than having them shipped to their homes. This will involve adding scheduling code as well as changing the existing ordering process. This change may require new components, changes to existing ones, or both. As components change, their roles and responsibilities may change, prompting you to restructure your code or create new components for it.

We describe each of these steps in detail in the following sections.

### Identifying Core Components

The challenge in starting out with a new logical architecture (or making major modifications to an existing one) is determining what the initial core components should be. One mistake many software architects make is spending too much effort trying to get the initial logical components perfect the first time. A better approach is to make a “best guess” as to what the initial core components might look like, based on the core functionalities of the system, and refine them through the workflow steps outlined in Figure 8-6. In other words, it’s better to iterate over the logical components as you learn more about the system than to try to get it all perfect the first time, when you know least about the system and its specific requirements.

In most cases, the architect does not need to know all (or sometimes any) of the system’s requirements and specifications to start creating logical components. Typically, the initial core components are based on major actions users might take or the system’s major processing workflows.

We like to think of the initial core components as empty buckets. The bucket doesn’t do anything until the architect starts “filling” it—that is, assigning user stories or requirements to that component. As illustrated in Figure 8-7, the component name should represent its proposed role and responsibility. However, until the architect assigns user stories to it (the next step in the workflow), it’s essentially a placeholder—a best guess at a functional building block.

Figure 8-7. In the beginning, initial components are like empty buckets

The following are three common approaches to creating initial core components; the first two approaches (the Workflow and Actor/Action) are ones we find useful, and the third (the Entity Trap) is an antipattern we caution against.
