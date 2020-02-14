def center_rov(move, xPos = 0, yPos = 0, Bbox = None, depth_sensor = None, logger=None):
    Kp = 20
    Ki = 0.0
    Kd = 0.0
    previousFlarePosX = 0
    previousFlarePosY = 0
    errorX = 0
    errorY = 0
    errorSumX = 0
    errorSumY = 0
    if Bbox:
        xPos = Bbox.xc
        yPos = Bbox.yc
        
    if previousFlarePosX != 0 & previousFlarePosY != 0:
        errorX = xPos - previousFlarePosX
        errorY = yPos - previousFlarePosY
        errorSumX += errorX
        errorSumY += errorY

    previousFlarePosX = xPos
    previousFlarePosY = yPos

    move.set_lin_velocity(right = -xPos * Kp + Ki * errorSumX + Kd * errorX)
    if logger:
        logger.log("xPos*Kp = "+str(xPos*Kp))
    if depth_sensor:
        current_depth = depth_sensor.get_depth()
        move.pid_set_depth(current_depth - yPos)
