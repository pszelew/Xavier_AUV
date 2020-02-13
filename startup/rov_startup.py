from logpy.LogPy import Logger
import threading

# Cameras
from camera_server.CameraClient import CameraClient
# Task running

# Sensors
from communication.communication import Communication

from communication.rpi_broker.ahrs import AHRS
from communication.rpi_broker.depth_sensor import DepthSensor
from communication.rpi_broker.hydrophones import Hydrophones
from communication.rpi_broker.distance import DistanceSensor

# Control
from communication.rpi_broker.movements import Movements
#from communication.rpi_broker.torpedoes import Torpedoes
#rom communication.rpi_broker.manipulator import Manipulator
from communication.rpi_broker.dropper import Dropper

#Task sceduller
from tasks.tasks_scheduler import TaskSchedululer

from definitions import MAINDEF, CAMERAS,IP_ADDRESS, CAMERA_SERVER_PORT, LOG_DIRECOTRY


class RovStartup():
    '''
    Creates object of all sensor types, packs their references into
    a list. Creates Communication thread.
    '''
    def __init__(self, logger):
        '''
        Creates and stores references of all slave objects.
        '''

        logger = Logger(filename='main_xavier', title="Main Xavier", directory=LOG_DIRECOTRY)
        logger.start()
        
        # cameras 
        self.camera_client = CameraClient(IP_ADDRESS, CAMERA_SERVER_PORT,name_modifer="_main")        
        logger.log("Cameras created")

        #communication
        self.communication = Communication()
        self.rpi_reference = self.communication.rpi_reference
        logger.log("communication was established")

        # sensors
        self.ahrs = AHRS(self.rpi_reference)
        self.depth_sensor = DepthSensor(self.rpi_reference)
        self.distance_sensor = DistanceSensor(self.rpi_reference)
        self.hydrophones = Hydrophones(self.rpi_reference)
        logger.log("sensors created")

        self.sensors = {'ahrs': self.ahrs,
                        'depth': self.depth_sensor,
                        'distance': self.distance_sensor,
                        'hydrophones': self.hydrophones}
        #control
        self.movements = Movements(self.rpi_reference)
        #self.torpedoes = Torpedoes(self.rpi_reference)
        #self.manipulator = Manipulator(self.rpi_reference)
        self.dropper = Dropper(self.rpi_reference)
        logger.log("control objects created")

        self.control = {'movements': self.movements,
                        #torpedoes': self.torpedoes,
                        #'manipulator': self.manipulator,
                        'dropper': self.dropper}
        
    @property
    def sensors(self):
        return self.sensors
    
    @property
    def control(self):
        return self.control

    @property
    def camera_client(self):
        return self.camera_client

