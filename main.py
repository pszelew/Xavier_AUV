from logpy.LogPy import Logger
import threading

# Cameras
from camera_server.cameraClient import CameraClient
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

from definitions import MAINDEF, CAMERAS,IP_ADDRESS, LOG_DIRECOTRY


class Main():
    '''
    Creates object of all sensor types, packs their references into
    a list. Creates Communication thread.
    '''
    def __init__(self):
        '''
        Creates and stores references of all slave objects.
        '''

        self.logger = Logger(filename='main_xavier', title="Main Xavier", directory=LOG_DIRECOTRY, console=True)
        self.logger.start()

        # cameras 
        self.camera_client = CameraClient(IP_ADDRESS,name_modifer="_main")        
        self.logger.log("Cameras created")

        #communication
        self.communication = Communication()
        self.rpi_reference = self.communication.rpi_reference
        self.logger.log("communication was established")

        # sensors
        self.ahrs = AHRS(self.rpi_reference)
        self.depth_sensor = DepthSensor(self.rpi_reference)
        self.distance_sensor = DistanceSensor(self.rpi_reference)
        self.hydrophones = Hydrophones(self.rpi_reference)
        self.logger.log("sensors created")

        self.sensors = {'ahrs': self.ahrs,
                        'depth': self.depth_sensor,
                        'distance': self.distance_sensor,
                        'hydrophones': self.hydrophones}
        #control
        self.movements = Movements(self.rpi_reference, self.logger)
        #self.torpedoes = Torpedoes(self.rpi_reference)
        #self.manipulator = Manipulator(self.rpi_reference)
        self.dropper = Dropper(self.rpi_reference)
        self.logger.log("control objects created")

        self.control = {'movements': self.movements,
                        #torpedoes': self.torpedoes,
                        #'manipulator': self.manipulator,
                        'dropper': self.dropper}

        # task sheduler
        self.task_scheduler = TaskSchedululer(self.control, self.sensors, self.logger)
        self.logger.log("Task scheduler created")

    def run(self):
        self.logger.log("main thread is running")
        self.task_scheduler.run()


if __name__ == "__main__":
    main = Main()
    main.run()
