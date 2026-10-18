# Chapter 16: Space-Based Architecture Style (continued)

## Common Risks (continued)

### Data Collisions

A data collision occurs when data is updated in one cache instance (cache A), and during replication to another cache instance (cache B), the same data is updated by that cache (cache B). This can happen when using replicated caching in an active/ active state, meaning that multiple processing units can update the same data at the same time. Collisions typically occur when the update rate of the data in the cache exceeds the replication latency (RL)—the time it takes to synchronize each same-named cache. In this scenario, the local update to cache B will be overridden by the old data from cache A, and the same data in cache A will be overridden by the update from cache B. This makes the data in each cache inconsistent.

To demonstrate the data collision problem, let’s assume there are two service instances (A and B) of an order placement service, each containing a replicated cache of product inventory (blue widgets). The flow is as follows:

1. The current inventory count is 500 units in each instance A and B. 

2. Instance A receives a request from a customer to purchase 10 units, and updates the inventory cache for blue widgets to 490 units.

3. Before instance A’s data can be replicated to instance B, instance B receives a purchase request for 5 units, and updates the inventory cache for blue widgets to 495 units.

4. The cache in instance B gets updated to 490 units due to replication from instance A’s update.

5. The cache in instance A gets updated to 495 units due to replication from instance B’s update.

6. Both caches are incorrect and out of sync: the inventory should be 485 units in each of the instances.

Several factors that influence how many data collisions might occur: the number of processing-unit instances that contain the same cache, the cache’s update rate, the cache’s size, and the RL of the caching product. We can probabilistically determine how many potential data collisions might occur based on these factors, using the following formula:

```latex
\text{CollisionRate} = N \times \frac{UR^2}{S} \times RL
```

Here, N represents the number of service instances using the same named cache. UR represents the update rate in milliseconds (squared), S is the cache size (in number of rows), and RL is the caching product’s replication latency (in milliseconds).

This formula is useful for determining the percentage of data collisions that will likely occur based on updates within a given time frame (for example, each hour), and thus how feasible it would be for this system to use replicated caching. For example, consider the values shown in Table 16-2 for the factors involved in this calculation.

Table 16-2. Base values

| Factor | Value |
|---|---|
| Update rate (UR): | 20 updates/second |
| Number of instances (N): | 5 |
| Cache size (S): | 50,000 rows |
| Replication latency (RL): | 100 milliseconds |
| Updates: | 72,000 per hour |
| Collision rate: | 14.4 per hour |
| Percentage: | 0.02% |

Applying these factors to the formula yields 72,000 updates an hour, with a high probability that 14 updates to the same data may collide. Given the low percentage (0.02%), replication would be a viable option.

Variations in RL can have a significant impact on data consistency. Replication latency depends on many factors, including the type of network and the physical distance between processing units. RL values must be calculated and derived from actual measurements in a production environment, which is why they’re rarely published. The value of 100 ms used in the prior example is a good planning number if the actual RL is unavailable. For example, changing the RL from 100 ms to 1 ms yields the same number of updates (72,000 per hour) but produces a much lower probability of collisions occurring (0.1 collisions per hour). This scenario is shown in Table 16-3.

Table 16-3. Impact on replication latency

| Factor | Value |
|---|---|
| Update rate (UR): | 20 updates/second |
| Number of instances (N): | 5 |
| Cache size (S): | 50,000 rows |
| Replication latency (RL): | 1 millisecond (changed from 100) |
| Updates: | 72,000 per hour |
| Collision rate: | 0.1 per hour |
| Percentage: | 0.0002% |

The number of processing units that contain the same named cache (as represented by N) also has a direct proportional relationship to the number of possible data collisions. For example, reducing the number of processing units from 5 instances to 2 instances yields a data-collision rate of only 6 per hour, out of 72,000 updates per hour, as shown in Table 16-4.

Table 16-4. Impact on the number of processing-unit instances

