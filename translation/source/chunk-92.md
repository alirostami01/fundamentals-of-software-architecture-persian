# Chapter 24: Making Teams Effective (continued)

## Architect Personalities (continued)

### The Armchair Architect

The armchair architect is an architect who hasn’t coded in a very long time (if ever) and doesn’t account for implementation details when creating an architecture. They are typically disconnected from the development team and are rarely around, simply moving on to the next project after completing the initial architecture diagrams.

Some armchair architects are simply in way over their heads: they just don’t know the technology or business domain well enough to provide leadership or guidance. Think about it: what do developers do? They write source code, of course. Writing source code is really hard to fake; either you can write source code or you can’t. What does an architect do? No one knows! Draw lots of lines and boxes? It’s all too easy to fake it as an architect.

For example, suppose an armchair architect designing a stock-trading system is in way over their head. Their architecture diagram might only contain two boxes: one representing the trading system, and one representing the trade compliance engine it communicates with. There’s nothing *wrong* with this architecture—it’s just too high-level to be of any use to anyone.

Armchair architects create loose boundaries around their development teams, so those teams end up doing the work the architect is supposed to be doing. Their velocity and productivity suffer as a result, and everyone gets confused about how the system should work.

It’s as easy to become an armchair architect as it is to become a control freak. When an architect finds that they don’t have time for the development teams that are implementing the architecture (or simply choosing not to spend time with them), that’s an indicator that they might be falling into the armchair-architect personality. Development teams need an architect’s support and guidance, and they need the architect to be available to answer questions. Other indicators of an armchair architect are the following:

- Not fully understanding the business domain, business problem, or technology being used
- Not enough hands-on experience developing software
- Not considering the implications associated with a certain implementation of the architecture solution (such as complexity, maintenance, and testing)

Few architects *intend* to become armchair architects; it just “happens” when they get spread too thin between projects or teams and lose touch with the technology or the business domain. To avoid this, we recommend getting more involved in the project’s technologies and building a stronger understanding of the business problem and domain.

### The Effective Architect

An *effective* software architect creates appropriate constraints and boundaries, ensures that team members are working well together, and provides them with the right level of guidance. The effective architect also makes sure that the team has the correct tools and technologies in place and removes any other roadblocks between the development team and its goals.

While this sounds obvious and easy, it’s not. There is an art to becoming an effective *leader* as well as an effective software architect. It requires collaborating closely with the development team and gaining their respect. In the following sections, we’ll show you some techniques for determining how involved an architect should be with a development team.

## How Much Involvement?

Becoming an effective architect is about knowing how much to be involved with a given development team—and when to stay out of their way. This concept, known as *Elastic Leadership*, is widely evangelized by author and consultant Roy Osherove. We’re going to deviate a bit from Osherove’s work in this area to focus on factors that are specific to software-architecture leadership.

Knowing how much to be involved with a development team can be challenging, and so is determining how many teams or projects you can manage at once. Here are five key factors to consider:

- ***Team familiarity*:** How well do the team members know each other? Have they worked together before? Generally, the better team members know each other, the more they can self-organize and the less they need the architect involved. Conversely, the newer the team members are, the more they’ll need the architect to facilitate collaboration and reduce cliques.
- ***Team size*:** We consider more than a team with 12 developers to be a big team, and one with 5 or fewer to be a small team. The larger the team, the more the architect is needed. We discuss this topic in more detail in “Team Warning Signs” on page 443.
- ***Overall experience*:** What is the team’s mix of senior and junior (inexperienced) developers? How well do its members know the technology and the business domain? (If the business domain is particularly complex, consider assessing team members’ overall level of technological experience separately from their business-domain experience.) Teams with lots of junior developers require more involvement and mentoring from the architect and more mentoring. In teams with more senior developers, the architect can become more of a facilitator than a mentor.
- ***Project complexity*:** Highly complex projects require the architect to be more available to assist with issues, while relatively simple, straightforward projects require less involvement.
- ***Project duration*:** Is the project short (say, two months), long (two years), or average duration (around six months)? The architect involvement needed grows with the length of the project.

