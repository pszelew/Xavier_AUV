import socket
import struct
import pickle
import cv2
from logpy.LogPy import Logger
from definitions import LOG_DIRECOTRY
from definitions import IP_ADDRESS, CAMERA_SERVER_PORT

class CameraClient:
    def __init__(self, unity_reference, name_modifer = ""):
        """
        Initialize Camera Client Class
        :param host: [String] Server host
        :param port: [Int] Server port
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
