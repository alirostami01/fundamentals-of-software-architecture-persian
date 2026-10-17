# Chapter 8: Component-Based Thinking (continued)

## Creating a Logical Architecture (continued)

### Identifying Core Components (continued)

#### The Workflow approach

A common approach architects use for identifying the initial core components of a logical architecture is the Workflow approach. As the name suggests, this approach leverages the major happy-path (nonerror) workflows a user might take through the system (or its main request-processing workflow). If the architect has some sense of the general flow, they can develop components based on those steps.

For example, assume you are building a new order-entry system for your company. You don’t know the specific requirements and specifications yet, but you at least know the general workflow for processing a new order. You can thus assign a component to each step in the workflow:

1. User browses the catalog of items → `Item Browser`

2. User places an order → `Order Placement`

3. User pays for the order → `Order Payment`

4. Send user an email with order details → `Customer Notification`

5. Prepare the order → `Order Fulfillment`

6. Ship the order → `Order Shipment`

7. Email customer that order has shipped → `Customer Notification`

8. Track shipment → `Order Tracking`

In the Workflow approach, not every step in the major workflow yields a new component. In the workflow above, steps 4 and 7 both use the `Customer Notification` component. The architect models as many major workflows or user journeys they can for the system, identifying corresponding components from those steps.

This is, again, only a “best guess” as to what the logical architecture might look like. These components represent empty buckets and have no responsibilities yet, so they will likely change as they evolve (as illustrated in Figure 8-6). This is perfectly normal and part of the iterative nature of software architecture. Don’t worry about trying to model every workflow in your system. Instead, focus on the major workflows. The rest will evolve as you learn more about the system and start gathering user stories and requirements.

#### The Actor/Action approach

Another way architects identify initial core components is the Actor/Action approach. This approach is particularly useful when a system has multiple actors. With this approach, the architect identifies the major actions a user can perform in the system (such as placing an order). The system itself is always an actor, too, performing automated functions such as billing and replenishing stock.

In our order-entry system example, an architect might identify three actors: the customer, the order packer (the person who packs the box and sends it off for shipping), and the system. The architect then identifies the major actions each of these actors takes and assigns components to those actions:

Customer actor

- Search for items → `Item Search`

- View the details about an item → `Item Details`

- Place an order → `Order Placement`

- Cancel an order → `Order Cancel`

- Register as a new customer → `Customer Registration`

- Update customer information → `Customer Profile`

Order packer actor

- Select the box size → `Order Fulfillment`

- Mark the order as ready for shipment → `Order Fulfillment`

- Ship the order to the customer → `Order Shipment`

System actor

- Adjust inventory → `Inventory Management`

- Order more stock from the supplier → `Supplier Ordering`

- Apply payment → `Order Payment`

Like with the Workflow approach, not every action necessarily has its own component. For example, selecting the box size for the order and marking it ready for shipping are both done by the `Order Fulfillment` component.

Generally, the Actor/Action approach generates more components than the Workflow approach, depending on how many major workflows the architect chooses to model. However, in both approaches, the architect can identify the initial core components and how they communicate even before receiving detailed requirements or specifications.

#### The Entity Trap

It’s all too tempting for an architect to start identifying components by focusing on the entities involved with the system, then deriving components from those entities. For example, in a typical order entry system, you may identify `Customer`, `Item`, and `Order` as the primary entities in the system, and correspondingly create a `Customer Manager` component, an `Item Manager` component, and an `Order Manager` component. We strongly advise against this approach for the following reasons.

First, the names of the logical components are ambiguous and don’t describe the role of the component. For example, asking what the `Order Manager` component does just by looking at the name yields the useless answer “it manages orders,” indicating nothing about its specific role or responsibility in the system. Compare that to a component name like `Validate Order`, and the importance of a good, descriptive component name becomes clear. If a component name includes a suffix like `Manager`, `Supervisor`, `Controller`, `Handler`, `Engine`, or `Processor`, that’s a good indicator that the architect might be caught in the Entity Trap antipattern.

Second, components become dumping grounds for domain-related functionalities. Consider an entity-based component name like `Order Manager`, as shown in Figure 8-8. Every bit of order functionality would go into that single component: order validation, order placement, order history, fulfilling the order, shipping the order, tracking the order, and so on. Essentially, it becomes like those “kitchen sink” utility classes every developer has written at least once in their career, with dozens of methods that perform string manipulation, data manipulation, time calculations, and whatever else the developer can put in there.

Third, when components become too coarse-grained, they do too much and lose their purpose. Rather than being fine-grained and single purpose (like the `Validate Order` component example), components can become too big. Such components are hard to maintain, test, and deploy, and hence not very reliable.

Figure 8-8. Using the Entity Trap antipattern produces components with too much responsibility

If an architect is building a system that truly is entity based and simply performs CRUD-based operations (create, read, update, and delete) against those entities, then the system doesn’t need an architecture, but rather a CRUD-based framework, tool, or no-code/low-code environment that allows the developers to generate most of the source code that acts on those entities.

### Assigning User Stories to Components

The next step in creating a logical architecture is to assign user stories or requirements to the logical components. This is an iterative process, since most user stories or requirements are not completely known up front; they evolve as the system evolves. This step is meant to start filling those empty buckets, giving the components specific roles and responsibilities, as illustrated in Figure 8-9.

Figure 8-9. Filling up the empty buckets (components) with user stories or requirements

To see how logical components evolve, consider the following user stories:

- Customer #1: As a customer, I would like to have my order validated to make sure I have entered everything completely and correctly.

- Order preparer: As the person preparing the order, I would like to know what size box I should use for the order, so I can pack it in the most efficient way possible.

- Customer #2: As a customer, I would like to receive an email each time the order status changes, so I always know the state of my order.

Assume that the architect has identified the following logical components so far:

- `Order Placement`

- `Order Fulfillment`

- `Order Shipment`

- `Inventory Management`

It makes sense to assign the first user story to the `Order Placement` component, since that’s the component the user is interacting with to place the order:

> Validate the order (Customer #1 user story) → `Order Placement`

Determining the box size should probably be handled by the `Order Fulfillment` component, since it’s responsible for all the system logic needed to prepare and pack the order in a box:

> Determine box size (Order preparer user story) → `Order Fulfillment`

But what about the third user story? Which of the four components listed should send emails to the customer when the order has been placed, is ready for shipment, and has shipped? The answer might be the `Order Placement`, `Order Fulfillment`, and `Order Shipment` components. But keep in mind that the user story is implemented through source code, which needs to reside in a specific directory or namespace. Since it wouldn’t be a good idea to replicate the code across three components, the architect needs to define a new component to handle this user story:

> Email customer (Customer #2 user story) → `Customer Notification` (new)

The `Order Placement`, `Order Fulfillment`, and `Order Shipment` components need to communicate with the new component to let it know to send an email. With this addition, the logical architecture now looks like Figure 8-10.

Figure 8-10. Evolving components based on new user stories
