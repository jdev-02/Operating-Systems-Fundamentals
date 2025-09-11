'''
Semaphore.py
CS3070: Gohlwar, Goohs, Norman 

Created: Spring '16
Updated: 13 Jan 2022
'''

'''This is the Semaphore implementation class.'''
import multiprocessing as mp

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
        self.counter = mp.Value('i',n).value
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
        if (self.counter > 0):
            #lock is open
            self.counter -= 1
            self.lock.release(caller)
        elif (self.counter == 0):
            #place waiting process in queue bc resource is locked, go to sleep
            self.queue.put(caller)
            self.lock.release(caller)
            caller.sleep()
        else:
            self.lock.release(caller)

            
    def signal(self, caller):
        ''' semaphore signal functionality.
            - caller is the process providing the "signal"
              (you will need caller because this is a simulated system,
               a production OS has this info available as part of the PCB)
        '''
        #release lock from current process
        self.lock.acquire(caller)
        if self.queue.empty() != True:
            #get next man up
            nextMan = self.queue.get()
            self.OS.wake(nextMan)
            self.counter += 1
            self.lock.release(caller)
        else: #queue empty
            self.counter += 1 
            self.lock.release(caller)
            #resource is free to be grabbed by an incoming process since nothing is in the queue waiting

#EOF