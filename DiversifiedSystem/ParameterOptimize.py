'''
Created on Mar 19, 2018

@author: adarsh
'''
from hyperopt import hp
from hyperopt import fmin, Trials
import hyperopt



'''
Define the objective function to find the maximums
'''
def objective(space):
    a = space['a']
    b = space['b']
    return -(a**2 + b**2)
    
# Parameter search space

'''
Use random integer distribution for finding alpha(a) and beta(b)
'''
space={
    'a': hp.uniform ('a',0.5,1),
    'b': hp.uniform ('b',0,0.5)   
    }
    
'''
Run the hyperparameter optimization
'''

# The Trials object will store details of each iteration


best = fmin(fn=objective,
            space=space,
            algo=hyperopt.rand.suggest,
            max_evals=10)

print("Maximum: ", best)