| Factor | Value |
|---|---|
| Update rate (UR): | 20 updates/second |
| Number of instances (N): | 2 (changed from 5) |
| Cache size (S): | 50,000 rows |
| Replication latency (RL): | 100 milliseconds |
| Updates: | 72,000 per hour |
| Collision rate: | 5.8 per hour |
| Percentage: | 0.008% |

The cache size is the only factor that is inversely proportional to the collision rate: as the cache size decreases, collision rates increase. In this example, reducing the cache size from 50,000 rows to 10,000 rows (and keeping everything else the same as in the first example) yields a collision rate of 72 per hour, significantly higher than with 50,000 rows, as shown in Table 16-5.

Table 16-5. Impact on cache size

| Factor | Value |
|---|---|
| Update rate (UR): | 20 updates/second |
| Number of instances (N): | 5 |
| Cache size (S): | 10,000 rows (changed from 50,000) |
| Replication latency (RL): | 100 milliseconds |
| Updates: | 72,000 per hour |
| Collision rate: | 72.0 per hour |
| Percentage: | 0.1% |

Under normal circumstances, most systems do not have consistent update rates over a long period of time (such as an eight-hour day). When using this calculation, we recommend understanding your system’s maximum update rate during peak usage and calculating minimum, normal, and peak collision rates.

## Governance

Space-based architecture, with its many moving parts, is a complicated architectural style to design and implement. Proper governance is critical to ensuring success— especially for controlling memory consumption, given this style’s issues with internal memory usage (as we noted earlier, in “Common Risks” on page 303).

To address these memory issues, we recommend writing a continuous, automated governance fitness function to have each instance of a processing unit make its current memory usage observable periodically. Since all instances of a processing unit have the same replicated cache, the fitness function only needs to report on the name of the processing unit. Use a separate fitness function to record the number of instances for each processing unit, allowing you to calculate the total memory consumption per processing unit. Figure 16-15 shows an example of this continuous fitness function’s output.

Figure 16-15. An example fitness function to track memory consumption

Another useful governance strategy to maintain overall data consistency is to track and measure synchronization time—specifically, how long it takes a cache update to sync to the corresponding database. A good method is to have each processing unit stream the request ID of an update along with its corresponding timestamp, and have each data writer stream the same request ID along with the timestamp after the database commit. Then, write a fitness function to associate these request IDs and subtract the timestamps to calculate the synchronization time. The fitness function could track this at an atomic level, using times associated with a particular processing unit, or holistically, by averaging the overall synchronization times. Analyzing these trends helps architects track the effects of changes to the architecture, such as whether the changes are making synchronization times better or worse, and whether the architecture is meeting the business’s synchronization timing goals. Figure 16-16 illustrates this kind of governance through a continuous fitness function.

Figure 16-16. An example fitness function to track aggregated average synchronization times

As we’ve noted, because data pumps act as a backpressure point in space-based architecture and because database writes take longer than cache writes, data pumps can form a bottleneck in the overall system. To govern this, we recommend tracking and measuring this kind of bottleneck when it arises. First, to determine the extent of the bottleneck, write a fitness function to track the queue depth of the queue used in the data pumps. Too much of a bottleneck increases the synchronization time (and thus data consistency) and also increases the chances of data loss and data collisions, particularly during periods of high user-concurrency levels. Like the previous fitness function, this function can report atomically about each data-pump queue or aggregate the overall system average. Figure 16-17 shows a bottleneck analysis for an Order Placement processing unit and its corresponding data pump in a typical order-processing system.

Figure 16-17. An example fitness function to track data-pump bottlenecks

Other governance fitness functions for space-based architecture could track the frequency of reads to the database (requests to data readers), which can affect scalability, elasticity, and responsiveness. It’s also a good idea to use fitness functions to measure scalability, elasticity, and responsiveness: since these architectural characteristics are the main reasons to use a space-based architecture, it makes sense to track and measure them.
