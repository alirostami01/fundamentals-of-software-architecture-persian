# Chapter 26: Architectural Intersections (continued)

## Architecture and Generative AI

As we write the second edition of this book in early 2025, *generative artificial intelligence* (Gen AI) and large language models (LLMs) have infiltrated the world of software development and software design. Many companies are incorporating them into systems to perform tasks that previously were only performed manually by humans. Not surprisingly, Gen AI intersects with software architecture too: architects are incorporating LLMs into software architectures, and some are even using Gen AI tools to assist them in thinking through hard problems.

### Incorporating Generative AI into Architecture

One approach we recommend for incorporating Gen AI into an architecture is to leverage *abstraction* and *modularity*. It’s important to be able to replace one LLM with another quickly, and to allow for guardrails (rails) and evaluate results (evals) from various LLMs.

For example, suppose a job search company wants to leverage Gen AI to anonymize résumés, with the goal of reducing bias and placing focus on job seekers’ skills rather than their demographics or other such factors. This task is normally done by humans, but could easily be done by an LLM. But are the LLM’s results accurate? Does it remove too much information from the résumé? Does it keep too much demographic information in place? For this sort of system, it’s vital to be able to gather samples and metrics and compare LLM engines. Tools such as Langfuse help create this kind of observability within the architecture.

### Generative AI as an Architect Assistant

Given a proper prompt, an LLM (such as Copilot) can produce source code that saves developers a lot of time and effort. They’re great for solving very specific, deterministic problems, such as “write source code in the C# programming language that generates a unique four-digit PIN number that has no repeating digits.” But can LLM technology assist software architects with typical tasks? Here are some general examples of architecture-related prompts:

- Risk assessment: “Are there risk areas within this architecture?”
- Risk mitigation: “How should I address this risk?”
- Antipatterns: “Are there any common antipatterns in this architecture?”
- Decisions: “Should I use orchestration or choreography for this workflow?”

As of the time of the writing of this second edition (early 2025), we haven’t had a tremendous amount of success with this endeavor. Asking an LLM whether microservices or space-based architecture would be most appropriate for a given situation rarely (if ever) yields the right answer. Why? Because, as we’ve demonstrated in this book, *everything in software architecture is a trade-off*. LLMs are great for understanding *knowledge*, but to this day, they still lack the *wisdom* necessary to make appropriate decisions. That wisdom includes so much context that it’s much faster for the architect to solve a business problem by themselves than to teach an LLM all about the problem and its extended environment and context. The fact that we’ve included eight other intersections to be concerned about should be evidence enough that this is a daunting task.

That said, we’ve seen some tools with promise. For instance, Thoughtworks Haiven can interpret an architecture diagram and fully describe a software architecture, saving the work of having to export a diagram into a machine-readable format such as XML and use it to prompt the LLM. Once they’ve imported that information, users can ask Haiven simple questions about the architecture, such as whether it can identify any bottlenecks or issues. Other efforts have included using an LLM to translate a PlantUML diagram or a pseudolanguage description of an architecture into executable ArchUnit code to govern the structure of a system. A lot of activity is happening in this area, so expect rapid change in the coming years in how Gen AI can assist architects.

## Summary

Software architecture is a holistic activity that involves many facets of an organization. Effective software architects realize that creating and maintaining an architecture is much more than just selecting a particular architectural style and moving forward with implementation. It’s also about making sure that the architecture is aligned with other aspects of the environment, and about using the communication and collaboration skills described in Part III to make that alignment happen.
