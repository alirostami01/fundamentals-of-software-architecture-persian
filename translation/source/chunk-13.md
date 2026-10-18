# Chapter 4. Architectural Characteristics Defined

We now delve into the details of structural design, one of the key roles for software architects. This primarily consists of two activities: architectural characteristics analysis, covered in this chapter, and logical component design, covered in Chapter 8. Architects may perform these two activities in any order (or even in parallel), but they come together at a critical join point.

When a company decides to solve a particular problem using software, it gathers a list of requirements for that system (there are many techniques for eliciting them, as covered in Chapter 8). We’ll refer to these requirements as the problem domain (or just the domain) throughout the book. You learned in Chapter 1 that architecture characteristics are the important aspects of a system that are independent from the problem domain and important to the system’s success. In this chapter we’ll dive deeper into defining that term, as well as specific architectural characteristics.

Architects often collaborate on defining the domain, but must also define, discover, and otherwise analyze all the things the software must do that isn’t directly related to the domain functionality: architectural characteristics. Architects’ role in defining architectural characteristics is part of what distinguishes software architecture from coding and design. They must also consider many other factors in designing a software solution, as illustrated in Figure 4-1.

Figure 4-1. A software solution consists of both domain requirements and architectural characteristics

The Longevity of the Term “Non-Functional Requirements”

Many organizations describe architectural characteristics with a variety of terms, including non-functional requirements, a term created to distinguish architectural characteristics from functional requirements. We dislike that term because it is self-denigrating and has a negative impact from a language standpoint: how do you convince teams to pay enough attention to something that’s “non-functional”? Another popular term is quality attributes, which we dislike because it implies after-the-fact quality assessment rather than design.

We prefer the term architectural characteristics because it describes concerns that are critical to the success of the architecture, and therefore the system as a whole, without discounting the importance of these concerns. In Head First Software Architecture (O’Reilly, 2024), we refer to architectural characteristics as the capabilities of the system; in contrast, the domain represents the system’s behavior.

Sometimes terms get “stuck,” and non-functional requirements seems to be a particularly sticky one among software architects. It’s still common in many organizations. The term first started appearing in software engineering literature in the late 1970s, around the same time as function point analysis, an estimation technique that decomposes system requirements into “function points” that each represent some unit of work. Theoretically, teams could add up all the function points at the end of the analysis process and get some insight into the project. Sadly, it provided a veneer of certainty but was plagued by subjectivity, as many estimation schemes are, and is no longer in use.

However, one insight that remains with us from that time is that much of the effort involved to create a system is about that system’s capabilities rather than its requirements. They called those efforts non-function points, which led to the term non-functional requirements becoming common.

## Architectural Characteristics and System Design

To be considered an architectural characteristic, a requirement must meet three criteria. It must specify a nondomain design consideration, influence some structural aspect of the design, and be critical or important to the application’s success. These interlocking parts of our definition are illustrated in Figure 4-2, which consists of these three components and a few modifiers.

Figure 4-2. The differentiating features of architectural characteristics

Let’s look more closely at these components:

An architecture characteristic specifies a nondomain design consideration.

Structural design in software architecture consists of two activities by an architect: understanding the problem domain and uncovering what kinds of capabilities the system needs to support to be successful. The domain design considerations cover the behavior of the system, and architectural characteristics define the capabilities. Taken together, these two activities define structural design.

While design requirements specify what the application should do, architectural characteristics specify how to implement the requirements and why certain choices were made: in short, the operational and design criteria for the project to succeed.

For example, specific levels of performance are often an important architectural characteristic, but often don’t appear in requirements documents. Even more pertinent: no requirements document actually states that a design must “prevent technical debt,” but it is a common design consideration. We cover this distinction between explicit and implicit characteristics in depth in “Extracting Architectural Characteristics from Domain Concerns” on page 67.

An architecture characteristic influences some structural aspect of the design.

The primary reason architects try to describe architectural characteristics on projects is to tease out important design considerations. Can the architect implement it via design, or does this architectural characteristic require special structural consideration to succeed?

For example, security is a concern in virtually every project, and all systems must take certain baseline precautions during design and coding. However, security rises to the level of an architectural characteristic when the architect determines that the architecture needs special structure to support it.

Consider two common architectural characteristics: security and scalability. Architects can accommodate security in a monolithic system by using good coding hygiene, including well-known techniques such as encryption, hashing, and salting. (Architectural fitness functions, which also fall under this umbrella, are discussed in Chapter 6.) Conversely, in a distributed architecture such as microservices, the architect would build a more hardened service with stricter access protocols—a structural approach. Thus, architects can accommodate security via either design or structure. On the other hand, consider scalability: no amount of clever design will allow a monolithic architecture to scale beyond a certain point. Beyond that, the system must change to a distributed architectural style.

Architects pay close attention to operational architectural characteristics (discussed in “Operational Architectural Characteristics” on page 59) because they are the characteristics that most often require special structural support.

An architecture characteristic must be critical or important to application success.

Applications can support a huge number of architectural characteristics…but they shouldn’t. Each architectural characteristic that a system supports adds complexity to its design. That’s why architects should strive to choose the fewest possible architectural characteristics rather than the most.

We divide architectural characteristics into implicit versus explicit architectural characteristics. Implicit ones rarely appear in requirements, yet they’re necessary for the project to succeed. Availability, reliability, and security underpin virtually all applications, yet they’re rarely specified in design documents. Architects must use their knowledge of the problem domain to uncover these architectural characteristics during the analysis phase. For example, a high-frequency trading firm may not have to specify low latency in every system because the architects in that problem domain already know how critical it is. Explicit architectural characteristics appear in requirements documents or other specific instructions.

In Figure 4-2, the choice of a triangle is intentional: each of the definition elements supports the others, which in turn support the overall design of the system. The fulcrum created by the triangle illustrates how these architectural characteristics often interact with one another. This is why architects use the term trade-off so much.
