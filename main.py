#!/usr/bin/python3
'''
File name: main.py
Author: Jérémy Cheynet <jeremy.cheynet@actronika.com>
Copyright: Copyright (C) 2019 Actronika SAS
'''
import argparse
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import serial

ser = serial.Serial()

MAX_SIZE = 50

x = []
x_label = ''
y = []
y_label = []
title = ''

def read_line(wait = True):
    line = ser.readline()
    while ser.in_waiting and wait:
        line = ser.readline()
    line = line.decode("utf-8")
    line = line.replace('\n', '')
    line = line.replace('\0', '')
    data = line.split(';')
    return data

def animate(i):
    data = read_line()
    try:
        for i in range(len(data)):
            tmp = float(data[i])
    except:
        print("Oups can't convert")
        return

    if len(x) >= MAX_SIZE:
        x.pop(0)
        for i in range(len(y)):
            y[i].pop(0)

    x.append(float(data[0]))
    ax.clear()
    for i in range(len(y_label)):
        y[i].append(float(data[i+1]))
        ax.plot(x, y[i], label=y_label[i])
    leg = ax.legend()
    ax.set(xlabel=x_label, title=title)
    ax.legend(loc='upper right')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--serial', help='Serial port', default='/dev/ttyUSB0')
    parser.add_argument('-b', '--baudrate', help='Baud rate of serial port', default=115200)
    parser.add_argument('-m', '--max-point', help='Number max of point to display', default=300, type=int)
    parser.add_argument('-i', '--interval', help='Time interval between each update of screen (in ms)', default=10, type=int)
    args = parser.parse_args()


    MAX_SIZE = args.max_point

    ser.baudrate = args.baudrate
    ser.port = args.serial
    ser.open()

    label_valid = False
    while not label_valid:
        label = read_line(False)

        if len(label) < 2:
            title = label[0]
            continue

        x_label = str(label[0])
        for i in range(1, len(label)):
            y_label.append(label[i])
            y.append(0)
            y[i-1] = []

        label_valid = True

    fig, ax = plt.subplots()
    ani = animation.FuncAnimation(fig, animate, interval=args.interval)
    plt.show()
