# Chapter 25: Negotiation and Leadership Skills

Negotiation and leadership skills are hard skills, obtained only through many years of learning, practice, and mistakes—but they are critical in becoming an effective software architect. This book can’t make anyone an expert in negotiation and leadership overnight, but the techniques we introduce in this chapter are a good starting point. To dive deeper into this topic, we suggest Tanya Reilly’s book *The Staff Engineer’s Path: A Guide for Individual Contributors* (O’Reilly, 2022) and the classic negotiation book *Getting to Yes: Negotiating Agreement Without Giving In* (Penguin Books, 2011) by Roger Fisher, William L. Ury, and Bruce Patton.

## Negotiation and Facilitation

In Chapter 1, we listed core expectations for software architects. The last expectation we discussed was understanding and being able to navigate your organization’s office politics. The reason this is such an important expectation is that almost every decision you make as a software architect will be challenged: by developers who think they know more, by other architects who think they have a better idea or way of approaching the problem, and by stakeholders who think your solution is too expensive or will take too much time.

Negotiation is one of an architect’s most important skills. Effective software architects understand the politics of the organization, have strong negotiation and facilitation skills, and can overcome disagreements to create solutions that all stakeholders agree on.

### Negotiating with Business Stakeholders

Consider the following scenario in which you, as the lead architect, must negotiate with a key business stakeholder:

- ***Scenario 1*:** Parker, the senior vice president and product sponsor for this project, insists that the new global trading system must support “five nines” of availability (99.999%). However, based on the amount of time between global markets when trading doesn’t occur (two hours), you know that three nines of availability (99.9%) would be sufficient to meet the project requirements. The problem is, you’ve seen that Parker does not like to be wrong and doesn’t respond well to being corrected, especially if they perceive it as condescending. Parker isn’t technically knowledgeable, but thinks they are, so they tend to get involved in the non-functional aspects of projects. As the architect, your goal is to convince Parker, through negotiation, that three nines (99.9%) of availability would be enough.

You’ll have to be careful to not be too egotistical and forceful in your analysis, but you also need to make sure you’re not missing anything that might prove you wrong during the negotiation. There are several key negotiation techniques you can use to help with this sort of stakeholder negotiation. The first is:

> **Tip:** Pay attention to the buzzwords and jargon people use, even if they seem meaningless. They often contain clues that can help you better understand and negotiate the situation.

Corporate buzzwords are generally meaningless, but can nevertheless provide valuable information when you’re about to enter into negotiations. Say you ask when a particular feature is needed and Parker responds, “I needed it yesterday.” You can’t literally provide that, but it should tell you that time to market is important to this stakeholder. Similarly, the phrase “this system must be lightning fast” means performance is a big concern, and “zero downtime,” rather than being literal, means that availability is critical in this application. Effective software architects read between the lines of such exaggerated statements to identify the stakeholder’s real concerns. This leads to a second negotiation technique:

> **Tip:** Gather as much information as possible *before* entering into a negotiation.

Parker’s use of the phrase “five nines” indicates that they want the system to have high availability (specifically, 99.999% of uptime). However, it might be the case that Parker is unaware of what “five nines” of availability actually means in terms of amount of downtime per year. Table 25-1 shows the downtimes based on the number of nines of availability.

**Table 25-1.** The nines of availability

| Percentage uptime | Downtime per year (per day) |
|---|---|
| 90.0% (one nine) | 36 days 12 hrs (2.4 hrs) |
| 99.0% (two nines) | 87 hrs 46 min (14 min) |
| 99.9% (three nines) | 8 hrs 46 min (86 sec) |
| 99.99% (four nines) | 52 min 33 sec (7 sec) |
| 99.999% (five nines) | 5 min 35 sec (1 sec) |
| 99.9999% (six nines) | 31.5 sec (86 ms) |

“Five nines” of availability comes out to 5 minutes and 35 seconds of downtime per year, or an average of 1 second a day of unplanned downtime. That’s ambitious, costly, and, as it turns out, unnecessary for Scenario 1 based on the amount of time between global trading when trading doesn’t occur. Stating these goals in hours and minutes (or, in this case, seconds) is a much better way to have the conversation than sticking with the “nines” vernacular because it brings some actual metrics and quantified numbers into the discussion.

Negotiating Scenario 1 would include validating Parker’s concerns (“I understand that availability is very important for this system”), then steering the negotiation from the nines vernacular to one of reasonable hours and minutes of unplanned downtime. Three nines (which you deem good enough) comes to an average of 86 seconds of unplanned downtime per day—certainly a reasonable number, given the context of this global trading system. Stating it this way might be enough to convince Parker that this amount of unplanned downtime is satisfactory. However, if it doesn’t, here’s another tip:

> **Tip:** When all else fails, state things in terms of *qualified* cost and time.

We recommend saving this negotiation tactic for last. We’ve seen too many negotiations start off on the wrong foot due to opening statements like “That’s going to cost a lot of money” or “We don’t have time for that.” Money and time (which includes the effort involved) are certainly key factors in any negotiation, but try other justifications and rationalizations that matter more before you bring them up. They should be a last resort. Once you reach an agreement with the stakeholder, you can consider cost and time if they are important.

Another important negotiation technique for such situations:

> **Tip:** When you need to qualify demands or requirements, “divide and conquer.”

In *The Art of War*, the ancient Chinese warrior Sun Tzu writes of one’s opponent, “If his forces are united, separate them.” You can use this divide-and-conquer tactic during negotiations as well. In Scenario 1, Parker is insisting on five nines (99.999%) of availability for the new trading system. But does the *entire system* need five nines of availability? You can qualify the requirement, narrowing it down to any specific area(s) of the system that genuinely need five nines of availability. This reduces the scope of difficult (and costly) requirements, not to mention the scope of the negotiation.
