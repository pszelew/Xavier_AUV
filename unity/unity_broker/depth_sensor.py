
class DepthSensor:
    """
    Depth Sensor
    """
    def __init__(self, unit_reference):
        self.unit_reference = unit_reference

    def get_depth(self):
        '''
        Get current depth
        :return: depth as single float in cm
        '''
        return self.unit_reference['depth']
