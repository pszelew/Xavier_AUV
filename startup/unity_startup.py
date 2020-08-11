from logpy.LogPy import Logger
import threading

# Cameras
from unity.camera_client import CameraClient
# Task running

# Sensors
from unity.communication import Communication

from unity.unity_broker.ahrs import AHRS
from unity.unity_broker.depth_sensor import DepthSensor
from unity.unity_broker.hydrophones import Hydrophones
from unity.unity_broker.distance import DistanceSensor

# Control
from unity.unity_broker.movements import Movements
from unity.unity_broker.torpedoes import Torpedoes
from unity.unity_broker.manipulator import Manipulator
from unity.unity_broker.dropper import Dropper

#Task sceduller
from tasks.tasks_scheduler import TaskSchedululer

from definitions import MAINDEF, CAMERAS,IP_ADDRESS, CAMERA_SERVER_PORT, LOG_DIRECOTRY


class UnityStartup():
    '''
    Creates object of all sensor types, packs their references into
    a list. Creates Communication thread.
    '''
    def __init__(self, logger, use_nn):
        '''
        Creates and stores references of all slave objects.
        '''        
        #unity
        self.unity = Communication()
        self.unity_observation = self.unity.observation
        logger.log("unity was established")
        
        self._camera_client = CameraClient(self.unity) 
        if use_nn:
            from neural_networks.DarknetNoServer import DarknetNoServer 
            self.vision=DarknetNoServer(self._camera_client)
            logger.log("darknet vision created")
        else:
            from unity.unity_vision import UnityVision
            self.vision=UnityVision(self.unity)
            logger.log("vision is being faked by calculations inside of Unity")

        # sensors
        self.ahrs = AHRS(self.unity_observation)
        self.depth_sensor = DepthSensor(self.unity_observation)
        self.distance_sensor = DistanceSensor(self.unity_observation)
        self.hydrophones = Hydrophones(self.unity)
        logger.log("sensors created")

        self._sensors = {'ahrs': self.ahrs,
                        'depth': self.depth_sensor,
                        'distance': self.distance_sensor,
                        'hydrophones': self.hydrophones}
        #control
        self.movements = Movements(self.unity, self.depth_sensor)
        self.torpedoes = Torpedoes(self.unity)
        self.manipulator = Manipulator(self.unity)
        self.dropper = Dropper(self.unity)
        logger.log("control objects created")

        self._control = {'movements': self.movements,
                        'torpedoes': self.torpedoes,
                        'manipulator': self.manipulator,
                        'dropper': self.dropper}

    @property
    def sensors(self):
        return self._sensors
    
    @property
    def control(self):
        return self._control
        
    @property
    def camera_client(self):
        return self._camera_client
