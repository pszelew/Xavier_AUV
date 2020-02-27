from tasks.task_executor_itf import ITaskExecutor
from communication.rpi_broker.movements import Movements
from neural_networks.DarknetClient import DarknetClient
from utils.stopwatch import Stopwatch
from configs.config import get_config
from time import sleep
from utils.signal_processing import mvg_avg
from utils.centering import center_rov


class GateTaskExecutor(ITaskExecutor):

    ###Initialization###
    def __init__(self, control_dict, sensors_dict,
                camera_client, main_logger):
        self._control = control_dict
        self.depth_sensor = sensors_dict['depth']
        self._logger = main_logger
        self.movements = control_dict['movements']
        self.darknet_client = DarknetClient()
        self.config = get_config('tasks')['qualification_task']
        self.confidence = 0

        self.movements.pid_turn_on()
        self._logger.log("Qualification task executor init done")


    ###Start the gate algorithm###
    def run(self):
        self._logger.log("Qualification task executor started")

        self.dive()

        #self.darknet_client.load_model('gate') # Loaded default in Darknet Server initialization

        self._logger.log("Gate model loaded")

        if not self.find_gate():
            self._logger.log("gate not found. task failed - aborting")
            return False

        while True:
            if not self.center_on_gate():
                self._logger.log("couldn't center on gate. task failed - aborting")
                return False

            self.go_to_gate()

            if self.is_gate_passed():
                self.end_task()
                self._logger.log("task succeeded!")
                return True

    def find_gate(self):
        self._logger.log("finding the gate")
        config = self.config['search']
        MAX_TIME_SEC = config['max_time_sec']
        MODE = config['mode']

        stopwatch = Stopwatch()
        stopwatch.start()
        self._logger.log("started find gate loop")

        while stopwatch.time() < config['max_time_sec']:

            if MODE == "mvg_avg":
                for i in range(config['number_of_samples']):
                    if self.is_this_gate():
                        return True
            elif MODE == "simple":
                bbox = False
                bbox = self.darknet_client.predict()[0].normalize(480, 480)
                if not bbox:
                    self._logger.log("gate not found")
                    return False
                self._logger.log("gate found")
                return True
            #self.movements.rotate_angle(0, 0, config['rotation_angle'])

        self._logger.log("gate not found")
        return False

    def is_this_gate(self):
        config = self.config['search']
        MOVING_AVERAGE_DISCOUNT = config['moving_avg_discount']
        CONFIDENCE_THRESHOLD = config['confidence_threshold']

        bbox = False

        bbox = self.darknet_client.predict()
        bbox = bbox[0].normalize(480, 480)


        if bbox:
            self.confidence = mvg_avg(1, self.confidence, MOVING_AVERAGE_DISCOUNT)
            self._logger.log("is_this_gate: something detected")
        else:
            self.confidence = mvg_avg(0, self.confidence, MOVING_AVERAGE_DISCOUNT)

        if self.confidence > CONFIDENCE_THRESHOLD:
            self._logger.log("is_this_gate: gate found")
            return True
        return False

    def dive(self):
        depth = self.config['max_depth']
        self._logger.log("Dive: setting depth")

        self.movements.pid_set_depth(depth)
        self._logger.log("Dive: holding depth")
        self.movements.pid_hold_depth()


    def center_on_gate(self):
        config = self.config['centering']
        MAX_TIME_SEC = config['max_time_sec']
        MAX_CENTER_DISTANCE = config['max_center_distance']

        stopwatch = Stopwatch()
        stopwatch.start()


        while stopwatch.time() <= MAX_TIME_SEC:

            bbox = self.darknet_client.predict()[0].normalize(480, 480)
            if bbox.x <= MAX_CENTER_DISTANCE & bbox.y <= MAX_CENTER_DISTANCE:
                self._logger.log("centered on gate successfully")
                return True
            center_rov(move=self._control, Bbox=bbox, depth_sensor=self.depth_sensor)
        self._logger.log("couldn't center on gate")
        return False

    def go_to_gate(self):
        self._logger.log("going to gate")
        config = self.config['go']
        GO_TIME_SEC = config['go_time_sec']
        MAX_ENGINE_POWER = config['max_engine_power']

        self.movements.set_lin_velocity(MAX_ENGINE_POWER, 0, 0)

        sleep(GO_TIME_SEC)

    def is_gate_passed(self):
        if not self.find_gate():
            self._logger.log("gate passed")
            return True
        self._logger.log("gate not passed")
        return False

    def end_task(self):
        self._logger.log("qualification_task: ending task")
        config = self.config['end']
        GO_TIME_SEC = config['go_time_sec']
        self._logger.log("moving forward for 5s - everything is fine")  # TODO: no to tak nie może być opisane xD
        sleep(GO_TIME_SEC)
        self.movements.set_lin_velocity(0, 0, 0)
        self._logger.log("finished movement")
