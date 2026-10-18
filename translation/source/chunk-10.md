## Measuring Modularity

Since modularity is so important, architects need tools to help them better understand it. Fortunately, researchers have created a variety of language-agnostic metrics for this purpose. We’ll focus here on three key concepts: cohesion, coupling, and connascence.

### Cohesion

Cohesion refers to the extent to which a module’s parts should be contained within the same module. In other words, it measures how related the parts are to one another. An ideal cohesive module is one where all parts are packaged together; breaking them into smaller pieces would require coupling the parts together via calls between modules to achieve useful results. The cautionary tale of modularity as it relates to cohesion is exemplified in the following quote from the book Structured Design (Pearson, 2008):

Attempting to divide a cohesive module would only result in increased coupling and decreased readability.

—Larry Constantine

Computer scientists have defined a range of cohesion, measured from best to worst:

Functional cohesion: Every part of the module is related to the other, and the module contains everything essential it needs to function.

Sequential cohesion: Two modules interact: one outputs data that becomes the input for the other.

Communicational cohesion: Two modules form a communication chain in which each operates on information and/or contributes to some output. For example, one adds a record to the database and the other generates an email based on that information.

Procedural cohesion: Two modules must execute code in a particular order.

Temporal cohesion: Modules are related based on timing dependencies. For example, many systems have a list of seemingly unrelated things that must be initialized at system startup; these different tasks are temporally cohesive.

Logical cohesion: The data within modules is related logically but not functionally. For example, consider a module that converts information from text, serialized objects, or streams into some other format. Its operations are related, but the functions are quite different. A common example of this type of cohesion exists in virtually every Java project in the form of the StringUtils package, a group of static methods that operate on String but are otherwise unrelated.

Coincidental cohesion: The elements in a module are unrelated other than being in the same source file. This represents the most negative form of cohesion.

Despite its many variants, cohesion is a less precise metric than coupling. Often, a particular module’s degree of cohesion is determined at the discretion of a particular architect. Consider this module definition:

```text
Customer Maintenance
• add customer
• update customer
• get customer
• notify customer
• get customer orders
• cancel customer orders
```

Should the last two entries reside in this module? Or should the developer create two separate modules? Here’s what that would look like:

```text
Customer Maintenance
• add customer
• update customer
• get customer
• notify customer
```

```text
Order Maintenance
• get customer orders
• cancel customer orders
```

Which is the correct structure? As always, it depends:

- Are these the only two operations for Order Maintenance? If so, it may make sense to collapse those operations back into Customer Maintenance.

- Is Customer Maintenance expected to grow much larger? If so, perhaps developers should look for opportunities to extract behavior into a different (or new) module.

- Does Order Maintenance require so much knowledge of Customer information that separating the two modules would require a high degree of coupling to make it functional? (This relates back to the prior Larry Constantine quote.)

These questions represent the kind of trade-off analysis that lies at the heart of a software architect’s job.

Computer scientists have developed a good structural metric to determine cohesion—specifically, Lack of Cohesion (which is a bit surprising, given how subjective this characteristic is). A well-known set of metrics named the Chidamber and Kemerer Object-Oriented Metrics Suite measures particular aspects of object-oriented software systems. It includes many common code metrics, such as Cyclomatic Complexity (see “Cyclomatic Complexity” on page 84) and several important coupling metrics, discussed in “Coupling” on page 44.

Chidamber and Kemerer have also developed a Lack of Cohesion in Methods (LCOM) metric, which measures the structural cohesion of a module. The initial version appears in Equation 3-1.

Equation 3-1. LCOM, version 1

LCOM = { |P| − |Q|, if |P| > |Q| ; 0, otherwise }

In this equation, P increases by 1 for any method that doesn’t access a particular shared field; Q decreases by 1 for methods that do share a particular shared field. If you find this formulation confusing, we sympathize—and it’s gradually become even more elaborate. The second variation, introduced in 1996 (thus the name LCOM96B), appears in Equation 3-2.

Equation 3-2. LCOM96B

LCOM96b = (1/a) ∑(j=1…a) (m − μ(Aj)) / m

We won’t bother untangling the variables and operators in Equation 3-2 because the following written explanation is clearer. Basically, the LCOM metric exposes incidental coupling within classes. A better definition of LCOM would be “the sum of sets of methods not shared via sharing fields.”

Consider a class with private fields a and b. Many of the methods only access a, and many other methods only access b. The sum of the sets of methods not shared via sharing fields (a and b) is high; therefore, this class incurs a high LCOM score, indicating a significant lack of cohesion in methods.

Consider the three classes shown in Figure 3-1. Here, fields appear as single letters inside octagons, and methods appear as blocks. In Class X, the LCOM score is low, indicating good structural cohesion. Class Y, however, lacks cohesion; each of the field/method pairs in Class Y could appear in its own class without affecting the system’s behavior. Class Z shows mixed cohesion; the last field/method combination could be refactored into its own class.

Figure 3-1. The LCOM metric, where fields are octagons, and methods are squares

The LCOM metric is useful to architects who are analyzing code bases in order to assist in restructuring, migrating, or understanding a code base. Shared utility classes are a common headache when moving architectures. Using the LCOM metric can help architects find classes that are incidentally coupled and should never have been a single class to begin with.

Many software metrics have serious deficiencies, and LCOM is not immune. All this metric can find is structural lack of cohesion; it has no way to determine if particular pieces fit together logically. This reflects back on our Second Law of Software Architecture: why is more important than how.

### Coupling

Fortunately, we have better tools to analyze coupling in code bases. These are based in part on graph theory: because the method calls and returns form a call graph, it can be analyzed mathematically. Edward Yourdon and Larry Constantine’s book Structured Design: Fundamentals of a Discipline of Computer Program and Systems Design (Prentice-Hall, 1979), which defined many core concepts, including the metrics afferent coupling and efferent coupling. Afferent coupling measures the number of incoming connections to a code artifact (component, class, function, and so on). Efferent coupling measures the outgoing connections to other code artifacts. There are tools for virtually every platform that allow architects to analyze the coupling characteristics of code.

Why Such Similar Names for Coupling Metrics?

Why are two critical metrics in the architecture world that represent opposite concepts named virtually the same thing, differing in only the vowels that sound the most alike? These terms originate from the book Structured Design. Borrowing concepts from mathematics, Yourdon and Constantine coined the now-common terms afferent and efferent coupling. They should really have been called incoming and outgoing coupling, but the authors leaned toward mathematical symmetry rather than clarity. Developers have come up with several mnemonics to help out. For instance, a appears before e in the English alphabet, just as incoming appears before outgoing. The letter e in efferent matches the initial letter in exit, which helps in remembering that it represents outgoing connections.
