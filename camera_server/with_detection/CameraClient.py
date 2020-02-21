import socket
import struct
import pickle
import cv2

from logpy.LogPy import Logger


HOST = '192.168.1.5'
PORT = 8888

vidWIDTH = 640
vidHEIGHT = 480


class CameraClient:
    def __init__(self, host=HOST, port=PORT, retry_no=5):
        """
        Initialize Camera Client Class
        :param host: [String] Server host
        :param port: [Int] Server port
        :param retry_no: [Int] Number of retries
        """
        self.host = host
        self.port = port
        self.retryNo = retry_no
        # set logger file
        self.logger = Logger(filename='cameraClient', title="CameraClient")
        if not self.__auto_retry(self.__create_socket()):
            self.logger.log(f"ERROR: Create socket failure")
            return
        if not self.__auto_retry(self.__connect_to_server()):
            self.logger.log(f"ERROR: Connect to server failure")
            return

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

    def __connect_to_server(self):
        """
        Establish connection to server
        :return: True if successful
        """
        try:
            self.logger.log(f"Connecting the port {self.host}:{self.port}")

            self.socket.connect((self.host, self.port))
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

    @property
    #only function instead of class.function
    def frame(self):
        """
        Get frame from server
        :return: Frame of image
        """
        limit = struct.calcsize(">L")
        data = b""
        self.socket.send("get_frame".encode())

        while len(data) < limit:
            data += self.socket.recv(4096)
        packed_msg_size = data[:limit]
        msg_size = struct.unpack(">L", packed_msg_size)[0]
        data = data[limit:]

        while len(data) < msg_size:
            data += self.socket.recv(4096)
        frame_data = data[:msg_size]
        # data = data[msg_size:]
        frame = pickle.loads(frame_data, fix_imports=True, encoding="bytes")
        frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)

        self.socket.send("get_bbox_cord".encode())
        cord = self.socket.recv(4096).decode('utf-8')


        return frame, cord


def frame_preview(camera_client, exit_key='q'):
    """
    Get frame preview
    :param camera_client: [CameraClient] connected camera client to get frame
    :param exit_key: [Char] Key to exit preview
    :return:
    """
    while True:
        frame = camera_client.frame[0]
        cord = camera_client.frame[1]
        cords = []
        for val in cord.split():
            cords.append(float(val))

        x = int(cords[0] * vidWIDTH)
        y = int(cords[1] * vidHEIGHT)
        w = int(cords[2] * vidWIDTH)
        h = int(cords[3] * vidHEIGHT)

        x1 = int(x - (w / 2))
        y1 = int(y - (h / 2))
        x2 = int(x + (w / 2))
        y2 = int(y + (h / 2))

        cv2.rectangle(frame, (x1, y1), (x2, y2), color=(0, 255, 0), thickness=2)
        cv2.imshow(f'Press {exit_key} to exit', frame)
        if cv2.waitKey(1) & 0xFF == ord(exit_key):
            break


if __name__ == "__main__":
    camCl = CameraClient()
    frame_preview(camCl)

