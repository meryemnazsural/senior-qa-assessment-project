# Load Test Scenarios

1. Baseline search response time for a common keyword such as `iphone`.
2. Compare high-demand keywords such as `iphone` and `samsung` under the same single-user pacing.
3. Verify system behavior when the search term should return zero or minimal results.
4. Track response times, request failure rate, and percentile latency in the Locust report.
5. Extend later with stepped concurrency, soak duration, or category-filtered searches if needed.
