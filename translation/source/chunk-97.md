# Chapter 25: Negotiation and Leadership Skills (continued)

## Negotiation and Facilitation (continued)

### Negotiating with Other Architects

It’s not unusual for architects to have to negotiate with other architects on a project. Consider Scenario 2, where two architects disagree on which protocol to use:

- ***Scenario 2*:** You’re the senior of two architects on a project, and you believe that asynchronous messaging would be the right approach for communication between a group of services, to increase both performance and scalability. However, Addison, the other architect on the project, strongly disagrees. They insist that REST would be a better choice, because it’s always faster than messaging and can scale just as well. They cite their research, which consists of a Google search and the output of a prompt to a popular generative AI tool. This is not the first heated debate you’ve had with Addison, nor will it be the last. You want to convince them that messaging is the right solution.

Now, as the senior architect, you certainly could tell Addison that their opinion doesn’t matter and ignore it. However, this will only intensify the animosity between you, and an unhealthy, noncollaborative relationship between the project’s two architects would almost certainly have a negative impact on the development team.

> **Tip:** Always remember that *demonstration defeats discussion*.

Rather than arguing over REST versus messaging, you should *demonstrate* to Addison why messaging would be a better choice in this specific environment. Because every environment is different, simply Googling it rarely yields the correct answer. But if you compare the two options in a production-like environment and show Addison the results, you might be able to avoid an argument entirely.

> **Tip:** Avoid being overly argumentative or letting things get too personal. Calm leadership, combined with clear and concise reasoning, will almost always win a negotiation.

This is a very powerful technique for dealing with adversarial relationships. Once things get personal or heated, the best thing to do is stop the negotiation. Re-engage later, when both parties have calmed down. Architects argue from time to time, but if you stay calm and project leadership, the other person will usually back down.

### Negotiating with Developers

Effective software architects gain the team’s respect through working together. That way, when they request something of the development team, it’s far less likely to spark an argument or resentment.

As you saw in Chapter 24, working with development teams can be difficult at times. When development teams feel disconnected from the architecture (or the architect), they often feel left out of decisions. This is a classic example of the *Ivory Tower* architecture antipattern. Ivory tower architects dictate from on high, giving development teams orders without regard for their opinions or concerns. This usually leads to the team losing respect for the architect and can eventually cause the team’s dynamics to break down altogether. One negotiation technique that can help address this situation is always providing a justification for your decisions.

> **Tip:** When convincing developers to adopt an architecture decision or to do a specific task, provide a justification rather than “dictating from on high.”

If you provide a reason *why* something needs to be done, developers are more likely to agree. For example, consider the following conversation between an architect and a developer about making a simple query within a traditional n-tiered layered architecture:

> **Architect:** “You must go through the Business layer to make that call.”
>
> **Developer:** “I disagree. It’s much faster just to call the database directly.”

There are several things wrong with this conversation. First, notice the architect’s use of the words “you must.” Not only is this type of commanding voice demeaning, it’s one of the worst ways to begin a negotiation (or a conversation). The developer’s response includes a reason: going through the Business layer will be slower and take more time.

Now consider an alternative approach:

> **Architect:** “Since change control is most important to us, we have formed a closed-layered architecture. This means all calls to the database need to come from the Business layer.”
>
> **Developer:** “OK, I get it—but in that case, how am I going to deal with these performance issues for simple queries?”

Here, the architect is *justifying* the demand that all calls go through the Business layer. Providing the justification *first* is always a good approach. Most people tend to stop listening as soon as they hear something they disagree with. Stating the reason before the demand ensures that the developer will hear the architect’s justification.

The architect has also taken a less personal approach to phrasing this demand. By saying “this means” rather than “you must,” they’ve turned the demand into a simple statement of fact. Now take a look at the developer’s response: instead of disagreeing with the layered-architecture restrictions, the developer asks a question about improving performance for simple calls. Now the two can engage in a collaborative conversation to find ways to make simple queries faster while still preserving the closed layers in the architecture.

Another effective negotiation tactic is to have the developer arrive at the solution on their own. For example, suppose that you, as an architect, are choosing between two frameworks, Framework X and Framework Y. Framework Y doesn’t satisfy the security requirements for the system, so you naturally choose Framework X. A developer on your team strongly disagrees, insisting that Framework Y would still be the better choice. Rather than argue the matter, you tell the developer that if they can show you how Framework Y addresses the security concerns, the team will use Framework Y.

One of two things will happen next. Option 1 is that the developer tries to demonstrate that Framework Y satisfies the security requirements, but fails. In failing, they come to understand firsthand why the team can’t use this framework. And because they arrive at the solution on their own, you automatically get their buy-in for the decision to use Framework X. You’ve essentially made it the developer’s decision. This is a win. Option 2 is that the developer finds a way to address the security requirements with Framework Y and demonstrates it to you. This is a win as well. In this case, you missed something in your assessment of Framework Y, and now you have a better solution to the problem (and the developer still feels involved in the decision).

> **Tip:** If a developer disagrees with a decision you make, have them arrive at the solution on their own.

Developers are smart people with useful knowledge. Collaborating with the development team is how architects gain their respect—and their assistance in finding better solutions. The more developers respect an architect, the easier it will be for the architect to negotiate with them.
