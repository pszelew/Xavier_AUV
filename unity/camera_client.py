import socket
import struct
import pickle
import cv2
from logpy.LogPy import Logger
from definitions import LOG_DIRECOTRY
from definitions import IP_ADDRESS, CAMERA_SERVER_PORT
from utils.testing import frame_preview

class CameraClient:
    def __init__(self, unity_reference, name_modifer = ""):
        """
        Initialize Camera Client Class
        :param host: [String] Server host
        :param unity_reference: reference to unity communication class
        :param retry_no: [Int] Number of retries
        """
        # set logger file
        self.logger = Logger(filename='camera_client'+name_modifer, title="CameraClient", directory=LOG_DIRECOTRY, logexists='append', console=True)
        self.logger.start()
        self.unity_reference = unity_reference

    @property
    def frame(self):
        """
        Get frame from server
        :return: Frame of image
        """
        frame = self.unity_reference.frame
        # data = data[msg_size:]
        return frame

    def change_camera(self,camera):
        self.unity_reference.change_camera(camera)
        return True

if __name__ == "__main__":
    # shows one frame from the simulation
    from unity.communication import Communication
    communication=Communication()
    camCl = CameraClient(communication)
    frame_preview(camCl)
    communication.close_simulation()