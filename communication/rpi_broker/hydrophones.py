
class Hydrophones:
    """
    Depth Sensor
    """
    def __init__(self, rpi_reference):
        self.rpi_reference = rpi_reference

    def get_angle(self,frequency):
        '''
        @param frequency is a listening frequency for demanded pinger
        '''
        return self.rpi_reference.get_angle(frequency)
