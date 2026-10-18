<!-- Source chunk 03 | PDF pages 34-36 | Expectations (Diverse Tech-Politics) + Roadmap; end of Chapter 1 | words: 1077 -->

Understand Diverse Technologies
An architect is expected to have exposure to multiple and diverse technologies, frameworks, platforms, and environments.
Every architect isn’t expected to be an expert in every framework, platform, and
language, but they should at least be familiar with a variety of technologies. Most
environments these days are heterogeneous, so at a minimum, architects should
know how to interface with multiple systems and services, whatever their language,
platform, or technology.
One of the best ways to meet this expectation is to stretch outside your comfort
zone, aggressively seeking out opportunities to gain experience in multiple languages,
platforms, and technologies. Architects should focus on technical breadth rather than
technical depth. Technical breadth includes the stuff you know about, but not at a
detailed level, combined with the stuff you know a lot about. For example, it’s far
more valuable for an architect to be familiar with the pros and cons of 10 different
caching products than to be an expert in only one of them.
Know the Business Domain
An architect is expected to have a certain level of business-domain expertise.
Effective software architects understand the business problem, goals, and requirements the architecture is intended to solve, collectively known as the business domain
of a problem space. It’s difficult to design an effective architecture if you don’t
understand the requirements of the business. Imagine being an architect at a major
bank and not understanding common financial terms like average directional index,
aleatory contracts, rates rally, or even nonpriority debt. You wouldn’t be able to communicate with stakeholders and business users and would quickly lose credibility.
The most successful architects we know have broad, hands-on technical knowledge
and a strong knowledge of a particular domain. They can communicate with C-level
executives and business users in language these stakeholders know and understand,
creating confidence that they know what they’re doing and are competent to create an
effective and correct architecture.
Possess Interpersonal Skills
An architect is expected to possess exceptional interpersonal skills, including teamwork,
facilitation, and leadership.
As technologists, developers and architects tend to prefer solving technical problems,
not people problems, so exceptional leadership and interpersonal skills are a difficult
expectation. However, as Gerald Weinberg was famous for saying, “No matter what
they tell you, it’s always a people problem. ” The guidance that architects provide is not
only technical—it includes leading the development teams through implementing the
architecture. Leadership skills are at least half of what it takes to become an effective
software architect, regardless of role or title.
The industry is flooded with software architects, all competing for a limited number
of positions. Those with strong leadership and interpersonal skills stand out from
the crowd. Conversely, we’ve known many software architects who are excellent technologists but struggle to lead teams, coach and mentor developers, or communicate
ideas and architecture decisions and principles. Needless to say, those architects have
difficulties holding down a job.
Understand and Navigate Politics
An architect is expected to understand the political climate of the enterprise and be able
to navigate its politics.
It might seem strange to talk about office politics in a book about software architecture, but negotiation skills are crucial to the role. To illustrate, consider two scenarios.
In the first scenario, a developer decides to leverage a particular design pattern to
reduce the complexity of a particular piece of convoluted code. That’s a fine decision,
and the developer does not need to seek approval for it. Programming aspects such as
code structure, class design, design-pattern selection, and sometimes even language
choice are all part of the art of programming.
In the second scenario, the architect responsible for a large customer relationship
management (CRM) system is having difficulty controlling database access from
other systems, securing certain customer data, and making changes to the database
schema. All of these problems stem from too many other systems using the CRM
database. The architect therefore decides to create application silos, where each application database is only accessible from the application that owns that database. This
decision will give the architect better control over the customer data, security, and
changes.
However, unlike the developer’s decision in the first scenario, the architect can expect
almost everyone in the company to challenge their decision (with the possible exception of the CRM application team). Other applications need the CRM data, and if
they can no longer access the database directly, they must ask the CRM system for
the data via remote access calls. Product owners, project managers, and business
stakeholders may object to increases in their costs or effort, while developers may feel
their approach is better. Almost every decision an architect makes will be challenged.
Whatever the objections, the architect must navigate organizational politics and apply
negotiation skills to get most decisions approved. This can be very frustrating; most
software architects started as developers and got used to making decisions without
approval or even review. As architects, they’re now finally able to make broad and
important decisions, but they must justify and fight for almost every one. Negotiation
skills, like leadership skills, are so necessary that we’ve dedicated an entire chapter to
them (Chapter 25).
Roadmap
This book consists of three parts:
Part I: Foundations
Part I defines the key components of software architecture, focusing on the two
key elements of architectural structure: architectural characteristics and logical
components. Analyzing each of these requires different techniques, which we
cover in depth. The outputs of these activities provide the software architect with
enough information to choose an appropriate architectural style to provide a
scaffolding for the general philosophy of the implementation.
Part II: Architecture Styles
Part II provides a catalog of architectural styles, the named topologies of software
architecture. We show the structural and communication differences in each
style, and provide a basis for comparison along a wide spectrum, including data
topologies, teams, and physical architectures.
Part III: Techniques and Soft Skills
Parts I and II focus on technical aspects of the job, but a major part of the role
of software architect involves what are traditionally called soft skills: skills that
involve other people instead of technology. Ironically, soft skills are often the
most difficult for burgeoning architects to acquire, because the main pathways
to the software architect role typically involve more technical than interpersonal
brilliance. However, once on the job, architects discover that these skills are
vitally important. Thus, Part III of our book covers some critical soft skills to help
you succeed in the role.
