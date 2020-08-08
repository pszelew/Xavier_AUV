import numpy as np
"""
Module includes IMovements
"""

class Movements:
    """
    Interfce for algorithm for accesing rpi Movement Class
    """
    def __init__(self, unity_reference):
        self.unity_reference = unity_reference

    def set_lin_velocity(self, front=0, right=0, up=0, num_of_steps: int=10):
        """
        Set linear velocity as 100% of engines power
        @param: front int in range [-100, 100], case negative value move back
        @param: right int in range [-100, 100], case negative value move down
        @param: up int in range [-100,100], case negative value move down
        """

        def to_range(value):
            return np.clip(value, -1, 1)

        self.unity_reference.set_longitudal_movement(to_range(front/100))
        self.unity_reference.set_lateral_movement(-to_range(right/100))
        self.unity_reference.set_vertical_movement(to_range(up/100))
        self.unity_reference.next_step(num_of_steps)

    def set_ang_velocity(self, roll=0, pitch=0, yaw=0, num_of_steps: int=10):
        """
        Set angular velocity as 100% of engines power
        @param: roll int in range [-100, 100], case negative - reverse direction
        @param: pitch int in range [-100, 100], case negative - reverse direction
        @param: yaw int in range [-100,100], case negative - reverse direction
        """
        self.unity_reference.set_yaw_movement(yaw/100)
        self.unity_reference.next_step(num_of_steps)

    def move_distance(self, front=0.0, right=0.0, up=0.0):
        """
        Make precise linear movement, valeues in meters
        @param: front float in range [-10, 10], case negative value move back
        @param: right float in range [-10, 10], case negative value move down
        @param: up float in range [-10,10], case negative value move down

        Not shure if it is going to work correctly
        """
        self.set_lin_velocity(front, right, up)


    def rotate_angle(self, roll=0.0, pitch=0.0, yaw=0.0):
        """
        Make precise angular movement
        @param: roll float in range [-360, 360], case negative - reverse direction
        @param: pitch float in range [-360, 360], case negative - reverse direction
        @param: yaw flaot in range [-360, 360], case negative - reverse direction
        """
        self.set_ang_velocity(roll, pitch, yaw)
        
    def pid_turn_on(self):
        """
        Turn on PID
        """
        pass

    def pid_turn_off(self):
        """
        Turn off PID
        """
        pass

    def pid_hold_depth(self):
        """
        Set the current depth as the default depth
        Function DOESN'T activate pid, use pid_turn_on additionally
        """
        pass

    def pid_set_depth(self, depth):
        """
        Set depth, function DOESN'T activate pid, use pid_turn_on additionally
        :param: depth - float - target depth for PID
        """
        pass

    def pid_yaw_turn_on(self):
        pass

    def pid_yaw_turn_off(self):
        pass

    def pid_set_yaw(self, yaw):
        pass
