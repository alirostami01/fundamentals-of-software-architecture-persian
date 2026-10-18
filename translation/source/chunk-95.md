# Chapter 24: Making Teams Effective (continued)

## Providing Guidance

Another way software architects can make teams effective is by using design principles to provide guidance. This also helps form the constraint “room” in which developers work to implement the architecture. Communicating design principles is one of the keys to creating a successful team.

To illustrate this point, imagine you’re guiding a development team in using what is typically called the *layered stack*—the collection of third-party libraries that make up the application. Development teams usually have lots of questions about the layered stack, including which libraries are OK, which are not, and whether or when they can make their own decisions about libraries.

You might begin by having the developers answer the following questions about a library they want to use:

- Are there any overlaps between the proposed library and the system’s existing functionality?
- What is the justification for using the proposed library?

The first question guides developers to check if the functionality provided by the new library can be satisfied through an existing library or existing functionality. When developers ignore this activity (which sometimes happens), they can end up creating lots of duplicate functionality, particularly in large projects and teams.

The second question prompts the developer to ask if the new library or functionality is truly needed. We recommend asking for both a technical justification and a business justification, in part because this technique helps make developers aware of the need to provide business justifications.

> **The Impact of Business Justifications**
>
> One of your authors was the lead architect on a particularly complex Java-based project with a large development team. One team member was obsessed with the Scala programming language and desperately wanted to use it on the project. Their desire to use Scala ended up becoming so disruptive that two key team members declared their intention to leave the project for other, “less toxic” environments. Your author convinced them to hold off. Then he told the Scala enthusiast that he would support using Scala within the project *if* the enthusiast provided a business justification for the costs of the training and rewriting involved. The Scala enthusiast was ecstatic and said they would get right on it. They left the meeting yelling, “Thank you—you’re the best!”
>
> The next day, the Scala enthusiast came into the office completely transformed and asked to speak with your author. They began by immediately (and humbly) saying, “Thank you.” The Scala enthusiast explained that they had come up with all the technical reasons in the world to use Scala, but none of those technical advantages had any business value in terms of the cost, budget, and timeline. In fact, the Scala enthusiast had realized two things: first, that the increase in cost, budget, and timeline would provide no benefit whatsoever; and, second, that they’d been disrupting the team. Before long, the Scala enthusiast had transformed into one of its best and most helpful members. Being asked to provide a business justification for something they wanted increased their awareness of the business’s needs, making them a better software developer and making the team stronger and healthier. The two key developers who’d been planning on leaving stayed on the team.

Another good way to communicate design principles is through graphical explanations about which decisions the development team can make and which they can’t. The graphic in Figure 24-11 shows what this might look like for controlling the layered stack.

> **Figure 24-11.** Providing guidance for the layered stack

These categories are only examples, but many more can be defined. In presenting Figure 24-11 to the team, the architect should apply each category to the third-party library proposed for use:

- ***Special purpose*:** These are specific libraries used for things like rendering PDFs, scanning barcodes, and other circumstances that do not warrant writing custom software.
- ***General purpose*:** These libraries are wrappers on top of the language API and include things like Apache Commons and Guava for Java.
- ***Framework*:** These libraries are used for things like persistence (such as Hibernate) and inversion of control (such as Spring). In other words, they make up an entire layer or structure of the application and are highly invasive.

Next, the architect creates the “room” around this design principle. Notice, in Figure 24-11, that the architect has authorized developers to make decisions about special-purpose libraries without consulting the architect. For general-purpose libraries, however, while developers can analyze overlap analysis, provide justifications, and make a recommendation, this category of library requires architect approval. Finally, framework libraries are entirely the architect’s responsibility—the development teams shouldn’t even perform analysis for these types of libraries.

## Summary

Making development teams effective is hard work. It requires lots of experience and practice, as well as strong people skills (which we will discuss in subsequent chapters). That said, the simple techniques in this chapter for elastic leadership, leveraging checklists, and providing guidance by communicating design principles do in fact work. We’ve seen how useful they prove to be in making development teams work more intelligently.

Some question architects’ role in such activities, insisting that this work should be assigned to the development manager or project manager. We strongly disagree. Software architects guide the team on technical matters and lead them through implementing the architecture. Building a close collaborative relationship with a development team allows the architect to observe team dynamics and facilitate changes to make the team more productive.
