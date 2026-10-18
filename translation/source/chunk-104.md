# Chapter 26: Architectural Intersections (continued)

## Architecture and Team Topologies

As we’ve discussed throughout Part II of the book, team topologies can have a direct impact on software architecture, and vice versa. This alignment is so important that we’ve included a section on team topologies for each architecture style we introduce in this book.

One of the most basic ways team topologies can align with architecture is by type of partitioning. Like architectures, teams can be domain partitioned or technically partitioned. Domain-partitioned teams are organized by domain area and are typically cross-functional, with specialization throughout the team. For example, a particular domain-partitioned team might focus on the customer-facing portion of a system, and as such would be responsible for the end-to-end processing of customer-related functionality, from the UI to the database. Technically partitioned teams, in contrast, each focus on one particular technical function of the architecture and are usually organized by technical categories: for example, UI teams, backend-processing teams, shared-services teams, and database teams would align with the layered architecture style very nicely. Alternatively, these teams might be technically partitioned into business-function teams and data-synchronization teams, which would align well with the space-based architectural style.

Understanding how teams are organized is vital for ensuring the success of the system. If the organization’s team topology is misaligned with the architecture, the teams will struggle to implement and maintain the architecture, which will be unlikely to meet its business goals.

## Architecture and Systems Integration

Systems rarely live in isolation. Most require additional processing and data from other systems—and that brings us to the intersection of architecture and systems integration. When one system needs to communicate with another system to perform additional processing or retrieve data, its architect faces a host of challenges and implications. For example, is the system that is being called available? Does it scale and perform to the same level as the requirements of the calling system?

When architects don’t focus enough on systems integration, the systems’ static and dynamic coupling often results in architectures that can’t scale, aren’t responsive, and lack agility. When integrating with other systems, consider which communication protocols to use, what types of contracts to have between systems, whether the systems’ architectural characteristics are compatible, and if the integration preserves each system’s architectural quantum.

## Architecture and the Enterprise

Every enterprise has a set of standards and guiding principles. By *enterprise*, we mean the collection of all systems and products within a company (or a department or division within the company). For example, many companies force certain security standards, practices, or procedures on architectural solutions, regardless of the type of system. Enterprise standards can also involve platforms, technologies, documentation standards, and diagramming standards, to name a few. Be aware of enterprise-level standards and practices, and ensure the architecture is properly aligned with them.

We have experienced many situations where the architect ignored enterprise-level practices, standards, and procedures. The usual result has been that the architectural solution, however technically effective, is deemed a failed “one-off” solution and scrapped. We can’t stress enough the importance of aligning the architecture with enterprise practices to ensure its success.

## Architecture and the Business Environment

The business environment has a significant and *direct* influence on the architecture of its systems (and vice versa), and the business environment never stops changing. Is the company undergoing severe cost-cutting measures to stay afloat, or aggressively expanding? Is the business pivoting and repositioning every quarter to find its niche in a highly volatile and competitive market, or does it find itself in a position of stability? An effective software architect understands the position and direction of the company, and aligns the architectures of critical systems to match the business environment.

We call this alignment *domain-to-architecture isomorphism*. For example, companies undergoing extreme cost-cutting measures would not align well with microservices or space-based architectures, which are very costly to create and maintain. Conversely, businesses that are aggressively expanding through mergers and acquisitions would not be served well by monolithic architecture styles that lack the ability to evolve and adapt.

One issue architects typically face with this intersection is business change, particularly *unknown change*. Former US Secretary of Defense Donald Rumsfeld once famously said that:

> There are known knowns; there are things we know we know. We also know there are known unknowns; that is to say we know there are some things we do not know. But there are also unknown unknowns—the ones we don’t know we don’t know.

Many products and systems start with a list of *known unknowns*: things developers must learn about the domain and technology they know will change. However, these same systems also fall victim to *unknown unknowns*: things no one knew were going to crop up, yet have appeared unexpectedly. “Unknown unknowns” are the nemeses of software systems. This is why all “Big Design Up Front” software efforts suffer: architects cannot design for unknown unknowns. To quote Mark:

> All architectures become iterative because of *unknown unknowns*. Agile just recognizes this and does it sooner.

Planning for change in software architecture is *hard*. Evolutionary architecture practices help address an ever-changing business landscape, as does iterative architecture. Embracing architectural characteristics such as *portability*, *scalability*, *evolvability*, and *adaptability* also helps make a software architecture more flexible and adaptable to change.

Barry O’Reilly, an experienced software architect specializing in complexity theory and software design, came up with a new way of thinking about constant business change, called *residuality theory*. In his book *Residues: Time, Change, and Uncertainty in Software Architecture* (Leanpub, 2024), O’Reilly describes techniques for treating business change as *stressors*, and the corresponding architectural changes as *residues*. His theory is that as the architect responds to change by applying more and more residues to the architecture, these residues will eventually start addressing *unknown* changes the architect cannot possibly predict, creating an architecture that has reached a critical state within complexity theory. It’s an interesting theory, one we are watching closely.
