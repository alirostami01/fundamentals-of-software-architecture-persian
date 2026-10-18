# Chapter 19: Choosing the Appropriate Architecture Style

It depends! With all the choices available (and new ones arriving almost daily), we would like to tell you which architecture style you should use—but we can’t. Nothing is more contextual to a number of factors within an organization and what software it builds. Choosing an architecture style represents the culmination of a whole process of analysis and thought about trade-offs for architecture characteristics, domain considerations, strategic goals, and a host of other things. That’s why, as we said back in Chapter 2, it depends.

However contextual the decision is, this chapter offers some general advice around choosing an appropriate architecture style.

## Shifting “Fashion” in Architecture

The software industry’s preferences in architecture styles shift over time, driven by a number of factors. These include:

**Observations from the past:** New architecture styles generally arise from observations about past experiences, especially observations about pain points. Architects’ experiences working with systems—which are often what lead us to become architects in the first place—influence our thoughts about future systems. New architecture designs often reflect fixes for the specific deficiencies encountered in past architecture styles. For example, after building architectures that centered on code reuse, architects realized the negative trade-offs and seriously rethought the implications of reusing code.

**Changes in the ecosystem:** In the software development ecosystem, everything changes all the time. This constant change is so chaotic that it’s impossible to even predict what type of change will come next. Not too many years ago, no one knew what Kubernetes was, and now it is a daily feature of many developers’ lives. In a few more years, Kubernetes may be replaced with some other tool that hasn’t been written yet.

**New capabilities:** Architects must keep a keen eye open not only for new tools but for new paradigms. When new capabilities arise, architecture can shift to an entirely new paradigm, rather than merely replacing one tool with another. For example, few anticipated the tectonic shift in the software development world caused by the advent of containers such as Docker. While that was an evolutionary step, it had an astounding impact on architects, tools, engineering practices, and so much more. Constant change in the ecosystem also regularly delivers new tools and capabilities. Even something that looks like a new one-of-something-we-already-have could include nuances that make it a game changer. New features don’t even have to rock the entire development world: a minor change that aligns exactly with an architect’s goals can change everything.

**Acceleration:** Not only does the ecosystem constantly change, but change keeps getting faster and more pervasive. New tools create new engineering practices, which lead to new designs and capabilities, keeping software architects in a constant state of flux. The rise and influence of generative AI is an outstanding example of this constant evolution and corresponding unpredictability.

**Domain changes:** The domains for which we write software constantly shift and change, as businesses evolve or merge with other companies.

**Technology changes:** Organizations try to keep up with at least some technological changes, especially those with obvious bottom-line benefits.

**External factors:** Many external factors only peripherally associated with software development can drive change within an organization. For example, architects and developers might be perfectly happy with a particular tool, but if its licensing cost becomes prohibitive, the business might be forced to migrate to another option.

Architects should understand current industry trends so they can make intelligent decisions about which trends to follow and when to make exceptions, regardless of how closely their organization follows current architecture fashion.

## Decision Criteria

When choosing an architectural style, architects must account for all the various factors that contribute to the domain design structure. Fundamentally, an architect designs two things: whatever domain has been specified, and the structural elements required to make the system a success (provided by architectural characteristics).

Only approach choosing an architectural style when you have sufficient knowledge about the following factors:

**The domain:** Understand as many important aspects of the business domain as you can, especially those that affect operational architecture characteristics. Architects don’t have to be subject matter experts, but should at least have a good general understanding of the major aspects of the domain under design. Other specialists, such as business analysts, can help you fill any gaps in your domain knowledge.

**Architecture characteristics that impact structural decisions:** Identify and elucidate which architecture characteristics are needed to support the domain and other external factors by conducting an architectural characteristics analysis, one of the core activities in choosing a style.

It’s possible to implement any of the generic architecture styles in pretty much any problem domain—generic implies that they are general-purpose, after all. The exceptions are domains that require special operational architectural characteristics, like a highly scalable auction site. However, in most cases, the real differences between architectural styles concern not the domain, but how well each style supports various architectural characteristics.

You may have noticed that the star charts we’ve used in Part II of this book to compare each architecture style focus on architectural characteristics, not domains. This reflects the importance of understanding architectural characteristics when choosing a style.

**Data architecture:** Architects and data developers must collaborate on databases, schemas, and other data-related concerns. Data architecture is a specialization in its own right, and we don’t cover it much in this book, outside of style-specific considerations. However, you need to understand the impact a given data design might have on your architectural design, particularly if the new system must interact with an older data architecture or one that’s already in use.

**Cloud deployments:** Using the cloud as an architectural destination is the latest in a long line of fundamental shifts in where computation and data reside. The trade-offs involved in designing an application to run on-premises are quite different from those involved in designing one for the cloud. It’s important to know how much data the application will need to store and how much data can move around (which can incur significant costs), among a host of other concerns.

The cloud is a great example of how sophisticated capabilities become commodities over time. A decade ago, building a highly elastic and scalable on-prem system required esoteric skills and was seen as almost magical. Now, architects can achieve the same results just by changing their cloud provider’s configuration parameters.

**Organizational factors:** Many external factors influence design. For example, the cost of a particular cloud vendor may prevent a business from adopting what would otherwise be the ideal design. Likewise, knowing that the company plans to engage in mergers and acquisitions might encourage an architect to gravitate toward open solutions and integration architectures.

**Knowledge of process, teams, and operational concerns:** Many specific project factors influence architects’ designs: the software development process, an architect’s interaction (or lack of) with operations, and the QA process. For example, if an organization lacks maturity in Agile engineering practices, architecture styles that rely on those practices for success (such as microservices) will present difficulties.
