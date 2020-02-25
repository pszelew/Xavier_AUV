from time import sleep
from configs.config import get_config

previous_position = 0
error_integral = 0

def center_rov(move, xPos = 0, yPos = 0, Bbox = None, depth_sensor = None,logger = None):
    global previous_position
    global error_integral
    config = get_config("tasks")['path_task']
    Kp = config['centering']['kp']
    Ki = config['centering']['ki']
    Kd = config['centering']['kd']
    
    if Bbox:
        xPos = Bbox.xc
        yPos = Bbox.yc
        
    error_integral = error_integral + xPos
    derivative = xPos - previous_position
    previous_position = xPos

    move.set_lin_velocity(right = xPos * Kp + error_integral * Ki + derivative * Kd )
    if logger:
        logger.log("xPos: "+str(xPos)+' velocity set '+str(xPos * Kp + error_integral * Ki + derivative * Kd))
    if depth_sensor:
        current_depth = depth_sensor.get_depth()
        move.pid_set_depth(current_depth - Kp * yPos)
    sleep(0.2)
    move.set_lin_velocity(right = 0)
