from tasks.task_executor_itf import ITaskExecutor
#from unity.unity_broker.movements import Movements
from communication.rpi_broker.movements import Movements
from utils.stopwatch import Stopwatch
from utils.centering import center_rov
from configs.config import get_config
from time import sleep

class UnityTest(ITaskExecutor):
    def __init__(self, control_dict, sensors_dict, cameras_dict, main_logger):
        """
        @param: movement_object is object of Movements Class
            (repository RPi_ROV4: RPi_ROV4/blob/master/control/movements/movements_itf.py)
        @param: camras_dict is dictionary of references to camera objects
            keywords: arm_camera; bottom_camera; front_cam1;
            for cameras objects look at /vision/front_cam_1.py
        """
        self.control_dict = control_dict
        self.sensors_dict = sensors_dict
        self.cameras_dict = cameras_dict
        self.logger = main_logger
        self.logger.log("Configure Unity Test")
        self.movements = control_dict['movements']
        self.ahrs = sensors_dict['ahrs']

    def run(self):
        self.logger.log("Running Unity Test")

        #print(self.cameras_dict.frame)
        self.movements.set_lin_velocity(front=30)
        self.movements.set_lin_velocity(right=30)
        self.movements.set_lin_velocity(up=30)
        self.movements.set_ang_velocity(yaw=30)
        self.movements.set_ang_velocity(roll=0)
        self.movements.set_ang_velocity(pitch=0)