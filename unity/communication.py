from pytransdec import TransdecCommunication
import cv2

class Communication:
    def __init__(self):
        self.transdec = TransdecCommunication()
        self.transdec.reset()
        self.vector_action = [0] * 7
        self.text_action=None

    @property
    def observation(self):
        return self.transdec.vector

    @property
    def frame(self):
        # transcode image from unity's RGB to cv2's BGR format 
        # to match interface's expectations
        return cv2.cvtColor(self.transdec.visual[0], cv2.COLOR_RGB2BGR)

    def reset(self):
        self.transdec.reset()

    def next_step(self, number_of_step = 1):
        for _ in range(number_of_step):
            self.transdec.step(self.vector_action)
        self.vector_action[6] = 0
        self.text_action=None

    def set_longitudal_movement(self, front_speed):
        self.vector_action[0] = front_speed

    def set_lateral_movement(self, right_speed):
        self.vector_action[1] = right_speed

    def set_vertical_movement(self, upward_speed):
        self.vector_action[2] = upward_speed
        
    def set_yaw_movement(self, right_turn_speed):
        self.vector_action[3] = right_turn_speed

    def change_camera(self, camera:int):
        self.vector_action[4]=camera

    def close_gripper(self):
        self.vector_action[5] = 1

    def open_gripper(self):
        self.vector_action[5] = 0

    def fire_torpedo(self, command):
        self.vector_action[6] = 1

    def get_observations(self):
        return self.transdec.vector

    def close_simulation(self):
        del self.transdec

    def choose_target(self, target_name):
        self.text_action=target_name

if __name__ == "__main__":
    unity = Communication()

