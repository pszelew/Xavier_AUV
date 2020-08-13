import numpy as np
from pytransdec import Actions
"""
Module includes IMovements
"""

class Movements:
    # adjust this values for the simulation
    # by setting the angular roll velocity for one step
    # and checking how much the ROV position changed 
    METERS_PER_STEP=0.1
    """
    Interface for controlling ROV movement in simulation
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
        self.unity_reference.set_vector_action(Actions.VERTICAL, -to_range(up/100))
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
        # this implementation isn't precise because it uses speed
        # but I don't know how much precision is available in a real environment
        # and if it makes sense to base the algorithms on it

        # move in each axis according to speed and then reset the linear velocity
        self.set_lin_velocity(100*np.sign(front), 0, 0, int(front/self.METERS_PER_STEP))
        self.set_lin_velocity(0, 100*np.sign(right), 0, int(right/self.METERS_PER_STEP))
        self.set_lin_velocity(0, 0, 100*np.sign(up), int(up/self.METERS_PER_STEP))
        self.set_lin_velocity(0, 0, 0)

    def __approach(self, observation_name, target, update_value_lambda, error=0.3, speed=10):
        """
        Repeatedly checks angle observation and updates the agent
        until it reaches the target angle.
        """
        # TODO: use PID
        while True:
            current=self.unity_reference.observation[observation_name]
            difference=target-current
            update_value_lambda(speed*np.sign(difference))
            if abs(difference)<=error:
                break

    def __approach_relative(self, observation_name, change, update_value_lambda):
        current=self.unity_reference.observation[observation_name]
        target=current+change
        self.__approach(observation_name, target, update_value_lambda)

    def rotate_angle(self, roll=0.0, pitch=0.0, yaw=0.0):
        """
        Make precise angular movement
        @param: roll float in range [-360, 360], case negative - reverse direction
        @param: pitch float in range [-360, 360], case negative - reverse direction
        @param: yaw float in range [-360, 360], case negative - reverse direction
        """
        # this implementation isn't precise because it uses rotation speed
        # but I don't know how much precision is available in a real environment
        # and if it makes sense to base the algorithms on it

        # move in each axis according to rotation observation and then reset the angular velocity
        # uncomment these when rotation around other axis becomes possible
        # rotate("rotation_z", roll, lambda value: self.set_ang_velocity(rollvalue, num_of_steps=1))
        # rotate("rotation_x", pitch, lambda value: self.set_ang_velocity(pitch=value, num_of_steps=1))
        self.__approach_relative("rotation_y", yaw, lambda value: self.set_ang_velocity(yaw=value, num_of_steps=1))
        self.set_ang_velocity(0, 0, 0)
        
    def pid_turn_on(self):
        """
        Turn on PID
        """
        # in the current simulation depth is kept on the same level by default
        pass

    def pid_turn_off(self):
        """
        Turn off PID
        """
        # same as with pid_turn_on
        pass

    def pid_hold_depth(self):
        """
        Set the current depth as the default depth
        Function DOESN'T activate pid, use pid_turn_on additionally
        """
        # same as with pid_turn_on
        pass

    def pid_set_depth(self, depth):
        """
        Set depth, function DOESN'T activate pid, use pid_turn_on additionally
        :param: depth - float - target depth for PID
        """
        self.__approach("depth", depth, lambda value: self.set_lin_velocity(up=-value, num_of_steps=1), speed=30)
        self.set_lin_velocity(0, 0, 0)

    def pid_yaw_turn_on(self):
        # same as with pid_turn_on
        pass

    def pid_yaw_turn_off(self):
        # same as with pid_turn_on
        pass

    def pid_set_yaw(self, yaw):
        current_yaw=self.unity_reference.observation['rotation_y']
        self.rotate_angle(0, 0, yaw-current_yaw)
