#!/usr/bin/env python3

import findlocation
import numpy as np
import particle
import math
import move
import localize
import sys
import camera
from time import sleep
import copy

#Import arlo robot
sys.path.append("../")
import ARLO.robot


def printMap(list, robot, grid_size):
    y, x= np.shape(list)
    startLine = "+" + ("------+"*x)
    print(startLine)
    for i in range(y):
        print("|", end="")
        for j in range(x):
            if (robot.getX()/grid_size == i and robot,getY()/grid_size == j):
                print('{:^6}|'.format("R"), end="")
            elif not (list[i,j] == 0):
                print('{:^6}|'.format(round(list[i,j], 1)), end="")
            else:
                print('{:^6}|'.format(""), end="")
        print()
        print(startLine)
    print()


try:
    arlo = ARLO.robot.Robot()
    cam = camera.Camera(0, 'arlo', useCaptureThread = True)

    target = np.array([150,0])
    boxOne = np.array([300,0])
    # Initialize particles
    num_particles = 1000
    grid_size = 30

    particles = localize.initialize_particles(num_particles)
    distToTarget = 100
    # Turn 360 until we find boxes (findlocation.py)
    while (distToTarget > 15):
        particles, map = copy.deepcopy(findlocation.localization_turnV2(particles, arlo, cam,
                                                                        np.zeros((20, 20), dtype=float)))

        # check location. Keep spinning
        print("meanParticle = ")
        meanParticle = particle.estimate_pose(particles)
        print(meanParticle.getX(), ", ", meanParticle.getY(), ", ", meanParticle.getTheta())

        #print("estimatetarget = ")
        vecLength, targetOri = findlocation.estimate_target(target[0], target[1], meanParticle)
        #print(vecLength)

        print("disttotarget = ")
        distToTarget = math.sqrt(( target[0] - meanParticle.getX() )**2 + ( target[1] - meanParticle.getY() )**2)
        print(distToTarget)

        move.turnAll((targetOri), particles, arlo)
        sleep(1)
        move.moveAll(round(distToTarget * 1.10, 5), particles, arlo)

        sleep(1)
        vecLength, targetOri = findlocation.estimate_target(boxOne[0], boxOne[1], meanParticle)
        move.turnAll((targetOri), particles, arlo)

        PrintMap(map, arlo, grid_size)

finally:
    cam.terminateCaptureThread()