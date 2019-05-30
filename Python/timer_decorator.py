import time 
from functools import wraps 
import numpy as np

def timer_this_func(a_func):
	@wraps(a_func)
	def wrapped_func():
		start = time.time()
		a_func()
		stop = time.time()
		print "Execution took: ", stop-start, ' seconds'
		
	return wrapped_func 
	
	
	
	
def timer_this_func_stats(a_func):
	@wraps(a_func)
	def wrapped_func():
		times_arr = []
		N = 10
		for i in range(0,N):
			start = time.time()
			a_func()
			stop = time.time()
			times_arr.append(stop-start)
		
		print ("Execution took: ", np.mean(times_arr), '+/-', 
				np.std(times_arr), ' seconds')
		
	return wrapped_func 