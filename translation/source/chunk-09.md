Architects and developers have struggled with the concept of modularity for quite some time, as is evident in this quote from Composite/Structured Design (Van Nostrand Reinhold, 1978):

95% of the words [written about software architecture] are spent extolling the benefits of “modularity” and little, if anything, is said about how to achieve it.

—Glenford J. Myers

Different platforms offer different reuse mechanisms for code, but all support some way of grouping related code together into modules. While this concept is universal in software architecture, it has proven slippery to define. A casual internet search yields dozens of definitions, with no consistency (and some contradictions). This isn’t a new problem. However, because no recognized definition exists, we must jump into the fray and provide our own definitions for the sake of consistency throughout the book.

Understanding modularity and its many incarnations in the development platform of choice is critical for architects. Many of the tools we have to analyze architecture (such as metrics, fitness functions, and visualizations) rely on modularity and related concepts. Modularity is an organizing principle. If an architect designs a system without paying attention to how the pieces wire together, that system will present myriad difficulties. To use a physics analogy, software systems model complex systems, which tend toward entropy (or disorder). In a physical system, energy must be added to preserve order. The same is true for software systems: architects must constantly expend energy to ensure structural soundness, which won’t happen by accident.

Preserving good modularity exemplifies our definition of an implicit architecture characteristic: virtually no project requirements explicitly ask the architect to ensure good modular distinction and communication, but sustainable code bases do require the order and consistency that this brings.

Modularity Versus Granularity

Developers and architects often use the terms modularity and granularity interchangeably, yet their meanings are very different. Modularity is about breaking systems apart into smaller pieces, such as moving from a monolithic architecture style (like the traditional n-tiered layered architecture) to a highly distributed architecture style, like microservices. Granularity, on the other hand, is about the size of those pieces—how big a particular part of the system (or service) should be. However, as stated in the following quote by one of your authors, it’s with granularity where architects and developers get into trouble:

Embrace modularity, but beware of granularity.

—Mark Richards

Granularity causes services or components to be coupled to one another, creating complex, hard-to-maintain architecture antipatterns like Spaghetti Architecture, Distributed Monoliths, and the famous Big Ball of Distributed Mud. The trick to avoiding these architectural antipatterns is to pay attention to granularity and the overall level of coupling between services and components.

Defining Modularity

Merriam-Webster defines a module as “each of a set of standardized parts or independent units that can be used to construct a more complex structure.” By contrast, in this book, we use modularity to describe a logical grouping of related code, which could be a group of classes in an object-oriented language or a group of functions in a structured or functional language. Developers typically use modules as a way to group related code together. For example, the com.mycompany.customer package in Java should contain things related to customers. Most languages provide mechanisms for modularity (package in Java, namespace in .NET, and so on).

Modern programming languages feature a wide variety of packaging mechanisms, and many developers find it difficult to choose between them. For example, in many modern languages, developers can define behavior in functions/methods, classes, or packages/namespaces, each with different visibility and scoping rules. Some languages complicate this further by adding programming constructs, such as the meta-object protocol, to provide even more extension mechanisms.

Architects must be aware of how developers package things, because packaging has important implications in architecture. For example, if several packages are tightly coupled, reusing one of them for related work becomes more difficult.

Modular Reuse Before Classes

Developers who trained in the days before object-oriented languages may puzzle over why there are so many different separation schemes. Much of the reason has to do with backward compatibility—not of code, but of how developers think about things.

In March 1968, the journal Communications of the Association for Computing Machinery (ACM) published a paper from computer scientist Edsger Dijkstra entitled “Go To Statement Considered Harmful.” He denigrated the common use of the GOTO statement, common in programming languages at the time, because it allowed nonlinear leaping around within code, making reasoning and debugging difficult.

Dijkstra’s paper helped usher in the era of structured programming languages in the mid-1970s, exemplified by Pascal and C, which encourage deeper thinking about how things fit together. Developers quickly realized that most programming languages offered no good way to group like things together logically. Thus, the short era of modular languages was born in the mid-1980s, such as Modula (Pascal creator Niklaus Wirth’s next language) and Ada. These languages embraced the programming construct of the module, much as we think about packages or namespaces today (but without the classes).

However, the modular programming era of the mid-1980s was short-lived because object-oriented languages became popular and offered new ways to encapsulate and reuse code. Still, language designers realized the utility of modules and retained them in the form of packages and namespaces. Many languages still contain compatibility features that seem odd today but were introduced to support these different paradigms. For example, Java supports modular paradigms (via packages and package-level initialization using static initializers), as well as object-oriented and functional paradigms, each with its own scoping rules and quirks.

In this book’s discussions about architecture, we use modularity as a general term to denote a related grouping of code: classes, functions, or any other grouping. This doesn’t imply a physical separation, merely a logical one. (The difference is sometimes important.) For example, lumping a large number of classes together in a monolithic application may be convenient; however, when it comes time to restructure the architecture, the coupling encouraged by loose partitioning can impede efforts to break the monolith apart. That’s why it’s useful to talk about modularity as a concept, separate from the physical separation that a particular platform forces or implies.

It is worth discussing the general concept of a namespace, which is separate from the technical implementation in the .NET platform that is also called a namespace. Developers often need precise, fully qualified names for different software assets (components, classes, and so on) to separate them from each other. The most obvious example that people use every day is the internet, which relies on unique, global identifiers tied to IP addresses.

Most languages have some modularity mechanism that doubles as a namespace to organize things like variables, functions, or methods. Sometimes the module structure is reflected physically: Java package structures, for example, must reflect the directory structure of the physical class files.

A Language with No Name Conflicts: Java 1.0

The original designers of Java had extensive experience dealing with name conflicts and clashes, which were common in programming platforms at the time. Java 1.0 used a clever hack to avoid ambiguity when two classes had the same name—such as if the problem domain included a catalog order and an installation order, both named order but with very different connotations (and classes). The Java designers’ solution was to create the package namespace mechanism, along with a requirement that the physical directory structure must match the package name. Because filesystems won’t allow two files with the same name to reside in the same directory, this leveraged the operating system’s inherent features to ambiguity and name conflicts. Thus, the original classpath in Java contained only directories.

However, as the language designers discovered, forcing every project to have a fully formed directory structure was cumbersome, especially as projects became larger. Plus, building reusable assets was difficult: frameworks and libraries had to be “exploded” into the directory structure. In the second major release of Java (1.2, but called Java 2), designers added the jar mechanism, which allows an archive file to act as a directory structure on a classpath. For the next decade, Java developers struggled with getting the classpath exactly right, as a combination of directories and JAR files. Their original intent had been broken: now two JAR files could create conflicting names on a classpath. This is why Java developers of that era tend to have numerous war stories about debugging class loaders.
