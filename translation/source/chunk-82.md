# Chapter 21: Architectural Decisions (continued)

## Architectural Significance

Many architects believe that if a decision involves a specific technology, then it’s not an architectural decision, but rather a technical decision. This is not always true. If an architect decides to use a particular technology because it directly supports a particular architecture characteristic (such as performance or scalability), then it’s still an architectural decision.

Michael Nygard, a well-known software architect and author of the second edition of *Release It!* (Pragmatic Bookshelf, 2018), addresses the problem of what decisions an architect should be responsible for (and hence what constitutes an architectural decision) by coining the term *architecturally significant*. According to Nygard, architecturally significant decisions are those that affect a system’s structure, non-functional characteristics, dependencies, interfaces, or construction techniques.

*Structure*, in this context, refers to decisions that affect the architecture patterns or styles being used. For example, a decision by an architect to share code between a set of microservices impacts the bounded context of the microservice, and thus affects the structure of the system.

The system’s *non-functional characteristics* are the architectural characteristics that are important for the system being developed or maintained. For example, if a choice of technology affects performance, and performance is an important aspect of the application, that choice becomes an architectural decision, even though it may specify a particular product, framework, or technology.

*Dependencies* refer to the coupling points between components and/or services within the system. Dependencies can affect architecture characteristics such as scalability, modularity, agility, testability, reliability, and so on, so decisions about dependencies become architectural decisions.

*Interfaces* refer to how services and components are accessed and orchestrated: usually through a gateway, integration hub, service bus, adapter, or API proxy. Making decisions about interfaces usually involves defining contracts, including versioning and deprecation strategies. Interfaces impact others using the system and hence are architecturally significant.

Finally, *construction techniques* refer to decisions about platforms, frameworks, tools, and even processes that, although technical in nature, might impact some aspect of the architecture.

## Architectural Decision Records

One of the most effective ways of documenting architectural decisions is through *Architectural Decision Records* (ADRs). Michael Nygard first evangelized ADRs in a 2011 blog post, and in 2017, Thoughtworks Technology Radar recommended the technique for widespread adoption.

An ADR consists of a short text file (usually one to two pages long) describing a specific architectural decision. While ADRs can be written using plain text or in a wiki page template, they are usually written in some sort of text document format, like AsciiDoc or Markdown.

Tooling is also available for managing ADRs. Nat Pryce, coauthor of *Growing Object-Oriented Software, Guided by Tests* (Addison-Wesley, 2009), has written an open source tool called ADR Tools that provides a command-line interface to manage ADRs, including numbering schemes, locations, and superseded logic. Micha Kops, a software engineer from Germany, provides some great examples of using ADR tools to manage architectural decision records.

### Basic Structure

The basic structure of an ADR consists of five main sections: *Title*, *Status*, *Context*, *Decision*, and *Consequences*. We usually add two additional sections as part of the basic structure: *Compliance* and *Notes*. The Compliance section is a space to think about and document how the architectural decision will be governed and enforced (manually or through automated fitness functions). The Notes section is a space to include metadata about the decision, such as the author, who approved it, when it was created, and so on.

It’s fine to extend this basic structure (as illustrated in Figure 21-2) to include any other needed section. Just keep the template consistent and concise. A good example of this might be to add an *Alternatives* section analyzing all the other possible solutions.

> **Figure 21-2.** Basic ADR structure

#### Title

ADR titles are usually numbered sequentially and contain a short phrase describing the architectural decision. For example, an ADR title describing a decision to use asynchronous messaging between the `Order` service and the `Payment` service might read: “42. Use of Asynchronous Messaging Between Order and Payment Services.” The title should be short and concise, but descriptive enough to remove any ambiguity about the nature and context of the decision.

#### Status

Every ADR has one of three statuses: *Proposed*, *Accepted*, or *Superseded*. The Proposed status means the decision must be approved by a higher-level decision maker or some sort of architectural governance body (such as an architecture review board). Accepted means the decision has been approved and is ready for implementation. Superseded means the decision has been changed and superseded by another ADR. The Superseded status always assumes that the prior ADR’s status was Accepted; in other words, a Proposed ADR would never be superseded by another ADR; it would be modified until Accepted.

The Superseded status is a powerful way of keeping historical records of what decisions have been made, why they were made at the time, what the new decision is, and why it was changed. Usually, when an ADR has been superseded, it is marked with the number of the decision that superseded it. Similarly, the decision that supersedes another ADR is marked with the number of the ADR it superseded.

For example, let’s say ADR 42 (“Use of Asynchronous Messaging Between Order and Payment Services”) is in Approved status. Due to later changes to the implementation and location of the `Payment` service, you decide that REST should now be used between the two services. You therefore create a new ADR (number 68) to document this changed decision. The corresponding statuses look as follows:

> *ADR 42. Use of Asynchronous Messaging Between Order and Payment Services*
> Status: Superseded by 68
>
> *ADR 68. Use of REST Between Order and Payment Services*
> Status: Accepted, supersedes 42

The link and history trail between ADRs 42 and 68 lets you avoid the inevitable “what about using messaging?” question regarding ADR 68.

> **ADRs and Request for Comments (RFC)**
>
> Sending a draft ADR out for comments can help an architect validate their assumptions and assertions with a larger audience of stakeholders. An effective way of engaging developers and initiating collaboration is creating a new kind of status called *Request for Comments* (RFC) and specifying a deadline for reviewers to complete their feedback. Once that date is reached, the architect can analyze the comments, make any necessary adjustments to the decision, make the final decision, and set the status to Proposed (or Accepted, if the architect has authority to approve the decision).
>
> An ADR with RFC status would look as follows:
>
> *STATUS*
> *Request For Comments, Deadline 09 JAN 2026*

Another significant aspect of the Status section of an ADR is that it forces the architect and their boss or lead architect to discuss the criteria for approving an architectural decision and determine whether the architect can do so on their own, or whether it must be approved through a higher-level architect, architecture review board, or some other governing body.

Three good starting places for these conversations are cost, cross-team impact, and security. Cost should include software purchase or licensing fees, additional hardware costs, and the overall level of effort to implement the architectural decision. To estimate this, multiply the estimated number of hours to implement the architectural decision by the company’s standard *full-time equivalency* (FTE) rate. The project owner or project manager usually has the FTE amount. This conversation might lead everyone to agree that, for example, if the cost of the architectural decision exceeds a certain amount, then it must be set to a Proposed status and approved by someone else. If the architectural decision impacts other teams or systems or has any sort of security implications, then it must be approved by a higher-level governing body or lead architect.

Once the team establishes and agrees on the criteria and corresponding limits (such as “costs exceeding $5,000 must be approved by the architecture review board”), document it well so that all architects creating ADRs will know when they can and cannot approve their own architectural decisions.
