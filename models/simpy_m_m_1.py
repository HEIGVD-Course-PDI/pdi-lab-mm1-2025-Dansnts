"""SimPy simulation of an M/M/1 queueing system.
The system has a single server and an infinite queue.
The inter-arrival time is exponentially distributed (Poisson arrivals).
The service time is exponentially distributed.
"""

import random
from statistics import mean

# ---------------------------------------------------------------------------
class SimpyQueue:
    """Class representing an M/M/1 queueing system using SimPy."""

    def __init__(self, env, server, arrival_rate, service_rate):
        """Initialize the parameters of the M/M/1 queueing system and the statistics arrays."""
        self.env = env
        self.server = server
        self.arrival_rate = arrival_rate 
        self.service_rate = service_rate 
        # Statistics
        self.response_times = []
        self.clients_in_system = []
        self.request_count = 0  # Track total requests for debugging


    def generate_requests(self):
        """Generate requests following a Poisson process."""
        while True:
            yield self.env.timeout(random.expovariate(self.arrival_rate))
            self.env.process(self.process_request())


    def process_request(self):
        """Place a request in the queue and process it when the server is available.
        
        The method also records statistics about the response time.
        """
        arrival_time = self.env.now
        self.request_count += 1

        with self.server.request() as request:
            yield request
            
            yield self.env.timeout(random.expovariate(self.service_rate))

        departure_time = self.env.now
        response_time = departure_time - arrival_time
        self.response_times.append(response_time)


    def record_statistics(self, sampling_interval):
        """Periodically collect statistics about the number of clients in the system."""
        while True:
            yield self.env.timeout(sampling_interval)
            self.clients_in_system.append(self.server.count + len(self.server.queue))


    def compute_statistics(self):
        """Compute and return the mean response time and mean number of clients in the system."""
        if not self.response_times:
            return {'E[T]': 0, 'E[N]': 0}
        
        mean_response_time = mean(self.response_times)
        mean_clients_in_system = mean(self.clients_in_system)
        
        # Debug info
        print(f"Total requests processed: {self.request_count}")
        print(f"Response times recorded: {len(self.response_times)}")
        print(f"Utilization: {self.arrival_rate / self.service_rate:.3f}")
        
        return {'E[T]': mean_response_time, 'E[N]': mean_clients_in_system}