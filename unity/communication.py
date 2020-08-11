from pytransdec import TransdecCommunication, Actions, CAMERAS
import cv2

# actions that are switched on only for one step
SWITCH_ACTIONS = [Actions.TORPEDO, Actions.MARKER_DROPPER]

class Communication:
    def __init__(self):
        self.transdec = TransdecCommunication()
        self.transdec.reset()
        self.vector_action = [0] * Actions.COUNT
        self.text_action=None

    @property
    def observation(self):
        return self.transdec.vector

    @property
    def frame(self):
        """
        Get frame from the simulation.
        :return: Frame from the simulation as BGR array
        """
        # transcode image from unity's RGB to cv2's BGR format 
        # to match interface's expectations
        return cv2.cvtColor(self.transdec.visual[0], cv2.COLOR_RGB2BGR)

    def reset(self):
        self.transdec.reset()

    def next_step(self, number_of_step = 1):
        for _ in range(number_of_step):
            self.transdec.step(self.vector_action)
        for i in SWITCH_ACTIONS:
            self.vector_action[i] = 0
        self.text_action=None

    def set_vector_action(self, action:Actions, value):
        self.vector_action[action]=value

    # this function is shared by CameraClient and UnityVision
    # so it makes sense to locate it here
    def change_camera(self, id):
        """
        Change active camera
        :param id: [Int] key in CAMERAS dict representing the camera
        """
        if id in CAMERAS:
            self.vector_action[Actions.CAMERA]=CAMERAS[id]
            return True
        else:
            return False
        self.next_step()

    def close_simulation(self):
        del self.transdec

    def choose_target(self, target_name):
        self.text_action=target_name

if __name__ == "__main__":
    unity = Communication()

