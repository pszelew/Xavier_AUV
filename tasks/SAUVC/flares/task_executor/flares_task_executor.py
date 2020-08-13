from tasks.task_executor_itf import ITaskExecutor
from utils.stopwatch import Stopwatch
from configs.config import get_config
from definitions import IP_ADDRESS, DARKNET_PORT
from structures.bounding_box import BoundingBox
from utils.signal_processing import mvg_avg
from utils.location_calculator import location_calculator
import math as m


class FlaresTaskExecutor(ITaskExecutor):

    ###Initialization###
    def __init__(self, control_dict, sensors_dict, vision, environment, main_logger):
        self._control = control_dict['movements']
        self._hydrophones = sensors_dict['hydrophones']
        self._vision = vision
        self._bounding_box = BoundingBox(0, 0, 0, 0)
        self._logger = main_logger
        self.config = get_config('tasks')['localization']
        self.confidence = 0
        self.flare_position = None

    ###Start the gate algorithm###
    def run(self):
        self._logger.log("Localization task executor started")
        self._control.pid_turn_on()

        self.dive()

        self._logger.log("starting localization task loop")

        self._vision.load_model('flare')

        while True:
            self.center_on_pinger()

            if not self.find_flare():
                self._logger.log("couldn't find flare - task failed, aborting")
                return False
            if not self.center_on_flare():
                self._logger.log("couldn't center on flare - task failed, aborting")
                return False

            # if traveled whole distance to flare, checked if flare knocked
            # else repeat loop
            if self.go_to_flare():
                if self.is_flare_knocked():
                    self._logger.log("knocked flare - task finished successfully")
                    return True

    def find_flare(self):
        # TODO: obsługa wykrycia dwóch flar

        self._logger.log("finding the flare")
        config = self.config['search']

        stopwatch = Stopwatch()
        stopwatch.start()
        self._logger.log("started find flare loop")

        while stopwatch < config['max_time_sec']:
            # sprawdza kilka razy, dla pewności
            #   (no i żeby confidence się zgadzało, bo bez tego to nawet jak raz wykryje, to nie przejdzie -
            #       - przy moving_avg_discount=0.9 musi wykryć 10 razy z rzędu
            for i in range(config['number_of_samples']):
                if self.is_this_flare():
                    return True
            self._control.rotate_angle(0, 0, config['rotation_angle'])

        self._logger.log("flare not found")
        return False

    def is_this_flare(self):
        config = self.config['search']
        MOVING_AVERAGE_DISCOUNT = config['moving_avg_discount']
        CONFIDENCE_THRESHOLD = config['confidence_threshold']

        bbox = self._vision.predict()[0].normalize(480, 480)

        if bbox is not None:
            self.confidence = mvg_avg(1, self.confidence, MOVING_AVERAGE_DISCOUNT)
            self._bounding_box.mvg_avg(bbox, 0.5, True)
            self._logger.log("is_this_flare: something detected")
        else:
            self.confidence = mvg_avg(0, self.confidence, MOVING_AVERAGE_DISCOUNT)

        if self.confidence > CONFIDENCE_THRESHOLD:
            self._logger.log("is_this_flare: flare found")
            return True

    def dive(self):
        depth = self.config['max_depth']
        self._logger.log("Dive: setting depth")
        self._control.pid_set_depth(depth)
        self._logger.log("Dive: holding depth")
        self._control.pid_hold_depth()

    def center_on_flare(self):
        """
        rotates in vertical axis so flare is in the middle of an image
        TODO: obsługa dwóch flar
        """
        config = self.config['centering']
        flare_size = get_config("objects_size")["localization"]["flare"]["height"]

        MAX_CENTER_ANGLE_DEG = config['max_center_angle_deg']
        MAX_TIME_SEC = config['max_time_sec']

        stopwatch = Stopwatch()
        stopwatch.start()

        while stopwatch <= MAX_TIME_SEC:
            bbox = self._vision.predict()[0].normalize(480,480)
            self.flare_position = location_calculator(bbox, flare_size, "height")
            angle = -m.degrees(m.atan2(self.flare_position['x'], self.flare_position['distance']))
            if abs(angle) <= MAX_CENTER_ANGLE_DEG:
                self._logger.log("centered on flare successfully")
                return True
            self._control.rotate_angle(0, 0, angle)
        self._logger.log("couldn't center on flare")
        return False

    def go_to_flare(self):
        """
        moves distance to flare + a little more to knock it
        :return: True - if managed to move distance in time
                 False - if didn't manage to move distance in time
        """
        config = self.config['go']
        MAX_TIME_SEC = config['max_time_sec']

        stopwatch = Stopwatch()
        stopwatch.start()

        self._control.move_distance(self.flare_position['distance'] + self.config['go']['distance_to_add_m'], 0, 0)

        if stopwatch <= MAX_TIME_SEC:
            self._logger.log("go_to_flare - traveled whole distance")
            return True
        else:
            self._logger.log("go_to_flare - didn't travel whole distance")
            return False

    def center_on_pinger(self):
        """
        rotates in vertical axis so pinger signal is in front
        """
        config = self.config['centering']
        MAX_TIME_SEC = config['max_time_sec']
        MAX_CENTER_ANGLE_DEG = config['max_center_angle_deg']

        self._logger.log("centering on pinger")
        stopwatch = Stopwatch()
        stopwatch.start()

        while stopwatch < MAX_TIME_SEC:
            angle = self._hydrophones.get_angle()
            if angle is None:
                self._logger.log("no signal from hydrophones - locating pinger failed")
                return False
            if abs(angle) < MAX_CENTER_ANGLE_DEG:
                self._logger.log("centered on pinger successfully")
                return True
            self._control.rotate_angle(0, 0, angle)
        self._logger.log("couldn't ceneter on pinger")
        return False

    def is_flare_knocked(self):
        """
        if doesn't see the flare, then it's knocked
        """
        if self._vision.predict()[0] is None:
            self._logger.log("can't see flare - flare knocked")
            return True
        self._logger.log("flare still visible - flare not knocked")
        return False
