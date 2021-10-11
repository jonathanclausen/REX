import numpy as np
import sys

import math

#Import arlo robot
sys.path.append("../")

import ARLO.robot
import Ex4.particle

grid_size = 10
sensor_max = 250
sensor_angle = math.radians(15 * 2)


## Log function
prob_free = 0.9
l_0 = prob_free
l_occ = np.log((1-prob_free) / prob_free)
l_free = np.log(prob_free / (1 - prob_free))

def occupancy_grid_mapping(grid, mean_particle, sensors):
    update_m = perceptualField(grid,mean_particle,sensors)
    for m in update_m:
        x = m[0] 
        y = m[1]
        grid[x][y] = grid[x][y] + inverse_range_sensor_model([x, y, grid[x][y]], mean_particle, sensors) - l_0
            

def inverse_range_sensor_model(cell,robot,sensor):
    r = math.sqrt(((cell[0] - robot.getX())**2) + ((cell[1] - robot.getY())**2) )
    angle = math.atan2( cell[1] - robot.getY, cell[0] - robot.getX() ) - robot.getTheta()
    
    if (r > (max(sensor_max, sensor + (grid_size**2 / 2))) or  abs(angle) > sensor_angle  ):
        return cell[2]
    if (sensor < sensor_max) and (abs(r - sensor) < grid_size/2):
        return l_occ
    if (r < sensor):
        return l_free
        
def perceptualField(m, robot):
    
    
    

     