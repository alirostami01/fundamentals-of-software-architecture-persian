<!-- Source chunk 04 | PDF pages 40-43 | Chapter 2 opening: Architecture Versus Design, Strategic vs Tactical, Level of Effort, Significance of Trade-Offs | words: 921 -->

CHAPTER 2
Architectural Thinking
Architectural thinking is about seeing things with an architect’s eye—in other words,
from an architectural point of view. Understanding how a particular change might
impact overall scalability, paying attention to how different parts of a system interact,
and knowing which third-party libraries and frameworks would be most appropriate
for a given situation are all examples of thinking architecturally.
Being able to think like an architect first involves understanding what software
architecture is and the differences between architecture and design. It then involves
having a wide breadth of knowledge to see solutions and possibilities that others do
not see; understanding the importance of business drivers and how they translate
to architectural concerns; and understanding, analyzing, and reconciling trade-offs
between various solutions and technologies.
In this chapter, we explore these aspects of thinking like an architect.
Architecture Versus Design
Take a moment and picture your dream house in your mind. How many floors does
it have? Is the roof flat or peaked? Is it a big sprawling, single-story ranch house or
a multistory contemporary house? How many bedrooms does it have? All of these
things define the overall structure of the house—in other words, its architecture. Now
take a moment to picture the inside of the house. Does it have carpeting or hardwood
floors? What color are the walls? Are there floor lamps or lights hanging from the
ceiling? All of these things relate to the design of the house.
Similarly, software architecture is less about a system’s appearance and more about
its structure, whereas design is more about a system’s appearance and less about its
structure. For example, the choice to use microservices defines the structure and
17
shape of the system (its architecture), whereas the look and feel of the user interface
(UI) screen define the design of the system.
But what about decisions such as whether to break apart a service into smaller parts
or deciding on a UI framework? Unfortunately, most decisions such as these fall
somewhere on a spectrum between architecture and design, making it difficult to
determine what should be considered architecture.
Leveraging the following criteria can help determine whether something is more
about architecture or more about design:
• Is it more strategic in nature or more tactical?•
• How much effort will it take to change or construct?•
• How significant are the trade-offs?•
These factors are shown in Figure 2-1, illustrating the spectrum between architecture
and design to help determine where a decision lies and who should have the responsibility for it.
Figure 2-1. The spectrum between architecture and design
Strategic Versus Tactical Decisions
The more strategic a decision, the more architectural it becomes. Conversely, the
more tactical a decision, the more it’s likely to be about design. Strategic decisions are
generally long-term, whereas tactical decisions are generally short-term and usually
independent of other actions or decisions.
One good way to determine whether a decision is more strategic or tactical is to
consider the following questions:
How much thought and planning is involved in the decision?
A decision that takes a couple of minutes is more likely to be tactical and hence
more about design, whereas a decision requiring weeks of planning is likely to be
more strategic and hence more about architecture.
How many people are involved in the decision?
A decision made alone or with a colleague is likely more tactical and on the
design side of the spectrum, whereas a decision requiring lots of meetings with
many different stakeholders is likely more strategic and on the architectural side
of the spectrum.
Is the decision a long-term vision or a short-term action?
A decision that is likely to change soon is usually tactical in nature and would be
more about design, whereas one that will last a very long time is typically more
strategic and more about architecture.
While these questions are a bit subjective, they nevertheless help in determining
whether something is strategic or tactical, and thus more about architecture or
design.
Level of Effort
In his famous paper “Who Needs an Architect?” , software architect Martin Fowler
writes that architecture is “the stuff that’s hard to change. ” The harder something is to
change, generally, the more effort is required, placing that decision or activity toward
the architectural side of the spectrum. Conversely, something that requires minimal
effort to implement or change places it more on the design side of the spectrum.
For example, moving from a monolithic layered architecture to microservices would
require significant effort, so it would be more about architecture. Rearranging fields
on a screen would require minimal effort, and therefore be more about design.
The Significance of Trade-Offs
Analyzing the trade-offs of a particular decision can help a lot in determining
whether it is more about architecture or design. The more significant the trade-offs
are, the more architectural the decision tends to be. For example, choosing to use
the microservices architecture style provides better scalability, agility, elasticity, and
fault tolerance. However, this architecture is highly complex, is very expensive, has
poor data consistency, and doesn’t perform well due to service coupling. These are
some pretty significant trade-offs. We can conclude that this decision is more on the
architectural side of the spectrum than design.
Even design decisions have trade-offs. For example, breaking apart a class file provides better maintainability and readability—at the cost of managing more classes.
Architecture Versus Design | 19
These trade-offs are not overly significant (especially compared to microservices’
trade-offs), so this decision is more on the design side of the spectrum.
