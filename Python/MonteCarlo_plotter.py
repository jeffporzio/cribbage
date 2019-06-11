import matplotlib.pyplot as plt
import numpy as np
import scipy.stats


def getDictFromFile(file):
	dict = {}
	with open(file, 'r') as f: 
		for line in f:
			key, val = line.split(',')
			if val=='0\n':
				val = 1 
			dict[int(key)] = int(val)
			
	return dict
	
def doAverage(keys, vals,n_iter):
	
	avg = 0.
	for i in range(0,len(vals)):
		avg += keys[i] * vals[i]
	avg /= n_iter
	
	
	std = 0
	for key,val in zip(keys,vals):
		std += 1.0 * (key - avg)**2 * val
	std /= (n_iter-1)
	std **= 0.5
	
	
	return avg, std
			
n_iter = int(1e6)
			
# Save them all when done.
best_file = "..\Data\MonteCarlo_out"+str(n_iter)+"_best.txt"
worst_file = "..\Data\MonteCarlo_out"+str(n_iter)+"_worst.txt"
random_file = "..\Data\MonteCarlo_out"+str(n_iter)+"_random.txt"

best_dict = getDictFromFile(best_file)
worst_dict = getDictFromFile(worst_file)
random_dict = getDictFromFile(random_file)
	
	
best_keys = [key for key in best_dict.keys()]
best_vals = [val for val in best_dict.values()]
random_keys = [key for key in random_dict.keys()]
random_vals = [val for val in random_dict.values()]
worst_keys = [key for key in worst_dict.keys()]
worst_vals = [val for val in worst_dict.values()]

best_avg, best_std = doAverage(best_keys, best_vals, n_iter)
random_avg, random_std = doAverage(random_keys, random_vals, n_iter)
worst_avg, worst_std = doAverage(worst_keys, worst_vals, n_iter)

best_vals = np.array(best_vals)
random_vals = np.array(random_vals)
worst_vals = np.array(worst_vals)


best_odd_vals = best_vals[1::2]
best_even_vals = best_vals[0::2]
random_odd_vals = random_vals[1::2]
random_even_vals = random_vals[0::2]
worst_odd_vals = worst_vals[1::2]
worst_even_vals = worst_vals[0::2]

"""
print best_odd_vals
print best_even_vals
print random_odd_vals
print random_even_vals
print worst_odd_vals
print worst_even_vals
"""

best_vals = best_odd_vals + best_even_vals
random_vals = random_odd_vals + random_even_vals
worst_vals = worst_odd_vals + worst_even_vals

best_keys = best_keys[::2]
random_keys = random_keys[::2]
worst_keys = worst_keys[::2]


# plots 
fs = 24
wd = 2
# Creates two subplots and unpacks the output array immediately
f, (ax1, ax2, ax3) = plt.subplots(3, 1, sharey=True, sharex=True)
ax1.bar(best_keys, best_vals, align='center',width=wd)
ax2.bar(random_keys, random_vals, align='center',width=wd)
ax3.bar(worst_keys, worst_vals, align='center',width=wd)

ax1.set_title('Best: %1.2f pm %1.2f' % (best_avg, best_std)      , fontsize=fs    )
ax2.set_title('Random: %1.2f pm %1.2f' % (random_avg, random_std), fontsize=fs    )
ax3.set_title('Worst: %1.2f pm %1.2f' % (worst_avg, worst_std)   , fontsize=fs    )

print "Best vs. Worst"
chiSq, p = scipy.stats.chisquare(best_vals, worst_vals, ddof=2)
print "chiSq: ", chiSq
print "p: %f" % (p)
print
	
print "Best vs. Random"
chiSq, p = scipy.stats.chisquare(best_vals, random_vals, ddof=2)
print "chiSq: ", chiSq
print "p: %f" % (p)
print

print "Random vs. Worst"
chiSq, p = scipy.stats.chisquare(random_vals, worst_vals, ddof=2)
print "chiSq: ", chiSq
print "p: %f" % (p)
print

plt.show()


