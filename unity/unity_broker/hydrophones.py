from pytransdec import Actions

class Hydrophones:
    """
    Depth Sensor
    """
    def __init__(self, unity_reference):
        self.unity_reference = unity_reference

    def get_angle(self,frequency):
        '''
        @param frequency is a listening frequency for demanded pinger
        '''
        self.unity_reference.set_vector_action(Actions.HYDROPHONE_FREQUENCY, frequency)
        self.unity_reference.next_step()
        return  self.unity_reference.observation['hydrophone_angle']
