# Chapter 22: Analyzing Architecture Risk (continued)

## Risk-Storming Use Case (continued)

### Elasticity

The second risk-storming exercise focuses on elasticity—spikes in user load (otherwise known as variable scalability). Although there are only 250 nurses (which means no more than 250 nurses will be accessing the `Diagnostics Engine`), the self-service portion of the system can access the `Diagnostics Engine` as well, which significantly increases the number of requests to the `Diagnostics Engine` interface. The risk-storming participants are concerned about flu season and COVID outbreaks, which will significantly increase the anticipated load on the system.

The participants unanimously identify the `Diagnostics Engine` interface as high risk (9). Since it can handle only 500 requests per second, they correctly calculate a high risk that it won’t be able to keep up with the anticipated throughput, particularly with REST as its interface protocol.

The team decided that one way to mitigate this risk is to use asynchronous queues (messaging) for communication between the API Gateway and the `Diagnostics Engine` interface. This will provide a backpressure point if calls to the `Diagnostics Engine` get backed up. While this is a good practice, it still doesn’t quite mitigate all the risk: nurses and self-service patients will still be waiting too long for responses from the `Diagnostics Engine`, and their requests will likely time out.

The participants decide to use a pattern known as the *Ambulance* pattern to separate these requests by using two message channels instead of just one. This would let the system prioritize nurses’ requests over self-service requests. This would help mitigate the risk, but still doesn’t address wait times. After more discussion, the group decides to reduce outbreak-related calls to the `Diagnostics Engine` by caching those particular diagnostics questions so that they never reach the `Diagnostics Engine` interface.

In addition to creating two messaging channels (one for the nurses and one for self-service patients), the team creates a new service called the `Diagnostics Outbreak Cache Server` that handles all requests related to a particular outbreak or flu-related question (Figure 22-11). This new architecture reduces the number of calls to the diagnostics engine, allowing for more concurrent requests related to other symptoms. Without the risk-storming effort, this risk might not have been identified until flu season.

> **Figure 22-11.** Architecture modifications to address elasticity risk

### Security

Encouraged by these successes, the architect decides to facilitate a final risk-storming session focused on another crucial characteristic for this system—security. Due to HIPAA regulatory requirements, the `Medical Records Interface` must allow only nurses to access patients’ medical records. The architect believes that the authentication and authorization checks in the API Gateway neutralize this risk, but is curious whether the participants will find any other security risks.

The participants all identify the diagnostics system’s API Gateway as a high security risk (6). They cite the high impact if administrative staff or self-service patients access medical records (3), but rate the likelihood as medium (2). While the security checks for each API call help, all calls (self-service, admin, and nurses) are still going through the same API Gateway. They eventually convince the facilitator, who had initially rated this risk as low (2), that the risk is in fact high and needs to be mitigated.

Everyone agrees that having separate API Gateways for each type of user (admin staff, self-service users, and nurses) would prevent non-nurse calls from ever reaching the `Medical Records Interface`. The architect’s final version of the architecture is shown in Figure 22-12.

> **Figure 22-12.** Architecture modifications to address security risk

This example illustrates the power of risk storming. Architects, developers, and key stakeholders collaborate, consider the architectural characteristics most vital to the system’s success, and identify risk areas that would otherwise have gone unnoticed.

The original architecture (Figure 22-8) is significantly changed after risk storming (Figure 22-12) in ways that address concerns about availability, elasticity, and security and make this architecture more effective and more likely to succeed.

## Summary

Risk storming is not a one-time process. It continues throughout a system’s lifecycle, as teams work to identify and mitigate risk areas before they appear in production. How often an organization should hold risk-storming sessions depends on many factors, including the frequency of change, any architecture-refactoring efforts, and the architecture’s incremental development. It’s typical to do some risk storming on particular dimensions after adding a major feature or at the end of every iteration, to ensure that the architecture is correct and will address the business’s needs.
