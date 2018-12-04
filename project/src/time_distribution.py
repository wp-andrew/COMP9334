from math import log
from random import random, seed
import matplotlib.pyplot as plt

sample_size = 1000
seed(1)
el, mu = 0.35, 1

# INTER ARRIVAL TIME DISTRIBUTION
arrival_time_distribution = [-log(1 - random()) / el for _ in range(sample_size)]
actual_mean      = sum(arrival_time_distribution) / len(arrival_time_distribution)
theoritical_mean = 1 / el

x = [i for i in range(sample_size)]
y = arrival_time_distribution
actual_average_line      = [actual_mean for _ in range(sample_size)]
theoritical_average_line = [theoritical_mean for _ in range(sample_size)]

plt.figure(1)
plt.subplot(211)
plt.bar(x, y)
plt.plot(actual_average_line, label='actual mean = %0.3f'%actual_mean)
plt.plot(theoritical_average_line, label='theoritical mean = %0.3f'%theoritical_mean)
plt.xlabel('k-th job')
plt.ylabel('inter arrival time')
plt.legend()

# SERVICE TIME DISTRIBUTION
service_time_distribution = [(-log(1 - random()) / mu) + (-log(1 - random()) / mu) + (-log(1 - random()) / mu) for _ in range(sample_size)]
actual_mean      = sum(service_time_distribution) / len(service_time_distribution)
theoritical_mean = 3 * (1 / mu)

x = [i for i in range(sample_size)]
y = service_time_distribution
actual_average_line      = [actual_mean for _ in range(sample_size)]
theoritical_average_line = [theoritical_mean for _ in range(sample_size)]

plt.subplot(212)
plt.bar(x, y)
plt.plot(actual_average_line, label='actual mean = %0.3f'%actual_mean)
plt.plot(theoritical_average_line, label='theoritical mean = %0.3f'%theoritical_mean)
plt.xlabel('k-th job')
plt.ylabel('service time')
plt.legend()
plt.show()
