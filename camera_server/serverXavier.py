import socket
import cv2
import struct
import pickle
import threading 
from logpy.LogPy import Logger
import os
from definitions import LOG_DIRECOTRY
from definitions import CAMERA_SERVER_PORT
from definitions import CAMERAS
# from definitions.CAMERAS import FRONT_CAMERA_DEVNAME
# from definitions.CAMERAS import BOTTOM_CAMERA_DEVNAME


class ServerXavier:
    def __init__(self, host=str(os.system('hostname -I')), port=CAMERA_SERVER_PORT, black_and_white=False, retry_no=5):
        """
        Initialize server
        :param host: [String] host address
        :param port: [Int] port
        :param black_and_white: [Bool] Is white and white camera image?
        :param retry_no: [Int] Number of retries
        """
        self.host = host
        self.port = port
        self.bw = black_and_white
        self.retryNo = retry_no
        # set logger file
        self.logger = Logger(filename='server_xavier', title="ServerXavier", directory=LOG_DIRECOTRY, logexists='append')
        self.logger.start()
        
        # start up camera
        front_camera_connected = False
        bottom_camera_connected = False
        try:
            front_camera = cv2.VideoCapture(CAMERAS.FRONT_CAMERA_DEVNAME)
            front_camera_connected = True
        except:
            self.logger.log("Front camera not connected")
        try:
            bottom_camera = cv2.VideoCapture(CAMERAS.BOTTOM_CAMERA_DEVNAME)
            bottom_camera_connected = True
        except:
            self.logger.log("Bottom camera not connected")
        if front_camera_connected and bottom_camera_connected:
            self.camerasDict = {"front": front_camera,"bottom": bottom_camera}    
            self.cameraCapture = self.camerasDict["front"]
        elif front_cammera_connected:
            self.camerasDict = {"front": front_camera}    
            self.cameraCapture = self.camerasDict["front"]
        elif bottom_camera_connected:
            self.camerasDict = {"bottom": bottom_camera}    
            self.cameraCapture = self.camerasDict["front"]
        else:
            self.print("No camera connected")
            self.logger.log("No camera connected")
            
        if not self.__auto_retry(self.__create_socket()):
            self.logger.log(f"ERROR: Create socket failure")
            return
        if not self.__auto_retry(self.__bind_socket()):
            self.logger.log(f"ERROR: Bind socket failure")
            return
        self.logger.log(f"Init complete")

        # variables for videoClient use
        self.VIDEO_PATH = ''
        self.VIDEO = None
        self.VIDEO_FRAME_COUNT = 0

    def __create_socket(self):
        """
        Create socket for making connection possible
        :return: [Bool] True if successful
        """
        try:
            self.socket = socket.socket()
            return True
        except socket.error as msg:
            self.logger.log(f'WARNING: Socket creation error: {msg}.')
            return False

    def __bind_socket(self):
        """
        Bind selected socket and listen for connections
        :return: [Bool] True if successful
        """
        try:
            self.logger.log(f"Binding the Port {self.port}")

            self.socket.bind((self.host, self.port))
            self.socket.listen(5)
            return True

        except socket.error as msg:
            self.logger.log(f"WARNING: Socket binding error: {msg}.")
            return False

    def __auto_retry(self, function):
        """
        Auto-retry function
        :param function: [Function] Function to try. Require False/0 if unsuccessful
        :return: True if finished with retry number of tries
        """
        for i in range(self.retryNo):
            if function:
                return True
            elif i == self.retryNo:
                self.logger.log("ERROR: Initialize error. Check logs for more info.")
                return False
            self.logger.log(f"Retrying. Try: {i} of {self.retryNo}.")

    def socket_accept(self):
        """
        Accept connection from client
        :return: None
        """
        conn, address = self.socket.accept()
        self.logger.log(f"Connection has been established! | {address[0]}:{address[1]}")
        threading.Thread(target=self.__handle_client, args=(conn,)).start()
    
    def change_camera(self, id):
        if id in self.camerasDict.keys():
            self.cameraCapture = self.camerasDict[id]
            return True
        else:
            return False

    def __handle_client(self, conn):
        """
        Handle client in separate function
        :param conn: Client connection data
        :return: None
        """
        counter = 1
        while True:
            data = conn.recv(1024).decode()
            if not data:
                break
            elif "change" in data:
                if self.change_camera(data.split(':')[1]):
                    conn.send('true'.encode())
                else:
                    conn.send('false'.decode())
            elif "get_frame" in data:
                conn.send(self.__frame(source=self.cameraCapture, h_flip=True))
            elif "get_video" in data:
                # set video variables
                if counter == 1:
                    self.VIDEO_PATH = data.split()[1]
                    self.VIDEO = cv2.VideoCapture(self.VIDEO_PATH)
                    self.VIDEO_FRAME_COUNT = self.VIDEO.get(7)

                if counter < self.VIDEO_FRAME_COUNT:
                    conn.send(self.__frame(source=self.VIDEO))
                    counter += 1
                else:
                    self.VIDEO.release()
                    self.VIDEO = cv2.VideoCapture(self.VIDEO_PATH)
                    conn.send(self.__frame(source=self.VIDEO))
                    counter = 2
        conn.close()

    def __frame(self, source, v_flip=False, h_flip=False):
        """
        Get picture frame
        :param v_flip: [Bool] Is image flipped vertical
        :param h_flip: [Bool] Is image flipped horizontal
        :return: frame
        """
        # Capture frame
        ret, frame = source.read()

        # Handles the mirroring of the current frame
        frame = cv2.flip(frame, self.__flip(v_flip, h_flip))

        if self.bw:
            # Change color to black and white if decided
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Code image
        result, frame = cv2.imencode('.jpg', frame)

        data = pickle.dumps(frame, 0)
        size = len(data)
        return struct.pack(">L", size) + data

    def __flip(self, v_flip, h_flip):
        """
        Get flip parameter
        :param v_flip: [Bool] Is image flipped vertical
        :param h_flip: [Bool] Is image flipped horizontal
        :return: [Int] value for cv2 flip method
        """
        if h_flip and v_flip:
            return -1
        elif v_flip:
            return 0
        else:
            return 1


if __name__ == "__main__":
    #print(socket.gethostbyname(socket.gethostname()))
    serverXavier = ServerXavier()
    while True:
        serverXavier.socket_accept()


