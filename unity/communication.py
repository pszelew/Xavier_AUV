from pytransdec import TransdecCommunication, Actions, CAMERAS
import cv2

# actions that are reset to zero after one step
SWITCH_ACTIONS = [Actions.TORPEDO, Actions.MARKER_DROPPER, Actions.HYDROPHONE_FREQUENCY]

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
            self.transdec.step(self.vector_action, self.text_action)
        for i in SWITCH_ACTIONS:
            self.vector_action[i] = 0
        self.text_action=None

    def set_vector_action(self, action:Actions, value):
        self.vector_action[action]=value

    # this function is shared by CameraClient and UnityVision
    # so it makes sense to locate it here
    def change_camera(self, camera):
        """
        Change active camera
        :param camera: [Int] key in CAMERAS dict representing the camera
        """
        if camera in CAMERAS:
            self.vector_action[Actions.CAMERA]=CAMERAS[camera]
            self.next_step()
            return True
        else:
            return False

    def close_simulation(self):
        del self.transdec

    def choose_target(self, target_name):
        self.text_action=target_name
        self.next_step()

if __name__ == "__main__":
    unity = Communication()

