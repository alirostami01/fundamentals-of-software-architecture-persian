# Chapter 6: Measuring and Governing Architecture Characteristics

Architects must deal with an extraordinarily wide variety of architecture characteristics across all different aspects of software projects. Operational aspects like performance, elasticity, and scalability commingle with structural concerns, such as modularity and deployability. It benefits architects to understand how to measure and govern architectural characteristics, rather than drown in ambiguous terms and broad definitions. This chapter focuses on concretely defining some of the more common architecture characteristics and discusses how to build governance mechanisms for them.

## Measuring Architecture Characteristics

Architects struggle to define architectural characteristics for a number of reasons:

- They aren’t physics: Many architecture characteristics in common usage have vague meanings. For example, how does an architect design for agility or deployability? What about wicked fast performance? People around the industry have wildly differing perspectives on common terms—sometimes driven by legitimate differing contexts, sometimes accidental.

- Wildly varying definitions: Even within the same organization, different departments may disagree on the definitions of critical characteristics such as performance. Until developers, architects, operations, and others can unify on a common definition, how can they have a proper conversation?

- Too composite: Many desirable architecture characteristics are really collections of other characteristics at a smaller scale, as you might remember from our discussion of composite architectural characteristics in Chapter 5. For example, agility breaks down into characteristics such as modularity, deployability, and testability.

Decomposing composite architectural characteristics into their constituent parts is an important part of establishing objective definitions for architecture characteristics, which solves all three of these problems.

When an organization agrees that everyone will use standard, concrete definitions for architecture characteristics, they create a ubiquitous language around architecture. This standardization allows them to unpack composite characteristics to uncover objectively measurable features.

### Operational Measures

Many architecture characteristics have obvious direct measurements, such as performance or scalability. Yet even these offer many nuanced interpretations, depending on the team’s goals. For example, perhaps your team measures the average response time for certain requests—a good example of a measure for an operational architecture characteristic. But if your team only measures the average, what happens if some boundary condition causes 1% of requests to take 10 times longer than others? If the site has enough traffic, the outliers may not even show up. To catch outliers, you might also want to measure the maximum response times.

High-level teams don’t just establish hard performance numbers; they base their definitions on statistical analysis. For example, say a video streaming service wants to monitor scalability. Rather than set an arbitrary number as the goal, the engineers measure the scale over time and build statistical models, then raise alarms if the real-time metrics fall outside the prediction models. If they do, the failure can mean two things: the model is incorrect (which teams like to know) or something is amiss (which teams also like to know).

The kinds of characteristics that teams measure evolve rapidly in conjunction with tools, targets, devices, and capabilities. For example, recently many teams have focused on performance budgets for metrics such as first contentful paint and first CPU idle, both of which speak volumes about performance issues for web page users on mobile devices. As these and myriad other things change, teams will find new things and ways to measure them.

> SIDEBAR: The Many Flavors of Performance

Many of the architecture characteristics we describe have multiple definitions. Performance is a great example. Many projects look at general performance: for example, how long request and response cycles take for a web application. However, through tremendous work, architects and DevOps engineers in many organizations have established specific performance budgets for specific parts of an application. For example, many organizations have researched user behavior and determined that the optimum time for first-page render (the first visible sign of progress for a web page in a browser or mobile device) is some fraction of a second. Most applications fall in the double-digit range for this metric. But for modern sites attempting to capture as many users as possible, this is an important metric to track, and the organizations behind such sites have built extremely nuanced measures.

Some of these metrics have additional implications for application design. Many forward-thinking organizations place K-weight budgets for page downloads; that is, they allow a maximum number of bytes’ worth of libraries and frameworks on a particular page. Their rationale derives from physics constraints: only so many bytes can travel over a network at a time, especially for mobile devices in low-bandwidth areas.
> END SIDEBAR

### Structural Measures

