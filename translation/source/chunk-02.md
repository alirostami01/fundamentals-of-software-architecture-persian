<!-- Source chunk 02 | PDF pages 30-34 | Laws (corollaries, 2nd/3rd laws) + Expectations of an Architect (intro-Ensure Compliance) | words: 1239 -->

Nothing exists on a nice, clean spectrum. Every decision a software architect makes
must account for a large number of variables that take on different values depending
on the circumstances. Trade-offs are the essence of software architecture decisions.
If you think you’ve discovered something that isn’t a trade-off, more likely you just
haven’t identified the trade-off…yet.
—Corollary 1
You can’t just do trade-off analysis once and be done with it.
—Corollary 2
Teams love standards, and it would be nice if architects could just do One Big
Trade-off Jamboree to decide on our defaults for which architecture styles to use, how
parts of the architecture should communicate, how to manage shared functionality,
and a host of other sticky decisions. But we can’t, because every situation requires
us to re-evaluate all those trade-offs. (We’ve seen teams try to do this—for example,
attempting to default to using only choreography in distributed workflows, only to
discover that it works sometimes and is a spectacular disaster at other times. See
“Choreography and Orchestration” on page 341 for our discussion.)
Architecture is broader than just the combination of structural elements, which is
why our dimensional definition incorporates principles, characteristics, and so on.
This is reflected in our Second Law of Software Architecture:
Why is more important than how.
—Second Law of Software Architecture
As an experienced architect, if someone shows me an architecture I’ve never seen
before, I can understand how it works, but I might struggle with why the previous
architect or team made certain decisions. Architects make decisions within extremely
specific contexts, making sweeping and generic decisions difficult. Why an architect
made a particular decision includes the trade-offs they considered, adding to the
context of why this decision versus another. It turns out that one of the defining
characteristics of software architecture decisions is they are rarely binary. This brings
us to the Third Law of Software Architecture:
Most architecture decisions aren’t binary but rather exist on a spectrum between
extremes.
—Third Law of Software Architecture
Throughout the book, we highlight why architects make certain decisions along with
trade-offs. We also highlight good techniques for capturing important decisions in
Chapter 21.
Readers will recognize these laws at work throughout the book, and we recommend
keeping them in mind when evaluating software architecture decisions. We come
back to these laws in Chapter 27 with some additional examples.
With a working definition of software architecture in place, let’s move into the role
itself. 
Expectations of an Architect
The role of a software architect can range from acting as an expert programmer
to defining an entire company’s strategic technical direction. This makes trying to
define it a fool’s errand, but what we can tell you more readily is what’s expected of a
software architect. We’ve identified eight core expectations for any software architect,
irrespective of their role, title, or job description:
- Make architecture decisions
- Continually analyze the architecture
- Keep current with latest trends
- Ensure compliance with decisions
- Understand diverse technologies, frameworks, platforms, and environments
- Know the business domain
- Lead a team and possess interpersonal skills
- Understand and navigate organizational politics
Succeeding as a software architect depends on understanding and living up to each of
these expectations. This section looks at all eight in turn.
Make Architecture Decisions
An architect is expected to define the architecture decisions and design principles used
to guide technology decisions within the team, within the department, or across the
enterprise.
Guide is the key word in this first expectation: architects should guide technology
choices rather than specify them. For example, deciding to use React.js for frontend
development is a technical decision rather than an architectural decision. Instead of
making this decision, the architect should instruct the development teams to use a
reactive-based framework for frontend web development, guiding them to choose
Angular, Elm, React.js, Vue, or any of the other reactive-based web frameworks. The
key is asking whether the architecture decision will guide teams in making the right
technical choices or make the choice for them. That said, there are some occasions
where architects need to make specific technology decisions in order to preserve a
particular architectural characteristic, such as scalability, performance, or availability.
Architects often struggle with finding this balance, so Chapter 21 is entirely about
architecture decisions.
Continually Analyze the Architecture
An architect is expected to continually analyze the architecture and the current technology environment and recommend solutions for improvement.
Architecture vitality assesses how viable an architecture that was defined three or
more years ago is today, given changes in both business and technology. In our
experience, not enough architects focus their energies on continually analyzing
existing architectures. As a result, most architectures experience elements of structural decay, which occurs when developers make coding or design changes that
impact the required architectural characteristics, such as performance, availability,
and scalability.
Other frequently forgotten aspects of this expectation are testing and release environments. Being able to modify code quickly is a kind of agility with obvious benefits,
but if it takes weeks to test the changes and months to release, the overall architecture
cannot achieve agility.
Architects must holistically analyze changes in the technology and the problem
domain to determine the ongoing soundness of the architecture. This kind of consideration is what keeps applications relevant, even if it rarely appears in job postings.
Keep Current with Latest Trends
An architect is expected to keep current with the latest technology and industry trends.
Developers must keep up to date on the latest technologies, as well as those they
use on a daily basis, to remain relevant (and to retain a job!). It’s even more critical
for architects to keep current on the latest technical and industry trends. Architects’
decisions tend to be long-lasting and difficult to change. Understanding trends helps
architects make decisions that will remain relevant into the future. For example,
architects in recent years have needed to learn about cloud-based storage and deployment, and as we write this second edition, generative AI is having a massive impact
on many parts of the development ecosystem.
Tracking trends and keeping current with those trends is hard, particularly for a
software architect. In Chapter 2, we discuss some techniques and resources for how
to do this.
Ensure Compliance with Decisions
An architect is expected to ensure compliance with architecture decisions and design
principles.
Ensuring compliance means continually verifying that the development teams are following the decisions and design principles defined, documented, and communicated
by the architect.
Imagine that you, as an architect, make a decision to restrict access to the database in
a layered architecture to only the Business and Services layers (not the Presentation
layer). This (as you’ll see in Chapter 10) means that the Presentation layer must go
through all layers of the architecture to make even the simplest of database calls.
However, a user interface (UI) developer disagrees with this decision and gives the
Presentation layer direct access to the database for performance reasons. You made
that architecture decision for a specific reason: so that changes to the database
changes would not affect the Presentation layer. If you aren’t ensuring compliance
with your architecture decisions, violations like this can occur. The result can be that
the architecture fails to provide the required characteristics, and the application or
system does not work as expected. In Chapter 6, we talk about measuring compliance
using automated fitness functions and other tools.
