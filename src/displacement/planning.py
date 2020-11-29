import time

import numpy as np

from src.displacement.movement import rotate, advance
from src.thymio.Thymio import Thymio


# this code do a sequence of  displacement corresponding to the entire global path planning
# i.e to go from the start to the goal

def update_path(thymio: Thymio, path, x, y, theta, interval_sleep=0.02):
    CONST_DISP = 2.5  # distance in cm between two squares
    # TODO wait for thread to die before new thread
    if path.shape[0] and path.shape[1]:
        print("x,y: ", x, y)
        print("path_x, path_y: ", path[0], path[1])
        target_x = path[0][0]
        target_y = path[1][0]
        delta_x = target_x - x
        delta_y = target_y - y
        # print("sign: ", np.sign(delta_x))
        # print("sign: ", np.sign(delta_x))

        i = 1
        if i < path.shape[0]:
            while (x + (i + 1) * int(np.sign(delta_x)) == path[0][i]) and (
                    y + (i + 1) * int(np.sign(delta_y)) == path[1][i]):
                target_x = path[0][i]
                target_y = path[1][i]
                i = i + 1
                if i >= path.shape[0]:
                    break

        print("cases en x: ", i * int(np.sign(delta_x)))
        print("cases en y: ", i * int(np.sign(delta_y)))
        delta_x = target_x - x
        delta_y = target_y - y
        delta_x_cm = delta_x * CONST_DISP
        delta_y_cm = delta_y * CONST_DISP
        delta_r = np.sqrt(delta_x_cm ** 2 + delta_y_cm ** 2)
        # print("x, y: ", x, y)

        # Relative rotation to target
        target_theta_rad = np.arctan2(delta_y_cm, delta_x_cm)
        target_theta_deg = np.rad2deg(target_theta_rad)
        target_theta_deg = np.abs(target_theta_deg) * np.sign(delta_x)
        delta_theta = target_theta_deg - theta
        delta_theta = (delta_theta + 180.0) % 360.0 - 180.0
        # delta_theta = (delta_theta + np.pi) % (2 * np.pi) - np.pi
        # print("theta: ", theta)
        # print("target_theta_deg: ", target_theta_deg)

        # Apply rotation, then displacement
        print("rotate of ", delta_theta)
        thread = rotate(thymio, delta_theta)
        while thread.is_alive():
            time.sleep(interval_sleep)

        print("advance ", delta_r)
        thread = advance(thymio, delta_r)
        while thread.is_alive():
            time.sleep(interval_sleep)

        new_path = path
        for _ in range(i - 1):
            new_path = np.delete(new_path, 0, 1)
        return new_path
