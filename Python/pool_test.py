import random, time, multiprocessing
 
def func(arg):
	#print '%s says %s'%(multiprocessing.current_process(), arg)
	return arg

def generate_jobs():
	n = 100
	while n > 0:
		yield n
		n -= 1
		
	
	
if __name__ == '__main__':
	multiprocessing.freeze_support()
	p     = multiprocessing.Pool(4)
	count = 0
	start = time.time()
	for i in range(10):
		print "chunk %d"%i
		for res in p.imap_unordered(func, generate_jobs()):
			print count, res
			count += 1
	p.close()
	p.join()