# Chapter 24: Making Teams Effective (continued)

## Team Warning Signs

We mentioned team size as one of the five factors that help an architect determine the level of involvement on a development team: the larger a team, the more architect involvement is needed; the smaller the team, the less involvement is needed. However, what constitutes a “large team”? In this section, we’ll look at three factors that can help an architect determine if the team is too large, and hence not as effective as it can be.

### Process Loss

The term *process loss* was coined by Fred Brooks in his book *The Mythical Man-Month* (Addison-Wesley, 1995). The basic idea of process loss, otherwise known as Brooks’s Law, is that *the more people you add to a project, the more time the project will take*. As Figure 24-7 shows, *group potential* is defined by the collective efforts of everyone on the team. However, Brooks states that any team’s *actual* productivity will always be less than its *potential* productivity; the difference is called the team’s *process loss*.

> **Figure 24-7.** Brooks’s Law holds that a team’s size affects its actual productivity

Process loss is a good factor in determining the correct team size for a particular project, and an effective software architect observes the development team to look for indications of process loss. For instance, if team members frequently run into merge conflicts when pushing code to a repository, this is an indication that they are working on the same code and possibly getting in each other’s way.

To avoid process loss, we recommend looking for areas of parallelism and having team members working on separate services or areas of the application. Anytime a project manager proposes adding a new team member to a project, an effective architect will look for opportunities to create parallel work streams. If they find none, they notify the project manager that a new addition could have a negative impact on the team.

### Pluralistic Ignorance

*Pluralistic ignorance* is when everyone privately rejects a norm, but agrees to it because they think they are missing something obvious. For example, suppose the majority of people on a large team agree that using messaging between two remote services is the best solution. One person thinks this is a silly idea, because of a secure firewall between the two services. However, that person publicly agrees along with everyone else to use messaging. Although they privately reject the idea, they are afraid that they might be missing something obvious if they speak up. The larger the group, the less willing people are to confront others. On a smaller team, they might have spoken up to challenge the original solution, prompting the team to land on another protocol (such as REST) for a better solution.

The concept of pluralistic ignorance was made famous by the Danish children’s story “The Emperor’s New Clothes”, by Hans Christian Andersen. In the story, two con artists, posing as tailors, convince the king that the new clothes they’ve “made” for him are invisible to anyone who is unworthy to see them. The king, who can’t see the clothes but is unwilling to admit that he himself must be unworthy, struts around totally nude, asking all of his subjects how they like his new clothes. The subjects, afraid of being considered unworthy, assure the king that his new clothes are the best thing ever. This folly continues until a child finally calls out to the king that he isn’t wearing any clothes at all.

During meetings, an effective software architect observes people’s facial expressions and body language, alert for the possibility that some might mask their skepticism because of pluralistic ignorance. If the architect senses this happening, they act as a facilitator—perhaps interrupting to ask a skeptic what they think about the proposed solution and supporting them when they speak up, even if the person is wrong. The point here is for the architect, as a facilitator, to make sure everyone feels it is a safe enough environment to speak up.

The third factor that indicates appropriate team size is called *diffusion of responsibility*. As teams get bigger, their growth has a negative impact on communication. If team members are confused about who is responsible for what and things are getting dropped, those are good signs that the team is too large.

Figure 24-8 shows someone standing next to a broken-down car on the side of a country road. In this scenario, how many people might stop and ask the motorist if everything is OK? Because it’s a small road, it’s probably in a small community, so maybe everyone who passes by will stop. But what if that same motorist is stranded on the side of a busy highway in a large city? Thousands of cars might simply drive by without anyone stopping to ask if everything is OK. This is a good example of the diffusion of responsibility. As cities get busier and more crowded, people assume the motorist has already called for help, or that some other member of the crowd witnessing the event will help. However, in most of these cases, help is not on the way, and the motorist is stuck with a dead or forgotten cell phone.

> **Figure 24-8.** Diffusion of responsibility

An effective architect not only guides the development team through implementing the architecture, but ensures that its members are healthy, happy, and working together to achieve a common goal. Looking for these three warning signs and helping to correct the problems they indicate is a good way to ensure an effective development team.

---

## Leveraging Checklists

Airline pilots use checklists on every flight. Even the most experienced, seasoned veteran pilots have checklists for takeoff, landing, and thousands of other situations—both common ones and unusual edge cases. They use checklists because one missed aircraft setting or procedure (such as forgetting to set the flaps to 10 degrees before takeoff) can mean the difference between a safe flight and a disaster.

In Dr. Atul Gawande’s excellent book *The Checklist Manifesto* (Picador, 2011), he describes the power of checklists to make surgical procedures safer. Alarmed at the high rate of staph infections in hospitals, Dr. Gawande created surgical checklists. Infection rates in hospitals using the checklists fell to near zero, while rates in control hospitals not using the checklists continued to rise.

Checklists work. They’re excellent vehicles for making sure every task is covered and addressed. So why doesn’t the software development industry leverage them too? Having worked for many years in this industry, we firmly believe that checklists make a big difference in the effectiveness of development teams. Of course, most software developers aren’t handling life-and-death matters like flying airliners or performing open-heart surgery. In other words, software developers don’t require checklists for everything. The key is knowing when to leverage them and when not to.

Figure 24-9 is not a checklist—it’s a set of procedural steps for creating a new database table, so it should not be in checklist form. Some of its tasks have dependencies; for example, the database table cannot be verified if the form has not yet been submitted. Any process with a procedural flow of dependent tasks should not be in a checklist. Nor should simple, familiar processes that are executed frequently without error.

> **Figure 24-9.** Example of a bad checklist

Good candidates for checklists include processes that don’t have a set procedural order or dependent tasks, as well as those where people frequently skip steps or make errors. Don’t go overboard and start making everything a checklist. Architects often do this once they find that checklists do, in fact, make development teams more effective. They risk invoking what is known as the *Law of Diminishing Returns*. The more checklists the architect creates, the less likely developers are to use them. It’s also wise to make checklists as small as possible while still capturing all the necessary steps. Developers generally will not follow overly long checklists. If any of the tasks listed can be automated, automate them and remove them from the checklist.

> **Tip:** Don’t worry about stating the obvious in a checklist. The obvious stuff is what usually gets missed.

Three of the checklists we’ve found most helpful cover developer code completion, unit and functional testing, and software releases. Each checklist is discussed in the following sections.
