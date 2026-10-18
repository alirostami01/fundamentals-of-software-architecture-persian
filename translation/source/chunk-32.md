# Chapter 9: Foundations (continued)

## Monolithic Versus Distributed Architectures (continued)

### The Other Fallacies

The eight fallacies previously listed form a famous set of observations—every architect learns them either from Deutsch’s list or the hard way, one by one, over the course of their career. The authors have also learned some painful, near-universal lessons that we offer as an extension to that famous list.

#### Fallacy #9. Versioning is easy

When two services need to communicate, they pass information in a contract, which includes information required for the communication. Often, a service’s internal implementation evolves over time, changing fields that the service accepts and passes to other services. One way to solve this problem is to use versioning for the contract—that is, create different versions for the old and new contracts including different sets of information. However, this seemingly simple decision leads to a host of trade-offs:

- Should the team version at the individual service level or for the whole system?

- How far should the versioning reach? What portion of the architecture will need to support it?

- How many versions should the team support at any given time? (Some teams accidentally find themselves honoring dozens of different versions for different purposes.)

- Should the team deprecate older versions at the system level or service by service?

While versioning is a reasonable approach for evolving communication between services, it has a host of trade-offs that architects should anticipate.

#### Fallacy #10. Compensating updates always work

Compensating updates is an architectural pattern in which some mechanism (like an `Orchestrator` service) makes sure that several related services all update jointly. If they don’t, the orchestrator reverses the update. The compensating update is from the orchestrator that issues a reversing operation to put the state back to what it was before.

This is a common pattern that most architects blithely assume always works… but it doesn’t. What happens if the compensating update fails? When architects demonstrate how complex interactions in distributed architectures like microservices work, they must also show how compensating updates work. Thus, architects designing transactional workflows in microservices should accommodate the “normal” compensation workflow, but must also consider how to recover if the update and the compensating update (or a portion of it) both fail.

#### Fallacy #11. Observability is optional (for distributed architectures)

A common architectural characteristic for architects to prioritize in distributed architectures is observability: the ability to observe each service’s interactions with other services and the ecosystem, as captured through monitors or logs. While logging is useful in monolithic architectures, it is critical in distributed architectures, which offer many communication failure modes that are hard to debug without comprehensive interaction logs.

## Team Topologies and Architecture

Architects and teams have done lots of research on the intersection of architecture and team topologies, above and beyond the implications of architecture partitioning, which we previously discussed. The very influential book Team Topologies by Matthew Skelton and Manuel Pais (IT Revolution Press, 2019) defines several team types that intersect with software architecture:

- Stream-aligned teams: In team topologies terminology, a stream is a stream of work scoped to a particular business domain or capability. Stream-aligned teams focus narrowly on a single line of work, such as a product, service, or specific set of features.

The goal of stream-aligned teams is to move as quickly as possible because they are delivering discrete value to the organization. Consequently, the other team types are designed to reduce any friction that could impede the stream-aligned teams.

- Enabling teams: An enabling team bridges a gap in some capability, providing a place for necessary research, learning, and other tasks that are important but not urgent. They supply knowledge and resources from specialized domains to support stream-aligned teams. Good enabling teams are highly collaborative and proactive.

- Complicated-subsystem teams: Many systems include highly specialized systems or parts that require similarly specialized skills. Members of complicated-subsystem teams fully understand a complex subsystem or domain and can help a stream-aligned team apply it. Their goal is to reduce other teams’ cognitive load.

- Platform teams: A platform team provides internal services and building blocks for solutions. As defined by Evan Botcher, a platform is

> a foundation of self-service APIs, tools, services, knowledge and support which are arranged as a compelling internal product. Autonomous delivery teams can make use of the platform to deliver product features at a higher pace, with reduced coordination.

Platform teams support the other teams, attempting to remove needless friction while providing necessary governance around concerns such as quality and security.

## On to Specific Styles

Architects need to understand a number of different architecture styles before they can perform trade-off analysis. Each style supports a different set of architectural characteristics—each one has a “sweet spot” that it handles best. By learning the different styles and their underlying philosophies, an architect better understands when each one works best (or least worst, anyway).
