# Chapter 26: Architectural Intersections (continued)

## Architecture and Implementation (continued)

### Architectural Constraints

A *constraint* is a governing rule or principle describing some sort of restriction within the architecture (such as limiting communications to only REST or using a specific type of database) required to achieve its goals. If the system’s implementation doesn’t adhere to its constraints, the architecture will fail. Thus, part of a software architect’s job is to identify and communicate the *constraints* of an architecture.

To illustrate what we mean by this particular intersection, consider a business trying to release a new system with a very limited budget and a tight deadline. This business expects lots of structural changes to the database and needs to get those changes done as quickly as possible. In this case, a traditional layered architecture (see Chapter 10) would be an excellent fit due to its simplicity, cost-effectiveness, and technical partitioning. Because this style separates the layers, database changes can be isolated to only one layer, making them easier and faster.

For the layered architecture to work in this particular business problem, the architect would need to define the following constraints:

- All database logic must reside in the Persistence layer.
- The Presentation layer cannot access the Persistence layer directly, but must go through all of the layers, even for simple queries.

These constraints are necessary to prevent spreading the database logic throughout the entire architecture, and so that changes to the physical database structure (such as dropping a table or changing a column name) won’t affect any code outside the Persistence layer.

Now let’s say the UI developers decide it’s faster to call the database directly and implement the architecture that way instead. In addition, the backend developers realize it would be much easier to maintain and test the code if the Business logic and database logic are together, so they also ignore the constraints and couple these concerns in the business layer of the architecture. This implementation is not aligned with the constraints of the architecture, which means that database changes will impact all of the code in every layer, take too long, and the system will not meet the business goals.

Architectural tools are also useful for governing architectural constraints.

## Architecture and Infrastructure

The scope of software architecture has grown over the last couple of decades to encompass more and more responsibility and perspective. Around the mid-2000s, the typical relationship between architecture and operations was contractual and formal, with lots of bureaucracy. Most companies outsourced operations to a third party to avoid the complexity of hosting their own operations, with SLAs for uptime, scale, responsiveness, and other important characteristics. Today, however, architecture styles such as microservices freely leverage characteristics that used to be solely operational. For example, elastic scale was once built into space-based architectures (see Chapter 16), but today, microservices handles it less painfully through tighter collaboration between architects and DevOps.

> **History: How Pets.com Gave Us Elastic Scale**
>
> People often assume that our current technical capabilities (like elastic scale) are just invented one day by some clever developer. In reality, though, the best ideas are often born of hard lessons. Pets.com is an early example. This ecommerce site appeared around 1998, hoping to become the Amazon.com of pet supplies. Its brilliant marketing department created a compelling mascot: a sock puppet with a microphone that said irreverent things. The mascot became a superstar, appearing in public at parades and national sporting events.
>
> Unfortunately, Pets.com’s management apparently spent all the money on the mascot, not on infrastructure. Once orders started pouring in, they weren’t prepared. The website was slow, transactions were lost, deliveries delayed…it was pretty much the worst-case scenario. Shortly after a disastrous Christmas rush, Pets.com closed down, selling its only remaining valuable asset—the mascot.
>
> What Pets.com needed was *elastic scale*: the ability to spin up more instances of resources when they became needed. Cloud providers now offer this feature as a commodity, but early ecommerce companies had to manage their own infrastructure, and many fell victim to a previously unheard-of phenomenon: too much success can kill a business. The fall of Pets.com, and other similar horror stories, led architects to pay more attention to such intersections when creating software architectures.

The intersection of architecture and infrastructure is important because it facilitates operational architectural characteristics. Just because an *architecture* can support high scalability doesn’t mean it will—if the corresponding *infrastructure* doesn’t support it, it won’t (as demonstrated by Pets.com). At client sites, we’ve all too often witnessed architects and developers being blamed for architectural failures that were really caused by a misalignment between architecture and infrastructure.

In most cases, this misalignment occurs because of a lack of communication and collaboration between the architect and those responsible for the infrastructure and operations. Architects often fail to realize infrastructure’s influence on characteristics such as scalability, responsiveness, fault tolerance, performance, availability, elasticity, and so on. This misalignment gave rise to the field of DevOps.

For many years, many companies considered operations to be separate from software development, often outsourcing them to a third-party company as a cost-saving measure. In the 1990s and 2000s, many architectures were designed defensively around the assumption that operations would be outsourced and thus outside of architects’ control. (For a good example of this, see Chapter 16.) However, in the mid-2000s, companies started experimenting with new forms of architecture that combined many operational concerns. For example, older architecture styles such as orchestration-driven SOA required elaborate tools and frameworks to support capabilities like scalability and elasticity, which greatly complicated implementation. So architects built architectures that could handle scale, performance, elasticity, and a host of other capabilities *internally*. The side effect was that these architectures were vastly more complex.

The creators of the microservices architecture style realized that operational concerns are better handled by operations. By creating a collaborative relationship between architecture and operations, the architects realized they could simplify their designs and rely on the operations people to handle the things they handle best. They teamed up with operations to create microservices, and to lay the foundations of what would become the DevOps movement. While DevOps has helped, this intersection of architecture and infrastructure is nevertheless still problematic for most companies.

While infrastructure is less of a concern, cloud environments can still get misaligned with an architecture. For example, deploying services across regions or even availability zones can decrease or even cancel out the performance and data integrity benefits of in-memory replicated caches and distributed caches. Similarly, co-locating services, containers, or even Kubernetes Pods on the same virtual machine will significantly increase performance, but it will also adversely impact scalability, fault tolerance, availability, and elasticity.

Aligning architecture with infrastructure involves close communication and collaboration between architects and infrastructure team members, or even adopting DevOps practices, so that all stakeholders understand the critical operational concerns. Only then can architects truly realize the operational benefits of the architecture they selected—the ones that led us to grant those wonderful five-star ratings.
