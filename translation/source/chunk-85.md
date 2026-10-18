# Chapter 22: Analyzing Architecture Risk

Every architecture comes with risks: some operational (such as availability, scalability, and data integrity), some structural (such as static coupling between logical components). Analyzing architecture risk is one of architects’ most important activities, allowing them to address deficiencies and structural decay within the architecture and take corrective action. In this chapter, we show you some key techniques and practices for quantifying, assessing, and identifying risk, and introduce an activity called *risk storming*.

## Risk Matrix

The first thing to determine in assessing architecture risk is its level: whether risk to a particular part of the architecture is low, medium, or high. The challenge here is that assessing risk can be *subjective*. One architect might hold the *opinion* that some aspect of the architecture is high risk, while another architect’s *opinion* might be that the same aspect is medium risk. We italicize *opinion* here to emphasize the subjectivity of assessing risk. Fortunately, architects have a useful risk-assessment matrix that helps us make risk more measurable.

The architecture risk-assessment matrix (Figure 22-1) uses two dimensions to qualify risk: the overall impact of the risk involved and the likelihood of that risk occurring. The architect rates each dimension as low (1), medium (2), or high (3), then multiplies the numbers within each intersection of the matrix. This provides a numerical representation of risk, making the process of qualifying risk more *objective*. Ratings of 1 and 2 are considered low risk (usually depicted in green), numbers 3 and 4 are considered medium risk (usually yellow), and numbers 6 through 9 are considered high risk (usually red). Using shading can be helpful for grayscale rendering and for people unable to distinguish colors.

> **Figure 22-1.** Matrix for determining architecture risk

To show you its utility, we’ll use the risk matrix in an example. Suppose you’re concerned about the availability of your application’s primary central database.

> **Tip:** When using this matrix to qualify risk, consider impact first and likelihood second. If you are unsure of the likelihood, use a high (3) rating until you can confirm.

First, you’ll consider overall impact: what happens if the database goes down or becomes unavailable? Let’s say you might deem the impact high risk and map that risk to the last row of the matrix in Figure 22-1 as a 3 (medium), 6 (high), or 9, (high). However, when you consider the second dimension—the likelihood of that risk occurring—you realize that the database is on highly available servers in a clustered configuration, and the *likelihood* that the database would become unavailable is low (first column in the matrix). The intersection between high impact and low likelihood gives you an overall risk rating of 3 (medium risk) for availability in the primary central database.

## Risk Assessments

You can use the risk matrix to build what is called a *risk assessment*: a summarized report of an architecture’s overall risk, with meaningful assessment criteria based on a context (services, subdomain areas, or domain areas of a system). We’ve performed many risk assessments, and have found architectural characteristics to be excellent risk-assessment criteria. Why spend time analyzing performance risk when the system’s critical architectural characteristics are scalability, elasticity, and data integrity? Knowing characteristics such as those described in Chapter 4 is the first step in analyzing architectural risk.

> **Tip:** The architectural characteristics that are most critical for the architecture to support make great risk-assessment criteria.

The basic format of a risk-assessment report is shown in Figure 22-2. Here, 1 and 2 represent low risk, 3 and 4 represent medium risk, and 6 and 9 represent high risk. The risk criteria run along the left side of the spreadsheet, and the context runs across the top.

> **Figure 22-2.** Example of a standard risk assessment

We use an ecommerce ordering system as the example for this risk assessment. It assesses five criteria, representing the system’s critical architectural characteristics. Across the top are four different contexts, each representing a separate domain (customer registration, catalog checkout, order fulfillment, and order shipping). A domain or subdomain context works well; analyzing risk at the level of services is usually too fine-grained and doesn’t account for risk involving communication or coordination between multiple services.

The nice thing about using quantified risk is that it considers both the risk criteria and the context. For example, in Figure 22-2, the total accumulated risk for data integrity is 17, making it the highest risk area from a criteria standpoint. The accumulated risk for availability is only 10 (the lowest risk criteria-wise). In terms of the relative risk of each context area, however, customer registration is the domain that carries the highest risk context-wise, whereas order fulfillment is the lowest-risk context. This is useful information when determining priorities and where to put additional effort into reducing risk.

This risk assessment example contains all of the risk-analysis results, but it’s sometimes useful to filter out details to highlight certain problems. For example, suppose that you, as the architect of this system, are in a meeting, presenting to stakeholders about the high-risk areas of the system. Rather than presenting the full risk assessment, as Figure 22-2 does, you could filter out the low- and medium-risk areas (the noise) to highlight the high-risk areas (the signal). Improving the overall signal-to-noise ratio lets you deliver a more effective, less distracting message. Figure 22-3 shows a filtered version of the same risk assessment. Compare the two images to see how much clearer the message is with the second filtered assessment.

> **Figure 22-3.** Filtering the risk assessment to show only high risks

One problem with the full version of the risk assessment is that it only shows a snapshot in time, not whether things are improving or getting worse. In other words, Figure 22-2 does not show the *direction of risk*. You can determine the direction of risk by using continuous measurements through fitness functions, as described in Chapter 6. Objectively analyzing each risk criterion lets you observe trends to spot the direction of each risk criterion.

In Figure 22-4, we add a third dimension to the risk assessment: *direction*. We use a right-side-up triangle to indicate that the risk for that particular criteria and context is getting worse—the tip of the triangle points up, toward a *higher* number. Conversely, we use an upside-down triangle to indicate that the risk is lessening (in other words, the tip is pointing down to a *lower* number). Finally, we use a circle to represent that the risk is not moving—getting neither better nor worse. This can get confusing, so we always recommend including a key when using any sort of symbol to represent direction.

> **Figure 22-4.** Showing direction of risk using triangles

This revised architectural risk assessment, now showing direction, tells a different story than the original. First, we can see that data integrity is getting worse based on continuous measurements (triangle pointing up) for catalog checkout, order fulfillment, and order shipping, which could indicate a database issue. However, security and availability are getting better overall (triangle pointing down) for customer registration and catalog checkout, indicating improvements in those areas.

Next, we describe a process called *risk storming* that teams can use to determine *how* to identify the risk level for particular contexts and criteria.
