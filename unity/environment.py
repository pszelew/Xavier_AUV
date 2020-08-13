class Environment:
    '''
    Replacement for time.sleep function that updates the unity environment.
    '''
    # If I wanted to use time.sleep with Unity I would have to create a separate thread,
    # that waits for some action and if it doesn't receive anything for some time 
    # it performs a step. Implementing all of that, synchronizing it correctly 
    # and fixing all of the bugs is just not worth it.
    # I didn't make this into function-like object because calls like self.sleep(seconds)
    # inside of tasks would look really confusing.

    # Remember to check if the calculation below works correctly for you.
    # But also code that heavily depends on time measurement
    # instead of constant corrections is bound to fail anyways.
    REFERENCE_FPS=60
    FRAMES_PER_STEP=10 # this is decision interval in robot agent
    SECONDS_PER_STEP=1/(REFERENCE_FPS/FRAMES_PER_STEP)

    def __init__(self, unity_reference):
        """
        :param unity_reference: reference to unity communication class
        """
        self.unity_reference = unity_reference

    def sleep(self, seconds):
        steps=int(seconds/self.SECONDS_PER_STEP)
        # This makes sure that the simulation will
        # update at least once and the program won't just freeze.
        if steps==0:
            steps=1
        self.unity_reference.next_step()