Some objective measures are not so obvious as performance. What about internal structural characteristics, such as well-defined modularity? This is a great example of an implicit architectural characteristic—architects are responsible for defining components and interactions, and want to build a sustainable structure for overall high quality. Unfortunately, there are not yet any comprehensive metrics to assess the quality of an architecture. However, there are metrics and common tools that allow architects to address some critical aspects of code structure, albeit along narrow dimensions.

One measurable aspect of code is complexity, defined by the Cyclomatic Complexity metric.

> SIDEBAR: Cyclomatic Complexity

Cyclomatic Complexity (CC) is a code-level metric designed by Thomas McCabe Sr., in 1976 to provide an objective measure for the complexity of code at the function/method, class, or application level. It is computed by applying graph theory to code—specifically, decision points, which cause different execution paths. For example, if a function has no decision statements (such as if statements), then CC = 1. If the function has a single conditional, then CC = 2 because there are two possible execution paths.

The formula for calculating the CC for a single function or method is $CC = E - N + 2$, where N represents nodes (lines of code), and E represents edges (possible decisions). Consider the C-like code shown in Example 6-1.

Example 6-1. Sample code for Cyclomatic Complexity evaluation

```java
public void decision(int c1, int c2) {
    if (c1 < 100)
        return 0;
    else if (c1 + C2 > 500)
       return 1;
    else
      return -1;
}
```

The Cyclomatic Complexity for Example 6-1 is 3 (3 – 2 + 2), shown in Figure 6-1.

> Figure 6-1. Cyclomatic Complexity graph for the decision function

The number 2 appearing in the Cyclomatic Complexity formula represents a simplification for a single function/method. For fan-out calls to other methods (known as connected components in graph theory), the more general formula is $CC = E - N + 2P$, where P represents the number of connected components.

> END SIDEBAR

Architects and developers universally agree that overly complex code represents a “code smell”—something that appears in code that is so bad that it has an imaginary odor. It harms virtually every one of the desirable characteristics of code bases: modularity, testability, deployability, and so on. If teams don’t keep an eye on gradually growing complexity, it will dominate the code base.

Cyclomatic Complexity is a great example of the bluntness of the metrics that architects have available. While it measures the complexity of code, it cannot determine whether that complexity is essential (because we’re solving a complicated problem) or accidental (because we’ve implemented a poor design). Metrics like CC are extremely useful for assessing code, whether it’s written by developers or generative AI. Generative AI tends to solve problems by brute force, often leading to accidental complexity.

> SIDEBAR: What’s a Good Value for Cyclomatic Complexity?

A common question the authors receive when talking about this subject is: what’s a good threshold value for CC? Of course, like all questions in software architecture, the answer is: it depends! Specifically, it depends on the complexity of the problem domain. For example, if you have an algorithmically complex problem, the solution will yield complex functions. Some of the key aspects of CC for architects to monitor: are functions complex because of the problem domain or because of poor coding? Alternatively, is the code partitioned poorly? In other words, could a large method be broken down into smaller, logical chunks, distributing the work (and complexity) into more well-factored methods?

In general, the industry thresholds for CC suggest that a value under 10 is acceptable, barring other considerations such as complex domains. We consider that threshold very high and would prefer code to fall under five, indicating cohesive, well-factored code. A metrics tool in the Java world, Crap4J, attempts to determine how poor (crappy) your code is by evaluating a combination of CC and code coverage; if CC grows to over 50, no amount of code coverage rescues that code from crappiness. The most terrifying professional artifact Neal ever encountered was a single C function that served as the heart of a commercial software package whose CC was over 800! It was a single function with over 4,000 lines of code, including liberal use of GOTO statements (to escape impossibly deeply nested loops).

Engineering practices like test-driven development (TDD) have the beneficial side effect of generating smaller, less complex methods on average for a given problem domain. When practicing TDD, developers try to write a simple test, then write the smallest amount of code to pass the test. This focus on discrete behavior and good test boundaries encourages well-factored, highly cohesive methods that exhibit low CC.

> END SIDEBAR
