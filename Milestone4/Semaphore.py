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

    def __init__(self, counter, simKernel):
        ''' use as provided.
            - n is the number to set the Semaphore counter to initially
            - simKernel provides the access to the simulated kernel a real OS
                 would have when constructing a Semaphore
            This constructor will run once when the OS invokes it.
        '''
        
        self.OS = simKernel
        self.counter = 1 # Assign counter initial value of 1 (lock is open)
        self.userQueue = self.OS.getQueue() # Create queue
        self.lock = self.OS.getAtomicLock() # Create lock
        
##########################################
#Instance Methods

    def wait(self, caller):
        ''' semaphore wait functionality.
            - caller is the process asking "wait?"
              (you will need caller because this is a simulated system,
               a production OS has this info available as part of the PCB)
        
        1. While semaphore != 1: loop/continue -> enter queue
            2. Enter critical section/gain access to shared resource
            3. Assign value of 0 to semaphore counter variable
         
        '''
        while (self.counter == 1):
                # Decrement counter
            self.lock.acquire(caller)
            self.counter -= 1
             # Execute critical section
        # Place waiting process in queue, go to sleep
        self.userQueue.put(caller)
        caller.sleep()
        

    def signal(self, caller):
        ''' semaphore signal functionality.
            - caller is the process providing the "signal"
              (you will need caller because this is a simulated system,
               a production OS has this info available as part of the PCB)
        
        1. Assign value of 1 to semaphore counter variable
        with lock
            dequeue waiting user
            increment counter back to 1
        '''
        # Get next man up
        nextman = self.OS.wake(self.OS.queue.get())
        if (self.counter != 1 and self.userQueue.get() != ""):
            self.lock.release(caller)
            self.counter += 1
            if (self.userQueue.get() != ""):
                self.wait(nextman)
            #now next man can enter since the counter is 1
        
        if (self.userQueue.get() == ""):
            #theres no processes in the queue
            self.lock.release(caller)
            self.counter += 1
        
'''
1. User: construct GET_BALANCE msg -> msg(dollar_amount)
2. GOTO: WAIT(semaphore) -> decrement
    3. Send GET_BALANCE msg
    4. Receive msg
    5. Extract balance from msg
    6. Construct new balance
    7. Construct PUT_BALANCE msg
    8. Send PUT_BALANCE msg
    9. SIGNAL(semaphore) -> increment
10. Loop
'''