from pytransdec import Actions
import math

class Hydrophones:
    """
    Depth Sensor
    """
    def __init__(self, unity_reference):
        self.unity_reference = unity_reference

    def get_angle(self,frequency):
        '''
        @param frequency is a listening frequency for demanded pinger
               zero frequency is reserved as a null value
        :return: angle to pinger on frequency or None
                if there is no pinger on the frequency
        '''
        self.unity_reference.set_vector_action(Actions.HYDROPHONE_FREQUENCY, frequency)
        self.unity_reference.next_step()
        angle=self.unity_reference.observation['hydrophone_angle']
        # The simulation sends infinity when there is no correct pinger
        # Looking at the tasks I couldn't guess what the returned value should be
        # because they only checked if the result is falsy 
        # and zero (completely valid angle value) is falsy too.
        # I decided to return None because it is falsy unlike infinity 
        # and doesn't collide with 0 angle.
        if math.isinf(angle):
            return None
        else:
            return angle