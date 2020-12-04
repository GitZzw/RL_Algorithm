"""
Reinforcement learning maze example.
Red rectangle:          explorer.
Black rectangles:       hells       [reward = -1].
Yellow bin circle:      paradise    [reward = +1].
All other states:       ground      [reward = 0].
This script is the main part which controls the update method of this example.
The RL is in RL_brain.py.
View more on my tutorial page: https://morvanzhou.github.io/tutorials/
"""

from maze_env import Maze
from RL_brain import QLearningTable
import numpy as np
import pandas as pd


def update():
    for episode in range(1000):
        # initial observation
        observation = env.reset()

        while True:
            # fresh env
            if(episode>700):
                env.render(0.1)
            else:
                env.render(0.0001)


            # RL choose action based on observation
            action = RL.choose_action(str(observation))

            # RL take action and get next observation and reward
            ## 执行action得到新的位置 回报函数 结束标志
            observation_, reward, done = env.step(action)

            # RL learn from this transition
            RL.learn(str(observation), action, reward, str(observation_))

            # swap observation
            observation = observation_

            # break while loop when end of this episode
            if done:
                break

    # end of game
#    print(RL.q_table)
    new_table = pd.DataFrame(dtype=np.float64);

    for i in RL.q_table._stat_axis.values.tolist():
        temp_list=i[1:-1].split(',')
        if(len(temp_list)>=4):
            ycor = ((float(temp_list[1])+float(temp_list[3]))/2-20)/40+1
            xcor = ((float(temp_list[0])+float(temp_list[2]))/2-20)/40+1
            new_table = new_table.append(
                pd.Series(
                    RL.q_table.loc[i,:],
                    index= RL.q_table.columns,
                    name = '({},{})'.format(int(xcor),int(ycor)),
                )
        )
    print(new_table)
    print('game over')
    env.destroy()

if __name__ == "__main__":
    env = Maze()
    RL = QLearningTable()
    #100ms调用update一次
    env.after(1, update)
    env.mainloop()
