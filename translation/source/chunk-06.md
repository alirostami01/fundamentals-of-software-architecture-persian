<!-- Source chunk 06 | PDF pages 46-52 | Chapter 2: Developing a Personal Radar (incl. Thoughtworks Technology Radar rings) | words: 1203 -->

Developing a Personal Radar
For most of the ’90s and the beginning of the ’00s, one of your authors was the CTO
of a small training and consulting company. When he started there, the primary
platform was Clipper, a rapid-application development tool for building DOS applications atop dBASE files. Until one day it vanished. The company had noticed the
rise of Windows, but the business market was still DOS…until it abruptly wasn’t.
One coworker lamented that they couldn’t take their enormous body of now-useless
Clipper knowledge and replace it with something else. Has any group in history, the
coworker wondered, learned and thrown away so much detailed knowledge within
their lifetimes as software developers do? The experience left a lasting impression:
ignore the march of technology at your peril.
It also taught us an important lesson about technology bubbles. When developers,
architects, and other technologists become heavily invested in a specific technology,
pouring our work and thought into it, we tend to live in a memetic bubble. Inside the
bubble, which also serves as an echo chamber, everyone knows and cares about that
technology as much as we do. We might not even see honest appraisals from outside
the bubble, especially if the bubble was created by a technology vendor in the first
place. And when the bubble begins to collapse, there’s no warning until it’s too late.
What we lack in our bubble is a technology radar: a living document to help us assess
the risks and rewards of existing and nascent technologies. The radar concept comes
from Thoughtworks, where Neal serves as a director and software architect. In this
section, we’ll describe how this concept came to be and then show you how to create
a personal radar.
The Thoughtworks Technology Radar
The Technology Advisory Board (TAB) is a group of senior technology leaders within
Thoughtworks that assists the CTO in making decisions about technology directions
and strategies for the company and its clients. To stay current, this group began
producing what’s now a biannual Technology Radar.
This had unexpected side effects. When Neal spoke at conferences, attendees began
seeking him out to thank him for helping produce the Radar, often adding that their
company had started producing its own version. Neal also realized that this was the
answer to a question constantly asked at conference speaker panels: “How do you
keep up with technology? How do you figure out what to pursue next?” The answer,
of course, is that the speakers all have some form of internal radar.
Parts. The Thoughtworks Radar consists of four quadrants that attempt to cover
most of the software-development landscape:
Tools
Everything from development tools like IDEs to enterprise-grade integration
tools
Languages and frameworks
Computer languages, libraries, and frameworks, typically open source
Techniques
Any practice that assists software development overall, including processes, engineering practices, and advice
Platforms
Technology platforms, including databases, cloud vendors, and operating
systems
Rings. The Radar has four rings, listed here from outer to inner:
Hold
The original meaning of the Hold ring was “hold off for now, ” to represent
technologies that were too new to reasonably assess yet—technologies that were
getting lots of buzz but weren’t yet proven. The Hold ring has evolved, and now
indicates something more like “don’t start anything new with this technology. ”
There’s no harm in using it on existing projects, but think twice about using it for
new development.
Assess
The Assess ring indicates that a technology is worth exploring (such as through
development spikes, research projects, or conference sessions) to see how it
will affect the organization. For example, when mobile browsers became prominent, many large companies visibly went through this phase when formulating a
mobile strategy.
Trial
The Trial ring is for technologies worth pursuing. If a capability is in this ring,
it is important to understand how to build it. Now is the time to pilot a low-risk
project.
Adopt
Thoughtworks feels strongly that the industry should adopt the items listed in
the Adopt ring.
In the example view of the Radar in Figure 2-7 , each “blip” represents a different
technology or technique. While Thoughtworks uses the radar to broadcast its collective opinions about the software world, many developers and architects also use it
as a way of structuring their technology assessment process and organizing their
thinking about what to invest time in. For personal use, we suggest altering the
meanings of the quadrants to the following:
Hold
This can include not only technologies and techniques to avoid, but also habits
you are trying to break. For example, if you’re an architect from the .NET world,
you might be accustomed to reading the latest news and gossip on forums about
team internals. While entertaining, this may be a low-value information stream.
Placing it in the Hold ring serves as a reminder of what you want to avoid.
Assess
Use the Assess ring for promising technologies that you’ve heard good things
about but haven’t had time to assess for yourself yet. This ring forms a staging
area for more serious future research.
Trial
The Trial ring indicates active research and development, such as performing
spike experiments within a larger code base. These are technologies worth spending time on to understand more deeply so that you can include them effectively
in trade-off analysis.
Adopt
Y our personal Adopt ring represents the new things you’re most excited about
and best practices for solving particular problems.
Figure 2-7. A sample Thoughtworks Technology Radar
Most technologists pick technologies on a more or less ad hoc basis, based on what’s
cool or what their employers are using—but it’s dangerous to your career to adopt a
laissez-faire attitude toward your technology portfolio. Creating a technology radar
helps you formalize your thinking about technology and balance opposing decision
criteria. (For example, it might be harder to get a new job focused on the “cooler”
technology, whereas a more established technology might have a huge job market but
offer less interesting work.)
Treat your technology portfolio like a financial portfolio: diversify! Choose some
technologies and/or skills that are widely in demand, and track that demand. But
you might also want to try some technology gambits, like generative AI or embedded IOT devices. Anecdotes abound about developers who freed themselves from
cubicle-dwelling servitude by working late at night on open source projects that
became popular and, eventually, purchasable. This is yet another reason to focus on
breadth rather than depth.
Building a personal radar provides a good scaffolding for broadening your technology portfolio—but ultimately, the exercise is more important than the outcome.
Creating the radar visualization gives you an excuse to carve out time from your busy
schedule to think about these things, which is often the only way to accomplish this
kind of thinking.
While the most important part of building your personal radar is the conversations
it generates, it also produces some very useful visualizations. After much popular
demand from technologists building their own radar visualizations, Thoughtworks
released a tool called Build Y our Own Radar. With a Google spreadsheet as input,
it generates radar visualization showing your personal radar. We encourage every
technologist to leverage it.
