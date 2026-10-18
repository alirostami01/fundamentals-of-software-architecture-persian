# Chapter 24: Making Teams Effective

In addition to creating technical architectures and making architecture decisions, software architects are also responsible for leading the development team and guiding it through implementing the architecture. Architects who do this well create effective development teams that work together closely to solve problems and create winning solutions. While this may sound obvious, we’ve seen too many architects ignore their development teams and create an architecture alone, in a siloed environment. When this architecture is handed off to the development team, the developers often struggle to implement it correctly.

Making teams productive is one of the ways successful software architects differentiate themselves. In this chapter, we introduce some basic techniques for improving development teams’ effectiveness.

## Collaboration

All too often, the software industry treats architecture and development as entirely separate activities. Consider Figure 24-1, which compares the traditional responsibilities of architects to those of developers. Architects are responsible for activities like analyzing business requirements to extract and define architectural characteristics, selecting architecture patterns and styles to solve the problem domain, and creating logical components. The development team uses the artifacts the architect creates during these activities to create class diagrams for components, build UI screens, and write and test source code.

> **Figure 24-1.** Traditional roles of architects versus developers

The image in Figure 24-1 illustrates why this traditional approach to architecture rarely works. Look at the unidirectional arrow that passes through the virtual and physical barriers separating the architect from the developer: that’s what causes all of the problems. Architects’ decisions don’t always make it to the development team, and when development teams change the architecture, it rarely gets back to the architect. In this model, because the architect is so disconnected from the development team, the architecture rarely accomplishes its goals.

The key to making architecture work is breaking down the barriers, both physical and virtual, between architects and developers, instead forming a strong bidirectional collaborative relationship between them. The architect and development team must be on the same virtual team, as in the collaborative model depicted in Figure 24-2. Not only does this model facilitate strong bidirectional communication and collaboration, it also allows the architect to mentor and coach developers.

> **Figure 24-2.** Making architecture work through collaboration

Unlike with the static, rigid old-school waterfall approaches, today’s software architectures change and evolve with nearly every iteration or phase of a product effort. Tight collaboration between the architect and the development team is essential for success.

In the rest of this chapter and in Chapter 25, we’ll show you techniques for forming the healthy, bidirectional, collaborative relationships that not only make development teams more effective, but create more robust and successful architectures.

## Constraints and Boundaries

It’s been our experience that a software architect can significantly influence the success or failure of a development team. Teams that feel left out of the loop or estranged from their architects often lack knowledge about various constraints on the system; without the right level of guidance, they struggle to implement the architecture correctly.

One of the roles of a software architect is to create and communicate the constraints within which developers must implement the architecture. Think of these constraints as forming a “room” in which the development team works to implement the architecture. As Figure 24-3 demonstrates, having boundaries that are too tight or too loose directly hampers teams’ ability to successfully implement the architecture.

> **Figure 24-3.** The boundaries a software architect creates affect the team’s ability to implement the architecture

Too many constraints make the room too small for the development team, preventing them from accessing many of the tools, libraries, and practices they need to implement the system. This causes frustration, and usually results in developers leaving the project for happier and healthier environments.

The converse can also happen. Constraints that are too loose (or having no constraints at all) make the room too big. In this case there are too many choices available, forcing the development team to essentially take on the role of the architect to make all of the important architectural decisions. Lacking proper guidance, the developers find themselves performing too many proofs of concept, struggling over design decisions, and becoming unproductive, confused, and frustrated.

Effective software architects strive to provide the right level of guidance and appropriate constraints so that the team has everything it needs. The rest of this chapter is devoted to showing how to create these appropriate boundaries.

## Architect Personalities

We’re going to generalize wildly for the sake of conceptual clarity here, and tell you that architects’ personalities come in three basic types: the *control-freak architect*, the *armchair architect*, and the *effective architect*. Control-freak architects tend to produce tight boundaries, armchair architects tend to produce loose boundaries, and effective architects produce appropriate boundaries. The following sections describe the details of each architecture personality.

### The Control-Freak Architect

The control-freak architect tries to control every detail of the software development process. Every decision they make is usually too fine-grained and too low-level, resulting in tight boundaries and too many constraints on the development team.

For example, a control-freak architect might restrict the development team from downloading useful or even necessary open source or third-party libraries, or place tight restrictions on naming conventions, class designs, method lengths, and so on. They might go so far as to write pseudocode for the development teams to implement, essentially stealing the art of programming away from the developers. Developers find this frustrating and often lose respect for the architect.

Unfortunately, it’s very easy to become a control-freak architect, particularly when you’re transitioning into architecture from a software developer role. Architects’ role is to create the building blocks of the application (the logical components) and determine how they all interact. The developers’ corresponding role is to determine how best to implement those logical components, using class diagrams and design patterns. New architects, being used to creating the class diagrams and selecting the design patterns themselves as developers, often find this temptation difficult to resist.

For example, suppose an architect creates a logical component that manages the reference data within the system: things like the static name-value pair data used on the website, product codes, and warehouse codes. The architect’s role is to identify the logical component (in this case, a `Reference Manager`), determine its core set of operations (for example, `GetData`, `SetData`, `ReloadCache`, and `NotifyOnUpdate`), and identify which other components need to interact with the `ReferenceManager`. A control-freak architect might think that the best way to implement this component is through a parallel loader pattern, leveraging an internal cache with a particular data structure. This might be an effective design, but it’s not the only design, and, more importantly, it’s not the architect’s job to come up with an internal design for the `Reference Manager`—that’s the developer’s job.

As we’ll talk about in this chapter, sometimes architects need to play the role of control freak, depending on the complexity of the project and the team’s skill level. However, most of the time, a control-freak architect disrupts the development team, doesn’t provide the right level of guidance, gets in the way, and is generally ineffective as a leader.
