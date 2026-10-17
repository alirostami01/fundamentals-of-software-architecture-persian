# Chapter 9: Foundations (continued)

## Fundamental Patterns (continued)

### Client/Server

Few unitary architectures exist outside embedded systems and other highly constrained environments. Generally, software systems tend to add functionality over time, and separating concerns becomes necessary to maintain their operational architecture characteristics, such as performance and scale.

Many architecture styles deal with how to separate parts of the system efficiently. One fundamental style in architecture separates technical functionality between frontend and backend: this is called a two-tier, or client/server, architecture. It comes in different flavors, depending on the era and the system’s computing capabilities.

#### Desktop and database server

One early PC architecture encouraged developers to write rich desktop applications in user interfaces like Windows, separating data into a separate database server. This architecture coincided with the appearance of standalone database servers that could connect through standard network protocols. This allowed presentation logic to reside on the desktop, while the more computationally intense action (both in volume and complexity) occurred on more robust database servers.

#### Browser and web server

Once modern web development arrived, it became common to split architectures into a web browser connected to a web server (which, in turn, was connected to a database server). This separation of responsibilities was similar to the desktop variant but with even thinner clients as browsers, allowing a wider distribution both inside and outside firewalls. Even though the database is separate from the web server, many architects still consider this a two-tier architecture, because the web and database servers run on one class of machine within the operations center, while the UI runs on the user’s browser.

#### Single-page JavaScript applications

As web responsiveness improved, so did JavaScript implementations in browsers. A family of client/server style applications emerged that resembles the original desktop variation, but with the rich client written in JavaScript in the browser, rather than as a desktop application.

As this section illustrates, there will always be layers to separate different parts of architectures, depending on the needs of the application and the capabilities of the platform.

#### Three-tier

Three-tier architecture, which provided even more layers of separation, became popular during the late 1990s. As tools like application servers became prominent in Java and .NET, companies started building even more layers into their topologies. One system might have a database tier using an industrial-strength database server; an application tier managed by an application server; and a frontend coded in generated HTML and, increasingly, JavaScript (as its capabilities expanded).

The three-tier architecture corresponded with network-level protocols such as Common Object Request Broker Architecture (CORBA) and Distributed Component Object Model (DCOM) to facilitate building distributed architectures.

Just as developers today don’t worry about how network protocols like TCP/IP work (because they just work), most architects don’t have to worry about this level of plumbing in distributed architectures. The capabilities offered by that era’s tools exist today either as tools (like message queues) or as architecture patterns (such as event-driven architecture, covered in Chapter 15).

> SIDEBAR: Three-Tier Architectures, Language Design, and Long-Term Implications

During the 1990s, as the Java language was designed, three-tier computing was all the rage. People assumed that, in the future, all systems would have three-tier architectures. One of the common headaches with the existing languages at the time, such as C++, was how cumbersome it was to move objects over the network in a consistent way between systems. So Java’s designers decided to build this capability into its core, using a mechanism called serialization.

Every Java object implements an interface that requires it to support serialization. The designers figured that since three-tiered architecture would be around forever, baking it into the language would offer great convenience. Of course, that architectural style came and went—yet the leftovers appear in Java to this day. Even though virtually no one still uses serialization, new Java features must support it for backward compatibility, greatly frustrating language designers.

Understanding the long-term implications of design decisions has always eluded us, in software as in other engineering disciplines. The perpetual advice to favor simple designs is in many ways a future-proofing strategy.
> END SIDEBAR

## Architecture Partitioning

The First Law of Software Architecture states that everything in software is a trade-off, and that includes how architects partition components in an architecture. Because components represent a general containment mechanism, architects can partition them any way they want. There are several common styles, with different sets of trade-offs. One particular type of component arrangement has an outsized impact: top-level partitioning.

Of the two architecture styles depicted in Figure 9-2, one will be familiar to many: the layered monolith (discussed in detail in Chapter 10). The other, called modular monolith, is an architecture style popularized by Simon Brown that consists of a single deployment unit, associated with a database and partitioned around domains rather than technical capabilities (discussed in Chapter 11). These two styles represent different methods of top-level partitioning. Note that in both variations, each top-level layer or component likely has other components embedded within it. Top-level partitioning is of particular interest to architects because it defines a fundamental architecture style and way of partitioning code.

Figure 9-2. Two types of top-level partitioning: technical (such as the layered architecture) and domain (such as the modular monolith)

Organizing architecture based on its technical capabilities, like the layered monolith style does, represents technical top-level partitioning.

A common version of this appears in Figure 9-3, where the architect has partitioned the system’s functionality into technical capabilities: presentation, business rules, services, persistence, and so on. This way of organizing a code base certainly makes sense. All the persistence code resides in one layer, making it easy for developers to find persistence-related code. Even though the basic concept of layered architecture predates it by decades, the Model-View-Controller design pattern (one of the fundamental patterns in Head First Design Patterns by Eric Freeman and Elisabeth Robson (O’Reilly, 2020)), matches with this architectural pattern, making it easy for developers to understand. Thus, in many organizations, it is the default architecture.

Figure 9-3. Two types of top-level partitioning in architecture

An interesting side effect of layered architecture’s predominance relates to how companies often organized the seating in their physical offices according to different project roles. Because of Conway’s Law, when using a layered architecture, it makes some sense to have all the backend developers sit together in one department, the DBAs in another, the presentation team in another, and so on.
