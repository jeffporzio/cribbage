
import itertools 



gen = itertools.combinations(range(0,52),5)
chunk_size = 250000

this_count = 0
last_count = -1 
didIncrease = this_count > last_count

while this_count > last_count:
	chunk = itertools.islice(gen,chunk_size)
	for item in chunk: 
		#print( item )
		this_count += 1 
	last_count += chunk_size
	
print( this_count )