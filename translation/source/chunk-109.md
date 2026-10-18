<!-- Source chunk 109 | PDF pages 520-524 | Appendix: Discussion Questions, Chapters 1-14 | words: 1150 -->
# Appendix: Discussion Questions

## Chapter 1: Introduction

1. What are the four dimensions that define software architecture?
2. What is the difference between an architecture decision and a design principle?
3. List the eight core expectations of a software architect.
4. What is the First Law of Software Architecture?

## Chapter 2: Architectural Thinking

1. Name three criteria for determining whether a decision is more about architecture or more about design.
2. List the three levels of knowledge in the knowledge triangle and provide an example of each.
3. Why is it more important for an architect to focus on technical breadth rather than technical depth?
4. What are some of the ways of maintaining your technical depth and remaining hands-on as an architect?

## Chapter 3: Modularity

1. Describe the difference between modularity and granularity, and provide an example of each.
2. What is the difference between coupling and cohesion?
3. What does the term *connascence* mean?
4. What is the difference between static and dynamic connascence?
5. What is the strongest form of connascence?
6. What is the weakest form of connascence?
7. Which is preferable within a code base: static or dynamic connascence?

## Chapter 4: Architecture Characteristics Defined

1. What three criteria must an attribute meet to be considered an architecture characteristic?
2. What is the difference between an implicit characteristic and an explicit one? Provide an example of each.
3. Provide an example of an operational characteristic.
4. Provide an example of a structural characteristic.
5. Provide an example of a cross-cutting characteristic.
6. Why is it impossible to create an industry-wide standard list of architecture characteristics?

## Chapter 5: Identifying Architectural Characteristics

1. Give a reason why it is a good practice to limit the number of characteristics (“-ilities”) an architecture should support.
2. True or false? Most architecture characteristics come from business requirements and user stories.
3. If a business stakeholder states that time to market (that is, getting new features and bug fixes pushed out to users as fast as possible) is the most important business concern, which architecture characteristics would the architecture need to support?
4. What is the difference between scalability and elasticity?
5. What is the definition of a *composite* architectural characteristic? Provide one example.

## Chapter 6: Measuring and Governing Architecture Characteristics

1. Why is cyclomatic complexity such an important metric to analyze for architecture?
2. What are architecture fitness functions? How can they be used to analyze an architecture?
3. Provide an example of an architecture fitness function to measure the scalability of an architecture.
4. What is the most important criterion for an architecture characteristic to allow architects and developers to create fitness functions?

## Chapter 7: The Scope of Architectural Characteristics

1. What is an architectural quantum, and why is it important to architecture?
2. Assume a system consisting of a single user interface with four independently deployed services, each containing its own separate database. Would this system have a single quantum or four quanta? Why?
3. What is the difference between *static* and *dynamic* coupling? Provide an example of each.
4. Why does *synchronous* communication have a bigger potential impact on operational architectural characteristics than *asynchronous* ones?

## Chapter 8: Component-Based Thinking

1. We define the term *component* as a building block of an application—something the application does. A component usually consists of a group of classes or source files. How do components typically manifest within an application or service?
2. What is the difference between technical partitioning and domain partitioning? Provide an example of each.
3. What is the advantage of domain partitioning?
4. Under what circumstances would technical partitioning be a better choice than domain partitioning?
5. What is the Entity Trap? Why is it not a good approach for component identification?
6. When might you choose the Workflow approach over the Actor/Action approach when identifying core components?

## Chapter 9: Foundations

1. List the eight fallacies of distributed computing.
2. Name three challenges that distributed architectures have that monolithic architectures don’t.
3. What is stamp coupling? What are some ways of addressing stamp coupling?
4. What is the difference between technical versus domain partitioning?
5. List three characteristics that distinguish an architectural style from a pattern.

## Chapter 10: Layered Architecture Style

1. What is the difference between an open layer and a closed layer?
2. Describe the concept of *layers of isolation* and its benefits.
3. What is the Architecture Sinkhole antipattern?
4. What are some of the main architecture characteristics that would drive you to use a layered architecture?
5. Why isn’t testability well supported in the layered architecture style?
6. Why isn’t agility well supported in the layered architecture style?

## Chapter 11: Modular Monolith Architecture Style

1. How does the modular monolith differ from the n-tiered layered architecture?
2. Describe the difference between the peer-to-peer and mediator approaches when communicating between modules.
3. What are the three common risks associated with the modular monolith architectural style?
4. Name three primary strengths of the modular monolith and when you should consider using it.
5. Given its modularity, why aren’t operational characteristics such as scalability and fault tolerance good in the modular monolith?

## Chapter 12: Pipeline Architecture Style

1. Can pipes be bidirectional in a pipeline architecture?
2. Name the four types of filters and their purpose.
3. Can a filter send data out through multiple pipes?
4. Explain why the pipeline architecture is well suited for cloud-based environments.
5. Is the pipeline architecture style technically partitioned or domain partitioned?
6. In what way does the pipeline architecture support modularity?

## Chapter 13: Microkernel Architecture Style

1. What is another name for the microkernel architecture style?
2. Under what situations is it OK for plug-in components to be dependent on other plug-in components?
3. What are some of the tools and frameworks that can be used to manage plug-ins?
4. What would you do if you had a third-party plug-in that didn’t conform to the standard plug-in contract in the core system?
5. Provide two examples of the microkernel architecture style.
6. What characteristics of the core system determine its degree of “microkern-ality”?
7. Why is the microkernel architecture always a single architecture quantum?
8. What is *domain/architecture isomorphism*?

## Chapter 14: Service-Based Architecture Style

1. Why are services in service-based architecture called *domain services*?
2. Name two common risks associated with service-based architecture.
3. Which database topologies (monolithic, domain, and dedicated) can you use with service-based architecture?
4. What techniques can you use to manage database changes within a service-based architecture?
5. Do domain services require a container (such as Docker) to run?
6. Which architecture characteristics does the service-based architecture style support well?
7. Why isn’t elasticity typically well supported in a service-based architecture?
8. How can you increase the number of architecture quanta in a service-based architecture?
