'''
Created on Mar 19, 2018

@author: adarsh
'''
from hyperopt import hp
from hyperopt import fmin, Trials
import numpy
import hyperopt
from random import seed
import matplotlib.pyplot as plt


sumOfCurrNext = 98.83744711093217
sumOfCurrPrev = 83.46098005076486
'''
Define the objective function to find the maximums
'''
def objective(space):
    a = space['a']
    b = space['b']
    return -(a * sumOfCurrNext + b * sumOfCurrPrev)
    
# Parameter search space

'''
Use random integer distribution for finding alpha(a) and beta(b)
a >> b and a+b nearly equal to 1
'''
space={
    'a': hp.uniform ('a',0.5,0.9),
    'b': hp.uniform ('b',0,0.1)
    }
    
'''
Run the hyperparameter optimization
'''

# The Trials object will store details of each iteration
seed = 1000
trials = Trials()

best = fmin(fn=objective,
            space=space,
            algo=hyperopt.rand.suggest,
            max_evals=1000,trials=trials,rstate= numpy.random.RandomState(seed))

print("Maximum: ", best)

# print('trials:')
# for trial in trials.trials[:2]:
#     print(trial)

'''
Plot of the function for a
'''
f, ax = plt.subplots(1)
xs = [t['misc']['vals']['a'] for t in trials.trials]
ys = [t['result']['loss'] for t in trials.trials]
ax.scatter(xs, ys, s=20, linewidth=0.01, alpha=0.75)
ax.set_title('$val$ $vs$ $a$ ', fontsize=18)
ax.set_xlabel('$a$', fontsize=16)
ax.set_ylabel('$val$', fontsize=16)
plt.show()

'''
Plot of the function for b
'''
f, ax = plt.subplots(1)
xs = [t['misc']['vals']['b'] for t in trials.trials]
ys = [t['result']['loss'] for t in trials.trials]
ax.scatter(xs, ys, s=20, linewidth=0.01, alpha=0.75)
ax.set_title('$val$ $vs$ $b$ ', fontsize=18)
ax.set_xlabel('$b$', fontsize=16)
ax.set_ylabel('$val$', fontsize=16)
plt.show()