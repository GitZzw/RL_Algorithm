"""
This part of code is the Dyna-Q learning brain, which is a brain of the agent.
All decisions and learning processes are made in here.
View more on my tutorial page: https://morvanzhou.github.io/tutorials/
"""

import numpy as np
import pandas as pd


class Learning:
    def __init__(self, actions, learning_rate=0.1, reward_decay=0.9, e_greedy=0.95):
        self.actions = actions  # a list
        self.lr = learning_rate
        self.gamma = reward_decay
        self.epsilon = e_greedy

        ## argmax type error
        self.q_table = pd.DataFrame(columns=self.actions).astype('float32')
        self.q_table2 = pd.DataFrame(columns=self.actions).astype('float32')


    def choose_action2(self, observation):
        self.check_state_exist2(observation)
        # action selection
        if np.random.uniform() < self.epsilon:
            # choose best action
            # state_action = self.q_table.ix[observation, :]
            state_action = self.q_table2.loc[observation, :]             # for label indexing
            state_action = state_action.reindex(np.random.permutation(state_action.index))     # some actions have same value
            action = state_action.argmax()
        else:
            # choose random action
            action = np.random.choice(self.actions)
        return action


    def check_state_exist2(self, state):
        if state not in self.q_table2.index:
            # append new state to q table
            self.q_table2 = self.q_table2.append(
                pd.Series(
                    [0]*len(self.actions),
                    index=self.q_table2.columns,
                    name=state,
                )
            )

    def choose_action(self, observation):
        self.check_state_exist(observation)
        # action selection
        if np.random.uniform() < self.epsilon:
            # choose best action


            # state_action = self.q_table.ix[observation, :]
            state_action = self.q_table.loc[observation, :]             # for label indexing
            state_action = state_action.reindex(np.random.permutation(state_action.index))     # some actions have same value
            action = state_action.argmax()


        else:
            # choose random action
            action = np.random.choice(self.actions)
        return action

    def learn2(self, s, a, r, s_):
        self.check_state_exist2(s_)

        q_predict = self.q_table2.loc[s, a]
        if s_ != 'terminal':
            q_target = r + self.gamma * self.q_table2.loc[s_, :].max()  # next state is not terminal
        else:
            q_target = r  # next state is terminal
        self.q_table2.loc[s, a] += self.lr * (q_target - q_predict)  # update



    def learn(self, s, a, r, s_):
        self.check_state_exist(s_)

        q_predict = self.q_table.loc[s, a]
        if s_ != 'terminal':
            q_target = r + self.gamma * self.q_table.loc[s_, :].max()  # next state is not terminal
        else:
            q_target = r  # next state is terminal
        self.q_table.loc[s, a] += self.lr * (q_target - q_predict)  # update

    def check_state_exist(self, state):
        if state not in self.q_table.index:
            # append new state to q table
            self.q_table = self.q_table.append(
                pd.Series(
                    [0]*len(self.actions),
                    index=self.q_table.columns,
                    name=state,
                )
            )


class EnvModel:
    """Similar to the memory buffer in DQN, you can store past experiences in here.
    Alternatively, the model can generate next state and reward signal accurately."""
    def __init__(self, actions):
        # the simplest case is to think about the model is a memory which has all past transition information
        self.actions = actions
        self.database = pd.DataFrame(columns=actions, dtype=np.object)

    def store_transition(self, s, a, r, s_):
        if s not in self.database.index:
            self.database = self.database.append(
                pd.Series(
                    [None] * len(self.actions),
                    index=self.database.columns,
                    name=s,
                ))
        ### database的列label是动作a，行label是出现过的状态坐标s,每个值为在s处执行a的回报和新的状态s,类似于下面所示
        """                              0                               1                                2                              3
[5.0, 5.0, 35.0, 35.0]       (0, [5.0, 5.0, 35.0, 35.0])    (0, [5.0, 45.0, 35.0, 75.0])     (0, [45.0, 5.0, 75.0, 35.0])    (0, [5.0, 5.0, 35.0, 35.0])
[45.0, 5.0, 75.0, 35.0]                             None                            None                             None    (0, [5.0, 5.0, 35.0, 35.0])
[5.0, 45.0, 35.0, 75.0]      (0, [5.0, 5.0, 35.0, 35.0])   (0, [5.0, 85.0, 35.0, 115.0])                             None   (0, [5.0, 45.0, 35.0, 75.0])
[5.0, 85.0, 35.0, 115.0]                            None  (0, [5.0, 125.0, 35.0, 155.0])  (-1, [45.0, 85.0, 75.0, 115.0])  (0, [5.0, 85.0, 35.0, 115.0])
[5.0, 125.0, 35.0, 155.0]  (0, [5.0, 85.0, 35.0, 115.0])  (0, [5.0, 125.0, 35.0, 155.0])                             None                           None
"""
        self.database.set_value(s, a, (r, s_))


### sample随机选取一个database里出现过的位置s和动作a(非none)
### 返回s和a
### 如选取第一行第一列为(0, [5.0, 5.0, 35.0, 35.0])，返回s=[5.0, 5.0, 35.0, 35.0] ，a=0
    def sample_s_a(self):
        s = np.random.choice(self.database.index)
        a = np.random.choice(self.database.loc[s].dropna().index)    # filter out the None value
        return s, a

### get_rs获得之前随机选取s和a对应的值如(0, [5.0, 5.0, 35.0, 35.0]) ,返回r=0，s_=[5.0, 5.0, 35.0, 35.0]
### 然后重新用该值更新Q表，相当于加深印象
    def get_r_s_(self, s, a):
        r, s_ = self.database.loc[s, a]
        return r, s_
