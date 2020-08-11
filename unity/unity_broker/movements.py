import numpy as np
from pytransdec import Actions
"""
Module includes IMovements
"""

class Movements:
    # adjust these values for the simulation
    DEGREES_PER_STEP=20
    METERS_PER_STEP=1
    """
    Interfce for algorithm for accesing rpi Movement Class
    """
    def __init__(self, unity_reference, depth_sensor):
        self.unity_reference = unity_reference
        self.depth_sensor = depth_sensor

    def set_lin_velocity(self, front=0, right=0, up=0, num_of_steps: int=10):
        """
        Set linear velocity as 100% of engines power
        @param: front int in range [-100, 100], case negative value move back
        @param: right int in range [-100, 100], case negative value move down
        @param: up int in range [-100,100], case negative value move down
        """

        def to_range(value):
            return np.clip(value, -1, 1)

        self.unity_reference.set_vector_action(Actions.LONGITUDINAL, to_range(front/100))
        self.unity_reference.set_vector_action(Actions.LATERAL, -to_range(right/100))
        self.unity_reference.set_vector_action(Actions.VERTICAL, to_range(up/100))
        self.unity_reference.next_step(num_of_steps)

    def set_ang_velocity(self, roll=0, pitch=0, yaw=0, num_of_steps: int=10):
        """
        Set angular velocity as 100% of engines power
        @param: roll int in range [-100, 100], case negative - reverse direction
        @param: pitch int in range [-100, 100], case negative - reverse direction
        @param: yaw int in range [-100,100], case negative - reverse direction
        """
        self.unity_reference.set_vector_action(Actions.YAW, yaw/100)
        self.unity_reference.next_step(num_of_steps)

    def move_distance(self, front=0.0, right=0.0, up=0.0):
        """
        Make precise linear movement, valeues in meters
        @param: front float in range [-10, 10], case negative value move back
        @param: right float in range [-10, 10], case negative value move down
        @param: up float in range [-10,10], case negative value move down
        """
        # this implementation isn't precise because it uses rotation speed
        # but I don't know how much precision is available in a real environment
        # and if it makes sense to base the algorithms on it

        # move in each axis according to speed and then reset the linear velocity
        if front!=0: # settings step as zero causes one step to be performed anyways unfortunately
            self.set_lin_velocity(100*np.sign(front), 0, 0, int(front/self.METERS_PER_STEP))
        if right!=0:
            self.set_lin_velocity(0, 100*np.sign(right), 0, int(right/self.DEGREES_PER_STEP))
        if up!=0:
            self.set_lin_velocity(0, 0, 100*np.sign(up), int(up/self.DEGREES_PER_STEP))
        self.set_lin_velocity(0, 0, 0)

    def rotate_angle(self, roll=0.0, pitch=0.0, yaw=0.0):
        """
        Make precise angular movement
        @param: roll float in range [-360, 360], case negative - reverse direction
        @param: pitch float in range [-360, 360], case negative - reverse direction
        @param: yaw flaot in range [-360, 360], case negative - reverse direction
        """
        # this implementation isn't precise because it uses rotation speed
        # but I don't know how much precision is available in a real environment
        # and if it makes sense to base the algorithms on it

        # move in each axis according to speed and then reset the angular velocity
        if roll!=0:
            self.set_ang_velocity(100*np.sign(roll), 0, 0, int(roll/self.DEGREES_PER_STEP))
        if pitch!=0:  
            self.set_ang_velocity(0, 100*np.sign(pitch), 0, int(pitch/self.DEGREES_PER_STEP))
        if yaw!=0:
            self.set_ang_velocity(0, 0, 100*np.sign(yaw), int(yaw/self.DEGREES_PER_STEP))
        self.set_ang_velocity(0, 0, 0)
        
    def pid_turn_on(self):
        """
        Turn on PID
        """
        # same as with pid_hold_depth
        pass

    def pid_turn_off(self):
        """
        Turn off PID
        """
        # same as with pid_hold_depth
        pass

    def pid_hold_depth(self):
        """
        Set the current depth as the default depth
        Function DOESN'T activate pid, use pid_turn_on additionally
        """
        # in the current simulation depth is kept on the same level by default
        pass

    def pid_set_depth(self, depth):
        """
        Set depth, function DOESN'T activate pid, use pid_turn_on additionally
        :param: depth - float - target depth for PID
        """
        error=0.3
        current_depth=self.depth_sensor.get_depth()
        while np.abs(current_depth-depth)>error:
            if current_depth<depth:
                self.set_lin_velocity(0, 0, 100)
            else:
                self.set_lin_velocity(0, 0, -100)
            current_depth=self.depth_sensor.get_depth()
        self.set_lin_velocity(0, 0, 0)

    def pid_yaw_turn_on(self):
        raise NotImplementedError()

    def pid_yaw_turn_off(self):
        raise NotImplementedError()

    def pid_set_yaw(self, yaw):
        raise NotImplementedError()
