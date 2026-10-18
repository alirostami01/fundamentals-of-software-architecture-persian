# Chapter 23: Diagramming Architecture (continued)

## Diagramming (continued)

### Diagramming Standards: UML, C4, and ArchiMate

The software industry uses several formal standards for technical diagrams. We’ll look at three of the most popular here.

#### UML

Grady Booch, Ivar Jacobson, and Jim Rumbaugh created the Unified Modeling Language (UML) standard in the 1980s to unify their competing design philosophies. It was supposed to be the best of all worlds, but, like many things designed by committee, failed to create much impact outside organizations that mandated its use. Architects and developers still use UML class and sequence diagrams to communicate structure and workflow, but most other UML diagram types have fallen into disuse.

#### C4

C4 is a diagramming technique developed by Simon Brown between 2006 and 2011 to address UML’s deficiencies and modernize its approach. The “four Cs” in C4 are:

- ***Context*:** The entire context of the system, including the roles of users and external dependencies.
- ***Container*:** The physical (and often logical) deployment boundaries and containers within the architecture. This view forms a good meeting point for operations teams and architects.
- ***Component*:** The component view of the system; this most neatly aligns with an architect’s view of the system.
- ***Class*:** C4 uses the same style of class diagrams as UML, which are effective, so there is no need to replace them.

C4 offers a good alternative for any company seeking to standardize on a diagramming technique. Its creators have been active for years and have gathered a huge following. Critically, it has kept up with changes in the software development ecosystem, expanding to take advantage of new capabilities. Many diagramming tools contain templates for C4 diagrams, and the C4 ecosystem contains tools and frameworks to assist architects. C4 defines standards for components, lines, containers, databases, and other common artifacts.

A C4 diagram of the Silicon Sandwich modular monolith data design appears in Figure 23-2.

> **Figure 23-2.** Silicon Sandwiches component diagram in C4

#### ArchiMate

ArchiMate (a portmanteau of *architecture* and *animate*) is an open source enterprise-architecture modeling language from The Open Group for describing, analyzing, and visualizing architectures within and across business domains. ArchiMate offers a lighter-weight modeling language for enterprise ecosystems. The goal of this technical standard is to be “as small as possible,” not to cover every edge case. It is a popular choice among architects.

### Diagram Guidelines

Every architect should build their own diagramming style, whether they use their own modeling language or one of the formal ones. It’s OK to borrow from representations you think are particularly effective. This section offers some general guidelines for creating technical diagrams.

#### Titles

Make sure all the elements of the diagram have titles, unless they’re very well-known to the audience. Use rotation and other effects to make titles “stick” to the right thing and to make efficient use of space.

#### Lines

Lines should be thick enough to be clearly visible. If the lines indicate information flow, use arrows to indicate directional or two-way traffic. Different types of arrowheads might suggest different semantics—just be consistent.

One of the few general standards in architecture diagrams is that solid lines almost always indicate synchronous communication, and dotted lines indicate asynchronous communication.

#### Shapes

While the formal modeling languages we’ve described all have standard shapes, there’s no pervasive set of standard shapes used across the software development world. Most architects make their own set of standard shapes; sometimes these are adopted across an organization to create a standard language.

We tend to use three-dimensional boxes to indicate deployable artifacts, rectangles to indicate containers, and cylinders to represent databases, but we don’t have any particular key beyond that.

#### Labels

It’s important to label every item in a diagram, especially if there is any chance of ambiguity.

#### Color

Architects often don’t use color enough. For many years, books were out of necessity printed in black and white, so architects and developers became accustomed to monochromatic drawings. While we still favor monochrome, we use color when it helps distinguish one artifact from another. For example, when discussing microservices architecture quantum in Chapter 19, we use shades of gray in Figure 19-6 (reproduced here as Figure 23-3) to indicate grouping.

> **Figure 23-3.** Reproduction of a microservices communication example from Chapter 19, showing different services in shades of gray

Be careful about using color to indicate critical differences, however; people who are colorblind or have other visual disabilities will not be able to see the distinction. We suggest using unique iconography in addition to color, so if someone can’t distinguish the color, they can still understand the meaning—just as any street-crossing lights use green for go and red for stop, but also show unique figures for each color.

#### Keys

If a diagram’s shapes are ambiguous for any reason, include a key that clearly indicates what each shape represents. An easily misinterpreted diagram is worse than no diagram at all.

## Summary

Diagramming standards are a useful way for organizations to provide consistent communication. Architects, however, frequently break the rules, especially when the standard doesn’t offer a good way to represent the design. We encourage organizations to establish standards but allow reasonable exceptions.

In the past, when heavyweight computer-assisted software engineering (CASE) tools were the norm, architects had to build elaborate models to represent simple things. They were often forced to include many useless details that were merely noise in that specific context. We favor lightweight diagramming tools and quick-and-dirty artifacts, especially early in the design process. Just don’t become so enamored with your creations that you lose your objectivity.
