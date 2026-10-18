# Chapter 17: Orchestration-Driven Service-Oriented Architecture (continued)

## Cloud Considerations

Orchestration-driven SOA predates the cloud by several decades, so no consideration exists for building this architecture (in its original incarnation) in the cloud.

However, the current-day use of this style makes it a good integration architecture for cloud and on-premises services that must integrate and participate in workflows. As primarily an integration architecture, it works well with cloud-based services and facilities.

## Common Risks

At the end of the last century and the beginning of this one, the big risks for this architecture were primarily about how much it cost, how long it took to implement, and (a shocking surprise) how difficult these systems are to maintain and update. Many of these projects were very expensive multiyear endeavors, with critical decisions made high in the company hierarchy. Rather than call these projects “failures,” companies mostly just transformed them into integration architectures with better boundaries, more closely aligned with the ideas of DDD.

When architects use an ESB in a modern system as an integration facility, the biggest risk is the slippery slope of allowing the ESB to gradually encapsulate the entire architecture. This is called the Accidental SOA antipattern: where an architect gradually and unintentionally builds a fully orchestration-driven SOA without realizing it. To avoid Accidental SOA, an architect must ensure reasonable encapsulation boundaries for orchestration and pay close attention to issues like transactional boundaries.

## Governance

When this architecture was popular, modern-day holistic testing was uncommon. Teams rarely tested SOA outside of formal quality-assurance-level testing, so tool and framework creators gave little consideration to facilitating testing the individual parts. Some testing frameworks emerged to create mocks and stubs for the massive machinery of the message bus and its related moving parts, but they were always cumbersome and inconsistent.

Governance suffered from the same limitations. The idea of automating architectural governance was even more foreign than automating testing. In this era, “governance” meant heavyweight frameworks, meetings, and code reviews—all manual.

However, architects still use ESBs strategically within organizations that need the particular mix of capabilities they offer. In particular, many companies have legacy systems that must interact with more modern systems, often combining results and aggregating behavior—all of which describes the central functionality of an ESB. In these scenarios, fitness functions can serve a critical role in preventing data or bounded contexts from “leaking” across parts of the ecosystem where they shouldn’t appear.

For example, consider a system that uses an ESB to coordinate between an enterprise resource planning (ERP) package, an online sales tool, and more modern microservices-based `Accounting` services. In this scenario, the system should only read from the ERP and sales systems and should write to the `Accounting` microservices. Architects can first build a fitness function that ensures that all communication is written consistently to logs, then write something like the following fitness function (given here in pseudocode):

```text
READ logs for ERP into ERP-logs for past 24 hours
READ logs for Sales into Sales-logs for past 24 hours
FOREACH entry IN ERP-logs
    IF 'operation' is 'update' and 'target' != 'accounting' THEN
       raise fitness function violation
            "Invalid communication between integration points"
    END IF
FOREACH entry IN Sales-logs
    IF 'operation' is 'update' and 'target' != 'accounting' THEN
       raise fitness function violation
            "Invalid communication between integration points"
    END IF
```

This fitness function reads the log entries from both integration points to ensure that no update operations take place whose target isn’t the `Accounting` system.

Using such fitness functions, architects can use tools like ESBs strategically while building guardrails around the places where teams typically misuse them.

## Team Topology Considerations

Just as architects did not consider data topologies for orchestration-driven SOA, the same is true for team topologies, which was an unknown topic when this architecture style was popular.

In fact, the strict taxonomy of this style serves as a communication antipattern that led architects to develop the principles of team topologies. The goal in this architecture is extreme separation of responsibilities, with a corresponding separation of team members. Among the companies that adopted it, it was rare indeed for someone building business services to chat with someone building enterprise services. They were expected to communicate through technical artifacts, such as contracts and interfaces. The level of abstraction in this style creates many integration layers, each implemented by different teams, using enterprise-level ticketing tools to communicate. It should be easy to see why developers find it time-consuming to build features in this style.

## Style Characteristics

Many of the criteria we now use to evaluate architecture styles were not priorities when orchestration-driven SOA was popular. The Agile software movement had just started and had not yet penetrated the large organizations likely to use this architecture.

A one-star rating in the characteristics ratings table in Figure 17-5 means the specific architecture characteristic isn’t well supported in the architecture, whereas a five-star rating means the architecture characteristic is one of the style’s strongest features. Definitions for the characteristics identified in the scorecard can be found in Chapter 4.

SOA is perhaps the most technically partitioned general-purpose architecture ever attempted! In fact, the backlash against the disadvantages of this structure led to more modern architectures, such as microservices. SOA has a single quantum, even though it is a distributed architecture, for two reasons. First, it generally uses a single database or just a few, creating coupling points across many different concerns. Second, and more importantly, the orchestration engine acts as a giant coupling point—no part of the architecture can have different characteristics than the mediator that orchestrates all behavior. Thus, this architecture manages to find the disadvantages of both monolithic and distributed architectures.

Figure 17-5. Service-oriented architecture characteristics ratings

Modern engineering goals such as deployability and testability score disastrously in this architecture, both because they are poorly supported and because those were not important (or even aspirational) goals when it was developed.

This architecture does support some goals, such as elasticity and scalability, despite the difficulties in implementing them. Tool vendors poured enormous effort into making these systems scalable by building session replication across application servers and other techniques. However, this being a distributed architecture, performance has never been a highlight, because each business request is split across so much of the architecture.

Because of all these factors, simplicity and cost have the inverse of the relationship most architects would prefer. Orchestration-driven SOA was an important milestone because it taught architects the practical limits of technical partitioning and how difficult distributed transactions can be in the real world.

## Examples and Use Cases

The primary examples of this architecture existed in the late 1990s and early 2000s in many large enterprises. They have gradually been displaced by more agile and domain-based distributed architectures, like microservices. Even large enterprises have realized that change is inevitable and that software isn’t static and needs to change with market forces and new capabilities.

Architects built orchestration-driven SOA architectures to try to achieve effective reuse across large organizations, but eventually realized how difficult their strict and elaborate taxonomy makes implementing common changes and updates. For example, a common domain change might be to update details about a single entity. On a lucky day, developers might only need to change components in the enterprise services layer to do the job. However, on a bad day (one where enterprise architects and/or business stakeholders didn’t anticipate this type of change), developers might have to update four or five layers in the architecture, making highly coupled changes in each. Architects working in this style dread hearing the word change because it requires deep analysis, and the scope of the work is so variable.

As we mentioned in “Governance” on page 324, architects still use the building blocks of orchestration-driven SOA (such as the ESB), particularly for integration architectures. For example, an ESB includes both an integration hub (to facilitate communication, protocol, and contract transformation) and an orchestration engine (to allow architects to build workflows between various integration endpoints). Because the orchestration-driven SOA includes many layers of indirection, it allows architects to implement enterprise services as integration points, as package software, or as bespoke code, among other possibilities, as illustrated in Figure 17-6.

Client requests use the message bus to determine which enterprise services to call, in what order to call them, and what information to aggregate. The enterprise services, in turn, communicate via APIs to custom code, old systems, or package software, and so on.

Orchestration-driven SOA represents an interesting innovation for how architects handle problems of integration at scale within the constraints of their ecosystem. For example, since most organizations weren’t using open source operating systems when this architecture was popular, alternative architectures like microservices were impossibly expensive. Architects should learn from past approaches. We can continue using the parts that still make sense, while internalizing the lessons of what failed and why.

Figure 17-6. The layers of abstraction in this architecture style allow for implementation flexibility
