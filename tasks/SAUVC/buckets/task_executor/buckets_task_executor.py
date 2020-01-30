from tasks.task_executor_itf import ITaskExecutor
from neural_networks.DarknetClient import DarknetClient
from communication.rpi_broker.movements import Movements
from utils.stopwatch import Stopwatch
from utils.centering import center_rov
from configs.config import get_config
from time import sleep
from definitions import IP_ADDRESS, DARKNET_PORT

class BucketTaskExecutor(ITaskExecutor):

    def __init__(self, control_dict: Movements,
                sensors_dict, camera_client,
                main_logger):
        self._control = control_dict['movements']
        self._dropper = control_dict['dropper']
        self._hydrophones = sensors_dict['hydrophones']
        self._logger = main_logger
        self.config = get_config("tasks")['buckets_task']
        self.MAX_TIME_SEC = self.config['search']['max_time_sec']
        self.PINGER_LOOP_COUNTER = self.config['search']['pinger_loop_counter']
        self.BLUE_LOOP_COUNTER = self.config['search']['blue_loop_counter']
        self.ANY_BUCKET_COUNTER = self.config['search']['any_bucket_counter']
        self.SEARCHING_BUCKETS_FORWARD_TIME = self.config['search']['SEARCHING_BUCKETS_FORWARD_TIME']
        self.PINGER_FREQ = self.config['search']['PINGER_FREQ']
        self.POSITION_THRESHOLD = self.config['search']['POSITION_THRESHOLD']
        self._control.pid_turn_on()
        self._control.pid_set_depth(self.config['search']['max_depth'])

        self.darknet_client = DarknetClient(DARKNET_PORT, IP_ADDRESS)

        self._logger.log('Buckets: diving')

    def run(self):
        self._logger.log("Buckets task exector started")

        self.darknet_client.load_model("bucket")
        '''
        TO DO: uncomment loading model when its done
        '''
        #self.darknet_client.load_model('buckets_task')
        stopwatch = Stopwatch()
        stopwatch.start()

        ## THIS LOOP SHOULD FIND AT LEAST FIRST BBOX WITH BUCKET
        while not self.find_buckets():
            self._logger.log("Finding buckets in progress")
            if stopwatch.time() >= self.MAX_TIME_SEC:
                self._logger.log("Finding buckets time expired")
                return 0

        #self.darknet_client.load_model("bucket")
        i = 0
        # THIS LOOP SHOULD FIND BUCKET WITH PINGER
        while i < self.PINGER_LOOP_COUNTER:
            if self.find_pinger_bucket():
                self._logger.log("Found pinger bucket")
                i = self.PINGER_LOOP_COUNTER
                self.drop_marker()
                self._logger.log("Marker dropped")
                return 1
            i += 1
        
        k = 0
        while k < self.BLUE_LOOP_COUNTER:
            if self.find_blue_bucket():
                self._logger.log("Found blue bucket")
                k = self.BLUE_LOOP_COUNTER
                self.drop_marker()
                self._logger.log("Marker dropped")
                return 1

        l = 0
        while l < self.ANY_BUCKET_COUNTER:
            if self.find_random_bucket():
                self._logger.log("Found random bucket")
                l = self.ANY_BUCKET_COUNTER
                self.drop_marker()
                self._logger.log("Marker dropped")
                return 1
        
        self._logger.log("Finding buckets failed")
        return 0

    def find_buckets(self):
        '''
        Looking for buckets firstly based on pinger, altenatively by vision system
        '''
        
        self._logger.log("Starting searching buckets task")
        angle_to_pinger = self._hydrophones.get_angle(self.PINGER_FREQ) 
        if angle_to_pinger:
            bbox = False
            i = 0
            while bbox is not True and i < 5:
                self._control.rotate_angle(yaw = angle_to_pinger)
                self._control.set_lin_velocity(front = 50)
                sleep(self.SEARCHING_BUCKETS_FORWARD_TIME)
                self._control.set_lin_velocity(front = 0)
                bbox = self.darknet_client.predict()
                angle_to_pinger = self._hydrophones._hydrophones.get_angle(freq)
                i += 1
        if bbox:
            center_rov(self._control, Bbox = bbox)
            self._logger.log("Buckets task found")
            return 1
        else:
            self._logger.log("Starting desparate algorythm")
            for i in range(18):
                self._control.rotate_angle(yaw = 20)
                bbox = self.darknet_client.predict()
                if bbox:
                    center_rov(self._control, Bbox = bbox)
                    self._logger.log("Buckets task found")
                    return 1
            self._logger.log("Searching buckets task failed")
            return 0


            

    def find_pinger_bucket(self):
        '''
        After localisation of carpet and buckets
        finding exact position of bucket with pinger
        '''
        self._logger.log("Locating exact position of pinger bucket")
        angle_to_pinger = self._hydrophones.get_angle(self.PINGER_FREQ)
        bbox = None
        if angle_to_pinger:
            i = 0
            while bbox is None and i < 5:
                self._control.rotate_angle(angle_to_pinger)
                sleep(2)
                bbox = self.darknet_client.predict()
                angle_to_pinger = self._hydrophones.get_angle(self.PINGER_FREQ)
                i += 1
            if bbox is None:
                self._logger.log("Finding pinger bucke failed")
                return 0

            else:
                control = self._control
                center_rov(control, Bbox = bbox)
                self._control.set_lin_velocity(front = 20)
                if center_a//bove_bucket():
                    return 1
                else:
                    self._logger.log("Could not center above bucket")
                    return 0

        else:
            self._logger.log("Could not receive signal from hydrophones")
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

    def center_above_bucket(self):
        '''
        centering above bucket
        '''
        self.darknet_client.change_camera("bottom")
        stopwatch = Stopwatch()
        stopwatch.start()
        bbox = self.darknet_client.predict()
        while bbox is None and stopwatch.time() < self.MAX_TIME_SEC:
            bbox = self.darknet_client.predict()
            sleep(0.3)
        if bbox is None:
            self._logger.log("Could not locate bucket")
            return 0
        position_x = bbox.x
        position_y = bbox.y
        Kp = 0.001
        i = 0
        while position_x > self.POSITION_THRESHOLD and position_y > self.POSITION_THRESHOLD:
            self._control.set_lin_velocity(front = position_y * Kp, right = position_x * Kp)
            bbox = self.darknet_client.predict()
            if bbox is not None:
                position_x = bbox.x
                position_y = bbox.y
            i += 1
            if i == 1000:
                self._logger.log("Could not center above bucket")
                return 0
        return 1
            

    def drop_marker(self):
        '''
        Dropping marker at current position
        '''
        self._dropper.drop_marker()
        



            

