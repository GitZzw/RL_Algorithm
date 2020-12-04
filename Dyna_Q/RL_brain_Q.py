"""
This part of code is the Q learning brain, which is a brain of the agent.
All decisions are made in here.
View more on my tutorial page: https://morvanzhou.github.io/tutorials/
"""

import numpy as np
import pandas as pd


class QLearningTableQ:
    def __init__(self, actions=['0','1','2','3'], learning_rate=0.1, reward_decay=0.9, e_greedy=0.9):
          # a list 此处为[0 1 2 3]
        #self.actions = actions
        self.actions = actions
        self.lr = learning_rate
        self.gamma = reward_decay
        self.epsilon = e_greedy
        ## 创建Q表为  0 1 2 3
        ## position1 ……………………
        ## position2 ……………………
        self.q_table = pd.DataFrame(columns=self.actions, dtype=np.float64)

    def choose_action(self, observation):
        ### observation为rect在canvas的位置，如[5.0, 125.0, 35.0, 155.0]
        self.check_state_exist(observation)
        # action selection
        if np.random.uniform() < self.epsilon:
            # choose best action
            state_action = self.q_table.loc[observation, :]
            # some actions may have the same value, randomly choose on in these actions
            action = np.random.choice(state_action[state_action == np.max(state_action)].index)
        else:
            # choose random action
            action = np.random.choice(self.actions)
        return action

    def learn(self, s, a, r, s_):
        self.check_state_exist(s_)
        ## 查询预测结果
        q_predict = self.q_table.loc[s, a]
        if s_ != 'terminal':
            ## 下个回合没结束  r为行动的reward
            q_target = r + self.gamma * self.q_table.loc[s_, :].max()  # next state is not terminal
        else:
            ## 下个回合结束
            q_target = r  # next state is terminal
        ## 更新Q表 +=更新
        self.q_table.loc[s, a] += self.lr * (q_target - q_predict)  # update

    def check_state_exist(self, state):
        if state not in self.q_table.index:
            # append new state to q table
                ## state为传入的rect当前位置如[5.0, 125.0, 35.0, 155.0]
            ### 初始化新的一行为全0000
            # temp_list=state[1:-1].split(',')
            # ycor = ((float(temp_list[1])+float(temp_list[3]))/2-20) % 40 + 1;
            # xcor = ((float(temp_list[0])+float(temp_list[2]))/2-20) % 40 + 1;
            self.q_table = self.q_table.append(
                pd.Series(
                    [0]*len(self.actions),
                    index=self.q_table.columns,
                    name=state,
                    #name = '({},{})'.format(int(xcor),int(ycor))
                )
            )

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
