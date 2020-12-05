import os
import sys
import time
import serial
import numpy as np
import math
import cv2
import matplotlib.pyplot as plt

#  A garder depuis ici

def plot_covariance_ellipse(state_est, cov_est):
    Pxy = cov_est[0:2, 0:2]
    eigval, eigvec = np.linalg.eig(Pxy)

    if eigval[0] >= eigval[1]:
        bigind = 0
        smallind = 1
    else:
        bigind = 1
        smallind = 0

    t = np.arange(0, 2 * math.pi + 0.1, 0.1)
    a = math.sqrt(eigval[bigind])
    b = math.sqrt(eigval[smallind])
    x = [a * math.cos(it) for it in t]
    y = [b * math.sin(it) for it in t]

    angle = math.atan2(eigvec[bigind, 1], eigvec[bigind, 0])
    R = np.array([[math.cos(angle), math.sin(angle)],
                  [-math.sin(angle), math.cos(angle)]])
    fx = R.dot(np.array([[x, y]]))
    px = np.array(fx[0, :] + state_est[0, 0]).flatten()
    py = np.array(fx[1, :] + state_est[1, 0]).flatten()

    return px, py


def plot(state_pred, cov_pred):
    plt.ion()
    fig, ax = plt.subplots()

    px, py = plot_covariance_ellipse(state_pred[0], cov_pred[0] / 1000)
    line_v = ax.axvline(x=state_pred[0][0], color="k")
    line_h = ax.axhline(y=state_pred[0][1], color="k")
    ellips, = ax.plot(px, py, "--r", label="covariance matrix")

    max_l = len(state_pred)
    l = [i for i in range(max_l)]
    l.insert(0, -1)
    for i in l:
        print(i)
        px, py = plot_covariance_ellipse(state_pred[i], cov_pred[i] / 1000)

        line_v.set_xdata(state_pred[i][0])
        line_h.set_ydata(state_pred[i][1])

        ellips.set_xdata(px)
        ellips.set_ydata(py)
        ax.relim()
        ax.autoscale_view()

        fig.canvas.draw()

        fig.canvas.flush_events()
        plt.axis([0, 72.5, 0, 80])
        plt.show()

        time.sleep(2)
