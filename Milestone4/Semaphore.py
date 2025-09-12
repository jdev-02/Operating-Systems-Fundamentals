'''
Semaphore.py
CS3070: Gohlwar, Goohs, Norman 

Created: Spring '16
Updated: 13 Jan 2022
'''

'''This is the Semaphore implementation class.'''

class Semaphore(object):
##########################################
#Constructor

    def __init__(self, n, simKernel):
        ''' use as provided.
            - n is the number to set the Semaphore counter to initially
            - simKernel provides the access to the simulated kernel a real OS
                 would have when constructing a Semaphore
            This constructor will run once when the OS invokes it.
        '''

        self.OS = simKernel
        self.n = n
        self.OS.write("accountName", n) #assigned with value of 1 as init val         
        self.queue = self.OS.getQueue() #create abstract queue
        self.lock = self.OS.getAtomicLock() #create lock
        
##########################################
#Instance Methods

    def wait(self, caller):
        ''' semaphore wait functionality.
            - caller is the process asking "wait?"
              (you will need caller because this is a simulated system,
               a production OS has this info available as part of the PCB)                 
               
        '''
        # Acquire lock
        self.lock.acquire(caller)

        # Decrement counter
        self.OS.write("accountName",self.n - 1)

        # Assign current counter value to local copy
        counter_state = self.OS.read("accountName") #read from shared memory
        #print(counter_state)
        
        if (counter_state < 0):
            self.queue.put(caller.getName())
            self.lock.release(caller)
            caller.sleep()
        else:
            self.lock.release(caller)

        # Raaj Version
        #if (counter_state == 1):
            # Lock is open (counter_state == 1) -> Decrement counter, write to shared memory location and release lock
        #    counter_state -= 1
        #    self.OS.write("accountName", counter_state)
        #    self.lock.release(caller)
        #elif (counter_state == 0):
            # Critical section occupied -> Place in queue, release lock and sleep
            #print("I am entering the queue")
        #    self.queue.put(caller.getName())
        #    self.lock.release(caller)
        #    caller.sleep()
            
    def signal(self, caller):
        ''' semaphore signal functionality.
            - caller is the process providing the "signal"
              (you will need caller because this is a simulated system,
               a production OS has this info available as part of the PCB)
        '''
        # Raaj: We need to mirror wait() ->
            # 1. Acquire lock
            # 2. Assign value of our shared memory counter to local variable
            # 3. Enter if/else section

        # Acquire lock
        self.lock.acquire(caller)

        # Increment counter
        self.OS.write("accountName",self.n+1)

        # Assign current counter value to local copy, different scope than wait() so we can re-use
        counter_state = self.OS.read("accountName") #read from shared memory

        if counter_state <= 0:
            # Get next man from queue, do not modify counter variable since it remains 0
            nextMan = self.queue.get()
            #print("I am exiting the queue")
            self.OS.wake(nextMan)

            # Prevent race condition of two processes in deadlock
            caller.slp_yield() 

        self.lock.release(caller)

        # Raaj Version
        #else: # Queue empty
        #    counter_state = self.OS.read("accountName") #read from shared memory
            # I am not sure we need this new variable new_val since counter_state scope is only in signal
            #new_val = counter_state + 1
        #    counter_state += 1
        #    self.OS.write("accountName", counter_state) 
        #self.lock.release(caller)
            #resource is free to be grabbed by an incoming process since nothing is in the queue waiting
#EOF