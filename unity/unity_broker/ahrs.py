
class AHRS:
    """
    Depth Sensor
    """
    def __init__(self, unity_reference):
        self.unity_reference = unity_reference

    def get_rotation(self):
        '''
        :return: dict with keys: 'yaw', 'pitch', 'roll'
        '''
        rotation = {
            'roll': self.unity_reference['rotation_x'],
            'pitch': self.unity_reference['rotation_y'],
            'yaw': self.unity_reference['rotation_z']
        }

        return rotation

    #@Base.multithread_method
    def get_linear_accelerations(self):
        '''
        :return: dictionary with keys "lineA_x"
        "lineA_y", lineA_z"
        '''
        linear_acceleration = {
            'lineA_x': self.unity_reference['acceleration_x'],
            'lineA_y': self.unity_reference['acceleration_y'],
            'lineA_z': self.unity_reference['acceleration_z']
        }

        return linear_acceleration

    #@Base.multithread_method
    def get_angular_accelerations(self):
        '''
        :return: dictionary with keys "angularA_x"
        "angularA_y", angularA_z"
        '''        
        angular_acceleration = {
            'angularA_x': self.unity_reference['angular_acceleration_x'],
            'angularA_y': self.unity_reference['angular_acceleration_y'],
            'angularA_z': self.unity_reference['angular_acceleration_z']
        }

        return angular_acceleration

    #@Base.multithread_method
    def get_all_data(self):
        '''
        :return: dictionary with rotation, linear and angular
        accelerations, keys: "yaw", "pitch", "roll",
        "lineA_x","lineA_y","lineA_z","angularA_x",
        "angularA_y","angularA_z"
        '''
        rotation = self.get_rotation()
        linear = self.get_linear_accelerations()
        angular = self.get_angular_accelerations()

        all_data = rotation + linear + angular 

        return all_data

    def get_yaw(self):
        return self.unity_reference['rotation_z']


    