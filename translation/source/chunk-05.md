<!-- Source chunk 05 | PDF pages 43-46 | Chapter 2: Technical Breadth, Frozen Caveman Antipattern, The 20-Minute Rule | words: 1431 -->

Technical Breadth
Unlike developers, who must have a significant amount of technical depth to perform
their jobs, software architects must have a significant amount of technical breadth to
see things from an architectural point of view. Technical depth is all about having
deep knowledge of a particular programming language, platform, framework, product, and so on, whereas technical breadth is all about knowing a little bit about a lot
of things.
To better understand the difference, consider the knowledge pyramid shown in
Figure 2-2 . It encapsulates all the technical knowledge in the world, which can be
broken down into three levels: stuff you know, stuff you know you don’t know, and stuff
you don’t know you don’t know.
Figure 2-2. The pyramid representing all knowledge
Stuff you know includes the technologies, frameworks, languages, and tools technologists use on a daily basis to perform their jobs (such as a Java programmer knowing
Java). They’re good, or even expert, at all these things. Notice that this level of
knowledge (represented by the top part of the pyramid) is the smallest and contains
the fewest things. This is because most technologists have to pick and choose the
areas in which to develop expertise—no one can be an expert at everything.
Stuff you know you don’t know (the middle part of the pyramid) includes things a
technologist knows a little about or has heard of but in which they have little or no
experience or expertise. For example, most technologists have heard of Clojure and
know it’s a programming language based on Lisp, but can’t write source code in Clojure. This level of knowledge is much bigger than the top level. This is because people
can become familiar with many more things than they can develop expertise in.
Stuff you don’t know you don’t know is the largest part of the knowledge pyramid. It
includes the entire host of technologies, tools, frameworks, and languages that would
be the perfect solution to a problem, if only the technologist trying to solve the
problem knew that these solutions exist. The goal in any individual’s career should
be to move things from the stuff you don’t know you don’t know into the second area
of the pyramid, the stuff you know you don’t know —and, when expertise becomes
necessary, to move things from the middle part of the pyramid to the top: the stuff
you know.
Early on in a developer’s career, expanding the top of the pyramid ( Figure 2-3 )
means gaining valuable expertise. However, the stuff you know is also stuff you must
maintain—nothing is static in the software world. If a developer becomes an expert
in Ruby on Rails, that expertise won’t last if they ignore Ruby on Rails for a year or
two. Keeping things at the top of the pyramid requires a time investment to maintain
expertise. This top part represents the individual’s technical depth: the things they
know really well.
Figure 2-3. Developers must maintain expertise to retain it
Technical Breadth | 21
However, the nature of knowledge changes as developers transition into the architect
role. A large part of the value of an architect is that they have a broad understanding
of technology and how to use it to solve particular problems. For example, it’s better
for an architect to know that five solutions exist for a particular problem than to
have singular expertise in only one. The most important parts of the pyramid for
architects are the top and middle sections; how far the middle section penetrates into
the bottom section represents an architect’s technical breadth, as shown in Figure 2-4.
Figure 2-4. How much someone knows about a topic is technical depth, and how many
topics someone knows is technical breadth
For an architect, breadth is more important than depth. Because architects must make
decisions that match capabilities to technical constraints, a broad understanding of a
wide variety of solutions is valuable. Thus, for an architect, the wise course of action
is to sacrifice some hard-won expertise and use that time to broaden their portfolio,
as shown in Figure 2-5. Some areas of expertise will remain, probably in particularly
enjoyable technology areas, while others usefully atrophy.
Figure 2-5. Enhanced breadth and shrinking depth for the architect role
Our knowledge pyramid illustrates how fundamentally different the roles of architect
and developer are. Developers spend their whole careers honing expertise. Transitioning to the architect role means a shift in that perspective, which many individuals
find difficult. This in turn leads to two common dysfunctions: first, an architect
tries to maintain expertise in a wide variety of areas, succeeding in none of them
and working themselves ragged in the process. Second, it manifests as stale expertise
—the mistaken sensation that your outdated information is still cutting edge. We see
this often in large companies where the developers who founded the company have
moved into leadership roles, yet still make technology decisions using ancient criteria
(see “Frozen Caveman Antipattern” on page 24).
Technical Breadth | 23
Frozen Caveman Antipattern
An antipattern is what programmer Andrew Koenig defines as something that seems
like a good idea when you begin, but leads you into trouble. A behavioral antipattern
commonly observed in the wild, the Frozen Caveman antipattern, describes architects
who revert to their pet irrational concern for every architecture. For example, one of
Neal’s colleagues worked on a system that featured a centralized architecture. Each
time they delivered the design to the client architects, the persistent question was:
“But what if we lose Italy?” Several years before, a freak communication problem had
prevented the client’s headquarters from communicating with its stores in Italy, causing great inconvenience. While the chances of this recurring were extremely small,
the architects had become obsessed with this particular architectural characteristic.
Generally, this antipattern manifests in architects who have been burned in the past
by a poor decision or unexpected occurrence, making them particularly cautious
about anything related. While risk assessment is important, it should be realistic as
well. Understanding the difference between genuine and perceived technical risk is
part of the ongoing learning process. Thinking like an architect requires overcoming
these Frozen Caveman ideas and experiences, seeing other solutions, and asking more
relevant questions.
Architects should focus on technical breadth so that they have a larger quiver from
which to draw arrows. Developers transitioning to the architect role may have
to change the way they view knowledge acquisition. Balancing the depth and the
breadth of their portfolio of knowledge is something every developer should consider
throughout their career. But how does an architect gain technical breadth? The next
sections provide a few techniques that will help you uncover the “stuff you don’t
know that you don’t know. ”
The 20-Minute Rule
As illustrated in Figure 2-5 , technical breadth is more important to architects than
technical depth. But how do you stay current on all the latest trends and buzzwords
while also working full-time, developing your career, spending time with friends, and
taking care of your family?
One technique we use is the 20-minute rule. The idea is to devote at least 20 minutes a
day to learning something new or diving deeper into a specific topic. Figure 2-6 illustrates some good places to spend your 20 minutes, such as InfoQ, DZone Refcardz,
and the Thoughtworks Technology Radar . Y ou can learn more about unfamiliar
buzzwords by looking them up on the internet, promoting that knowledge from “the
stuff you don’t know you don’t know” into the “stuff you know you don’t know. ” Y ou
could even spend that time reading a book like this one. The point is to carve some
time out of your busy day to focus on developing your technical breadth and thus
your career.
Figure 2-6. The 20-minute rule
Many technologists, when they first embrace this concept, plan their 20 minutes for
lunch or after work; however, in our experience, these time periods rarely work. It’s
easy to start using lunchtimes to catch up on work rather than take a break, and
evenings are even worse, with social plans, family time, and more after a long day.
Instead, we strongly recommend taking your 20 minutes first thing in the morning—
right after grabbing a cup of coffee or tea and, importantly, before you check your
email. Once you check email, your morning is over and your day has started. Get
your 20 minutes in while your mind is fresh and before distractions take over.
Following the 20-minute rule will increase your technical breadth and help you
develop and maintain the knowledge that will make you an effective software
architect.
