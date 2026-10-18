# Chapter 8: Component-Based Thinking (continued)

## Creating a Logical Architecture (continued)

### Analyzing Roles and Responsibilities

The next step in refining logical components is to analyze the roles and responsibilities of each component. This is how the architect ensures that the requirements or user stories assigned to those components belong there and that the components are not doing too much. What the architect is concerned about in this step is cohesion: how, and how much, a component’s operations interrelate. Over time, components can get too big, even though their operations all interrelate.

To illustrate how this step works, assume the architect has assigned the following requirements to the `Order Placement` component:

- Validate the order to ensure all fields have been entered and are correct.

- Display the shopping cart with the item descriptions, quantities, and prices.

- Determine the correct shipping address.

- Collect payment information.

- Generate a unique order ID.

- Apply payment for the order.

- Adjust inventory counts for the items ordered.

- Email the customer an order summary.

If the architect were to write a role and responsibility statement for this component, it would read as follows:

> This component is responsible for validating the order and displaying the valid shopping cart, complete with the item picture, description, quantity, and price. This component is also responsible for determining the correct shipping address for the order, as well as collecting all the payment information from the customer. In addition, it’s also responsible for applying the payment, adjusting inventory, and emailing the customer the order summary.

While all of these operations have to do with placing an order, the `Order Placement` component is clearly taking on too much responsibility, particularly with regard to applying the payment, adjusting the inventory, and emailing the customer. One way to see if a component is taking on too much responsibility is to look for conjunctive phrases such as and, also, in addition, or as well as, and excessive use of commas.

Recall from earlier in the chapter that a logical component is represented by a namespace or directory in the code repository. In the case of the `Order Placement` component, all the source code representing this component would be in the same directory or namespace, such as `com/app/order/placement` or `com.app.order.placement`. This is a lot of functionality—likely too much code for a single directory. Therefore, it would make sense to separate the class files for payment processing, inventory management, and email communications into separate directories representing those functionalities. That’s exactly what separating logical components is all about.

If the architect moves the responsibilities of applying the payment, adjusting the inventory, and sending the customer an email to separate components, they can reduce the responsibility of the single `Order Placement` component, making it easier to maintain, test, and deploy. The resulting components would look like this:

`Order Placement`

- Validate the order to ensure all fields have been entered and are correct.
- Display the shopping cart with the item descriptions, quantities, and prices.
- Determine the correct shipping address.
- Collect payment information.
- Generate a unique order ID.

`Payment Processing`

- Apply payment.

`Inventory Management`

- Adjust the inventory counts for the items ordered.

`Customer Notification`

- Email the customer an order summary.

Each component now has a clearer, more distinct role and responsibility.

### Analyzing Architectural Characteristics

The final analysis step is to consider the architectural characteristics the system will require. Some architectural characteristics, such as scalability, reliability, availability, fault tolerance, elasticity, and agility (the ability to respond quickly to change), may influence the size of a logical component.

For example, breaking up a larger component (one with lots of responsibility) into smaller components makes each of them easier to maintain and test (that’s agility), and provides better scalability, elasticity, and fault tolerance. Another good example is where two parts of a system deal with user input: if one part deals with hundreds of concurrent users and the other needs to support only a few at a time, they will need different architecture characteristics. Thus, while a purely functional view of component design might lead an architect to assign a single component to handle user interaction, analyzing the components in terms of architecture characteristics might lead to a subdivision.

Because the architect must know the architectural characteristics before building a logical architecture, it is usually done after determining which architectural characteristics are most important to the system.

### Restructuring Components

Feedback is critical in software design. Architects must continually iterate on their component designs in collaboration with developers. Designing software provides all kinds of unexpected difficulties. Thus, an iterative approach to component design is key. First, it’s virtually impossible to account for all the different discoveries and edge cases that will arise, any of which could encourage redesign. Second, as the architecture and developers delve more deeply into building the application, they gain a more nuanced understanding of where its behaviors and roles should lie.

Architects should expect to restructure components frequently throughout the lifecycle of a system or product—not only in greenfield systems, but in any that undergo frequent maintenance.

## Component Coupling

When components communicate with each other, or when a change to one component might impact other components, the components are said to be coupled together. The more coupled a system’s components are, the harder it is to maintain and test the system (see Figure 8-11). Therefore, it’s important to pay close attention to coupling.

Figure 8-11. Components can be coupled even if they don’t communicate directly

### Static Coupling

Static coupling occurs when components communicate synchronously with each other. Architects need to be concerned about two types of coupling: afferent and efferent.

Afferent coupling (also known as incoming or fan-in coupling) is the degree to which other components depend on a target component. For instance, consider the `Customer Notification` component from our order-entry example in Figure 8-12. To email the customer, both the `Order Placement` and `Order Shipment` components need to communicate with the `Customer Notification` component. This means that the `Customer Notification` component is said to be afferently coupled to the `Order Placement` and `Order Shipment` components and would have an afferent coupling level of 2 (the number of incoming dependencies). Afferent coupling is usually denoted as `CA`.

Figure 8-12. The `Customer Notification` component is afferently coupled to the other components

Efferent coupling (also known as outgoing or fan-out coupling) is the degree to which a target component depends on other components. For example, as illustrated in Figure 8-13, the `Order Placement` component is dependent on the `Order Fulfillment` component and, as such, is efferently coupled to it and would have an efferent coupling level of 1 (the number of outgoing dependencies). Efferent coupling is usually denoted as `CE`.

Figure 8-13. The `Order Placement` component is efferently coupled to the `Order Fulfillment` component

### Temporal Coupling

Temporal coupling describes nonstatic dependencies, usually those based on timing or transactions (single units of work). For example, when the system is processing an order, the functionality in the `Order Placement` component must be invoked before the functionality in the `Order Shipment` component. Those components are thus said to be temporally coupled.

The problem with temporal coupling is that it’s hard to detect using the tooling currently available on the market. In most cases, this kind of coupling is instead identified through design documents or detected through error conditions.
