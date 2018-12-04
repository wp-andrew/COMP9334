from collections import deque
from math import log
from random import random, seed

def simulate(mode, arrival, service, m, setup_time, delayedoff_time, time_end, debug, random_seed):
    if mode == "random":
        el, mu = arrival, service
        arrival, service = deque(), deque()
        seed(random_seed)
        next_arrival_time = -log(1 - random()) / el
        next_service_time = (-log(1 - random()) / mu) + (-log(1 - random()) / mu) + (-log(1 - random()) / mu)
        while next_arrival_time < time_end:
            arrival.append(next_arrival_time)
            service.append(next_service_time)
            next_arrival_time = next_arrival_time + (-log(1 - random()) / el)
            next_service_time = (-log(1 - random()) / mu) + (-log(1 - random()) / mu) + (-log(1 - random()) / mu)

    dispatcher = deque()
    servers = [[]] + [["OFF", None, float('Inf')] for _ in range(m)]
    cumulative_response_time = 0.0
    nb_of_completed_jobs = 0
    departure_times = []
    
    master_clock = min([arrival[i] for i in range(1) if len(arrival) > 0]
                       + [servers[server_no][2] for server_no in range(1, m + 1)]
                       + [float('inf')])
    # while there is at least 1 job in the system
    while master_clock <= time_end and master_clock != float('Inf'):
        ## Handling arrivals ##
        if len(arrival) > 0 and master_clock == arrival[0]:
            arrival_time, service_time = arrival.popleft(), service.popleft()
            # pick a server in the DELAYEDOFF state with the highest Tc and the first server in the OFF state
            to_BUSY, to_SETUP  = [None, 0], None
            for server_no in range(1, m + 1):
                if servers[server_no][0] == "DELAYEDOFF" and servers[server_no][2] > to_BUSY[1]:
                    to_BUSY = [server_no, servers[server_no][2]]
                elif servers[server_no][0] == "OFF" and not to_SETUP:
                    to_SETUP = server_no
            # if there is at least one server in the DELAYEDOFF state
            if to_BUSY[0]:
                # send job to the server with the highest Tc
                servers[to_BUSY[0]] = ["BUSY", [arrival_time, service_time], master_clock + service_time]
            # else if there is at least one server in the OFF state
            elif to_SETUP:
                # setup the first server in the OFF state
                servers[to_SETUP] = ["SETUP", None, master_clock + setup_time]
                # put the job at the end of the queue, MARKED
                dispatcher.append([arrival_time, service_time, "MARKED"])
            else:
                # put the job at the end of the queue, UNMARKED
                dispatcher.append([arrival_time, service_time, "UNMARKED"])
                
        else:
            for server_no in range(1, m + 1):
                if master_clock == servers[server_no][2]:
                    # if the server has finished its SETUP
                    if servers[server_no][0] == "SETUP":
                        # take the first MARKED job off the queue
                        for queue_no in range(len(dispatcher)):
                            if dispatcher[queue_no][2] == "MARKED":
                                servers[server_no] = ["BUSY", dispatcher[queue_no][0:2], master_clock + dispatcher[queue_no][1]]
                                dispatcher.remove(dispatcher[queue_no])
                                break

                    ## Handling departures ##
                    # else if the server has finished processing a job
                    elif servers[server_no][0] == "BUSY":
                        cumulative_response_time += (servers[server_no][2] - servers[server_no][1][0])
                        departure_times.append((servers[server_no][1][0], servers[server_no][2]))
                        nb_of_completed_jobs += 1
                        # if the dispatcher queue is empty
                        if len(dispatcher) == 0:
                            # change the server state to DELAYEDOFF
                            servers[server_no] = ["DELAYEDOFF", None, master_clock + delayedoff_time]
                        else:
                            # take a job from the head of the queue, server remains BUSY
                            arrival_time, service_time, status = dispatcher.popleft()
                            servers[server_no] = ["BUSY", [arrival_time, service_time], master_clock + service_time]
                            # if the job is MARKED
                            if status == "MARKED":
                                # if there is at least an UNMARKED job at the queue, take the first UNMARKED job and MARKED it
                                for queue_no in range(len(dispatcher)):
                                    if dispatcher[queue_no][2] == "UNMARKED":
                                        dispatcher[queue_no][2] = "MARKED"
                                        break
                                # else turn OFF one of the servers in the SETUP state with the highest Tc
                                else:
                                    to_OFF = [None, 0]
                                    for server_nb in range(1, m + 1):
                                        if servers[server_nb][0] == "SETUP" and servers[server_nb][2] > to_OFF[1]:
                                           to_OFF = [server_nb, servers[server_nb][2]]
                                    servers[to_OFF[0]] = ["OFF", None, float('Inf')]

                    # else if the server's countdown timer expires
                    elif servers[server_no][0] == "DELAYEDOFF":
                        # turn OFF the server
                        servers[server_no] = ["OFF", None, float('Inf')]

        if debug:
            print("{}\t{}\t{}".format(master_clock, dispatcher, servers[1:]))
        master_clock = min([arrival[i] for i in range(1) if len(arrival) > 0]
                           + [servers[server_no][2] for server_no in range(1, m + 1)]
                           + [float('inf')])

    return cumulative_response_time / nb_of_completed_jobs, departure_times
