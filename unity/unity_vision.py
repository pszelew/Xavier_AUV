from logpy.LogPy import Logger
from utils.project_managment import PROJECT_ROOT
from definitions import IP_ADDRESS, LOG_DIRECOTRY
from unity.communication import Communication
from structures.bounding_box import BoundingBox
import time

def observation_to_bounding_box(observation):
    return BoundingBox(
        observation['bounding_box_x']*480,
        observation['bounding_box_y']*480,
        observation['bounding_box_w']*480,
        observation['bounding_box_h']*480,
        observation['bounding_box_p'])

class UnityVision():
    """
    Class using Unity bounding box calculation for vision directly.
    It allows running the tasks without trained YOLO models.
    """
    def __init__(self, unity_reference:Communication, threshold=0.5):
        """
        :param unity_reference: reference to unity communication class
        """
        self.logger = Logger(filename='unity_vision', title="Unity_Vision", directory=LOG_DIRECOTRY, logexists='append', console=True)
        self.unity_reference=unity_reference
    
    def load_model(self, model_name, retries=3) -> bool:
        """
        Loads new model from memory
        :param model_name: string with dir name that contains trained model
        :param retries: max retries before giving up
        :return: Response from darknet server. True if operation succeeded
        """
        
        self.unity_reference.choose_target(model_name)

        return True

    def change_camera(self,camera,retries = 3) -> bool:
        self.unity_reference.change_camera(camera)
        return True

    def predict(self):
        return [observation_to_bounding_box(self.unity_reference.get_observations())]

    def change_threshold(self, threshold = 0.5, retries = 3) -> bool:
        return True