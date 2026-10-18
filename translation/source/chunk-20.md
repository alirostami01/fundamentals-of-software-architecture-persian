### Process Measures

Some architecture characteristics intersect with software development processes. For example, agility often appears as a desirable feature. However, it is a composite architecture characteristic, made up of features such as testability and deployability.

Testability is measurable through code-coverage tools for virtually all platforms that report on what percentage of the code the tests execute. Like all software checks, though, these cannot replace thinking and intent. For example, a code base can have 100% code coverage, yet use poor assertions that don’t actually provide confidence in the code’s correctness.

Testability is an objectively measurable characteristic, as is deployability. Deployability metrics include percentage of successful deployments, how long deployments take, and issues/bugs raised by deployments. Every team must arrive at a good set of measurements that capture useful qualitative and quantitative data for their organization’s and team’s priorities and goals.

While agility and its related parts clearly relate to the software development process, that process may influence the structure of the architecture. For example, if ease of deployment and testability are high priorities, the architect would emphasize good modularity and isolation at the architecture level—an example of an architecture characteristic driving a structural decision. Virtually anything within the scope of a software project can rise to the level of an architecture characteristic if it manages to meet our three criteria, forcing an architect to make significant decisions to account for it.

## Governance and Fitness Functions

Once architects establish and prioritize architecture characteristics, how can they make sure that developers will respect those priorities and implement their designs correctly and safely, regardless of schedule pressure? On many software projects, urgency dominates, yet architects still need tools and techniques to provide architectural governance. Modularity is a great example of an aspect of architecture that is important but not urgent.

### Governing Architecture Characteristics

Governance, derived from the Greek word kubernan (to steer) is an important responsibility of the architect role. As the name implies, its scope covers any aspect of the software development process that architects want to influence. For example, ensuring software quality falls under architectural governance because neglecting it can lead to disastrous quality problems.

Fortunately, architects have increasingly sophisticated solutions to this problem—a good example of incremental growth within the software development ecosystem’s capabilities. The drive toward automation spawned by Extreme Programming created continuous integration (CI). CI led to further automation in operations, which we now call DevOps, and this chain continues through to architectural governance. The book Building Evolutionary Architectures (O’Reilly, 2022) by Neal Ford et al. describes a family of techniques called fitness functions used to automate many aspects of architecture governance. We’ll spend the rest of this chapter looking at fitness functions.

### Fitness Functions

The word evolutionary in the title Building Evolutionary Architectures comes more from evolutionary computing than from biology. One of the authors, Dr. Rebecca Parsons, spent some time in the evolutionary computing space, including working with tools like genetic algorithms. When a developer designs a genetic algorithm to produce some beneficial outcome, they often want to guide the algorithm by providing an objective measure of the quality of its outcome. That guidance mechanism is called a fitness function: an object function used to assess how close the output comes to achieving its aim.

For example, suppose you need to solve the traveling salesperson problem, a famous problem used as a basis for machine learning. Given a salesperson, a list of cities they must visit, and the distances between those cities, what is the optimum possible route—minimizing distance, time, and cost? If you design a genetic algorithm to solve this problem, you might use one fitness function to evaluate the length of the route and another to evaluate the overall cost associated with the route. Yet another might evaluate the time the traveling salesperson is away.

Practices in evolutionary architecture borrow this concept to create an architectural fitness function: any mechanism that provides an objective integrity assessment of some architecture characteristic or combination of architecture characteristics.

Fitness functions are not some new framework for architects to download. Rather, they offer a new perspective on many existing tools. Notice in the definition the phrase any mechanism—the verification techniques for architecture characteristics are as varied as the characteristics are. Fitness functions overlap many existing verification mechanisms, depending on the way they are used: in chaos engineering or as metrics, monitors, or unit testing libraries (see Figure 6-2).

> Figure 6-2. The mechanisms of fitness functions

Many different tools may be used to implement fitness functions, depending on the architecture characteristics. Let’s look at a couple of examples of fitness functions that test various aspects of modularity.

#### Cyclic dependencies

Modularity is an implicit architecture characteristic that most architects care about. Because poorly maintained modularity harms the structure of a code base, architects generally place a high priority on maintaining good modularity. However, on many platforms, there are forces working against those good intentions. For example, when coding in any popular Java or .NET development environment, as soon as a developer references a class not already imported, the IDE helpfully presents a dialog asking if they would like to auto-import the reference. This occurs so often that most programmers reflexively swat the auto-import dialog away. But arbitrarily importing classes between components can spell disaster for modularity. For example, Figure 6-3 illustrates Cyclic Dependencies, a particularly damaging antipattern that architects aspire to avoid.

In Figure 6-3, each component references something in the other components. Having a network like this damages modularity, because it’s impossible to reuse a single component without bringing the others along. And if those other components are coupled to other components? The architecture will tend more and more toward the Big Ball of Mud antipattern. How can architects govern this behavior without constantly looking over the developers’ shoulders? Code reviews help, but happen too late in the development cycle to be fully effective. If the development team imports rampantly across the code base for a week until the code review, they’ve already done serious damage to the code base.

> Figure 6-3. Cyclic dependencies between components

The solution to this problem is to write a fitness function to look after cycles, as shown in Example 6-2.

Example 6-2. Fitness function to detect component cycles

```java
public class CycleTest {
    private JDepend jdepend;
    @BeforeEach
    void init() {
      jdepend = new JDepend();
      jdepend.addDirectory("/path/to/project/persistence/classes");
      jdepend.addDirectory("/path/to/project/web/classes");
      jdepend.addDirectory("/path/to/project/thirdpartyjars");
    }
    @Test
    void testAllPackages() {
      Collection packages = jdepend.analyze();
      assertEquals("Cycles exist", false, jdepend.containsCycles());
    }
}
```

This code uses the metrics tool JDepend to check the dependencies between packages. The tool understands the structure of Java packages and fails the test if it finds any cycles. An architect can wire this test into a project’s continuous build on and stop worrying about trigger-happy developers accidentally introducing cycles. This is a great example of a fitness function guarding the important rather than urgent practices of software development: it’s an important concern for architects, yet has little impact on day-to-day coding.

#### Distance from the Main Sequence fitness function

In “Coupling” on page 44, we introduced the more esoteric metric of Distance from the Main Sequence, which can also be verified using fitness functions, as shown in Example 6-3.

Example 6-3. Distance from the Main Sequence fitness function

```java
@Test
void AllPackages() {
    double ideal = 0.0;
    double tolerance = 0.5; // project-dependent
    Collection packages = jdepend.analyze();
    Iterator iter = packages.iterator();
    while (iter.hasNext()) {
      JavaPackage p = (JavaPackage)iter.next();
      assertEquals("Distance exceeded: " + p.getName(),
        ideal, p.distance(), tolerance);
    }
}
```

This code uses JDepend to establish a threshold for acceptable values, failing the test if a class falls outside the range. (The tool ArchUnit, highlighted in the next section, allows architects to create similar fitness functions.) This example of an objective measure for an architecture characteristic illustrates the importance of collaboration between developers and architects when designing and implementing fitness functions. The intent is not for a group of architects to ascend to an ivory tower and develop esoteric fitness functions that developers cannot understand—it’s to implement automated governance rules that ensure the quality of the code base.

> TIP: Architects must ensure that developers understand the purpose of a fitness function before imposing it on them.
