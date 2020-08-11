
class DepthSensor:
    """
    Depth Sensor
    """
    def __init__(self, observations):
        self.observations = observations

    def get_depth(self):
        '''
        Get current depth
        :return: depth as single float in cm
        '''
        return self.observations['depth']
