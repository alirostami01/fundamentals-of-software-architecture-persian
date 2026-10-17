The sophistication of fitness function tools has increased over the last few years, especially as some special-purpose tools have emerged. One such tool is ArchUnit, a Java testing framework inspired by—and using—several parts of the JUnit ecosystem. ArchUnit provides a variety of predefined governance rules, codified as unit tests, and allows architects to write specific tests that address modularity. Consider the layered architecture illustrated in Figure 6-4.

> Figure 6-4. Layered architecture

When designing a layered monolith such as the one in Figure 6-4, the architect defines the layers for good reasons (we describe these motivations, trade-offs, and other aspects in Chapter 10). However, some developers may not understand the importance of these patterns, while others may adopt a “better to ask forgiveness than permission” attitude because of some overriding local concern, such as performance. But allowing them to erode the reasons for the architecture will hurt the long-term health of the architecture.

ArchUnit allows architects to address this problem via a fitness function, shown in Example 6-4.

Example 6-4. ArchUnit fitness function to govern layers

```java
layeredArchitecture()
    .layer("Controller").definedBy("..controller..")
    .layer("Service").definedBy("..service..")
    .layer("Persistence").definedBy("..persistence..")

    .whereLayer("Controller").mayNotBeAccessedByAnyLayer()
    .whereLayer("Service").mayOnlyBeAccessedByLayers("Controller")
    .whereLayer("Persistence").mayOnlyBeAccessedByLayers("Service")
```

In Example 6-4, the architect defines the desirable relationship between layers and writes a verification fitness function to govern it.

There is a similar tool in the .NET space, NetArchTest. Example 6-5 shows a layer verification in C#.

Example 6-5. NetArchTest for layer dependencies

```csharp
// Classes in the presentation should not directly reference repositories
var result = Types.InCurrentDomain()
    .That()
    .ResideInNamespace("NetArchTest.SampleLibrary.Presentation")
    .ShouldNot()
    .HaveDependencyOn("NetArchTest.SampleLibrary.Data")
    .GetResult()
    .IsSuccessful;
```

Our discussion of testability highlights a problem with any metric or measurement: the possibility that developers will try to game the system. Once they learn how architects are measuring compliance, they may code to the metric rather than build the correct thing. For example, a common failing of testability occurs when developers who are taking shortcuts write unit tests, but without any assertions. “Touching” the code but not verifying that it works amounts to cheating on the code-coverage metric. Writing governance code using tools like ArchUnit helps architects prevent this behavior by ensuring that every unit test includes at least one assertion. Of course, dedicated rule-breakers will always find a way, but fitness functions like this prevent accidental lapses.

Another example of fitness functions is Netflix’s “Chaos Monkey” and the attendant Simian Army. When Netflix decided to move its operations to Amazon’s cloud, the architects no longer had control over operations, which worried them: what would happen if a defect appeared operationally? To solve this problem, they spawned the discipline of chaos engineering. The Chaos Monkey essentially acts as a production fitness function, simulating general chaos to see how well the system can endure it. Latency was a problem with some AWS instances, so the Chaos Monkey would simulate high latency. (In fact, this was such a problem, they eventually created a specialized Latency Monkey). This led them to develop additional tools: for instance, the Chaos Kong, which simulates an entire Amazon datacenter failure, has helped Netflix avoid such outages when they occur for real.

In particular, the Conformity, Security, and Janitor “Monkeys” (fitness functions) exemplify the automated-governance approach. The Conformity Monkey allows Netflix architects to define governance rules enforced by the monkey in production. For example, if they decide that each service should respond without errors for all requests, they build that check into the Conformity Monkey. The Security Monkey checks each service for well-known security defects, like ports that shouldn’t be active and configuration errors.

Finally, the Janitor Monkey looks for instances to which no other services route anymore. Netflix has an evolutionary architecture, so developers routinely migrate to newer services, leaving old services running with no collaborators. Because running services on the cloud consumes money, the Janitor Monkey looks for orphan services and disintegrates them out of production.

Chaos engineering offers an interesting new perspective on architecture: it’s not a question of if something will eventually break, but when. Anticipating those breakages and testing to prevent them makes systems much more robust. A book by some of the Netflix innovators, Casey Rosenthal and Nora Jones, called Chaos Engineering (O’Reilly, 2020) highlights this approach.

Atul Gawande’s influential book The Checklist Manifesto (Metropolitan, 2009) describes how professionals such as airline pilots and surgeons use checklists. (Sometimes they’re even legally mandated to do so.) It’s not because those professionals don’t know their jobs or are forgetful. Rather, when professionals do a highly detailed job over and over, it becomes easy for details to slip by them; a succinct checklist forms an effective reminder.

This is the correct perspective on fitness functions—they are not a heavyweight governance mechanism, but a mechanism for architects to express and automatically verify important architectural principles. Developers know that they shouldn’t release insecure code, but that competes with dozens or hundreds of other priorities. Tools like the Security Monkey, and fitness functions generally, allow architects to build important governance checks into the substrate of the architecture.
