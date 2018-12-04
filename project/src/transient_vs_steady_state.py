from SetupDelayedoffSystem import simulate
import matplotlib.pyplot as plt

def get_running_mean(departure_times):
    response_times = []
    for departure_time in departure_times:
        response_times.append(departure_time[1] - departure_time[0])
    running_mean = [0]
    cumulative_mrt = 0
    for idx in range(len(response_times)):
        cumulative_mrt += response_times[idx]
        running_mean.append(cumulative_mrt / (idx + 1))
    return running_mean

mode = 'random'
el = 0.35   # lambda
mu = 1
m = 5
setup_time = 5
Tc = 0.1
time_end = 10000

mean_response_time, departure_times = simulate(mode, el, mu, m, setup_time, Tc, time_end, False, 0)
running_mean = get_running_mean(departure_times)

x = [i for i in range(len(running_mean))]
y = running_mean
z = [mean_response_time for _ in range(len(running_mean))]

plt.plot(x, y, label='Running Mean')
plt.plot(x, z, label='Theoretical Mean')
plt.xlabel('k-th job')
plt.ylabel('mean response time of first k jobs')
plt.legend()
plt.show()
