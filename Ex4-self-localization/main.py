import findlocation
import numpy as np
import particle
import math
import move
import localize
import sys
import camera
from time import sleep

#Import arlo robot
sys.path.append("../")
import ARLO.robot

try:
    arlo = ARLO.robot.Robot()
    cam = camera.Camera(0, 'arlo', useCaptureThread = True)

    target = np.array([75,0])
    # Initialize particles
    num_particles = 1000
    particles = localize.initialize_particles(num_particles)

    # Turn 360 until we find boxes (findlocation.py)

    findlocation.localization_turn(particles, arlo, cam)


    # check location. Keep spinning
    print("meanParticle = ")
    meanParticle = particle.estimate_pose(particles)
    print(meanParticle.getX(), ", ", meanParticle.getY(), ", ", meanParticle.getTheta())

    print("estimatetarget = ")
    vecLength, targetOri = findlocation.estimate_target(target[0], target[1], meanParticle)
    print(vecLength)

    print("disttotarget = ")
    distToTarget = math.sqrt(( target[0] - meanParticle.getX() )**2 + ( target[1] - meanParticle.getY() )**2)
    print(distToTarget)


    move.turnAll((targetOri), particles, arlo) 
    print("turning radians= ", targetOri)
    sleep(2)
    move.moveAll(distToTarget, particles, arlo)
    

finally:
    cam.terminateCaptureThread()
    


    