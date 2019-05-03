import time 
from functools import wraps 

def timer_this_func(a_func):
	@wraps(a_func)
	def wrapped_func():
		start = time.time()
		a_func()
		stop = time.time()
		print "Execution took: ", stop-start, ' seconds'
		
	return wrapped_func 