



class DispatchThreadManager {

public:
	DispatchThreadManager();

	~DispatchThreadManager();

private:

	void dispatchWorkerThreads();

	void calculateStuff(Hand*, int threadId);


	const int NUM_OF_THREADS = 20;

	std::thread thread_pool[NUM_OF_THREADS];
	std::atomic(bool) future_pool[NUM_OF_THREADS];

	
}

DispatchThreadManager::DispatchThreadManager() {
	//TODO: init future_pool to true
}

DispatchThreadManager::~DispatchThreadManager() {

}

void DispatchThreadManager::dispatchWorkerThreads() {

	while (there are jobs left) {
		// logic here to break up the big set
		Hand* tempHand = stuff;

		for (int i = 0; i < NUM_OF_THREADS; i++) {
			if (thread != null && future_pool[i].get()) {

				thread_pool[i] = new std::thread(calculateStuff, tempHand, i, this);

			}
		}
	}
}

void DispatchThreadManager::calculateStuff(Hand* hand. int threadId) {
	future_pool[threadId].set(false);

	// do your math

	// store in another thread-safe class

	future_pool[threadId].set(true);
}



///////////////////////////////////////////////////////////////////////////////////////////////////////////

//NEW PROGRAM

int main() {

	DispatchThreadManager* dtm = new DispatchThreadManager();

	//TODO: create storage singleton or whatever

	std::thread dispathThread = new std::thread(dispatchWorkerThreads, dtm);


	return 1;
}