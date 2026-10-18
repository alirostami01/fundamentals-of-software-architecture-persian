# Chapter 13: Microkernel Architecture Style

The microkernel architecture style (also referred to as the plug-in architecture) was invented several decades ago and is still widely used today. This architecture style is a natural fit for product-based applications: that is, applications packaged and made available for download and installation as a single, monolithic deployment, typically installed on the customer’s site as a third-party product. However, it is also widely used in nonproduct custom business applications, especially problem domains that require customization. For example, an insurance company in the US that has unique rules for each state, or an international shipping company that must adhere to various legal and logistical variations, would both benefit from this style.

## Topology

The microkernel style is a relatively simple monolithic architecture consisting of two components: a core system and plug-ins. Application logic is divided between independent plug-in components and the basic core system, which isolates application features and provides extensibility, adaptability, and custom processing logic. Figure 13-1 illustrates the basic topology of the microkernel architecture style.

Figure 13-1. Basic components of the microkernel architecture style

## Style Specifics

The essence of the microkernel architecture consists of two types of components: the core system and plug-ins.

### Core System

The core system is formally defined as the minimal functionality required to run the system. Let’s look at the Eclipse IDE for a good example of this. Eclipse’s core system is just a basic text editor: open a file, change some text, and save the file. It’s not until you add plug-ins that Eclipse starts becoming a usable product.

However, another definition of the core system is the happy path: a general processing flow through the application that involves little or no custom processing. A microkernel architecture takes the cyclomatic complexity of the application, removes it from the core system, and places it into separate plug-in components. This allows for better extensibility and maintainability, as well as increased testability.

To dive deeper, we’ll return to Going Green, the electronic device recycling application we introduced in Chapter 7. Let’s say you’re working on Going Green’s application, which must assess each electronic device it receives according to specific, custom assessment rules. The Java code for this sort of processing might look as follows:

```java
public void assessDevice(String deviceID) {
   if (deviceID.equals("iPhone6s")) {
      assessiPhone6s();
   } else if (deviceID.equals("iPad1"))
      assessiPad1();
   } else if (deviceID.equals("Galaxy5"))
      assessGalaxy5();
   } else ...
      ...
   }
}
```

Rather than placing all this client-specific customization—which has lots of cyclomatic complexity—in the core system, you could create a separate plug-in component for each electronic device being assessed. Not only do specific client plug-in components isolate independent device logic from the rest of the processing flow, they also allow for expansion: adding a new device to assess is simply a matter of adding a new plug-in component and updating the registry. With the microkernel architecture style, assessing an electronic device only requires the core system to locate and invoke the corresponding device plug-ins, as illustrated in this revised source code:

```java
public void assessDevice(String deviceID) {
   String plugin = pluginRegistry.get(deviceID);
   Class<?> theClass = Class.forName(plugin);
   Constructor<?> constructor = theClass.getConstructor();
   DevicePlugin devicePlugin =
      (DevicePlugin)constructor.newInstance();
   devicePlugin.assess();
}
```

In this example, all of the complex rules and instructions for assessing a particular electronic device are self-contained in a standalone, independent plug-in component that can be generically executed from the core system.

Depending on its size and complexity, you could implement the core system as a layered architecture or as a modular monolith (as illustrated in Figure 13-2). In some cases, you might even split the core system into separately deployed domain services, with each domain service containing plug-in components specific to that domain. For the sake of this example, we’ll assume that you implement it as a layered architecture for Going Green.

Suppose `Payment Processing` is the domain service representing the core system. Each payment method (credit card, PayPal, store credit, gift card, and purchase order) would have a separate plug-in component specific to that payment domain.

Figure 13-2. Variations of the microkernel architecture core system

The core system’s Presentation layer can be embedded within the core system or implemented as a separate user interface, with the core system providing backend services. As a matter of fact, you could also implement a separate UI using a microkernel architecture style. Figure 13-3 illustrates these Presentation layer variants in relation to the core system.

Figure 13-3. User interface variants

### Plug-In Components

Plug-in components are standalone, independent components that contain specialized processing, additional features, and custom code meant to enhance or extend the core system. Additionally, they isolate highly volatile code, creating better maintainability and testability within the application. Ideally, plug-in components should have no dependencies between them.

Communication between the plug-in components and the core system is generally point-to-point, meaning the “pipe” that connects the plug-in to the core system is usually a method invocation or function call to the entry-point class of the plug-in component. In addition, the plug-in component can be either compile based or runtime based. Runtime plug-in components can be added or removed at runtime without redeploying the core system or other plug-ins, and are usually managed through frameworks such as Open Service Gateway Initiative (OSGi) for Java, Penrose (Java), Jigsaw (Java), or Prism (.NET). Compile-based plug-in components are much simpler to manage, but modifying, removing, or adding them requires the entire monolithic application to be redeployed.

Point-to-point plug-in components can be implemented as shared libraries (such as a JAR, DLL, or Gem), package names in Java, or namespaces in C#. In our Going Green application, each electronic device plug-in can be written and implemented as a JAR, DLL, or Ruby Gem (or any other shared library), with the name of the device matching the name of the independent shared library, as illustrated in Figure 13-4.

Figure 13-4. Shared library plug-in implementation

An easier approach, shown in Figure 13-5, is to implement each plug-in component as a separate namespace or package name within the same code base or IDE project. When creating the namespace, we recommend the following semantics: `app.plug-in.<domain>.<context>`. For example, consider the namespace `app.plug-in.assessment.iphone6s`. The second node (`plug-in`) makes it clear that this component is a plug-in and therefore should strictly adhere to the basic rules (they must be self-contained and separate from other plug-ins). The third node describes the domain (in this case, `assessment`), allowing plug-in components to be organized and grouped by a common purpose. The fourth node (`iphone6s`) describes the specific context for the plug-in, making it easy to locate the device plug-in for modification or testing.

Figure 13-5. Package or namespace plug-in implementation

Plug-in components do not always have to use point-to-point communication with the core system. Alternatives include using REST or messaging to invoke plug-in functionality, with each plug-in being a standalone service (or maybe even a microservice, implemented using a container). Although this may sound like a good way to increase overall scalability, note that this topology (illustrated in Figure 13-6) is still only a single architecture quantum, due to the monolithic core system. Every request must first go through the core system to get to the plug-in service.

The benefits of the remote-access approach to plug-in components implemented as individual services is that it allows for better overall component decoupling, better scalability and throughput, and runtime changes without any special frameworks (like OSGi, Jigsaw, or Prism). It also allows for asynchronous communications to plug-ins which, depending on the scenario, could significantly improve overall user responsiveness. Using the Going Green example, rather than having to wait for the electronic device assessment to run, the core system could make an asynchronous request to kick off an assessment for a particular device. When the assessment completes, the plug-in can notify the core system through another asynchronous messaging channel, which in turn notifies the user that the assessment is complete.

Figure 13-6. Remote plug-in access using REST

With these benefits come trade-offs. Remote plug-in access turns the microkernel architecture into a distributed architecture rather than a monolithic one, making it difficult to implement and deploy for most third-party on-prem products. Furthermore, it creates more overall complexity and cost, and complicates the overall deployment topology. If a plug-in becomes unresponsive or stops running, particularly if the system is using REST, the request cannot be completed. This would not be the case with a monolithic deployment. The choice between point-to-point and remote communication should be based on the project’s specific requirements and a careful trade-off analysis.
