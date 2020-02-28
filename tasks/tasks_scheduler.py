from tasks.task_executor_itf import ITaskExecutor

#from tasks.SAUVC.gate.task_executor.gate_task_executor import GateTaskExecutor as GateExecutor
from tasks.SAUVC.buckets.task_executor.buckets_task_executor import BucketTaskExecutor
from tasks.tests.coke_centering import CokeCenteringTest
from tasks.SAUVC.qualification.task_executor.qualification_task_executor import GateTaskExecutor as GateExecutor

class TaskSchedululer(ITaskExecutor):

    def __init__(self, control_dict, sensors_dict, main_logger):
        """
        @param: movement_object is an object of Movements Class
            keywords: movements; torpedoes; manipulator;
        @param: sensors_dict is a dictionary of references to sensors objects
            keywords: ahrs; depth; hydrophones; distance;
        @param: camera_client 
        @param: main_logger is a reference to logger of main thread
        """
        self.control_dict = control_dict
        self.sensors_dict = sensors_dict
        self.logger = main_logger

    def run(self):
        """
        This method is started by main object.
        """
        self.logger.log("Task scheduler is running")

               
        coke_centering_test = CokeCenteringTest(self.control_dict,self.sensors_dict,
                                               self.logger)
        coke_centering_test.run()

        '''
        gate_executor = GateExecutor(self.control_dict, self.sensors_dict,
                                     self.logger)
        gate_executor.run()
        '''
        #self.logger.log("Gate finshed")

        #bucket_executor = BucketTaskExecutor(self.control_dict['movements'], self.sensors_dict,
        #                             self.logger)
        #bucket_executor.run()
        
        self.logger.log("Scheduler finished")
