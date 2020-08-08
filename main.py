from logpy.LogPy import Logger
import threading

from startup.rov_startup import RovStartup
from startup.unity_startup import UnityStartup

#Task scheduler
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

        # startup
        if MAINDEF.MODE=='SIMULATION':
            self.startup=UnityStartup(self.logger)
        else:
            self.startup=RovStartup(self.logger)

        # task sheduler
        self.task_scheduler = TaskSchedululer(self.startup.control, self.startup.sensors, self.startup.vision, self.logger)
        self.logger.log("Task scheduler created")

    def run(self):
        self.logger.log("main thread is running")
        self.task_scheduler.run()


if __name__ == "__main__":
    main = Main()
    main.run()
