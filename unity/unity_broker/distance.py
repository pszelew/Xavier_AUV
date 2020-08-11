class DistanceSensor:
    """
    Distance Sensor
    """
    def __init__(self, observations):
        self.observations = observations

    def get_front_distance(self):
        '''
        Get distance from obstacle in front of ROV

        :return: distance in cm as single float
        '''
        return  self.observations['front_distance']
