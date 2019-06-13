
import itertools 



gen = itertools.combinations(range(0,52),5)
chunk_size = 250000

this_count = 0
last_count = -1 
didIncrease = this_count > last_count

"""
Generators accessed via itertools.islice do not return a 
StopIteration exception, they simply throw a "pass" in 
their internal loop.  By checking to see if this_count 
is greater than last_count and hiding the this_count 
incrementation inside the "for item in chunk", it will 
not be executed once the generator runs out of slices. 
Then last_count will catch up and kill the loop it's 
wrapped in. Does throw chunk_size - (N % chunk_size)
passes in the loop, but this is the top scope. 
"""

while this_count > last_count:
	chunk = itertools.islice(gen,chunk_size)
	for item in chunk: 
		#print( item )
		this_count += 1 
	last_count += chunk_size
	
print( this_count )