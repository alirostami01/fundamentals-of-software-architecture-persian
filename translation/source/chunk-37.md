# Chapter 11: The Modular Monolith Architecture Style (continued)

## Data Topologies

Because the modular monolith architecture is usually deployed as a single unit of software, it typically relies on a monolithic database topology. Using a single database helps reduce communication between modules, since the data is shared. However, if the modules are independent from each other and perform specific functions, they can also have their own databases containing specific contextual data, even though the architecture itself is monolithic. Figure 11-6 illustrates these two database topology options.

Figure 11-6. Data can be monolithic or modules can have their own databases

## Cloud Considerations

Although modular monolithic architectures can be deployed in cloud environments (particularly if it’s a small system), they’re not generally well suited for cloud deployment: their monolithic nature renders them less likely to be able to take advantage of the on-demand provisioning that cloud environments offer. That said, smaller systems implemented in this architectural style can still leverage many cloud services, such as file storage, database, and messaging.

## Common Risks

As with any monolithic system, the primary risk with the modular monolith architectural style is that it can get too big to properly maintain, test, and deploy. Monolithic architectures in and of themselves aren’t bad; it’s when they get too big that problems start to occur. What “too big” means varies from system to system, but here are some of the warning signs that the system might be too big:

- Changes take too long to make.

- When one area of the system is changed, other areas unexpectedly break.

- Team members get in each other’s way when applying changes.

- It takes too long for the system to start up.

Another risk is going overboard with code reuse. Code reuse and sharing are a necessary part of software development, but in this architecture style, too much code reuse blurs the module boundaries, leading the architecture into the risky territory of the unstructured monolith: a monolithic architecture with such highly interdependent code that it cannot be unraveled.

Too much intermodule communication is another risk in this architectural style. Ideally, modules should be independent and self-contained. As we’ve noted, it’s normal (and sometimes necessary) for some modules to communicate with others, particularly within a complex workflow. However, if there’s too much intercommunication between modules, it’s a good indication that the domains may have been ill-defined in the first place. In such cases, it’s worth putting additional thought into redefining the domains to accommodate complex workflows and interdependencies.

## Governance

The primary artifact in the modular monolith style is a module, which represents a particular domain or subdomain and is usually represented through the directory structure or namespace (or package structure in the Java platform). Therefore, one of the first forms of automated governance architects can apply is defining and ensuring compliance with the modules used in the architecture.

To write automated governance checks, architects use a host of tools, including ArchUnit for the Java platform, ArchUnitNet and NetArchTest for the .NET platform, PyTestArch for Python, and TSArch for TypeScript and JavaScript. The pseudocode in Example 11-1 ensures that all of the source code represented in the architecture example shown in Figure 11-2 falls under one of the listed namespaces that represent each defined module in the system.

Example 11-1. Pseudocode for ensuring the code follows the system’s defined modules

```text
# The following namespaces represent the modules in the system
LIST module_list = {
   com.orderentry.orderplacement,
   com.orderentry.inventorymanagement,
   com.orderentry.paymentprocessing,
   com.orderentry.notification,
   com.orderentry.fulfillment,
   com.orderentry.shipping
   }

# Get the list of namespaces in the system
LIST namespace_list = get_all_namespaces(root_directory)

# Make sure all the namespaces start with one of the listed modules
FOREACH namespace IN namespace_list {
   IF NOT namespace.starts_with(module_list) {
      send_alert(namespace)
   }
}
```

If a developer creates any additional high-level namespaces or directories outside the defined modules and their corresponding namespaces (or directories), they will receive an alert indicating the source code is not in compliance with the architecture.

This form of governance works well with the monolithic structure option of this architecture style (see “Monolithic Structure” on page 167), but is challenging with the modular structure option (see “Modular Structure” on page 168) because the code might not be contained in the same monolithic source code repository. With the modular structure option, each module must be tested separately, as shown in Example 11-2.

