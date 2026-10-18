<!-- Source chunk 106 | PDF pages 510-513 | Chapter 27 opening: intro, First Law, Shared Library Versus Shared Service | words: 1195 -->
# Chapter 27: The Laws of Software Architecture, Revisited

Way back in Chapter 1, we described the three laws of software architecture:

- Everything in software architecture is a trade-off.

- *Why* is more important than *how*.

- Most architecture decisions aren’t binary but rather exist on a spectrum between extremes.

Just about every example in this book has illustrated these laws, which points to their origin story. When we wrote the first edition, we hoped to find numerous things that seemed universally true about software architecture and codify them as *laws*. To our surprise, we ended up identifying just two laws in the first edition, then uncovered one more while writing the second. True to our original intent, these three laws seem pretty universal and inform many important perspectives for working software architects.

In this brief chapter, we’ll revisit these laws in light of the examples we’ve shown and point out some nuances about trade-off analysis.

## First Law: Everything in Software Architecture Is a Trade-Off

Our first law is one of the defining characteristics of software architecture—everything is a trade-off. Many people think that the job of a software architect is to find silver bullet solutions to sticky problems and become a hero, but that rarely happens.

(Architects rarely get credit for good decisions, but always get blamed for bad ones.) No, the real job of software architecture is analyzing trade-offs.

We believe, for a couple of reasons, that every architect should hone their reputation as an objective arbiter of trade-offs, rather than evangelizing for a particular approach.

First, evangelism in architecture is dangerous in the long term, because yesterday’s best practice tends to become tomorrow’s antipattern. Architects make trade-off decisions based on current factors and situations as best they can, with incomplete knowledge. However, even if a decision is sound when it’s made, the software development ecosystem exists in a constant state of evolution and churn, which means that the circumstances slowly change and are likely to eventually weaken (or invalidate) the decision. If the architect has invested social capital in evangelizing for that solution, their reputation may suffer when that decision must change later. Always stay clear-eyed and objective about technology choices to avoid attaching your credibility to a decision that didn’t age well.

Second, decision makers in organizations aren’t really looking for enthusiastic advocacy so much as sober objectivity. An architect who develops a reputation as the go-to person for an objective trade-off analysis becomes a valuable asset to their organization. When the decision is critical, decision makers want someone whose judgment they can trust; that should be you.

Let’s look at some examples of trade-off analysis for a couple of software architecture decisions, and then discuss a common gap in understanding.

### Shared Library Versus Shared Service

A common conundrum for architects involves shared behavior in distributed architectures, such as microservices or EDA: should we use a shared library that is compiled into each service at build time, or use a shared service that other services call at runtime, as illustrated in Figure 27-1?

Figure 27-1. Should the solution use a shared library or shared service for common functionality?

In Figure 27-1, the service on the left encapsulates the shared behavior, and other services call to access it. On the right, we have a shared library, which is compiled into each service before deployment. Which is better?

By now, readers know the answer to all such questions: “It depends!” But you need to answer the inevitable follow-up question: “Depends on what?” Like many nontrivial decisions in software architecture, the answer to this question isn’t immediately obvious, so it’s time for you, as the architect, to undertake trade-off analysis.

First, you must determine all the contextualized trade-offs that make a difference for this solution. This list will be highly specific to both the organization and the solution, so you’ll need to rely on your knowledge of the organization, technology landscape, team capabilities, budgets, and everything else that informs your trade-off options. For this solution, we’ve created the following list of pertinent factors:

*Heterogeneous code*

If solutions are written in multiple platforms, then the service will be easier to work with because, regardless of the technology stack, callers access the service via the network, making the implementation platform irrelevant. For the library, the team will need a version of the code for each technology stack and will have to keep the versions in sync, greatly adding to the project’s overall complexity.

*High code volatility*

Recall that code volatility measures how fast the code changes (commonly known as *churn*). In a service, callers access new functionality as soon as they deploy the updated service, so if you need to change the library, you’ll have to recompile and deploy each service to take advantage of the new features.

*Ability to version changes*

Versioning is much easier in the library than in the service. When the library needs to update, the team can resolve the version differences at compile time and build just what they need. For the service, version information must be determined at runtime, which complicates the interaction with the service.

*Overall change risk*

Change risk is better for the library. Once you change the library code and successfully compile it into the service, you can have high confidence that it will work. The service, on the other hand, may change without any compile-time verification, which raises the potential likelihood of a runtime fault at invocation time.

*Performance*

The library will clearly have better performance, as the calls to shared functionality are in-process calls, compared to the network calls required for the service. These calls will be much slower than in-process calls because of network latency and other factors.

*Fault tolerance*

As we discussed in Chapter 9, runtime access to services always suffers potential network issues, including the service in question here. The library provides better fault tolerance: once you compile, test, and deploy the service, you can have high confidence that it is stable.

*Scalability*

Just like performance, calls between services suffer from latency, which diminishes scalability. Thus, the library will offer better scalability, as access to the shared behavior is a very efficient in-process call.

Once you’ve determined your list of important factors, you can create a matrix to compare how well each does for each criterion, as shown in Table 27-1.

Table 27-1. Trade-offs between shared service and shared library

| Factor | Shared library | Shared service |
|---|---|---|
| Heterogeneous code | - | + |
| High code volatility | - | + |
| Ability to version changes | + | - |
| Overall change risk | + | - |
| Performance | + | - |
| Fault tolerance | + | - |
| Scalability | + | - |

The accumulation of positives for the shared library makes it the winner…at least, for these factors and in this context. It may or may not be the solution to the problem at hand—you may need to apply additional weighting (see “Second Corollary: You Can’t Do It Just Once” on page 494 for more details)—but now you and your team have a good idea of the forces at play.

