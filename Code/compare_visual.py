"""
Simplest model-based RL, Dyna-Q.
Red rectangle:          explorer.
Black rectangles:       hells       [reward = -1].
Yellow bin circle:      paradise    [reward = +1].
All other states:       ground      [reward = 0].
This script is the main part which controls the update method of this example.
The RL is in RL_brain.py.
View more on my tutorial page: https://morvanzhou.github.io/tutorials/
"""

from env import Maze
from algorithm import Learning, EnvModel


def update():
    s = env.reset()
    s2 = env.reset2()
    for episode in range(1000):
        #print(RL.q_table)

        while True:
            env.render()
            a = RL.choose_action(str(s))
            a2 = RL.choose_action2(str(s2))
            s_, r, done = env.step(a)
            s2_,r2,done2 = env.step2(a2)
            RL.learn(str(s), a, r, str(s_))
            RL.learn2(str(s2), a2, r2, str(s2_))
            # use a model to output (r, s_) by inputting (s, a)
            # the model in dyna Q version is just like a memory replay buffer
            env_model.store_transition(str(s), a, r, s_)
            for n in range(10):     # learn 10 more times using the env_model
                ms, ma = env_model.sample_s_a()  # ms in here is a str
                mr, ms_ = env_model.get_r_s_(ms, ma)
                RL.learn(ms, ma, mr, str(ms_))

                # print(env_model.database)
                # print('################')
                # print(RL.q_table)
                # print('################')
            s = s_
            s2 = s2_
            if done:
                s = env.reset()
                break

            if done2:
                s2 = env.reset2()
                break

    # end of game
    print('game over')
    print(RL.q_table)
    env.destroy()


if __name__ == "__main__":
    env = Maze()
    env_model = EnvModel(actions=list(range(env.n_actions)))
    RL = Learning(actions=list(range(env.n_actions)))
    env.after(0, update)
    env.mainloop()
