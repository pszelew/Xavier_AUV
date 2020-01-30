previousFlarePosX = 0
previousFlarePosY = 0
errorX = 0
errorY = 0
errorSumX = 0
errorSumY = 0
Ki = 2
Kd = 3

def center_rov(move, xPos = 0, yPos = 0, Bbox = None):
    if Bbox:
        xPos = Bbox.x
        yPos = Bbox.y
        
    if previousFlarePosX != 0 & previousFlarePosY != 0:
        errorX = xPos - previousFlarePosX
        errorY = yPos - previousFlarePosY
        errorSumX += errorX
        errorSumY += errorY

    previousFlarePosX = xPos
    previousFlarePosY = yPos

    move.move_distance(0, (xPos * 10 + .Ki * .errorSumX + .Kd * .errorX),
                            (yPos * 10 + .Ki * .errorSumY + .Kd * .errorY))