While most of these factors might seem obvious, project duration is sometimes confusing. As we indicated, the shorter the project’s duration, the less involvement is needed; the longer the project, the more involvement is needed. Does that seem counterintuitive? Consider a quick two-month project. Two months is not a lot of time to qualify requirements, experiment, develop code, test every scenario, and release into production. In this case, the architect should act more like an armchair architect; the development team already has a keen sense of urgency, and a control-freak architect would just get in the way and delay the project. Now think about a two-year project: the developers are more relaxed, not feeling a sense of urgency. They’re likely to be planning vacations and taking long lunches. Thus, for longer duration projects the architect is needed to ensure that the project moves along on schedule and that the team accomplishes the most complex tasks first.

To illustrate how to use these factors to determine an appropriate level of involvement, assume a fixed scale of 20 points for each factor, as shown in Figure 24-4. The side of the scale with negative values indicates less involvement, ending in the extreme of the armchair architect. The positive values indicate more involvement, ending in the extreme of the control-freak architect.

> **Figure 24-4.** Scale for measuring architects’ amount of involvement with development teams

This scale is not exact, of course, but it does help in determining the amount of involvement the architect should expect to have with a development team. For example, consider the project scenario, Scenario 1, shown in Table 24-1 and Figure 24-5. The values for each factor in the table move the “needle” toward either extreme: +20 for a factor that indicates more involvement, -20 for one that indicates less involvement. The factor scores rated here for Scenario 1 total -60, indicating that the architect should limit their involvement in daily interactions, facilitating but staying out of the team’s way. They will be needed to answer questions and make sure the team is on track, but for the most part the architect should be largely hands-off and let the experienced team do what they do best—develop software quickly.

**Table 24-1.** Scenario 1 example for amount of involvement

| Factor | Value | Rating | Personality |
|---|---|---|---|
| Team familiarity | New team members | +20 | Control freak |
| Team size | Small (4 members) | -20 | Armchair architect |
| Overall experience | All experienced | -20 | Armchair architect |
| Project complexity | Relatively simple | -20 | Armchair architect |
| Project duration | 2 months | -20 | Armchair architect |
| Accumulated score | | -60 | Armchair architect |

> **Figure 24-5.** Amount of involvement for Scenario 1

Now consider Scenario 2, described in Table 24-2 and illustrated in Figure 24-6, where the team members know each other well, but the team is large (12 team members) and consists mostly of junior developers. The project is relatively complex, with a duration of six months. In this case, the accumulated score comes out to +20, indicating that the effective architect should take on a mentoring and coaching role and be fairly involved in day-to-day activities, but not so much as to disrupt the team.

**Table 24-2.** Scenario 2 example for amount of involvement

| Factor | Value | Rating | Personality |
|---|---|---|---|
| Team familiarity | Know each other well | -20 | Armchair architect |
| Team size | Large (12 members) | +20 | Control freak |
| Overall experience | Mostly junior | +20 | Control freak |
| Project complexity | High complexity | +20 | Control freak |
| Project duration | 6 months | -20 | Armchair architect |
| Accumulated score | | +20 | Control freak |

> **Figure 24-6.** Amount of involvement for Scenario 2

Architects use these factors at the start of a project to determine how involved they plan to be, but as the project progresses, their level of involvement usually changes. We thus recommend analyzing these factors continually throughout the project’s lifecycle.

It is difficult to make these factors objective, since some (such as the team’s overall experience level) might carry more significance than others. In these cases the metrics can easily be weighted or modified to suit a particular situation.

The primary message here is that the appropriate amount of architect involvement on a development team varies according to these five factors. By using these factors to gauge their level of involvement, architects can draw the appropriate boundaries and create the right size “room” for the team.
