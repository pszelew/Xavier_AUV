import time

class Environment:
    '''
    time.sleep wrapper.
    See unity.environment for explanation on why it is needed.
    '''

    def sleep(self, seconds):
        time.sleep(seconds)