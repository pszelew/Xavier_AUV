from logpy.LogPy import Logger
from utils.project_managment import PROJECT_ROOT
from definitions import IP_ADDRESS, LOG_DIRECOTRY
from neural_networks.utils.DarknetYoloModel import DarknetYoloModel
import time

class DarknetNoServer():
    """
    Class for interacting with darknet without running server.
    """
    def __init__(self, camera_client, threshold=0.5):
        """
        :param port: Port of running darknet server
        :param camera_client: Instance of camera client which feeds model with images
        """
        self.logger = Logger(filename='darknet_no_server', title="Darknet_No_Server", directory=LOG_DIRECOTRY, logexists='append', console=True)
        self.model = DarknetYoloModel(model_path=f"{PROJECT_ROOT}/neural_networks/models",
                             threshold=threshold)
        self.camera_client=camera_client
        self.model.load(model_name='gate')
    
    def load_model(self, model_name, retries=3) -> bool:
        """
        Loads new model from memory
        :param model_name: string with dir name that contains trained model
        :param retries: max retries before giving up
        :return: Response from darknet server. True if operation succeeded
        """
        self.logger.log(f"INFO: loading new model: {model_name}")
        self.model.load(model_name)
        return True

    def change_camera(self,camera,retries = 3) -> bool:
        self.camera_client.change_camera(camera)
        return True

    def predict(self):
        img = self.camera_client.frame
        start = time.time()
        self.logger.log("Starting prediction")
        result = self.model.predict(img)
        predict_time = time.time()-start
        self.logger.log(f"INFO: prediction time: " + str(predict_time))
        return result