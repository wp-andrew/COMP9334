from collections import deque
from SetupDelayedoffSystem import simulate

test_folder = ""

def run_simulation(simulation_number, debug, random_seed):
    with open(test_folder + "mode_" + str(simulation_number) + ".txt") as file:
        mode = file.readline().strip()
    with open(test_folder + "para_" + str(simulation_number) + ".txt") as file:
        para = []
        for line in file.readlines():
            para.append(line.strip())
    with open(test_folder + "arrival_" + str(simulation_number) + ".txt") as file:
        arrival = deque()
        for line in file.readlines():
            arrival.append(float(line.strip()))
    with open(test_folder + "service_" + str(simulation_number) + ".txt") as file:
        service = deque()
        for line in file.readlines():
            service.append(float(line.strip()))
    
    if mode == "random":
        mean_response_time, departure_times = simulate(mode, arrival[0], service[0], int(para[0]), float(para[1]), float(para[2]), float(para[3]), debug, random_seed)
    else:   # mode == "trace"
        mean_response_time, departure_times = simulate(mode, arrival, service, int(para[0]), float(para[1]), float(para[2]), float('inf'), debug, random_seed)
    
    with open(test_folder + "mrt_" + str(simulation_number) + ".txt", "w") as file:
        file.write(str(mean_response_time) + "\n")
    with open(test_folder + "departure_" + str(simulation_number) + ".txt", "w") as file:
        for departure_time in departure_times:
            file.write(str(departure_time[0]) + "\t" + str(departure_time[1]) + "\n")

    return mean_response_time, departure_times

with open(test_folder + "num_tests.txt") as file:
    num_tests = int(file.readline())
    
for test_number in range(1, num_tests + 1):
    run_simulation(test_number, False, 0)