Example 11-2. Pseudocode for validating the `InventoryManagement` module

```text
# Get the list of namespaces in the system
LIST namespace_list = get_all_namespaces(root_directory)

# Make sure all the namespaces start with com.orderentry.inventorymanagement
FOREACH namespace IN namespace_list {
   IF NOT namepace.starts_with("com.orderentry.inventorymanagement") {
      send_alert(namespace)
   }
}
```

Another way to govern a modular monolith architecture is to control the amount of communication between modules. Defining what is “too much” communication is highly subjective and varies from system to system, but for the most part, architects should try to minimize the number of interdependencies between modules. Example 11-3 shows pseudocode for making sure the maximum total interdependency doesn’t exceed a limit of five communication (or coupling) points.

Example 11-3. Pseudocode for limiting any given module’s total number of dependencies

```text
# Walk the directory structure, gathering modules and the source code files
# contained within those modules
LIST module_list = {
   com.orderentry.orderplacement,
   com.orderentry.inventorymanagement,
   com.orderentry.paymentprocessing,
   com.orderentry.notification,
   com.orderentry.fulfillment,
   com.orderentry.shipping
   }
MAP module_source_file_map
FOREACH module IN module_list {
  LIST source_file_list = get_source_files(module)
  ADD module, source_file_list TO module_source_file_map
}

# Determine how many references exist for each source file and send an alert if
# the system's total dependency count is greater than 5
FOREACH module, source_file_list IN module_source_file_map {
  FOREACH source_file IN source_file_list {
    incoming count = used_by_other_module(source_file, module_source_file_map) {
    outgoing_count = uses_other_module(source_file) {
    total_count = incoming count + outgoing count
  }
  IF total_count > 5 {
    send_alert(module, total_count)
  }
}
```

A final form of automated governance is to ensure that modules stay independent of one another by restricting one specific module from talking to another module. For example, in Figure 11-2, the `OrderPlacement` module should not communicate with the `Shipping` module. Example 11-4 shows the ArchUnit code in Java to govern this dependency.

Example 11-4. ArchUnit code for governing dependency restrictions between specific modules

```java
public void order_placement_cannot_access_shipping() {
   noClasses().that()
   .resideInAPackage("..com.orderentry.orderplacement..")
   .should().accessClassesThat()
   .resideInAPackage("..com.orderentry.shipping..")
   .check(myClasses);
}
```

## Team Topology Considerations

Because the modular monolith is considered a domain-partitioned architecture, it works best when teams are also aligned by domain area (such as cross-functional teams with specialization). When a domain-based requirement comes along, a domain-focused, cross-functional team can work together on that feature, from the presentation logic all the way to the database. Conversely, teams organized by technical categories (such as UI teams, backend teams, database teams, and so on) do not work well with this architectural style, primarily due to its domain partitioning. Assigning domain-based requirements to technically organized teams requires a lot of communication and collaboration, which often proves difficult.

Here are some considerations for aligning the specific team topologies outlined in “Team Topologies and Architecture” on page 151 with the modular monolith style:

- Stream-aligned teams: Stream-aligned teams generally own the flow through the system from beginning to end, nicely matching the monolithic and generally self-contained shape of the modular monolith.

- Enabling teams: Due to this style’s high level of modularity and separation of concerns, enabling team topologies also works well. Specialists and cross-cutting team members can make suggestions and perform experiments by introducing additional modules to the system, with minimal impact to other existing modules.

- Complicated-subsystem teams: Each module in a modular monolith architecture generally performs a specific role based on its domain or subdomain (such as `PaymentProcessing`). This works well with the complicated-subsystem team topology, because different team members can focus on complicated domain or subdomain processing independent of other team members (and modules).

- Platform teams: Developers can leverage the benefits of the platform-teams topology by utilizing common tools, services, APIs, and tasks, primarily due to the high degree of modularity found in this architectural style.
