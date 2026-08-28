# AQT-Simulation_Coffee-Shop-Simulation_Rojas

a.	Context
Model a coffee shop with a fixed number of baristas serving customers who arrive at random times throughout an 8-hour day, and measure how long customers wait in line. This is a classic operations-research question: “If we add a second barista, how much shorter is the average wait?”
b.	Simulation Design
●	Customer arrivals follow a Poisson process (random, independent arrivals) at an average rate of 12 customers/hour.
●	Each order takes a random amount of time to prepare, averaging 7 minutes (exponential distribution).
●	Baristas are modeled as a shared SimPy Resource with a configurable capacity (number of baristas).
●	The simulation records every customer’s wait time and runs for a simulated 8-hour (480-minute) shift.
c.	Setting uo
Using the environment already created in the reference guide (Steps 1–2):
# from inside the activated simulation_env
pip install simpy numpy matplotlib
 
# save the code below as coffee_shop_simulation.py, then run:
python coffee_shop_simulation.py

d.	 Simulation Code (main.py)
Full commented source is attached as a separate .py file. Check out the attached github repository for the entirety of the source code. Core logic:
class CoffeeShop:
    def __init__(self, env, num_baristas):
        self.env = env
        self.baristas = simpy.Resource(env, capacity=num_baristas)
        self.wait_times = []
 
def customer(env, name, shop):
    arrival_time = env.now
    with shop.baristas.request() as request:
        yield request                      # wait for a free barista
        wait = env.now - arrival_time
        shop.wait_times.append(wait)
        yield env.process(shop.make_coffee(name))
 
def customer_arrivals(env, shop):
    rate_per_minute = ARRIVAL_RATE_PER_HOUR / 60.0
    while True:
        yield env.timeout(random.expovariate(rate_per_minute))
        env.process(customer(env, 'Customer', shop))

e.	Sample output
Running the model with 2 baristas over a simulated 8-hour day (representative run):
●	Customers served: 98
●	Average wait time: 3.76 minutes
●	Longest wait time: 22.93 minutes
●	Customers who waited more than 5 minutes: 28.6%
