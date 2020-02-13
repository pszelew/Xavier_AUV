from pytransdec import TransdecCommunication

class Communication:
    def __init__(self):
        self.transdec = TransdecCommunication()
        self.transdec.reset()
        self.command = [0] * 7

    @property
    def observation(self):
        return self.transdec.vector

    @property
    def frame(self):
        return self.transdec.visual

    def reset(self):
        self.transdec.reset()

    def next_step(self, number_of_step = 1):
        for _ in range(number_of_step):
            self.transdec.step(self.command)
        self.command[6] = 0

    def set_longitudal_movement(self, front_speed):
        self.command[0] = front_speed

    def set_lateral_movement(self, right_speed):
        self.command[1] = right_speed

    def set_vertical_movement(self, upward_speed):
        self.command[2] = upward_speed
        
    def set_yaw_movement(self, rigt_turn_speed):
        self.command[3] = rigt_turn_speed
        
    def set_front_camera(self):
        self.command[4] = 0

    def set_bottom_camera(self):
        self.command[4] = 1

    def close_gripper(self):
        self.command[5] = 1

    def open_gripper(self):
        self.command[5] = 0

    def fire_torpedo(self, command):
        self.command[6] = 1

    def close_simulation(self):
        del self.transdec


if __name__ == "__main__":
    unity = Communication()

