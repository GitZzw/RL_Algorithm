"""
This part of code is the Q learning brain, which is a brain of the agent.
All decisions are made in here.
View more on my tutorial page: https://morvanzhou.github.io/tutorials/
"""

import numpy as np
import pandas as pd


class QLearningTable:
    def __init__(self, actions=['0up','1down','2right','3left'], learning_rate=0.01, reward_decay=0.9, e_greedy=0.9):
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
