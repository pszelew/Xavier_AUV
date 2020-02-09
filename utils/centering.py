from time import sleep
from configs.config import get_config
def center_rov(move, xPos = 0, yPos = 0, Bbox = None, depth_sensor = None):
    config = get_config("tasks")['path_task']
    Kp = config['centering']['kp']
    """
    TODO implement saving previous position outside center_rov()
    it is needed for integral and derivational part of regulator
    """
    '''
    Ki = 0.1
    Kd = 0.1
    previousFlarePosX = 0
    previousFlarePosY = 0
    errorX = 0
    errorY = 0
    errorSumX = 0
    errorSumY = 0
    '''
    if Bbox:
        xPos = Bbox.x
        yPos = Bbox.y
        
    '''
    if previousFlarePosX != 0 & previousFlarePosY != 0:
        errorX = xPos - previousFlarePosX
        errorY = yPos - previousFlarePosY
        errorSumX += errorX
        errorSumY += errorY

    previousFlarePosX = xPos
    previousFlarePosY = yPos
'''
    move.set_lin_velocity(right = xPos * Kp )#+ Ki * errorSumX + Kd * errorX)
    if depth_sensor:
        current_depth = depth_sensor.get_depth()
        move.pid_set_depth(current_depth - Kp * yPos)
