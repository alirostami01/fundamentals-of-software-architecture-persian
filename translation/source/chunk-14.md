## Architectural Characteristics (Partially) Listed

Architectural characteristics exist along a broad spectrum of complexity, ranging from low-level code characteristics (such as modularity) to sophisticated operational concerns (such as scalability and elasticity). There is no true universal standard, though people have attempted to codify one. Instead, each organization interprets these terms for itself. Additionally, because the software ecosystem changes so fast, new concepts, terms, measures, and verifications are constantly appearing, providing new opportunities to define architectural characteristics.

While the sheer volume and breadth of architecture characteristics make it hard to quantify them, architects do categorize them. The following sections describe a few such broad categories and provide some examples.

### Operational Architectural Characteristics

Operational architectural characteristics cover capabilities such as performance, scalability, elasticity, availability, and reliability. Table 4-1 lists some operational architectural characteristics.

Table 4-1. Common operational architectural characteristics

| Term | Definition |
|---|---|
| Availability | How much of the time the system will need to be available; if that’s 24/7, steps need to be in place to allow the system to be up and running quickly in case of any failure. |
| Continuity | The system’s disaster recovery capability. |
| Performance | How well the system performs; ways to measure this include stress testing, peak analysis, analysis of the frequency of functions used, and response times. |
| Recoverability | Business continuity requirements: in case of a disaster, how quickly the system must get back online. This includes backup strategies and requirements for duplicate hardware. |
| Reliability/safety | Whether the system needs to be fail-safe, or if it is mission critical in a way that affects lives. If it fails, will it cost the company large sums of money? This is often a spectrum rather than a binary. |
| Robustness | The system’s ability to handle error and boundary conditions while running, for example, if the internet connection or power fails. |
| Scalability | The system’s ability to perform and operate as the number of users or requests increases. |

Operational architectural characteristics overlap heavily with operations and DevOps concerns.

### Structural Architectural Characteristics

Architects are responsible for proper code structure. In many cases, the architect has sole or shared responsibility for the code’s quality, including its modularity, its readability, how well coupling between components is controlled, readable code, and a host of other internal quality assessments. Table 4-2 lists a few structural architectural characteristics.

Table 4-2. Structural architectural characteristics

| Term | Definition |
|---|---|
| Configurability | How easily end users can change aspects of the software’s configuration through interfaces. |
| Extensibility | How well the architecture accommodates changes that extend its existing functionality. |
| Installability | How easy it is to install the system on all necessary platforms. |
| Leverageability/reuse | The extent to which the system’s common components can be leveraged across multiple products. |
| Localization | Support for multiple languages on entry/query screens in data fields. |
| Maintainability | How easy it is to apply changes and enhance the system. |
| Portability | The system’s ability to run on more than one platform (such as Oracle and SAP DB). |
| Upgradeability | How easy and quick it is to upgrade to a newer version on servers and clients. |

### Cloud Characteristics

The software development ecosystem constantly changes and evolves; the most recent excellent example is the arrival of the cloud. When the first edition was published, cloud-based computing existed but wasn’t pervasive. Now, most systems have some interaction with cloud-based systems in at least some capacity. A few of these considerations appear in Table 4-3.

Table 4-3. Cloud provider architectural characteristics

| Term | Definition |
|---|---|
| On-demand scalability | The cloud provider’s ability to scale up resources dynamically based on demand. |
| On-demand elasticity | The cloud provider’s flexibility as resource demands spike; similar to scalability. |
| Zone-based availability | The cloud provider’s ability to separate resources by computing zones to make for more resilient systems. |
| Region-based privacy and security | The cloud provider’s legal ability to store data from various countries and regions. Many countries have laws governing where their citizens’ data may reside (and often restricting it from storage outside their region). |

For this book’s second edition, we’ve added a section to each of the architectural style chapters that describes how that style accommodates and facilitates cloud considerations.

### Cross-Cutting Architectural Characteristics

While many architectural characteristics fall into easily recognizable categories, others fall outside them or defy categorization, yet form important design constraints and considerations. Table 4-4 describes a few of these.

Table 4-4. Cross-cutting architectural characteristics

| Term | Definition |
|---|---|
| Accessibility | How easily all users can access the system, including those with disabilities like colorblindness or hearing loss. |
| Archivability | The system’s constraints around archiving or deleting data after a specified period of time. |
| Authentication | Security requirements to ensure users are who they say they are. |
| Authorization | Security requirements to ensure users can access only certain functions within the application (by use case, subsystem, web page, business rule, field level, etc.). |
| Legal | The legislative constraints in which the system operates, such as data protection laws like GDPR or financial-records laws like Sarbanes-Oxley in the US, or any regulations regarding the way the application is to be built or deployed. This includes what reservation rights the company requires. |
| Privacy | The system’s ability to encrypt and hide transactions from internal company employees, even DBAs and network architects. |
| Security | Rules and constraints about encryption in the database or for network communication between internal systems; authentication for remote user access, and other security measures. |
| Supportability | The level of technical support the application needs; to what extent logging and other facilities are required to debug errors in the system. |
| Usability/achievability | The level of training required for users to achieve their goals with the application/solution. |
