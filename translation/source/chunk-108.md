<!-- Source chunk 108 | PDF pages 517-519 | Chapter 27: Second Law, Out of Context antipattern, Spectrum Between Extremes, Parting Words of Advice | words: 884 -->
# Chapter 27: The Laws of Software Architecture, Revisited (continued)

## Second Law: Why Is More Important Than How

Our second law emphasizes the importance of *why* over *how*. As experienced architects, we can look at an existing system and tell someone *how* it works. However, there will be some decisions where it isn’t clear *why* the previous architect chose this option over another, because they didn’t record all of the decision criteria with their ultimate solution.

This is why we emphasize the importance of using both architecture diagrams *and* ADRs (covered in Chapter 21). Every trade-off analysis generates a tremendous amount of context that doesn’t appear in the solution. It’s critical to document that analysis (along with the known compromises and limitations of the solution) to prevent future architects (who might be you) from having to redo the analysis just to understand *why*.

### Out of Context Antipattern

One antipattern that’s common in trade-off analysis is the *Out of Context* antipattern. This antipattern occurs when the architect understands the trade-offs but not how to *weight* all of them based on the current context.

Consider the trade-off analysis we did in “Shared Library Versus Shared Service” on page 488. Taken objectively, the shared library appears to be the preferred solution, since it achieved more positive than negative assessments. However, this trade-off analysis has a potential flaw: do all of its criteria have equal weight?

Imagine that a team has code in several platforms. They aren’t overly concerned with performance or scale, but want a clean way to manage shared behavior. In this case, the first two trade-off criteria carry a much higher priority, which should lead them to choose the shared service. As a bonus, the team has already figured out what issues they will have to mitigate.

Architects rely on experience to build trade-off criteria, but must also weigh those criteria to find the correct fit for the solution. Generic trade-off analysis isn’t very useful—it only becomes valuable when applied in a specific context.

## The Spectrum Between Extremes

In our first edition, we identified only two laws. However, we have gradually realized that a third law exists:

> Most architecture decisions aren’t binary but rather exist on a spectrum between extremes.
>
> —Third Law of Software Architecture

It would be nice to live in a world with nice, clean, binary decisions—but software architecture doesn’t exist in that world. People often observe how difficult it is to come up with comprehensive definitions of important concepts in software architecture: architecture versus design, orchestration versus choreography, topics versus queues, and so on. The underlying reason is that the decision criteria aren’t binary; they lie along a rather messy spectrum.

In “Architecture Versus Design” on page 17, we discussed the spectrum between architecture and design and how to determine where a particular decision lies within that spectrum. In fact, this law provides a useful way to think about decisions that are closer to the software architecture side of the spectrum than the design side:

> A software architecture decision is one where each of the options has significant trade-offs.

If everything in software architecture is a trade-off, then an architectural decision must involve trade-offs for each option.

As an architect, don’t try to reduce every decision to a binary—few of those exist in our world. That’s one of the reasons that every answer in software architecture is “it depends”—it depends on where on the spectrum of possible solutions the criterion in question falls.

As architects, we make our decisions in a swamp of uncertainty. Accommodating this is annoying, but necessary. Not only do we sometimes have to base important decisions on incomplete information, but often the decision wouldn’t be clear-cut, even if we had the full scoop, because it resides somewhere on a spectrum between two extremes.

Welcome to software architecture!

## Parting Words of Advice

> How do we get great designers? Great designers design, of course.
>
> —Fred Brooks

> So how are we supposed to get great architects, if they only get the chance to architect fewer than a half-dozen times in their career?
>
> —Ted Neward

Practice is the proven way to build skills and become better at anything in life, including architecture. We encourage new and existing architects to keep honing their skills in the craft of designing architecture as well as widening their individual technology breadth. To that end, we’ve created some architecture katas modeled after the examples in this book, which you can find on the companion website. We encourage you to use them to practice and build your skills in architecture.

People who use our katas often ask: is there an answer guide somewhere? Unfortunately, no. To quote Neal:

> There are not right or wrong answers in architecture—only *trade-offs*.

When your authors started using architecture katas during our live training classes, we initially kept the drawings the students produced, with the goal of creating an answer repository. We quickly gave up, though, because we realized that these were incomplete artifacts. The teams had captured *how* they implemented their solutions with drawings of topologies. The *why* was much more interesting—but while they explained the trade-offs they considered in class, they didn’t have the time to create architecture decision records. Keeping just the *how* meant we had only half of the story.

So, our parting words of advice: always learn, always practice, and *go do some architecture*!
