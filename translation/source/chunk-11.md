### Core Metrics

While component coupling has raw value to architects, several other derived metrics allow for deeper evaluation. The metrics discussed in this section were created by software engineer Robert C. Martin, and apply widely to most object-oriented languages.

Abstractness is the ratio of abstract artifacts (abstract classes, interfaces, and so on) to concrete artifacts (implementations). The Abstractness metric measures a code base’s degree of abstractness versus implementation. For example, on one end of the scale would be a code base with no abstractions, just a huge, single function of code (as in a single main() method). The other end of the scale would be a code base with too many abstractions, making it difficult for developers to understand how things wire together. (For example, it takes developers a while to figure out what to do with an AbstractSingletonProxyFactoryBean abstract class, given its many layers of abstraction and ambiguous name.)

The formula for Abstractness appears in Equation 3-3.

Equation 3-3. Abstractness

A = Σma / (Σmc + Σma)

Architects calculate Abstractness by calculating the ratio of the sum of abstract artifacts to the sum of the concrete and abstract ones. In the equation, ma represents abstract elements (interfaces or abstract classes) with the module, and mc represents concrete elements (nonabstract classes). This metric looks for the same criteria. The easiest way to visualize this metric is to consider an application with 5,000 lines of code, all in one main() method. Its Abstractness numerator would be 1, while the denominator would be 5,000, yielding an Abstractness score of almost 0. That’s how this metric measures the ratio of abstractions in code.

Another derived metric, Instability, is defined as the ratio of efferent coupling to the sum of both efferent and afferent coupling, as shown in Equation 3-4.

Equation 3-4. Instability

I = Ce / (Ce + Ca)

In the equation, ce represents efferent (or outgoing) coupling, and ca represents afferent (or incoming) coupling.

The Instability metric determines the volatility of a code base. A code base that exhibits high degrees of instability breaks more easily when changed because of high coupling. For example, if a class calls too many other classes to delegate work, the calling class will show high susceptibility to breakage if one or more of the called methods changes.

### Distance from the Main Sequence

One of the few holistic metrics architects have for architectural structure is Distance from the Main Sequence, a derived metric based on Instability and Abstractness, shown in Equation 3-5.

Equation 3-5. Distance from the Main Sequence

D = |A + I − 1|

In the equation, A = Abstractness and I = Instability.

Note that both Abstractness and Instability are fractions whose results will always fall between 0 and 1 (except in some extreme cases). Thus, graphing the relationship produces the graph in Figure 3-2.

Figure 3-2. The main sequence defines the ideal relationship between Abstractness and Instability

The Distance metric imagines an ideal relationship between Abstractness and Instability; classes that fall near this idealized line exhibit a healthy mixture of these two competing concerns. For example, graphing a particular class allows developers to calculate the Distance from the Main Sequence metric, illustrated in Figure 3-3.

Figure 3-3. Normalized Distance from the Main Sequence for a particular class

The Figure 3-3 metric graphs the candidate class, then measures its distance from the idealized line. The closer to the line, the better balanced the class. Classes that fall too far into the upper righthand corner enter what architects call the Zone of Uselessness: code that is too abstract becomes difficult to use. Conversely, code that falls into the lower lefthand corner, as illustrated in Figure 3-4, enters the Zone of Pain: code with too much implementation and not enough abstraction becomes brittle and hard to maintain.

Figure 3-4. The Zones of Uselessness and Pain

Many platforms provide tools to calculate these measures, which assist architects when analyzing code bases to get familiar with them, prepare for a migration, or assess technical debt.

The Limitations of Metrics

While the industry has a few code-level metrics that provide valuable insight, our tools are extremely blunt compared to analysis tools in other engineering disciplines. Even metrics derived directly from the structure of code require interpretation. For example, Cyclomatic Complexity (see “Cyclomatic Complexity” on page 84) measures complexity in code bases, but this metric cannot distinguish between essential complexity (the code is complex because the underlying problem is complex) and accidental complexity (the code is more complex than it should be). Virtually all code-level metrics require interpretation, but it is still useful to establish baselines for critical metrics such as Cyclomatic Complexity so that architects can assess which type the code base exhibits. We discuss setting up just such tests in “Governance and Fitness Functions” on page 86.

Yourdon and Constantine’s Structured Design, published in 1979, predates the popularity of object-oriented languages. It focuses instead on structured programming constructs, such as functions (not methods). It also defines other types of coupling that are outdated because of modern program language design. Object-oriented programming introduced additional concepts that overlay afferent and efferent coupling, including a more refined vocabulary to describe coupling called connascence.
