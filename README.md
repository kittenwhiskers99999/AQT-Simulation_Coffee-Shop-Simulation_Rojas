# AQT-Simulation_Coffee-Shop-Simulation_Rojas

Part 1: Simulation Tools Researched
Five simulation tools were researched, covering both code-based and GUI-based options, from beginner-friendly to industrial-grade:
1. SimPy
A lightweight, pure-Python library for discrete-event simulation (DES). Simulations are written as ordinary Python generator functions — a process "yields" a timeout or waits for a shared resource (like a barista, a checkout counter, or a machine) to become free. No extra software beyond Python and pip is required.
2. Mesa
The standard Python framework for agent-based modeling (ABM). Agents live on a grid or network, follow simple local rules each "step," and Mesa collects data on the population as a whole. Good for modeling emergent behavior — e.g., how a disease spreads, or how traffic jams form from individual driver decisions.
3. NetLogo
A standalone desktop application with its own simplified, Logo-based scripting language, built specifically to make agent-based modeling approachable for people without a programming background. It ships with a large library of ready-made sample models that can be opened and modified directly.
4. AnyLogic
A commercial, Java-based desktop application that supports three simulation paradigms in one tool: discrete-event, agent-based, and system dynamics. It is widely used in industry for supply chain, manufacturing, and business process simulation, and has a free "Personal Learning Edition" for students.
5. JaamSim
A free, open-source, drag-and-drop discrete-event simulation tool. Models are built visually by placing and connecting objects (queues, servers, resources) rather than writing code, which makes it attractive for process-flow modeling, though it still requires installing a Java runtime and learning its GUI.
Part 2 — Selected Tool: SimPy
SimPy was chosen as the tool for our lessons and lab exercises for the following reasons:
●	Fastest setup — a single command (pip install simpy) inside the virtual environment already created in Step 2 of the setup guide. No separate application, license, or Java runtime to install.
●	Pure Python — it plugs directly into the same environment already used for NumPy, Matplotlib, and Pandas, so results can be analyzed and plotted with tools we already know.
●	Readable code — a SimPy model reads almost like a plain description of the process being simulated (customer arrives → waits for barista → gets served), which makes it easy to follow in a classroom setting.
●	Directly matches Step 3 of the reference setup guide, which already lists simpy as one of the core libraries to install — no deviation from the prescribed environment.
●	Well documented, actively maintained, and widely used for teaching queueing theory and operations-research concepts.
Part 3 — Project Simulation: Coffee Shop Queueing Simulation
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
