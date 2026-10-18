Any list of architectural characteristics will necessarily be incomplete; any software project may invent architectural characteristics based on unique factors. Many of the terms we’ve just listed are imprecise and ambiguous, sometimes because of subtle nuance or a lack of objective definitions. For example, interoperability and compatibility may appear to be equivalent, and that will be true for some systems. However, they differ because interoperability implies ease of integration with other systems, which in turn implies published, documented APIs. Compatibility, on the other hand, is more concerned with industry and domain standards. Another example is learnability: one definition is “how easy it is for users to learn to use the software,” and another definition is “the level at which the system can automatically learn about its environment in order to become self-configuring or self-optimizing using machine learning algorithms.”

Many definitions overlap: availability and reliability, for instance. Yet consider the internet protocol IP, which underlies TCP. IP is available but not reliable: packets may arrive out of order, and the receiver may have to ask for missing packets again.

There is no complete list of standards defining these categories. The International Organization for Standards (ISO) publishes a list organized by capabilities that overlaps with our list here, but mainly establishes an incomplete category list. Here are some of the ISO definitions, reworded to update terms and add categories to align with modern concerns:

Performance efficiency

Measure of the performance relative to the amount of resources used under known conditions. This includes time behavior (measure of response, processing times, and/or throughput rates), resource utilization (amounts and types of resources used), and capacity (degree to which the maximum established limits are exceeded).

Compatibility

Degree to which a product, system, or component can exchange information with other products, systems, or components and/or perform its required functions while sharing the same hardware or software environment. It includes coexistence (can perform its required functions efficiently while sharing a common environment and resources with other products) and interoperability (degree to which two or more systems can exchange and utilize information).

Usability

Users can use the system effectively, efficiently, and satisfactorily for its intended purpose. It includes appropriateness recognizability (users can recognize whether the software is appropriate for their needs), learnability (how easily users can learn how to use the software), user error protection (protection against users making errors), and accessibility (make the software available to people with the widest range of characteristics and capabilities).

Reliability

Degree to which a system functions under specified conditions for a specified period of time. This characteristic includes subcategories such as maturity (does the software meet the reliability needs under normal operation), availability (software is operational and accessible), fault tolerance (does the software operate as intended despite hardware or software faults), and recoverability (can the software recover from failure by recovering any affected data and reestablish the desired state of the system).

Security

Degree to which the software protects information and data so that people or other products or systems have the degree of data access appropriate to their types and levels of authorization. This family of characteristics includes confidentiality (data is accessible only to those authorized to have access), integrity (the software prevents unauthorized access to or modification of software or data), nonrepudiation (can actions or events be proven to have taken place), accountability (can user actions of a user be traced), and authenticity (proving the identity of a user).

Maintainability

Represents the degree of effectiveness and efficiency to which developers can modify the software to improve it, correct it, or adapt it to changes in environment and/or requirements. This characteristic includes modularity (degree to which the software is composed of discrete components), reusability (degree to which developers can use an asset in more than one system or in building other assets), analyzability (how easily developers can gather concrete metrics about the software), modifiability (degree to which developers can modify the software without introducing defects or degrading existing product quality), and testability (how easily developers and others can test the software).

Portability

Degree to which developers can transfer a system, product, or component from one hardware, software, or other operational or usage environment to another. This characteristic includes the subcharacteristics of adaptability (can developers effectively and efficiently adapt the software for different or evolving hardware, software, or other operational or usage environments), installability (can the software be installed and/or uninstalled in a specified environment), and replaceability (how easily developers can replace the functionality with other software).

The last item in the ISO list addresses the functional aspects of software:

Functional suitability

This characteristic represents the degree to which a product or system provides functions that meet stated and implied needs when used under specified conditions. This characteristic is composed of the following subcharacteristics:

- Functional completeness: Degree to which the set of functions covers all the specified tasks and user objectives.
- Functional correctness: Degree to which a product or system provides the correct results with the needed degree of precision.
- Functional appropriateness: Degree to which the functions facilitate the accomplishment of specified tasks and objectives.

However, we do not believe that functional suitability belongs in this list. It does not describe architectural characteristics but rather the motivational requirements to build the software. This illustrates how thinking about the relationship between architectural characteristics and the problem domain has evolved. We cover this evolution in Chapter 7.

> SIDEBAR: The Many Ambiguities in Software Architecture

A source of consistent frustration among architects is the lack of clear definitions for so many critical things, including the activity of software architecture itself! The absence of a standard leads companies to define their own terms for common things. This often leads to industry-wide confusion, because architects either use opaque terms or, worse yet, the same terms for wildly different meanings.

As much as we’d like, we can’t impose a standard nomenclature on the software development world. However, to help avoid terminology-based misunderstandings, domain-driven design advises organizations to establish and use a ubiquitous language among employees. We follow and recommend that advice.

## Trade-Offs and Least Worst Architecture

We said earlier that architects should support only those architectural characteristics that are critical or important to the system’s success. Systems can only support a few of the architectural characteristics we’ve listed, for a variety of reasons. First, support for an architectural characteristic is rarely free. Each supported characteristic requires design effort from the architect, effort from developers to implement and maintain it, and perhaps structural support.

Second, architectural characteristics are synergistic with each other and the problem domain. As much as we would prefer otherwise, each design element interacts with all the others. For example, taking steps to improve security will almost certainly negatively impact performance: the application must do more on-the-fly encryption, indirection (for hiding secrets), and other activities that can degrade performance. Airplane pilots often struggle when learning to fly helicopters, which have controls for each hand and each foot. Changing one control impacts all of the others because they are synergistic. Flying a helicopter is a balancing exercise, which nicely describes the trade-off process when choosing architectural characteristics; they are similarly synergistic with both other architectural characteristics and the domain design: changing one often entails changing another. Like our belabored helicopter pilot, architects must learn to juggle interlocking items.

Third, as we discussed previously, the lack of standard definitions for architectural characteristics means that organizations struggle with ambiguity. While the industry will never be able to create an immutable list of architectural characteristics (because new ones constantly appear), each organization can create its own list (or ubiquitous language) with objective definitions.

Finally, not only is the number of architectural characteristics constantly increasing, but the number of categories has increased over the last decade as well. For example, a few decades ago, architects cared little for operational concerns, which were considered a separate “black box.” However, with the increased popularity of architectures like microservices, architects and operations must collaborate more intensely and frequently. As software architecture becomes more complex, it tends to entangle with other parts of the organization.

Thus, it’s very rare for architects to be able to design a system and maximize every single architectural characteristic. More often, the decisions come down to trade-offs between several competing concerns.

> TIP: Never strive for the best architecture; aim for the least worst architecture.

Trying to support too many architectural characteristics leads to generic solutions that attempt to solve every business problem. The design quickly becomes unwieldy, so such architectures rarely work.

Strive to design architecture that is as iterative as possible. The easier it is to change the architecture, the less everyone needs to stress about discovering the exact correct thing in the first attempt. One of the most important lessons of Agile software development is the value of iteration; this holds true at all levels of software development, including architecture.
