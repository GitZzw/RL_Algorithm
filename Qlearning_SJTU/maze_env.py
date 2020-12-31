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
import time
import sys
if sys.version_info.major == 2:
    import Tkinter as tk
else:
    import tkinter as tk


UNIT = 40   # pixels
MAZE_H = 14  # grid height
MAZE_W = 16  # grid width


class Maze(tk.Tk, object):
    def __init__(self):
        super(Maze, self).__init__()
        self.action_space = ['u', 'd', 'l', 'r']
        self.n_actions = len(self.action_space)
        self.title('maze')
        self.count = 0
        # 生成(40*4)*(40*4)的网格
        self.geometry('{0}x{1}'.format(MAZE_H * UNIT, MAZE_H * UNIT))
        self._build_maze()

    def _build_maze(self):
        #  生成窗口（canvas）
        self.canvas = tk.Canvas(self, bg='white',
                           height=MAZE_H * UNIT,
                           width=MAZE_W * UNIT)

        # create grids
        # 横着的线
        for c in range(0, MAZE_W * UNIT, UNIT):
            x0, y0, x1, y1 = c, 0, c, MAZE_H * UNIT
            self.canvas.create_line(x0, y0, x1, y1)
        # 竖着的线
        for r in range(0, MAZE_H * UNIT, UNIT):
            x0, y0, x1, y1 = 0, r, MAZE_W * UNIT, r
            self.canvas.create_line(x0, y0, x1, y1)

        # create origin
        # 原点的位置是[20,20]，即第一个块的中心
        origin = np.array([20, 20])

        # hell  创建黑色hell
        # 第一个为向右两格，向下一格
        hell1_center = origin + np.array([-UNIT+UNIT * 3, UNIT*2-2*UNIT])
        self.hell1 = self.canvas.create_rectangle(
            hell1_center[0] - 15, hell1_center[1] - 15,
            hell1_center[0] + 15, hell1_center[1] + 15,
            fill='black')
        hell2_center = origin + np.array([-UNIT+UNIT*4, UNIT*2-2*UNIT])
        self.hell2 = self.canvas.create_rectangle(
            hell2_center[0] - 15, hell2_center[1] - 15,
            hell2_center[0] + 15, hell2_center[1] + 15,
            fill='black')

        hell3_center = origin + np.array([-UNIT+UNIT * 5, UNIT*2-2*UNIT])
        self.hell3 = self.canvas.create_rectangle(
            hell3_center[0] - 15, hell3_center[1] - 15,
            hell3_center[0] + 15, hell3_center[1] + 15,
            fill='black')

        hell4_center = origin + np.array([-UNIT+UNIT * 6, UNIT*3-2*UNIT])
        self.hell4 = self.canvas.create_rectangle(
            hell4_center[0] - 15, hell4_center[1] - 15,
            hell4_center[0] + 15, hell4_center[1] + 15,
            fill='black')

        hell5_center = origin + np.array([-UNIT+UNIT * 2, UNIT*3-2*UNIT])
        self.hell5 = self.canvas.create_rectangle(
            hell5_center[0] - 15, hell5_center[1] - 15,
            hell5_center[0] + 15, hell5_center[1] + 15,
            fill='black')
        hell6_center = origin + np.array([-UNIT+UNIT * 2, UNIT*4-2*UNIT])
        self.hell6 = self.canvas.create_rectangle(
            hell6_center[0] - 15, hell6_center[1] - 15,
            hell6_center[0] + 15, hell6_center[1] + 15,
            fill='black')
        hell7_center = origin + np.array([-UNIT+UNIT * 3, UNIT*5-2*UNIT])
        self.hell7 = self.canvas.create_rectangle(
            hell7_center[0] - 15, hell7_center[1] - 15,
            hell7_center[0] + 15, hell7_center[1] + 15,
            fill='black')
        hell8_center = origin + np.array([-UNIT+UNIT * 4, UNIT*5-2*UNIT])
        self.hell8 = self.canvas.create_rectangle(
            hell8_center[0] - 15, hell8_center[1] - 15,
            hell8_center[0] + 15, hell8_center[1] + 15,
            fill='black')
        hell9_center = origin + np.array([-UNIT+UNIT * 5, UNIT*5-2*UNIT])
        self.hell9 = self.canvas.create_rectangle(
            hell9_center[0] - 15, hell9_center[1] - 15,
            hell9_center[0] + 15, hell9_center[1] + 15,
            fill='black')
        hell10_center = origin + np.array([-UNIT+UNIT * 6, UNIT*6-2*UNIT])
        self.hell10 = self.canvas.create_rectangle(
            hell10_center[0] - 15, hell10_center[1] - 15,
            hell10_center[0] + 15, hell10_center[1] + 15,
            fill='black')
        # 第二个为向下两格，向右一格
        hell11_center = origin + np.array([-UNIT+UNIT * 6, UNIT * 7-2*UNIT])
        self.hell11 = self.canvas.create_rectangle(
            hell11_center[0] - 15, hell11_center[1] - 15,
            hell11_center[0] + 15, hell11_center[1] + 15,
            fill='black')

        hell12_center = origin + np.array([-UNIT+UNIT *2, UNIT*7-2*UNIT])
        self.hell12 = self.canvas.create_rectangle(
            hell12_center[0] - 15, hell12_center[1] - 15,
            hell12_center[0] + 15, hell12_center[1] + 15,
            fill='black')
        hell13_center = origin + np.array([-UNIT+UNIT * 3, UNIT*8-2*UNIT])
        self.hell13 = self.canvas.create_rectangle(
            hell13_center[0] - 15, hell13_center[1] - 15,
            hell13_center[0] + 15, hell13_center[1] + 15,
            fill='black')
        hell14_center = origin + np.array([-UNIT+UNIT * 4, UNIT*8-2*UNIT])
        self.hell14 = self.canvas.create_rectangle(
            hell14_center[0] - 15, hell14_center[1] - 15,
            hell14_center[0] + 15, hell14_center[1] + 15,
            fill='black')
        hell15_center = origin + np.array([-UNIT+UNIT * 5, UNIT*8-2*UNIT])
        self.hell15 = self.canvas.create_rectangle(
            hell15_center[0] - 15, hell15_center[1] - 15,
            hell15_center[0] + 15, hell15_center[1] + 15,
            fill='black')

        hell1_center = origin + np.array([-UNIT+UNIT * 3, UNIT*2-2*UNIT])
        self.hell1 = self.canvas.create_rectangle(
            hell1_center[0] - 15, hell1_center[1] - 15,
            hell1_center[0] + 15, hell1_center[1] + 15,
            fill='black')
        hell2_center = origin + np.array([-UNIT+UNIT*4, UNIT*2-2*UNIT])
        self.hell2 = self.canvas.create_rectangle(
            hell2_center[0] - 15, hell2_center[1] - 15,
            hell2_center[0] + 15, hell2_center[1] + 15,
            fill='black')

        hell3_center = origin + np.array([-UNIT+UNIT * 5, UNIT*2-2*UNIT])
        self.hell3 = self.canvas.create_rectangle(
            hell3_center[0] - 15, hell3_center[1] - 15,
            hell3_center[0] + 15, hell3_center[1] + 15,
            fill='black')

        hell4_center = origin + np.array([-UNIT+UNIT * 6, UNIT*3-2*UNIT])
        self.hell4 = self.canvas.create_rectangle(
            hell4_center[0] - 15, hell4_center[1] - 15,
            hell4_center[0] + 15, hell4_center[1] + 15,
            fill='black')

        hell5_center = origin + np.array([-UNIT+UNIT * 2, UNIT*3-2*UNIT])
        self.hell5 = self.canvas.create_rectangle(
            hell5_center[0] - 15, hell5_center[1] - 15,
            hell5_center[0] + 15, hell5_center[1] + 15,
            fill='black')
        hell6_center = origin + np.array([-UNIT+UNIT * 2, UNIT*4-2*UNIT])
        self.hell6 = self.canvas.create_rectangle(
            hell6_center[0] - 15, hell6_center[1] - 15,
            hell6_center[0] + 15, hell6_center[1] + 15,
            fill='black')
        hell7_center = origin + np.array([-UNIT+UNIT * 3, UNIT*5-2*UNIT])
        self.hell7 = self.canvas.create_rectangle(
            hell7_center[0] - 15, hell7_center[1] - 15,
            hell7_center[0] + 15, hell7_center[1] + 15,
            fill='black')
        hell8_center = origin + np.array([-UNIT+UNIT * 4, UNIT*5-2*UNIT])
        self.hell8 = self.canvas.create_rectangle(
            hell8_center[0] - 15, hell8_center[1] - 15,
            hell8_center[0] + 15, hell8_center[1] + 15,
            fill='black')
        hell9_center = origin + np.array([-UNIT+UNIT * 5, UNIT*5-2*UNIT])
        self.hell9 = self.canvas.create_rectangle(
            hell9_center[0] - 15, hell9_center[1] - 15,
            hell9_center[0] + 15, hell9_center[1] + 15,
            fill='black')
        hell10_center = origin + np.array([-UNIT+UNIT * 6, UNIT*6-2*UNIT])
        self.hell10 = self.canvas.create_rectangle(
            hell10_center[0] - 15, hell10_center[1] - 15,
            hell10_center[0] + 15, hell10_center[1] + 15,
            fill='black')
        # 第二个为向下两格，向右一格
        hell11_center = origin + np.array([-UNIT+UNIT * 6, UNIT * 7-2*UNIT])
        self.hell11 = self.canvas.create_rectangle(
            hell11_center[0] - 15, hell11_center[1] - 15,
            hell11_center[0] + 15, hell11_center[1] + 15,
            fill='black')

        hell12_center = origin + np.array([-UNIT+UNIT *2, UNIT*7-2*UNIT])
        self.hell12 = self.canvas.create_rectangle(
            hell12_center[0] - 15, hell12_center[1] - 15,
            hell12_center[0] + 15, hell12_center[1] + 15,
            fill='black')
        hell13_center = origin + np.array([-UNIT+UNIT * 3, UNIT*8-2*UNIT])
        self.hell13 = self.canvas.create_rectangle(
            hell13_center[0] - 15, hell13_center[1] - 15,
            hell13_center[0] + 15, hell13_center[1] + 15,
            fill='black')
        hell14_center = origin + np.array([-UNIT+UNIT * 4, UNIT*8-2*UNIT])
        self.hell14 = self.canvas.create_rectangle(
            hell14_center[0] - 15, hell14_center[1] - 15,
            hell14_center[0] + 15, hell14_center[1] + 15,
            fill='black')
        hell15_center = origin + np.array([-UNIT+UNIT * 5, UNIT*8-2*UNIT])
        self.hell15 = self.canvas.create_rectangle(
            hell15_center[0] - 15, hell15_center[1] - 15,
            hell15_center[0] + 15, hell15_center[1] + 15,
            fill='black')

        hell16_center = origin + np.array([-UNIT+UNIT * 11, UNIT*2-2*UNIT])
        self.hell16 = self.canvas.create_rectangle(
            hell16_center[0] - 15, hell16_center[1] - 15,
            hell16_center[0] + 15, hell16_center[1] + 15,
            fill='black')
        hell17_center = origin + np.array([-UNIT+UNIT * 12, UNIT*2-2*UNIT])
        self.hell17 = self.canvas.create_rectangle(
            hell17_center[0] - 15, hell17_center[1] - 15,
            hell17_center[0] + 15, hell17_center[1] + 15,
            fill='black')
        hell18_center = origin + np.array([-UNIT+UNIT * 13, UNIT*2-2*UNIT])
        self.hell18 = self.canvas.create_rectangle(
            hell18_center[0] - 15, hell18_center[1] - 15,
            hell18_center[0] + 15, hell18_center[1] + 15,
            fill='black')
        hell19_center = origin + np.array([-UNIT+UNIT * 12, UNIT*3-2*UNIT])
        self.hell19 = self.canvas.create_rectangle(
            hell19_center[0] - 15, hell19_center[1] - 15,
            hell19_center[0] + 15, hell19_center[1] + 15,
            fill='black')
        hell20_center = origin + np.array([-UNIT+UNIT * 12, UNIT*4-2*UNIT])
        self.hell20 = self.canvas.create_rectangle(
            hell20_center[0] - 15, hell20_center[1] - 15,
            hell20_center[0] + 15, hell20_center[1] + 15,
            fill='black')
        # 第二个为向下两格，向右一格
        hell21_center = origin + np.array([-UNIT+UNIT * 12, UNIT * 5-2*UNIT])
        self.hell21 = self.canvas.create_rectangle(
            hell21_center[0] - 15, hell21_center[1] - 15,
            hell21_center[0] + 15, hell21_center[1] + 15,
            fill='black')

        hell22_center = origin + np.array([-UNIT+UNIT *12, UNIT*6-2*UNIT])
        self.hell22 = self.canvas.create_rectangle(
            hell22_center[0] - 15, hell22_center[1] - 15,
            hell22_center[0] + 15, hell22_center[1] + 15,
            fill='black')
        hell23_center = origin + np.array([-UNIT+UNIT * 12, UNIT*7-2*UNIT])
        self.hell23 = self.canvas.create_rectangle(
            hell23_center[0] - 15, hell23_center[1] - 15,
            hell23_center[0] + 15, hell23_center[1] + 15,
            fill='black')
        hell24_center = origin + np.array([-UNIT+UNIT * 11, UNIT*8-2*UNIT])
        self.hell24 = self.canvas.create_rectangle(
            hell24_center[0] - 15, hell24_center[1] - 15,
            hell24_center[0] + 15, hell24_center[1] + 15,
            fill='black')
        hell25_center = origin + np.array([-UNIT+UNIT * 10, UNIT*8-2*UNIT])
        self.hell25 = self.canvas.create_rectangle(
            hell25_center[0] - 15, hell25_center[1] - 15,
            hell25_center[0] + 15, hell25_center[1] + 15,
            fill='black')
        hell26_center = origin + np.array([-UNIT+UNIT * 9, UNIT*7-2*UNIT])
        self.hell26 = self.canvas.create_rectangle(
            hell26_center[0] - 15, hell26_center[1] - 15,
            hell26_center[0] + 15, hell26_center[1] + 15,
            fill='black')

        a1_center = origin + np.array([-UNIT+UNIT * 2, UNIT*10-2*UNIT])
        self.h1 = self.canvas.create_rectangle(
            a1_center[0] - 15, a1_center[1] - 15,
            a1_center[0] + 15, a1_center[1] + 15,
            fill='black')
        a2_center = origin + np.array([-UNIT+UNIT * 3, UNIT*10-2*UNIT])
        self.h2 = self.canvas.create_rectangle(
            a2_center[0] - 15, a2_center[1] - 15,
            a2_center[0] + 15, a2_center[1] + 15,
            fill='black')
        a3_center = origin + np.array([-UNIT+UNIT * 4, UNIT*10-2*UNIT])
        self.h3 = self.canvas.create_rectangle(
            a3_center[0] - 15, a3_center[1] - 15,
            a3_center[0] + 15, a3_center[1] + 15,
            fill='black')
        a4_center = origin + np.array([-UNIT+UNIT * 5, UNIT*10-2*UNIT])
        self.h4 = self.canvas.create_rectangle(
            a4_center[0] - 15, a4_center[1] - 15,
            a4_center[0] + 15, a4_center[1] + 15,
            fill='black')

        a5_center = origin + np.array([-UNIT+UNIT * 6, UNIT*10-2*UNIT])
        self.h5 = self.canvas.create_rectangle(
            a5_center[0] - 15, a5_center[1] - 15,
            a5_center[0] + 15, a5_center[1] + 15,
            fill='black')
        a6_center = origin + np.array([-UNIT+UNIT * 4, UNIT*11-2*UNIT])
        self.h6 = self.canvas.create_rectangle(
            a6_center[0] - 15, a6_center[1] - 15,
            a6_center[0] + 15, a6_center[1] + 15,
            fill='black')
        a7_center = origin + np.array([-UNIT+UNIT * 4, UNIT*12-2*UNIT])
        self.h7 = self.canvas.create_rectangle(
            a7_center[0] - 15, a7_center[1] - 15,
            a7_center[0] + 15, a7_center[1] + 15,
            fill='black')
        a8_center = origin + np.array([-UNIT+UNIT * 4, UNIT*13-2*UNIT])
        self.h8 = self.canvas.create_rectangle(
            a8_center[0] - 15, a8_center[1] - 15,
            a8_center[0] + 15, a8_center[1] + 15,
            fill='black')
        a9_center = origin + np.array([-UNIT+UNIT * 4, UNIT*14-2*UNIT])
        self.h9 = self.canvas.create_rectangle(
            a9_center[0] - 15, a9_center[1] - 15,
            a9_center[0] + 15, a9_center[1] + 15,
            fill='black')
        a10_center = origin + np.array([-UNIT+UNIT * 4, UNIT*15-2*UNIT])
        self.h10 = self.canvas.create_rectangle(
            a10_center[0] - 15, a10_center[1] - 15,
            a10_center[0] + 15, a10_center[1] + 15,
            fill='black')
        a11_center = origin + np.array([-UNIT+UNIT * 9, UNIT*10-2*UNIT])
        self.h11 = self.canvas.create_rectangle(
            a11_center[0] - 15, a11_center[1] - 15,
            a11_center[0] + 15, a11_center[1] + 15,
            fill='black')
        a12_center = origin + np.array([-UNIT+UNIT * 9, UNIT*11-2*UNIT])
        self.h12 = self.canvas.create_rectangle(
            a12_center[0] - 15, a12_center[1] - 15,
            a12_center[0] + 15, a12_center[1] + 15,
            fill='black')
        a13_center = origin + np.array([-UNIT+UNIT * 9, UNIT*12-2*UNIT])
        self.h13 = self.canvas.create_rectangle(
            a13_center[0] - 15, a13_center[1] - 15,
            a13_center[0] + 15, a13_center[1] + 15,
            fill='black')
        a14_center = origin + np.array([-UNIT+UNIT * 9, UNIT*13-2*UNIT])
        self.h14 = self.canvas.create_rectangle(
            a14_center[0] - 15, a14_center[1] - 15,
            a14_center[0] + 15, a14_center[1] + 15,
            fill='black')
        a15_center = origin + np.array([-UNIT+UNIT * 9, UNIT*14-2*UNIT])
        self.h15 = self.canvas.create_rectangle(
            a15_center[0] - 15, a15_center[1] - 15,
            a15_center[0] + 15, a15_center[1] + 15,
            fill='black')
        a16_center = origin + np.array([-UNIT+UNIT * 10, UNIT*15-2*UNIT])
        self.h16 = self.canvas.create_rectangle(
            a16_center[0] - 15, a16_center[1] - 15,
            a16_center[0] + 15, a16_center[1] + 15,
            fill='black')
        a17_center = origin + np.array([-UNIT+UNIT * 11, UNIT*15-2*UNIT])
        self.h17 = self.canvas.create_rectangle(
            a17_center[0] - 15, a17_center[1] - 15,
            a17_center[0] + 15, a17_center[1] + 15,
            fill='black')
        a18_center = origin + np.array([-UNIT+UNIT * 12, UNIT*15-2*UNIT])
        self.h18 = self.canvas.create_rectangle(
            a18_center[0] - 15, a18_center[1] - 15,
            a18_center[0] + 15, a18_center[1] + 15,
            fill='black')
        a19_center = origin + np.array([-UNIT+UNIT * 13, UNIT*14-2*UNIT])
        self.h19 = self.canvas.create_rectangle(
            a19_center[0] - 15, a19_center[1] - 15,
            a19_center[0] + 15, a19_center[1] + 15,
            fill='black')
        a20_center = origin + np.array([-UNIT+UNIT * 13, UNIT*13-2*UNIT])
        self.h20 = self.canvas.create_rectangle(
            a20_center[0] - 15, a20_center[1] - 15,
            a20_center[0] + 15, a20_center[1] + 15,
            fill='black')
        a21_center = origin + np.array([-UNIT+UNIT * 13, UNIT*12-2*UNIT])
        self.h21 = self.canvas.create_rectangle(
            a21_center[0] - 15, a21_center[1] - 15,
            a21_center[0] + 15, a21_center[1] + 15,
            fill='black')
        a22_center = origin + np.array([-UNIT+UNIT * 13, UNIT*11-2*UNIT])
        self.h22 = self.canvas.create_rectangle(
            a22_center[0] - 15, a22_center[1] - 15,
            a22_center[0] + 15, a22_center[1] + 15,
            fill='black')
        a23_center = origin + np.array([-UNIT+UNIT * 13, UNIT*10-2*UNIT])
        self.h23 = self.canvas.create_rectangle(
            a23_center[0] - 15, a23_center[1] - 15,
            a23_center[0] + 15, a23_center[1] + 15,
            fill='black')


        # 创建得分点  create oval
        # 向右两格向下一格
        oval_center = origin + np.array([UNIT * 13, UNIT*13])
        self.oval = self.canvas.create_oval(
            oval_center[0] - 15, oval_center[1] - 15,
            oval_center[0] + 15, oval_center[1] + 15,
            fill='yellow')

        # oval_center1 = origin + np.array([UNIT * 3, UNIT*9])
        # self.oval1 = self.canvas.create_oval(
        #     oval_center1[0] - 15, oval_center1[1] - 15,
        #     oval_center1[0] + 15, oval_center1[1] + 15,
        #     fill='yellow')
        #
        #
        # oval_center2 = origin + np.array([UNIT * 0, UNIT*6])
        # self.oval2 = self.canvas.create_oval(
        #     oval_center2[0] - 15, oval_center2[1] - 15,
        #     oval_center2[0] + 15, oval_center2[1] + 15,
        #     fill='yellow')
        # create red rect
        self.rect = self.canvas.create_rectangle(
            origin[0] - 15, origin[1] - 15,
            origin[0] + 15, origin[1] + 15,
            fill='red')

        # pack all
        self.canvas.pack()

    def reset(self):
        self.update()
        time.sleep(0.1)
        self.canvas.delete(self.rect)
        origin = np.array([20, 20])
        self.rect = self.canvas.create_rectangle(
            origin[0] - 15, origin[1] - 15,
            origin[0] + 15, origin[1] + 15,
            fill='red')
        # return observation

        return self.canvas.coords(self.rect)

    def step(self, action):
        # s为返回的当前rect在画布中的坐标
        s = self.canvas.coords(self.rect)
        base_action = np.array([0, 0])
        # action:up
        #如果上下方向大于一格 y移动减一格(向上为负)
        if action == '0up':
            if s[1] > UNIT:
                base_action[1] -= UNIT
        elif action == '1down':   # down
            if s[1] < (MAZE_H - 1) * UNIT:
                base_action[1] += UNIT
        elif action == '2right':   # right
            if s[0] < (MAZE_W - 1) * UNIT:
                base_action[0] += UNIT
        elif action == '3left':   # left
            if s[0] > UNIT:
                base_action[0] -= UNIT

        # 移动rect
        self.canvas.move(self.rect, base_action[0], base_action[1])  # move agent

        # 返回移动后的坐标
        s_ = self.canvas.coords(self.rect)  # next state

        # reward function
        # 如果移动后到了oval
        # done为episode标志变量，是否结束一轮游戏
        if s_ in [self.canvas.coords(self.oval)]:
            reward = 1
            # self.count += 1
            # if(self.count == 3):
            #     done = True
            #     self.count = 0
            done = True
            s_ = 'terminal'
        # 如果移动后到了hell
        elif s_ in [self.canvas.coords(self.hell1), self.canvas.coords(self.hell2),self.canvas.coords(self.hell3),
                    self.canvas.coords(self.hell4), self.canvas.coords(self.hell5),self.canvas.coords(self.hell6),
                    self.canvas.coords(self.hell7), self.canvas.coords(self.hell8),self.canvas.coords(self.hell9),
                    self.canvas.coords(self.hell10), self.canvas.coords(self.hell11),self.canvas.coords(self.hell12),
                    self.canvas.coords(self.hell13), self.canvas.coords(self.hell14),self.canvas.coords(self.hell15),
                    self.canvas.coords(self.hell16), self.canvas.coords(self.hell17),self.canvas.coords(self.hell18),
                    self.canvas.coords(self.hell19), self.canvas.coords(self.hell20),self.canvas.coords(self.hell21),
                    self.canvas.coords(self.hell22), self.canvas.coords(self.hell23),self.canvas.coords(self.hell24),
                    self.canvas.coords(self.hell25), self.canvas.coords(self.hell26),
                    self.canvas.coords(self.h1), self.canvas.coords(self.h2),self.canvas.coords(self.h3),
                    self.canvas.coords(self.h4), self.canvas.coords(self.h5),self.canvas.coords(self.h6),
                    self.canvas.coords(self.h7), self.canvas.coords(self.h8),self.canvas.coords(self.h9),
                    self.canvas.coords(self.h10), self.canvas.coords(self.h11),self.canvas.coords(self.h12),
                    self.canvas.coords(self.h13), self.canvas.coords(self.h14),self.canvas.coords(self.h15),
                    self.canvas.coords(self.h16), self.canvas.coords(self.h17),self.canvas.coords(self.h18),
                    self.canvas.coords(self.h19), self.canvas.coords(self.h20),self.canvas.coords(self.h21),
                    self.canvas.coords(self.h22), self.canvas.coords(self.h23)]:
            reward = -1
            done = True
            s_ = 'terminal'

        else:
            reward = 0
            done = False

        return s_, reward, done

    def render(self,index):
        time.sleep(index)
        self.update()


def update():
    for t in range(10):
        s = env.reset()
        while True:
            env.render()
            a = 1
            s, r, done = env.step(a)
            if done:
                break

# if __name__ == '__main__':
#     env = Maze()
#
#
#     env.after(100, update) #100ms调用update一次
#     env.mainloop()
