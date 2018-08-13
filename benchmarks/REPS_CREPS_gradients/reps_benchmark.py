"""
REPS benchmark

Validates the implementation of the analytical computation of the gradient by
comparing it to the previous implementation using numerical approximation.

Compares the runtime performance of both implementations.
"""

import numpy as np
from reps import REPSOptimizer
from bolero.environment.objective_functions import Rosenbrock
import matplotlib.pyplot as plt
import time

def eval_loop(Opt, opt, n_dims, n_iter):
    x = np.empty(n_dims)
    opt.init(n_dims)
    objective = Opt(0, n_dims)
    results = np.empty(n_iter)
    for i in xrange(n_iter):
        opt.get_next_parameters(x)
        results[i] = objective.feedback(x)
        opt.set_evaluation_feedback(results[i])
    return results - objective.f_opt

n_dims = 10
n_iter = 1000
n_trials = 5

x = np.zeros(n_dims)

optimizers = {
    "Numerical gradient": REPSOptimizer(x, random_state=0, approx_grad = True),
    "Analytical gradient": REPSOptimizer(x, random_state=0),
    }

plt.figure(figsize=(12, 8))
for name, opt in optimizers.items():
	start_time = time.time()
	for i in range(n_trials):
		r = eval_loop(Rosenbrock, opt, n_dims, n_iter)
	total_time = time.time() - start_time
	print name, 'completed in average time of', round(total_time / n_trials, 2), 'seconds'
	plt.plot(-np.maximum.accumulate(r), label = name)
plt.xlabel("Function evaluations")
plt.ylabel("$f(x)$")
plt.title("Rosenbrock function")
plt.yscale("log")
plt.legend(loc='best')
plt.show()