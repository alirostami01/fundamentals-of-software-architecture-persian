# Chapter 24: Making Teams Effective (continued)

## Leveraging Checklists (continued)

> **The Hawthorne Effect**
>
> The hardest part of introducing checklists to a development team is getting developers to actually use them. It’s all too common for some developers to run out of time and simply check off all the items in a checklist without actually performing the tasks.
>
> One way to address this issue is by talking with the team about the difference using checklists can make and having them read *The Checklist Manifesto* by Atul Gawande. Make sure each team member understands the reasoning behind each checklist. Consider having them decide collaboratively what procedures should and shouldn’t be on a checklist—creating a sense of ownership also helps.
>
> When all else fails, there’s the *Hawthorne effect*: the tendency for people who know they are being observed or monitored to change their behavior, generally to do the right thing. This effect doesn’t require actual monitoring so much as a perception; for example, many employers mount non-functioning cameras in highly visible areas, while others install website monitoring software that they rarely check. (How many of those reports are actually viewed by managers?)
>
> To use the Hawthorne effect to govern checklists, let the team know that because using checklists is critical to the team’s productivity, all checklists will be verified to make sure the task was actually performed. In reality, occasional spot-checks are all that’s needed; developers will be much less likely to skip items or falsely mark them as completed.

### Developer Code-Completion Checklist

The developer code-completion checklist is a useful tool, particularly when a developer states that they are “done” with the code. It also is useful for arriving at a “definition of done”: if everything in the checklist is complete, the developer can say they are actually done with the code they were working on.

Here are some things to include in a developer code-completion checklist:

- Coding and formatting standards not included in automated tools
- Frequently overlooked items (such as absorbed exceptions)
- Project-specific standards
- Special team instructions or procedures

Figure 24-10 shows an example developer code-completion checklist. There are some obvious tasks here, like “Run code cleanup and code formatting” and “Make sure there are no absorbed exceptions.” How often do developers in a hurry forget to run code cleanup and formatting from the IDE? Plenty often. In *The Checklist Manifesto*, Gawande finds the same phenomenon with respect to surgical procedures—the obvious tasks are often the ones missed.

> **Figure 24-10.** Example of a developer code-completion checklist

The architect should always review the checklist to see if any items can be automated or written as plug-ins for a code-validation checker. While the project-specific tasks in the checklist (such as executing the custom validator, verifying the audit log is written, calling the `setFailure()` method, and including the `@ServiceEntrypoint` annotation) are good to have in a checklist, some of these could be automated. For example, while an automated check might not be feasible for “Include `@ServiceEntrypoint` on service API class,” it would work for “Verify that only public methods are calling `setFailure()`”—a straightforward check to automate with any code-crawling tool. Checking for areas of automation shortens the checklist’s size and improves its ratio of signal to noise.

### Unit and Functional Testing Checklist

Perhaps one of the best checklists is for unit and functional testing. This checklist contains some of the more unusual and edge cases that software developers tend to forget to test. Whenever someone from QA finds a code issue based on a particular test case, add that test case to this checklist.

This particular checklist is usually one of the longest, since it encompasses all the types of tests that can be run against code. Its purpose is to ensure the most complete testing possible so that when the developer is done with the checklist, the code is essentially production ready.

Here are some of the items found in a typical unit and functional testing checklist:

- Special characters in text and numeric fields
- Minimum and maximum value ranges
- Unusual and extreme test cases
- Missing fields

As with the developer code-completion checklist, if any items can be written as automated tests or are already included in the automated test suite, they should be removed from the checklist and automated.

Developers sometimes don’t know where to start when writing unit tests or how many they should write. This checklist provides a way to make sure general and specific test scenarios are included in the development process. In organizations where testing and development are performed by separate teams, this checklist helps to bridge the gap. The more development teams perform complete testing, the easier they make the testing teams’ jobs, freeing them up to focus on business scenarios not covered in the checklists.

### Software-Release Checklist

Releasing software into production is perhaps one of the most error-prone points in the software development lifecycle, so it makes for a great checklist. This checklist helps avoid failed builds and deployments, and significantly reduces the risk associated with releasing software.

The software-release checklist is usually the most volatile of the checklists presented here, because it changes each time a deployment fails or has problems, to address new errors and shifting circumstances.

The software-release checklist typically includes:

- Configuration changes in servers or external configuration servers
- Third-party libraries added to the project (JAR, DLL, etc.)
- Database updates and corresponding database-migration scripts

Anytime a build or deployment fails, the architect should analyze the root cause of the failure and add a corresponding entry to the software-release checklist. This way, the item will be verified during the next build or deployment, preventing the problem from happening again.
