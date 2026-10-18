# Chapter 22: Analyzing Architecture Risk (continued)

## Risk Storming

No architect can singlehandedly determine the overall risk of a system, for two reasons. First, an architect working alone might miss or overlook a risk area; second, very few architects have full knowledge of *every* part of the system. This is where risk storming can help.

*Risk storming* is a collaborative exercise to determine architectural risk within a specific dimension (either context or criteria). While most risk-storming efforts involve multiple architects, we strongly recommend including senior developers and tech leads as well. Not only will they provide an implementation perspective on architectural risk, but involving them helps them better understand the architecture.

Risk storming involves three phases: identification, consensus, and mitigation. In the individual phase (phase 1), all participants, working alone, use the risk matrix to assign risk to various areas of the architecture. This individual phase of risk storming is essential so that participants don’t influence other participants or direct people’s attention away from particular areas of the architecture. In the two collaborative phases, all participants work together to gain consensus on what the risk areas are and discuss them (phase 2), and come up with solutions for mitigating the risk (phase 3).

All three phases utilize a comprehensive or contextual architecture diagram (see Chapter 23). The architect conducting the risk-storming effort—we’ll call this person the *facilitator*—is responsible for sending all participants updated diagrams for the risk-storming session.

Figure 22-5 shows an example architecture we’ll use to illustrate the risk-storming process. In this architecture, an Elastic Load Balancer forwards a request to each EC2 instance containing the web servers (Nginx) and application services. The application services make calls to a MySQL database, a Redis cache, and a MongoDB database (for logging). They also make calls to the Push Expansion Servers, which in turn all interface with the MySQL database, Redis cache, and MongoDB logging facility. (Don’t worry if you don’t understand all of these products and buzzwords—this overly vague, generalized architecture is only meant to illustrate how risk storming works.)

> **Figure 22-5.** Example architecture diagram for risk storming session

We’ll begin with phase 1.

### Phase 1: Identification

The *identification* phase of risk storming involves each participant individually identifying areas of risk within the architecture. It’s critical that, in this phase, each participant should record their unbiased view of the risk involved, without being redirected or swayed by other participants. The identification phase has three steps:

1. The facilitator sends all participants an invitation to the collaborative phases. The invitation contains the architecture diagram (or where to find it), the risk criteria and context to be analyzed, and the date, time, and location (physical or virtual) of the collaborative session, along with any other logistical details.
2. Participants use the risk matrix to analyze the architecture risks individually.
3. Participants classify each risk as low (1–2), medium (3–4), or high (6–9), and write the numbers on small green, yellow, or red sticky notes.

Most risk-storming efforts analyze only one particular criterion or context (such as “Where are our security risks?” or “What areas are at risk within customer registration?”). However, if there are issues with staff availability or timing, the risk-assessment team may have to analyze multiple dimensions within a specific context (such as performance and scalability). In these cases, participants typically write the specific criterion next to the risk number on the sticky notes. For example, suppose three participants identify risk with a central database. All three participants identify the risk as high (6), but one participant sees this as a risk to availability, while the other two see it as a risk to performance. The participants should discuss these two criteria separately.

> **Tip:** Whenever possible, restrict risk-storming efforts to a single criterion or context. This allows participants to focus their attention on that specific dimension and avoids confusion about what the actual risk is.

### Phase 2: Consensus

The *consensus* phase of risk storming is highly collaborative, with the goal of gaining consensus among all participants regarding the risk or risks within the architecture. This activity is most effective when the facilitator posts a large printed architecture diagram on the wall (or an electronic version on a large screen). When the participants arrive at the risk-storming session, the facilitator instructs them to begin placing their risk-level sticky notes on the relevant area of the architecture diagram (see Figure 22-6).

Once all of the sticky notes are in place, the collaborative phase can begin. The goal here is to analyze the risk areas as a team and reach a consensus about their risk level. In the example pictured in Figure 22-6, the team has identified several areas of risk. (The actual criteria aren’t important for this example.) We can see that:

- Two participants identified the Elastic Load Balancer as medium risk (3), whereas one participant identified it as high risk (6).
- One participant identified the Push Expansion Servers as high risk (9).

- Three participants identified the MySQL database as medium risk (3).
- One participant identified the Redis cache as high risk (9).

- Three participants identified MongoDB logging as low risk (2).
- No one identified any other areas of the architecture as carrying any risk, so there are no sticky notes on any other areas.

> **Figure 22-6.** Initial identification of risk areas

The MySQL database and MongoDB logging need no further discussion in this session, since all participants agree on their risk levels. However, there’s a difference of opinion about the Elastic Load Balancer, and the Push Expansion Servers and Redis cache were only identified as risks by one participant each. Working through these discrepancies is what the collaborative phase is all about.

Two participants (Austen and Logan) identified the Elastic Load Balancer as medium risk (3); one (Addison) identified it as high risk (6). Austen and Logan ask Addison why they identified the risk as high. Addison responds that if the Elastic Load Balancer goes down, the entire system will become inaccessible. While this is true—and brings the *impact* rating up to high—the other two participants convince Addison that there is low risk of this happening due to clustering. Addison agrees, and the group brings the *likelihood* risk level down to a medium (3).

This could have gone a different way, however. If Austen and Logan missed a particular aspect of risk in the Elastic Load Balancer that Addison saw, Addison might have convinced the other two participants to classify this risk’s level as high instead of medium. That’s why the collaboration phase of risk storming is so important.

One participant identified the Push Expansion Servers as high risk (9), but no other participant identified any risk in this area of the architecture at all. The person who identified the risk explains that they rated the risk as high because they’ve had bad experiences with Push Expansion Servers continually crashing under high loads similar to this architecture’s load. This example shows the value of risk storming— without that participant’s involvement, no one would have seen the high risk until well into production.

The Redis cache is an interesting case. One participant, a developer named Devon, identified it as high risk (9), but no one else saw that cache as having any risk. When the other participants ask Devon about their rationale for rating this risk as high, Devon responds, “What’s a Redis cache?” Whenever a risk-storming participant identifies a technology as unknown to them, that area automatically gets assigned a high risk level (9).

> **Tip:** Always assign unproven or unknown technologies the highest risk rating (9), since the risk matrix cannot be used for this criterion or context.

The example of the Redis cache illustrates why it’s important to bring developers into risk-storming sessions. The fact that this participant didn’t know a given technology is valuable information for the architect about overall risk. The architect might decide to change the technology or incur training costs to bring the development team up to speed.

This phase continues until all participants agree on the risk areas identified. Once all the sticky notes are consolidated, this phase ends. Its final outcome is shown in Figure 22-7.

> **Figure 22-7.** Consensus of risk areas
