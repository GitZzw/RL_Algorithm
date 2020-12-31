"""
Reinforcement learning maze example.
Red rectangle:          explorer.
Black rectangles:       hells       [reward = -1].
Yellow bin circle:      paradise    [reward = +1].
All other states:       ground      [reward = 0].
This script is the environment part of this example. The RL is in RL_brain.py.
View more on my tutorial page: https://morvanzhou.github.io/tutorials/
"""


import numpy as np
np.random.seed(1)
import tkinter as tk
import time


UNIT = 40   # pixels
MAZE_H = 7  # grid height
MAZE_W = 7  # grid width


class Maze(tk.Tk, object):
    def __init__(self):
        super(Maze, self).__init__()
        self.action_space = ['u', 'd', 'l', 'r']
        self.n_actions = len(self.action_space)
        self.title('maze')
        self.geometry('{0}x{1}'.format(MAZE_H * UNIT, MAZE_H * UNIT))
        self._build_maze()



    def _build_maze(self):
        self.canvas = tk.Canvas(self, bg='white',
                           height=MAZE_H * UNIT,
                           width=MAZE_W * UNIT)

        # create grids
        for c in range(0, MAZE_W * UNIT, UNIT):
            x0, y0, x1, y1 = c, 0, c, MAZE_H * UNIT
            self.canvas.create_line(x0, y0, x1, y1)
        for r in range(0, MAZE_H * UNIT, UNIT):
            x0, y0, x1, y1 = 0, r, MAZE_H * UNIT, r
            self.canvas.create_line(x0, y0, x1, y1)

        origin = np.array([20, 20])

        # hell  创建黑色hell
        # 第一个为向右两格，向下一格
        hell1_center = origin + np.array([UNIT * 1,UNIT * 0])
        self.hell1 = self.canvas.create_rectangle(
            hell1_center[0] - 15, hell1_center[1] - 15,
            hell1_center[0] + 15, hell1_center[1] + 15,
            fill='black')
        hell2_center = origin + np.array([UNIT * 1, UNIT*1])
        self.hell2 = self.canvas.create_rectangle(
            hell2_center[0] - 15, hell2_center[1] - 15,
            hell2_center[0] + 15, hell2_center[1] + 15,
            fill='black')

        hell3_center = origin + np.array([UNIT * 1, UNIT*2])
        self.hell3 = self.canvas.create_rectangle(
            hell3_center[0] - 15, hell3_center[1] - 15,
            hell3_center[0] + 15, hell3_center[1] + 15,
            fill='black')

        hell4_center = origin + np.array([UNIT * 1, UNIT*3])
        self.hell4 = self.canvas.create_rectangle(
            hell4_center[0] - 15, hell4_center[1] - 15,
            hell4_center[0] + 15, hell4_center[1] + 15,
            fill='black')

        hell5_center = origin + np.array([UNIT * 1, UNIT*4])
        self.hell5 = self.canvas.create_rectangle(
            hell5_center[0] - 15, hell5_center[1] - 15,
            hell5_center[0] + 15, hell5_center[1] + 15,
            fill='black')
        hell6_center = origin + np.array([UNIT * 1, UNIT*5])
        self.hell6 = self.canvas.create_rectangle(
            hell6_center[0] - 15, hell6_center[1] - 15,
            hell6_center[0] + 15, hell6_center[1] + 15,
            fill='black')


        hell7_center = origin + np.array([UNIT * 2, UNIT*5])
        self.hell7 = self.canvas.create_rectangle(
            hell7_center[0] - 15, hell7_center[1] - 15,
            hell7_center[0] + 15, hell7_center[1] + 15,
            fill='black')
        hell8_center = origin + np.array([UNIT *5, UNIT*6])
        self.hell8 = self.canvas.create_rectangle(
            hell8_center[0] - 15, hell8_center[1] - 15,
            hell8_center[0] + 15, hell8_center[1] + 15,
            fill='black')
        hell9_center = origin + np.array([UNIT *5, UNIT*5])
        self.hell9 = self.canvas.create_rectangle(
            hell9_center[0] - 15, hell9_center[1] - 15,
            hell9_center[0] + 15, hell9_center[1] + 15,
            fill='black')

        hell10_center = origin + np.array([UNIT * 5, UNIT*4])
        self.hell10 = self.canvas.create_rectangle(
            hell10_center[0] - 15, hell10_center[1] - 15,
            hell10_center[0] + 15, hell10_center[1] + 15,
            fill='black')


        hell11_center = origin + np.array([UNIT * 5, UNIT*3])
        self.hell11 = self.canvas.create_rectangle(
            hell11_center[0] - 15, hell11_center[1] - 15,
            hell11_center[0] + 15, hell11_center[1] + 15,
            fill='black')

        hell12_center = origin + np.array([UNIT * 5, UNIT*2])
        self.hell12 = self.canvas.create_rectangle(
            hell12_center[0] - 15, hell12_center[1] - 15,
            hell12_center[0] + 15, hell12_center[1] + 15,
            fill='black')

        hell13_center = origin + np.array([UNIT * 5, UNIT*1])
        self.hell13 = self.canvas.create_rectangle(
            hell13_center[0] - 15, hell13_center[1] - 15,
            hell13_center[0] + 15, hell13_center[1] + 15,
            fill='black')

        hell14_center = origin + np.array([UNIT *4, UNIT*1])
        self.hell14 = self.canvas.create_rectangle(
            hell14_center[0] - 15, hell14_center[1] - 15,
            hell14_center[0] + 15, hell14_center[1] + 15,
            fill='black')



        # 创建得分点  create oval
        # 向右两格向下一格
        oval_center = origin + np.array([UNIT * 3, UNIT*3])
        self.oval = self.canvas.create_oval(
            oval_center[0] - 15, oval_center[1] - 15,
            oval_center[0] + 15, oval_center[1] + 15,
            fill='Yellow')

        # oval2_center = origin + np.array([UNIT * 2, UNIT*5])
        # self.oval2 = self.canvas.create_oval(
        #     oval2_center[0] - 15, oval2_center[1] - 15,
        #     oval2_center[0] + 15, oval2_center[1] + 15,
        #     fill='blue')

        origin2 = origin + np.array([UNIT * 6, UNIT*6])
        # create red rect
        self.rect2 = self.canvas.create_rectangle(
            origin2[0] - 15, origin2[1] - 15,
            origin2[0] + 15, origin2[1] + 15,
            fill='red')

        self.rect = self.canvas.create_rectangle(
            origin[0] - 15, origin[1] - 15,
            origin[0] + 15, origin[1] + 15,
            fill='blue')

        # pack all
        self.canvas.pack()

    def reset2(self):
        self.update()
        time.sleep(0.001)
        self.canvas.delete(self.rect2)
        origin = np.array([20, 20])
        origin2 = origin + np.array([UNIT * 6, UNIT*6])
        self.rect2 = self.canvas.create_rectangle(
            origin2[0] - 15, origin2[1] - 15,
            origin2[0] + 15, origin2[1] + 15,
            fill='blue')
        return self.canvas.coords(self.rect2)

    def reset(self):
        self.update()
        time.sleep(0.001)
        self.canvas.delete(self.rect)
        origin = np.array([20, 20])
        self.rect = self.canvas.create_rectangle(
            origin[0] - 15, origin[1] - 15,
            origin[0] + 15, origin[1] + 15,
            fill='red')
        # return observation
        return self.canvas.coords(self.rect)

    def step(self, action):
        s = self.canvas.coords(self.rect)
        base_action = np.array([0, 0])
        if action == 0:   # up
            if s[1] > UNIT:
                base_action[1] -= UNIT
        elif action == 1:   # down
            if s[1] < (MAZE_H - 1) * UNIT:
                base_action[1] += UNIT
        elif action == 2:   # right
            if s[0] < (MAZE_W - 1) * UNIT:
                base_action[0] += UNIT
        elif action == 3:   # left
            if s[0] > UNIT:
                base_action[0] -= UNIT

        self.canvas.move(self.rect, base_action[0], base_action[1])  # move agent

        s_ = self.canvas.coords(self.rect)  # next state

        # reward function
        if s_ == self.canvas.coords(self.oval):
            reward = 1
            done = True
        elif s_ in [self.canvas.coords(self.hell1), self.canvas.coords(self.hell2),self.canvas.coords(self.hell3),
                    self.canvas.coords(self.hell4), self.canvas.coords(self.hell5),self.canvas.coords(self.hell6),
                    self.canvas.coords(self.hell7), self.canvas.coords(self.hell8),self.canvas.coords(self.hell9),
                    self.canvas.coords(self.hell10), self.canvas.coords(self.hell11),self.canvas.coords(self.hell12),
                    self.canvas.coords(self.hell13),self.canvas.coords(self.hell14),]:
            reward = -1
            done = True
        else:
            reward = 0
            done = False

        return s_, reward, done


    def step2(self, action):
        s = self.canvas.coords(self.rect2)
        base_action = np.array([0, 0])
        if action == 0:   # up
            if s[1] > UNIT:
                base_action[1] -= UNIT
        elif action == 1:   # down
            if s[1] < (MAZE_H - 1) * UNIT:
                base_action[1] += UNIT
        elif action == 2:   # right
            if s[0] < (MAZE_W - 1) * UNIT:
                base_action[0] += UNIT
        elif action == 3:   # left
            if s[0] > UNIT:
                base_action[0] -= UNIT

        self.canvas.move(self.rect2, base_action[0], base_action[1])  # move agent

        s_ = self.canvas.coords(self.rect2)  # next state

        # reward function
        if s_ == self.canvas.coords(self.oval):
            reward = 1
            done = True
        elif s_ in [self.canvas.coords(self.hell1), self.canvas.coords(self.hell2),self.canvas.coords(self.hell3),
                    self.canvas.coords(self.hell4), self.canvas.coords(self.hell5),self.canvas.coords(self.hell6),
                    self.canvas.coords(self.hell7), self.canvas.coords(self.hell8),self.canvas.coords(self.hell9),
                    self.canvas.coords(self.hell10), self.canvas.coords(self.hell11),self.canvas.coords(self.hell12),
                    self.canvas.coords(self.hell13),self.canvas.coords(self.hell14),]:
            reward = -1
            done = True
        else:
            reward = 0
            done = False

        return s_, reward, done


    def render(self):
        time.sleep(0.01)
        self.update()
