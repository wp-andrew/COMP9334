from SetupDelayedoffSystem import simulate
import matplotlib.pyplot as plt
import numpy as np

def transient_removal(m, w, mt):
    mt_smooth = []
    for i in range(2, m-w+1):
        if i <= w:
            mt_smooth.append(np.mean(np.array(mt[1:(2*i-1)])))
        else:
            mt_smooth.append(np.mean(np.array(mt[(i-w):(i+w)])))
    return mt_smooth

mode = 'random'
el = 0.35   # lambda
mu = 1
m = 5
setup_time = 5
Tc = 0.1
time_end = 10000

nb_of_replications = 30
min_len = float('inf')  # min number of data points in a single replication

list_of_response_times = []
for random_seed in range(nb_of_replications):
    _, departure_times = simulate(mode, el, mu, m, setup_time, Tc, time_end, False, random_seed)
    response_times = []
    for departure_time in departure_times:
        response_times.append(departure_time[1] - departure_time[0])
    list_of_response_times.append(response_times)
    min_len = min(min_len, len(response_times))

mt = [0 for _ in range(min_len)]
for i in range(min_len):
    for j in range(nb_of_replications):
        mt[i] += list_of_response_times[j][i]
    mt[i] /= nb_of_replications

w = 1000
mt_smooth = transient_removal(min_len, w, mt)

plt.plot(mt_smooth)
plt.title('w = {}'.format(w))
plt.show()
