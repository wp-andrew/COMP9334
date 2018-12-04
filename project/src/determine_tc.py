from math import sqrt
from SetupDelayedoffSystem import simulate
import numpy as np

mode = 'random'
el = 0.35   # lambda
mu = 1
m = 5
setup_time = 5
Tc = 0.1
time_end = 10000

nb_of_replications = 30
t = 2.0452  # for 30 independent experiments and 95% confidence interval

# Baseline system
list_of_emrt_base = []
for random_seed in range(nb_of_replications):
    _, departure_times = simulate(mode, el, mu, m, setup_time, Tc, time_end, False, random_seed)
    response_times = []
    for i in range(1000, len(departure_times)):
        response_times.append(departure_times[i][1] - departure_times[i][0])
    emrt = np.mean(np.array(response_times))
    list_of_emrt_base.append(emrt)

# Compare systems of different Tc with the baseline, until we
# found one with a response time of at least 2 units less.
Tc = 1
lower_limit, upper_limit = 0, 0
while lower_limit < 2:
    list_of_emrt = []
    for random_seed in range(nb_of_replications):
        _, departure_times = simulate(mode, el, mu, m, setup_time, Tc, time_end, False, random_seed)
        response_times = []
        for i in range(1000, len(departure_times)):
            response_times.append(departure_times[i][1] - departure_times[i][0])
        emrt = np.mean(np.array(response_times))
        list_of_emrt.append(emrt)

    list_of_emrt_differences = [list_of_emrt_base[i] - list_of_emrt[i] for i in range(nb_of_replications)]
    sample_emrt = sum(list_of_emrt_differences) / nb_of_replications
    sample_std  = sqrt(sum([(sample_emrt - emrt)**2 for emrt in list_of_emrt_differences]) / (nb_of_replications - 1))

    lower_limit = sample_emrt - (t * sample_std / sqrt(nb_of_replications))
    upper_limit = sample_emrt + (t * sample_std / sqrt(nb_of_replications))
    print('Tc = {}\tC.I. = {}'.format(Tc, [lower_limit, upper_limit]))

    Tc += 1
