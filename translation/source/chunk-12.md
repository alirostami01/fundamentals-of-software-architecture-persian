### Connascence

Meilir Page-Jones’s book What Every Programmer Should Know about Object-Oriented Design (Dorset House, 1996) created a more precise language to describe different types of coupling in object-oriented languages. Connascence isn’t a coupling metric like afferent and efferent coupling—rather, it represents a language that helps architects describe different types of coupling more precisely (and understand some common consequences of types of coupling).

Two components are connascent if a change in one would require the other to be modified in order to maintain the overall correctness of the system. Page-Jones distinguishes two types of connascence: static and dynamic.

#### Static connascence

Static connascence refers to source-code-level coupling (as opposed to execution-time coupling, covered in “Dynamic connascence” on page 50). Architects view static connascence as the degree to which something is coupled via either afferent or efferent coupling. There are several types of static connascence:

*Connascence of Name*

Multiple components must agree on the name of an entity.

Method names and method parameters are the most common way that code bases are coupled and the most desirable, especially in light of modern refactoring tools that make system-wide name changes trivial to implement. For example, developers no longer change the name of a method in an active code base but rather refactor the method name using modern tools, affecting the change throughout the code base.

*Connascence of Type*

Multiple components must agree on the type of an entity.

This type of connascence refers to the common tendency in many statically typed languages to limit variables and parameters to specific types. However, this capability isn’t purely for statically typed languages—some dynamically typed languages also offer selective typing, notably Clojure and Clojure Spec.

*Connascence of Meaning*

Multiple components must agree on the meaning of particular values. It is also called Connascence of Convention.

The most common obvious case for this type of connascence in code bases is hardcoded numbers rather than constants. For example, it is common in some languages to consider defining somewhere that int TRUE = 1; int FALSE = 0. Imagine the problems that would arise if someone flipped those values.

*Connascence of Position*

Multiple components must agree on the order of values.

This is an issue with parameter values for method and function calls, even in languages that feature static typing. For example, if a developer creates a method void updateSeat(String name, String seatLocation) and calls it with the values updateSeat("14D", "Ford, N"), the semantics aren’t correct, even if the types are.

*Connascence of Algorithm*

Multiple components must agree on a particular algorithm.

A common case for Connascence of Algorithm occurs when a developer defines a security hashing algorithm that must run and produce identical results on both the server and client to authenticate the user. Obviously, this represents a high degree of coupling—if any details of either algorithm change, the handshake will no longer work.

#### Dynamic connascence

The other type of connascence Page-Jones defines is dynamic connascence, which analyzes calls at runtime. The types of dynamic connascence include:

*Connascence of Execution*

The order of execution of multiple components is important.

Consider this code:

```
email = new Email();
email.setRecipient("foo@example.com");
email.setSender("me@me.com");
email.send();
email.setSubject("whoops");
```

It won’t work correctly because certain properties must be set in a specific order.

*Connascence of Timing*

The timing of the execution of multiple components is important.

The common case for this type of connascence is a race condition caused by two threads executing at the same time, affecting the outcome of the joint operation.

*Connascence of Values*

Several values depend on one another and must change together.

Consider a case where a developer has defined a rectangle by defining four points to represent its corners. To maintain the integrity of the data structure, the developer cannot randomly change one of the points without considering the impact on the other points to preserve the shape of the rectangle.

A more common and problematic case involves transactions, especially in distributed systems. In a system designed with separate databases, when someone needs to update a single value across all of the databases, the values must either all change together or not change at all.

*Connascence of Identity*

Multiple components must reference the same entity.

A common example of Connascence of Identity involves two independent components that must share and update a common data structure, such as a distributed queue.

#### Connascence properties

Connascence is an analysis framework for architects and developers, and some of its properties help ensure that we use it wisely. These connascence properties include:

*Strength*

Architects determine the strength of a system’s connascence by the ease with which a developer can refactor its coupling. Some types of connascence are demonstrably more desirable than others, as shown in Figure 3-5. Refactoring toward better types of connascence can improve the coupling characteristics of a code base.

Architects should prefer static connascence to dynamic because developers can determine it by simple source-code analysis, and because modern tools make it trivial to improve static connascence. For example, Connascence of Meaning could be improved by refactoring to Connascence of Name, creating a named constant rather than a magic value.

Figure 3-5. Connascence strength can be a good refactoring guide

*Locality*

The locality of a system’s connascence measures how proximal (close) its modules are to each other in the code base. Proximal code (code in the same module) typically has more and higher forms of connascence than more separated code (in separate modules or code bases). In other words, forms of connascence that would indicate poor coupling when the components are far apart are fine when the components are closer together. For example, if two classes in the same module have Connascence of Meaning, it is less damaging to the code base than if those classes were in different modules.

Architects were largely unaware of the importance of this observation when the author first published it. In modern terms, he is suggesting that architects should limit the scope of implementation details (high coupling) as narrowly as practical, which is the same advice derived from domain-driven design’s (DDD) bounded context idea. The architectural observation is the same—limit implementation coupling. Meilir-Page described a good design principle that was reintroduced more fully via DDD (see “Domain-Driven Design’s Bounded Context” on page 97 in Chapter 7).

It’s a good idea to consider strength and locality together. Stronger forms of connascence within the same module represent less “code smell” than the same connascence spread apart.

*Degree*

The degree of connascence relates to the size of the impact of changing a class in a particular module—does that change impact a few classes or many? Lesser degrees of connascence require fewer changes to other classes and modules and hence damage code bases less. In other words, having high dynamic connascence isn’t terrible if an architect only has a few modules. However, code bases tend to grow, making a small problem correspondingly bigger in terms of change.

In What Every Programmer Should Know about Object-Oriented Design, Page-Jones offers three guidelines for using connascence to improve system modularity:

- Minimize overall connascence by breaking the system into encapsulated elements.

- Minimize any remaining connascence that crosses encapsulation boundaries.

- Maximize connascence within encapsulation boundaries.

The legendary software architecture innovator Jim Weirich, who repopularized the concept of connascence, offers two great rules from his talk on “Connescence Examined” during the Emerging Technologies for the Enterprise conference in 2012:

Rule of Degree: Convert strong forms of connascence into weaker forms of connascence. Rule of Locality: As the distance between software elements increases, use weaker forms of connascence.

Architects benefit from learning about connascence for the same reason it’s beneficial to learn about design patterns: connascence provides more precise language to describe different types of coupling. For example, an architect can tell someone, “We need a service and there can only be one instance,” or they can tell someone, “We need a Singleton service.” The Singleton design pattern nicely encapsulates the context and solution to a common problem with a simple name.

Similarly, when performing a code review, an architect can instruct a developer, “Don’t add a magic string constant in the middle of a method declaration. Extract it as a constant instead.” Or they could say, “You have Connascence of Meaning; refactor it to Connascence of Name."

## From Modules to Components

We use the term module throughout this book as a generic name for bundles of related code. However, most architects refer to modules as components, the key building blocks for software architecture. This concept of a component, and the corresponding analysis of logical or physical separation, has existed since the earliest days of computer science, yet developers and architects still struggle to achieve good outcomes.

We’ll discuss deriving components from problem domains in Chapter 8, but we must first discuss another fundamental aspect of software architecture: architectural characteristics and their scope.
