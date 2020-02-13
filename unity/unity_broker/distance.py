
class DistanceSensor:
    """
    Distance Sensor
    """
    def __init__(self, unity_reference):
        self.unity_reference = unity_reference

    def get_front_distance(self):
        '''
        Get distance from obstacle in front of ROV

        :return: distance in cm as single float
        '''
        return 300#return float(self.unity_reference.get_front_distance())
