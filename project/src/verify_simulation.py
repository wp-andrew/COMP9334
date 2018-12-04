from collections import deque
from SetupDelayedoffSystem import simulate

# illustrate the setting up of servers, shutting down a server
# that is being setup and changing a job in the dispatcher
# from UNMARKED to MARKED.
print("EXAMPLE 1")
mode = 'trace'
arrival = deque([10, 20, 32, 33])
service = deque([1, 2, 3, 4])
m = 3
setup_time = 50
delayedoff_time = 100
time_end = float('inf')
simulate(mode, arrival, service, m, setup_time, delayedoff_time, time_end, True, 0)
print()

# illustrate the situation when there are multiple servers in
# the DE-LAYEDOFF state.
print("EXAMPLE 2")
mode = 'trace'
arrival = deque([1, 1.5, 11, 11.2, 11.3, 13])
service = deque([4, 0.5, 1, 1.4, 5, 1])
m = 3
setup_time = 5
delayedoff_time = 10
time_end = float('inf')
simulate(mode, arrival, service, m, setup_time, delayedoff_time, time_end, True, 0)
print()
