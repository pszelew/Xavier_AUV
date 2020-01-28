from tasks.task_executor_itf import ITaskExecutor
from neural_networks.DarknetClient import DarknetClient
from communication.rpi_broker.movements import Movements
from utils.stopwatch import Stopwatch
from structures.bounding_box import BoundingBox
from configs.config import get_config
from time import sleep
from definitions import IP_ADDRESS, DARKNET_PORT

class BucketTaskExecutor(ITaskExecutor):

    def __init__(self, control_dict: Movements,
                sensors_dict, camera_client,
                main_logger):
        self._control = control_dict
        self._bounding_box = BoundingBox(0, 0, 0, 0)
        self._hydrophones = sensors_dict['hydrophones']
        self._logger = main_logger
        self.config = get_config("tasks")['buckets_task']
        self.MAX_TIME_SEC = self.config['max_time_sec']
        self.PINGER_LOOP_COUNTER = self.config['pinger_loop_conunter']
        self.BLUE_LOOP_COUNTER = self.config['blue_loop_counter']
        self.ANY_BUCKET_COUNTER = self.config['any_bucket_counter']
        self._control.pid_turn_on()
        self._control.pid_hold_depth(get_config('depth'))

        self.darknet_client = DarknetClient(DARKNET_PORT, IP_ADDRESS)

        self._logger.log('Buckets: diving')

    def run(self):
        self._logger.log("Buckets task exector started")

        self.darknet_client.load_model("bucket")
        
        stopwatch = Stopwatch()
        stopwatch.start()

        ## THIS LOOP SHOULD FIND AT LEAST FIRST BBOX WITH BUCKET
        while not self.find_buckets():
            self._logger.log("Finding buckets in progress")
            if stopwatch >= self.MAX_TIME_SEC:
                self._logger.log("Finding buckets time expired")
                return -1

        i = 0
        # THIS LOOP SHOULD FIND BUCKET WITH PINGER
        while i < self.PINGER_LOOP_COUNTER:
            if self.find_pinger_bucket():
                self._logger.log("Found pinger bucket")
                i = self.PINGER_LOOP_COUNTER
                self.drop_marker()
                self._logger.log("Marker dropped")
                return 0
            i += 1
        
        k = 0
        while k < self.BLUE_LOOP_COUNTER:
            if self.find_blue_bucket():
                self._logger.log("Found blue bucket")
                k = self.BLUE_LOOP_COUNTER
                self.drop_marker()
                self._logger.log("Marker dropped")
                return 0

        l = 0
        while l < self.ANY_BUCKET_COUNTER:
            if self.find_random_bucket():
                self._logger.log("Found random bucket")
                l = self.ANY_BUCKET_COUNTER
                self.drop_marker()
                self._logger.log("Marker dropped")
                return 0
        
        self._logger.log("Finding buckets failed")
        return -1

    def find_buckets(self):
        '''
        Looking for buckets firstly based on pinger, altenatively by vision system
        '''

    def find_pinger_bucket(self):
        '''
        After localisation of carpet and buckets
        finding exact position of bucket with pinger
        '''
        if bucket:
            self.center_above_bucket(bucket)
            return 1
        else:
            return 0

    def find_blue_bucket(self):
        '''
        Finding exact position of blue color bucket
        '''
        if bucket:
            self.center_above_bucket(bucket)
            return 1
        else:
            return 0

    def find_random_bucket(self):
        '''
        Finding exact position of random bucket
        '''
        if bucket:
            self.center_above_bucket(bucket)
            return 1
        else:
            return 0

    def center_above_bucket(self, bucket_position):
        '''
        centering above bucket
        '''
    
    def drop_marker(self):
        '''
        Dropping marker at current position
        '''


            

