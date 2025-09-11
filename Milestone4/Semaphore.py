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
        self.OS.write("accountName",n) #assigned with value of 1 as init val         
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
        self.lock.acquire(caller)
        self.OS.write("accountName",self.n-1)
         #feedback from the 1400 on 11 SEP collab - decrement nd check the value before going into the logic, then write to it

        counter_state = self.OS.read("accountName") #read from shared memory
        #change to follow the algo from the proof
        if (counter_state > 0):
            #lock is open
            new_val = counter_state - 1
            self.OS.write("accountName",new_val)
            self.lock.release(caller)
        else:
            #place waiting process in queue bc resource is locked, go to sleep
            self.queue.put(caller.getName())
            self.lock.release(caller)
            caller.sleep()
            
    def signal(self, caller):
        ''' semaphore signal functionality.
            - caller is the process providing the "signal"
              (you will need caller because this is a simulated system,
               a production OS has this info available as part of the PCB)
        '''
        #release lock from current process
        self.lock.acquire(caller)
        if not self.queue.empty():
            #get next man up
            nextMan = self.queue.get()
            self.OS.wake(nextMan)
            caller.slp_yield() #prevents race condition of two processes in the deadlock
        else: #queue empty
            counter_state = self.OS.read("accountName") #read from shared memory
            new_val = counter_state + 1
            self.OS.write("accountName",new_val) 
        self.lock.release(caller)
            #resource is free to be grabbed by an incoming process since nothing is in the queue waiting

#EOF