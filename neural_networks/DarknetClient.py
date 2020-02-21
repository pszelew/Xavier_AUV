import pickle
import requests
import time
import argparse as ap
import cv2
from logpy.LogPy import Logger
from utils.project_managment import PROJECT_ROOT
from definitions import LOG_DIRECOTRY, DARKNET_PORT
import os


class DarknetClient():
    """
    Class for interacting witch python darknet server.
    """
    def __init__(self, port=DARKNET_PORT, url= 'http://192.168.0.103'):#url=f"http://localhost"):
        """
        :param port: Port of running darknet server
        :param url: Url of running darknet server external eg: "http://192.168.0.104"
        """
        self.port = str(port)
        self.url = url
        self.logger = Logger(filename='darknet_client', title="Darknet_Client", directory=LOG_DIRECOTRY, logexists='append')
        self.logger.log(url)

    def load_model(self, model_name, retries=3) -> bool:
        """
        Sends a post request to darknet server, and load new model from memory
        :param model_name: string with dir name that contains trained model
        :param retries: max retries before giving up
        :return: Response from darknet server. True if operation succeeded
        """
        data = {'model_name': str(model_name)}
        for i in range(retries):
            try:
                server_url = self.url + ":" + self.port + "/load_model"
                req = requests.post(url=server_url,data = data)
                result = req.content
                self.logger.log("Model loaded correctly")
                break
            except Exception as e:
                time.sleep(0.1)
                result = False
                self.logger.log(str(e))
        
        return result

    def change_camera(self,camera,retries = 3) -> bool:
        """
        Sends a post requests to darknet server, and change source camera
        from with server takes frames.
        :param camera: name of camera in string that specifies source eg: "bottom"
        :param retries: max retries before giving up
        :return: Response from darknet server. True if operation succeeded
        """
        data = {'cam_name': str(camera)}
        for i in range(retries):
            try:
                server_url = self.url + ":" + self.port + "/change_camera"
                req = requests.post(url=server_url,data = data)
                result = req.content
                break
            except Exception:
                time.sleep(0.1)
                result = False
        return result

    def predict(self):
        """
        Request prediction from darknet server, and get BoudingBox
        :return: Response from darknet server contains bbox structure
        """
        server_url = self.url + ":" + self.port + "/predict"
        req = requests.get(url=server_url)
        result = req.content
        result = pickle.loads(result)

        self.logger.log("Img predict")
        if result:
            self.logger.log(str(result[0].normalize(480,480)))

        return result

    def predict_with_image(self):
        """
        Request prediction from darknet server. When server get BoudingBox with image
        :return: Response from darknet server contains bbox structure and image
        """
        server_url = self.url + ":" + self.port + "/predict_with_image"
        req = requests.get(url=server_url)
        result = req.content
        result = pickle.loads(result)
        return result 

    def prediction_time(self):
        """
        Request prediction time from darknet server
        :return: Response from darknet server time of prediction 
        """
        server_url = self.url + ":" + self.port + "/prediction_time"
        req = requests.get(url=server_url)
        result = req.content
        return float(result)

    def change_threshold(self, threshold = 0.5, retries = 3) -> bool:
        """
        Change detection threshold from 0 to 1.
        :return: Response from darknet server. True if operation succeeded
        """
        data = {'threshold': str(threshold)}
        for i in range(retries):
            try:
                server_url = self.url + ":" + self.port + "/change_threshold"
                req = requests.post(url=server_url,params = data)
                result = req.content
                break
            except Exception:
                time.sleep(0.1)
                result = False
        return result


if __name__ == "__main__":
    parser = ap.ArgumentParser(description="Darknet client")

    parser.add_argument("-u", '--url', default=f"http://localhost", type=str, help="Url of running darknet server")
    parser.add_argument("-p", '--port', default=5000, type=int, help="Port on which darknet server is runing")

    args = parser.parse_args()

    client = DarknetClient()
    start_time = time.time()
    x = 5 # displays the frame rate every 5 second
    counter = 0
    while True:
        response_time = time.time()
        #result = client.predict_with_image()
        result = client.predict()
        response_time = time.time()-response_time
        print(result)
        '''
        if result is not []:
            frame = result[-1]
            bbox = result[0]
        
            if(len(result) > 1):
                frame = cv2.rectangle(frame, bbox.p1, bbox.p2, (255, 0, 255))
        
        cv2.imshow('image', frame)
        key = cv2.waitKey(10)  # pauses for 100 mili sec before fetching next image
        if key == 'q':  # if q is pressed, exit loop
            cv2.destroyAllWindows()
            break
        
        '''

        counter+=1
        if (time.time() - start_time) > x :
            print("\n____________________________\nFPS: ", counter / (time.time() - start_time),
                  "\naverage prediction_time: ", client.prediction_time(),
                  "\ntime for getting response with prediction: ", response_time)
            counter = 0
            start_time = time.time()
            print(result)
