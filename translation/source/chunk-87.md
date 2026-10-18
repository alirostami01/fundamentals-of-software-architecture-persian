# Chapter 22: Analyzing Architecture Risk (continued)

## Risk Storming (continued)

### Phase 3: Risk Mitigation

Once all participants agree on the risk levels of the architecture, the *risk mitigation* phase begins. Mitigating risk usually involves changing certain areas of the architecture that otherwise might have been deemed perfect the way they were.

This phase, which is also collaborative, seeks ways to reduce or eliminate the risks identified in the second phase. Depending on the risks identified, the original architecture may need to be completely changed, or the changes could be limited to straightforward architectural refactoring in specific areas, such as adding a queue for backpressure to reduce a throughput bottleneck.

Whatever the changes required, the risk mitigation phase usually incurs additional costs. For that reason, it’s important for this phase to involve key business stakeholders with the authority to decide whether the cost of a given mitigation solution outweighs the risk.

For example, suppose that, in our example risk-storming session the team identifies the central database as having medium risk (4) with regard to overall system availability. The participants agree that clustering the database and breaking it into separate physical databases would mitigate that risk. However, that solution would cost $50,000. The facilitating architect meets with key business stakeholders, including the owner, to discuss the trade-offs of availability risk and cost. The business owner decides that the price tag is too high and that the cost does not outweigh the risk of availability. The architect then suggests a different approach: instead of expensive clustering, what about splitting the database into two separate domain-based databases? This solution would only cost $16,000, while still reducing the availability risk. The stakeholders agree to this compromise.

This scenario shows how risk storming shapes not only the overall architecture, but also the negotiations between architects and business stakeholders. In combination with the risk assessments we described at the start of this chapter, risk storming is an excellent vehicle for identifying and tracking risk, improving the architecture, and structuring negotiations between key stakeholders.

## User-Story Risk Analysis

Risk storming is useful in many aspects of software development aside from identifying architectural risk. For example, a development team could use risk storming to determine the overall risk associated with user-story completion within a given iteration (and consequently the overall risk assessment of that iteration) during story grooming. Using the same risk matrix, the team can identify user-story risk by identifying the overall impact if the story is not completed within the iteration, and the likelihood that the story will not be completed in the current iteration. Then they can identify high-risk stories, track them carefully, and better prioritize them.

## Risk-Storming Use Case

To illustrate the power of risk storming and how it can improve overall architecture, let’s consider the example of a support system for a call center where nurses advise patients on various health conditions. The system requirements are:

- A third-party diagnostics engine will serve up questions and guide nurses and patients through their medical issues. This engine can handle about 500 requests a second.
- Patients can either call in using the call center to speak to a nurse or use a self-service website that accesses the same diagnostic engine directly.
- The system must support 250 concurrent nurses nationwide and up to hundreds of thousands of concurrent self-service patients nationwide.
- Nurses can access patients’ medical records through a medical records exchange, but patients cannot access their own medical records.
- The system must be HIPAA (Health Insurance Portability and Accountability Act) compliant, meaning it’s essential that no one but nurses can access patients’ medical records. The self-service option cannot guarantee HIPAA compliance.
- The system needs to be able to handle high volume during cold, flu, and COVID outbreaks.
- Calls are routed to nurses based on each nurse’s skill profile (such as languages spoken or medical specializations).

After analyzing these requirements, Logan, the architect responsible for this system, creates the high-level architecture diagrammed in Figure 22-8. This architecture has three separate web-based UIs: one for self-service, one for nurses receiving calls, and one for administrative staff to add and maintain nurse profiles and configuration settings. The call-center portion of the system consists of a `Call Accepter` service, which receives calls, and the `Call Router` service, which routes the caller to the next available nurse based on the nurse’s skill profile. The `Call Router` service accesses the central database to get nurse profile information. Central to this architecture is a diagnostics-system API Gateway, which performs security checks and directs requests to the appropriate backend service.

> **Figure 22-8.** High-level architecture for a nursing-hotline diagnostics system

The four main services in this system are the `Case Management` service, the `Nurse Profile Management` service, the `Medical Records Interface` service to the medical records exchange, and the external third-party `Diagnostics Engine Interface` service. All communications use REST, except for proprietary protocols to the external systems and call-center services. The areas the architecture must support are, in summary, availability, elasticity, and security.

After many reviews, Logan believes the architecture is ready for implementation. However, being a responsible and effective architect, Logan decides to hold a risk-storming exercise.

### Availability

As facilitator, Logan decides to focus the first risk-storming exercise on availability, which is critical to the system’s success. After the identification and collaboration phases, the participants come up with the following risk areas (illustrated in Figure 22-9):

- Central database availability: high risk (6) due to high impact (3) and medium likelihood (2) of the database being unavailable when needed.
- `Diagnostics Engine` availability: high risk (9) due to high impact (3) and unknown likelihood (3) of unavailability.
- `Medical Records Interface` availability: low risk (2); this component is not required to determine a particular medical outcome.
- The team has deemed no other parts of the system to be availability risks, since the architecture includes multiple instances of each service and clusters the API Gateway.

> **Figure 22-9.** Availability risk areas, as identified by the risk-storming team

All participants agree that if the database went down, nurses could write down case notes manually, but the call router could not function. To mitigate this risk, they collectively decide to break apart the single physical database into two separate databases: one clustered database containing nurse-profile information, and one single-instance database for case notes. Not only does this architecture change address the database availability concerns, it also helps secure the case notes.

It’s much harder to mitigate availability risk in external systems (in this case, the `Diagnostics Engine` and `Medical Records Interface`) because they are controlled by a third party. The team decides to research whether these systems have published service-level agreements (SLAs) or service-level objectives (SLOs). An SLA is usually a legally binding contractual agreement; an SLO is usually not legally binding. They find SLAs for both systems. The `Diagnostics Engine` SLA guarantees 99.99% availability (that’s 52.60 minutes of downtime per year), and the `Medical Records Interface` guarantees at 99.90% availability (that’s 8.77 hours of downtime per year). Based on this analysis, this information was enough for the risk assessment team to remove the identified risk.

After this risk-storming session, the team changes the architecture, as illustrated in Figure 22-10, creating two databases and adding the SLAs to the architecture diagram.

> **Figure 22-10.** Availability risk areas can be mitigated by using separate databases
