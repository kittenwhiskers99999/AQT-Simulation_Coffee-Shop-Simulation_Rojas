"""
Coffee Shop Queueing Simulation
Author: <YOUR NAME HERE>
Tool used: SimPy (discrete-event simulation library for Python)

WHAT THIS SIMULATES
--------------------
A coffee shop with a fixed number of baristas serves customers who arrive
randomly throughout an 8-hour day. Customers arrive following a Poisson
process (random, independent arrivals) and each order takes a random amount
of time to prepare (exponentially distributed service time). The simulation
tracks how long each customer waits in line before being served.

This is a classic "M/M/c queue" problem (c = number of servers), commonly
used in operations research to decide questions like:
    "If we add a second barista, how much does average wait time drop?"

HOW TO RUN
----------
1. pip install simpy numpy matplotlib
2. python coffee_shop_simulation.py
"""

import random
import simpy
import numpy as np
import matplotlib.pyplot as plt

# ---------------------------------------------------------------------------
# Simulation parameters (change these to experiment)
# ---------------------------------------------------------------------------
RANDOM_SEED = 42
NUM_BARISTAS = 2            # number of servers (try 1 vs 2 vs 3)
ARRIVAL_RATE_PER_HOUR = 12  # average customers arriving per hour
SERVICE_TIME_MEAN = 7       # average minutes to prepare one order
SIM_TIME_MINUTES = 8 * 60   # simulate one 8-hour work day


class CoffeeShop:
    """Wraps the SimPy environment and resources for the coffee shop."""

    def __init__(self, env, num_baristas):
        self.env = env
        self.baristas = simpy.Resource(env, capacity=num_baristas)
        self.wait_times = []

    def make_coffee(self, customer_name):
        """The time it takes a barista to prepare one order."""
        service_time = random.expovariate(1.0 / SERVICE_TIME_MEAN)
        yield self.env.timeout(service_time)


def customer(env, name, shop):
    """A single customer: arrives, waits for a free barista, gets served."""
    arrival_time = env.now

    with shop.baristas.request() as request:
        yield request  # wait here until a barista is free
        wait = env.now - arrival_time
        shop.wait_times.append(wait)
        yield env.process(shop.make_coffee(name))


def customer_arrivals(env, shop):
    """Generates customers with random (Poisson) interarrival times."""
    customer_id = 0
    rate_per_minute = ARRIVAL_RATE_PER_HOUR / 60.0

    while True:
        interarrival = random.expovariate(rate_per_minute)
        yield env.timeout(interarrival)
        customer_id += 1
        env.process(customer(env, f"Customer-{customer_id}", shop))


def run_simulation():
    random.seed(RANDOM_SEED)

    env = simpy.Environment()
    shop = CoffeeShop(env, NUM_BARISTAS)
    env.process(customer_arrivals(env, shop))
    env.run(until=SIM_TIME_MINUTES)

    return np.array(shop.wait_times)


def report_results(wait_times):
    print("=" * 50)
    print("COFFEE SHOP SIMULATION RESULTS")
    print("=" * 50)
    print(f"Baristas on duty:        {NUM_BARISTAS}")
    print(f"Simulated day length:    {SIM_TIME_MINUTES/60:.0f} hours")
    print(f"Customers served:        {len(wait_times)}")
    print(f"Average wait time:       {wait_times.mean():.2f} minutes")
    print(f"Longest wait time:       {wait_times.max():.2f} minutes")
    print(f"Customers who waited >5 min: {(wait_times > 5).mean() * 100:.1f}%")
    print("=" * 50)

    plt.figure(figsize=(8, 5))
    plt.hist(wait_times, bins=25, color="#6f4e37", edgecolor="white")
    plt.xlabel("Customer wait time (minutes)")
    plt.ylabel("Number of customers")
    plt.title(f"Wait Time Distribution ({NUM_BARISTAS} barista(s), "
              f"{SIM_TIME_MINUTES // 60}-hour day)")
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig("wait_time_distribution.png", dpi=150)
    print("Saved chart to wait_time_distribution.png")
    plt.show()


if __name__ == "__main__":
    waits = run_simulation()
    report_results(waits)