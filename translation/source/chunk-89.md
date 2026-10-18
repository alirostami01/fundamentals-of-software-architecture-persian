# Chapter 23: Diagramming Architecture

Newly minted software architects are often surprised at how varied the job is, outside the technical knowledge and experience that brought them into the role to begin with. In particular, effective communication is critical to an architect’s success. No matter how brilliant your technical ideas, if you can’t convince managers to fund those ideas and developers to build them, your brilliance will never manifest.

Diagramming is a critical communication skills for architects. While entire books exist about each topic, we’ll hit some particular highlights for each.

To visually describe an architecture, the architect often must show different views: for example, they might start with an overview of the entire topology, then drill down into the design details of specific parts of the architecture. However, showing a portion without indicating its place within the overall architecture will confuse viewers.

*Representational consistency* is the practice of always showing the relationships between parts of an architecture before changing views, and it’s equally important in diagrams and in presentations. For example, if you wanted to describe the details of how the plug-ins relate to one another in the Silicon Sandwiches solution, you’d start with an architecture diagram showing the system’s entire topology, then the relationship between it and the plug-in structure, before going into the plug-in structure itself. Figure 23-1 provides an example.

> **Figure 23-1.** Using representational consistency to indicate context in a larger diagram

Use representational consistency carefully to ensure that viewers understand the scope of the items being presented and eliminate a common source of confusion.

## Diagramming

The topology of an architecture is always of interest to architects and developers because it captures how the structure fits together, and allows teams to form a valuable shared understanding. We encourage all architects to hone their diagramming skills to razor sharpness.

### Tools

The current generation of diagramming tools for architects is extremely powerful, and every architect should learn their tool of choice deeply. But don’t neglect low-fidelity artifacts, especially early in the design process. Building very ephemeral design artifacts early prevents architects from becoming overly attached to what they have created, an antipattern we call *Irrational Artifact Attachment*.

> **Irrational Artifact Attachment**
>
> The Irrational Artifact Attachment antipattern describes the proportional relationship between a person’s irrational attachment to some artifact and how long it took the person to produce that artifact. If an architect spends four hours creating a beautiful diagram in some tool like Visio, they’ll be even more irrationally attached to that artifact than if they’d invested only two hours.
>
> One benefit of the Agile approach to software development is that it involves creating “just-in-time” artifacts with as little ceremony and ritual as possible. This is one reason so many Agilists love index cards and sticky notes: using low-tech tools lets people throw away what’s not right, freeing them to experiment and allow the true nature of the artifact to emerge through revision, collaboration, and discussion.

The classic ephemeral artifact is a cell-phone photo of a whiteboard diagram (along with the inevitable “Do Not Erase!” imperative). These days, many architects have abandoned the whiteboard in favor of a tablet attached to an overhead projector. This offers several advantages. First, the tablet has an unlimited canvas and can fit as many drawings as the team might need. Second, it allows the team to copy/paste “what if” scenarios, which would obscure the original if done on a whiteboard. Third, images created on a tablet are already digitized and don’t have the inevitable glare of whiteboard photos. Fourth, using electronic images makes remote work much easier and more collaborative.

Eventually, you’ll need to create nice diagrams in a fancy tool, but before you invest that time, make sure the team has iterated on the design sufficiently. Whatever platform you’re using, you’ll find powerful diagramming tools. We happily used OmniGraffle for the original versions of all of the diagrams in this book, which were then refined by O’Reilly illustrators. While we don’t necessarily advocate one tool over another, we recommend looking for the following features, as a baseline:

- ***Layers*:** Drawing tools often support layers, which architects should learn to use well. Layers allow the user to link groups of items together logically and show or hide them as needed. For example, you might build a comprehensive diagram for a presentation, but hide the overwhelming details when not directly discussing them. Layers also provide a good way to present pictures that build incrementally.
- ***Stencils/templates*:** Stencil tools allow users to amass a library of common visual components, including composites of other basic shapes. For example, throughout this book, you have seen standard icons for things like individual microservices; these exist as single items in the authors’ stencil tool. Building a set of stencils for patterns and artifacts that are common within an organization creates consistency across architecture diagrams and makes it faster to build new diagrams.
- ***Magnets*:** Many drawing tools offer assistance for drawing lines between shapes. Magnets represent the places on those shapes where lines snap to connect automatically, providing alignment and other visual niceties. Some tools allow users to add more magnets or create their own.

> **Use Layers Semantically, Not Decoratively**
>
> We prefer drawing tools that support layers, but we suggest using them *semantically*— that is, in ways that contribute meaning to the overall image. For example, the base layer of each diagram should represent the topology of the architecture: its containers, databases, dependencies, brokers, and other core elements. This layer should focus on architecture rather than implementation; for instance, specify “synchronous communication” rather than naming a specific protocol. The next layer should contain implementation details: what type of database, which communication protocols, and so on.
>
> Using layers in this manner makes diagrams extensible: it’s possible to add other contextualized layers to present domain-driven design boundaries, transactional scope, or any other meta-information the architect wants to contrast against the topology of the architecture.

In addition to these specific helpful features, the tool should, of course, support basic functions such as lines, colors, shapes, and other visual artifacts, and should be able to export to a wide variety of formats.
