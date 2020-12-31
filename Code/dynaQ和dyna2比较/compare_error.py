# Implementation of the following model based RL methods:
#   - DynaQ [1]
#   - Monte Carlo Tree Search [2]
#   - Temporal Difference Tree Search [3]
#   - Dyna2 [4]
# to be used with OpenAI Gym environments. Demonstrations are included with the
# following environments: GridWorld-v0.
#
# [1] - David Silver (2015), COMPM050/COMPGI13 Lecture 8, slide 27
# [2] - David Silver (2015), COMPM050/COMPGI13 Lecture 8, slide 36
# [3] - David Silver (2015), COMPM050/COMPGI13 Lecture 8, slide 51
# [4] - David Silver, Richard Sutton and Martin Muller (2012), page 29
#
# By Ricardo Dominguez Olmedo, Aug-2017

# Import necessary libraries and functions
import numpy as np
from util import Agent
from util import Featurize
from util import LinearVFA
from util import EGreedyPolicyTabular
from util import EGreedyPolicyVFA
from util import TableLookupModel

# Implementation of the model based integrated architecture DynaQ
class DynaQ(Agent):
    def __init__(self, env, policy, VFA, featurize, train_eps, planning, alpha,
        gamma = 1, horizon = 1000, verbosity = 0):
        # Inputs:
        #   -env: openAI gym environment object
        #   -policy: object containing a policy from which to sample actions
        #   -VFA: object containing the value function approximator
        #   -featurize: object which featurizes states
        #   -train_eps: numer of random episodes to generate experience to train
        #       the model initially
        #   -planning: number of planning steps
        #   -alpha: step size parameter
        #   -gamma: discount-rate parameter
        #   -horizon: finite horizon steps
        #   -verbosity: if TRUE, prints to screen additional information

        self.env = env
        self.policy = policy
        self.featurize = featurize
        self.VFA = VFA
        self.planning = planning
        self.alpha = alpha
        self.gamma = gamma
        self.horizon = horizon
        self.verbosity = verbosity

        self.nS = env.observation_space.n   # Number of states
        self.nA = env.action_space.n    # Number of actions
        self.policy.setNActions(self.nA)
        self.featurize.set_nSnA(self.nS, self.nA)
        self.featDim = featurize.featureStateAction(0,0).shape # Dimensions of the
                                                               # feature vector
        self.VFA.setUpWeights(self.featDim) # Initialize weights for the VFA

        self.model = TableLookupModel(self.nS, self.nA) # Initialize model as a
                                                        # Table Lookup Model
        # Initially prevent agent from learning
        self.learn = 0

        # Uncoment for previous random exploration in order to improve initial model
        self.trainModel(train_eps)

    def trainModel(self, train_eps):
        self.model_learn = 1  # Model will be learnt
        self.preventlearn()   # Value function will not be learnt
        self.runEpisodes(train_eps)
        self.model_learn = 0

    # Computes a single episode.
    # Returns the episode reward return.
    def episode(self):
        episodeReward = 0

        # Initialize S
        state = self.env.reset()

        # Repeat for each episode
        for t in range(self.horizon):
            # Take action A, observe R, S'
            state, reward, done = self.step(state)

            # Update the total episode return
            episodeReward += reward

            # Finish the loop if S' is a terminal state
            if done: break

        # Update the policy parameters if the agent is learning
        if self.learn: self.policy.episodeUpdate()

        return episodeReward

    def step(self, state):
        # Choose A from S using policy
        action = self.policy.getAction(self.VFA, self.featurize, state)

        # Take A, observe R and S'
        state_prime, reward, done, info = self.env.step(action)

        # Update model with new experience
        if self.learn or self.model_learn:
            experience = (state, action, reward, state_prime)
            self.model.addExperience(experience)

        # If the agent is learning, update the VFA weights using Q-learning
        if self.learn:
            # Update value function using Q learning update
            self.Qupdate(state, action, reward, state_prime)

            # Update value function by looking back at past experience
            for i in range(self.planning):
                # Sample random previously observed state and action
                s = self.model.sampleRandState()
                a = self.model.sampleRandAction(s)

                # Use to model to compute expected return and following state
                r = self.model.sampleReward(s, a)
                s_prime = self.model.sampleStatePrime(s, a)

                # Update value function using Q learning update
                self.Qupdate(s, a, r, s_prime)

        return state_prime, reward, done

    # Update value function using Q learning update
    def Qupdate(self, state, action, reward, state_prime):
        # Get greedy action
        action_star = self.policy.greedyAction(self.VFA, self.featurize, state_prime)

        # Compute the pertinent feature vectors
        features = self.featurize.featureStateAction(state, action)
        features_star = self.featurize.featureStateAction(state_prime, action_star)

        # Compute the value of the features via function approximation
        value = self.VFA.getValue(features)
        value_star = self.VFA.getValue(features_star)

        # Update the VFA weights
        delta_w = (self.alpha * (reward + self.gamma * value_star - value)
            * self.VFA.getGradient(features))
        self.VFA.updateWeightsDelta(delta_w)


class Dyna2(Agent):
    def __init__(self, env, policy, VFAshort, VFAlong, featurize, train_eps,
        planning, alpha, beta, gamma = 1, horizon = 100, verbosity = 0):
        # Inputs:
        #   -env: openAI gym environment object
        #   -policy: object containing a policy from which to sample actions
        #   -VFAshort: object containing the value function approximator for the
        #       short-term memory
        #   -VFAlong: object containing the value function approximator for the
        #       long-term memory
        #   -featurize: object which featurizes states
        #   -train_eps: numer of random episodes to generate experience to train
        #       the model initially
        #   -planning: number of planning steps
        #   -alpha: step size parameter for long term memory value function update
        #   -beta: step size parameter for short term memory value function update
        #   -lamda: trace discount paramater
        #   -gamma: reward discount-rate parameter
        #   -horizon: finite horizon steps
        #   -verbosity: if TRUE, prints to screen additional information

        self.env = env
        self.policy = policy
        self.VFAshort = VFAshort
        self.VFAlong = VFAlong
        self.featurize = featurize
        self.planning = planning
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma
        self.horizon = horizon
        self.verbosity = verbosity

        self.nS = env.observation_space.n   # Number of states
        self.nA = env.action_space.n    # Number of actions
        self.policy.setNActions(self.nA)
        self.featurize.set_nSnA(self.nS, self.nA)
        self.featDim = featurize.featureStateAction(0,0).shape # Dimensions of the
                                                               # feature vector
        self.VFAshort.setUpWeights(self.featDim) # Initialize weights for the VFA
                                                 # for short term memory
        self.VFAlong.setUpWeights(self.featDim) # Initialize weights for the VFA
                                                # for long term memory
        self.QVFA = LinearVFA() # Q(s,a) is approximated through Linear Value
                                # Function Approximation, with weights equal to
                                # the sum of the weights of the short and long
                                # term memory VFAs.
        self.updateQ() # Initialize QVFA

        # Initially prevent agent from learning
        self.learn = 0

        # Initialize model
        self.model = TableLookupModel(self.nS, self.nA) # Initialize model as a
                                                        # Table Lookup Model
        self.model_learn = 0

        # Uncoment for previous random exploration in order to improve initial model
        self.trainModel(train_eps)

    def trainModel(self, train_eps):
        self.model_learn = 1  # Model will be learnt
        self.preventlearn()   # Value function will not be learnt
        self.runEpisodes(train_eps)
        self.model_learn = 0

    def updateQ(self):
        weights_short = self.VFAshort.getWeights()
        weights_long = self.VFAlong.getWeights()
        Qweights = weights_long + weights_short # Assuming that both VFAs use the
                                                # same featurize function
        self.QVFA.setWeights(Qweights)

    # Computes a single episode.
    # Returns the episode reward return.
    def episode(self):
        episodeReward = 0

        # Clear short term memory
        self.VFAshort.setUpWeights(self.featDim) # Initialize weights for the VFA
                                                 # for short term memory

        state = self.env.reset() # Initialize S
        if self.learn:
            self.search(state) # Search in order to update short term memory
            self.updateQ() # Take into account previous search in Q VFA

        # Pick A
        action = self.policy.getAction(self.QVFA, self.featurize, state)

        # Repeat for each episode
        for t in range(self.horizon):
            # Take action A, observe R, S'
            state, action, reward, done = self.step(state, action)

            # Update the total episode return
            episodeReward += reward

            # Finish the loop if S' is a terminal state
            if done: break

        # Update the policy parameters if the agent is learning
        if self.learn: self.policy.episodeUpdate()

        return episodeReward

    def search(self, state):
        for ep in range(self.planning):
            s = state # Initialize S
            self.updateQ()
            a = self.policy.getAction(self.QVFA, self.featurize, s) # Pick A
            for k in range(self.horizon):
                s_prime = self.model.sampleStatePrime(s, a) # Get expected S'
                r = self.model.sampleReward(s, a) # Get expected R
                self.updateQ() # Update QVFA
                a_prime = self.policy.getAction(self.QVFA, self.featurize,
                    s_prime) # Pick A' using QVFA and S'
                self.TDupdateShort(s, a, r, s_prime, a_prime) # Update short-term
                                                              # memory weights
                if self.model.isTerminal(s_prime): break # Finish episode if S'
                                                         # is terminal
                s = s_prime
                a = a_prime

    def step(self, state, action):
        # Take A, observe R and S'
        state_prime, reward, done, info = self.env.step(action)

        # Update model with new experience
        if self.learn or self.model_learn:
            experience = (state, action, reward, state_prime)
            self.model.addExperience(experience)

        self.search(state_prime) # Search tree
        action_prime = self.policy.getAction(self.QVFA, self.featurize,
            state_prime) # Pick A'

        # Update long-term weights
        if self.learn:
            self.TDupdateLong(state, action, reward, state_prime, action_prime)

        return state_prime, action_prime, reward, done

    def getValueMemory(self, features):
        value_short = self.VFAshort.getValue(features) # Short term memory value
        value_long = self.VFAlong.getValue(features) # Long term memory value
        total_value = value_short + value_long # Memory value considered as sum
                                                # of short and long term memory
        return total_value

    def TDupdateShort(self, state, action, reward, state_prime, action_prime):
        # Compute the pertinent feature vectors
        features = self.featurize.featureStateAction(state, action)
        features_prime = self.featurize.featureStateAction(state_prime, action_prime)

        # Compute the value of the features via function approximation
        value = self.getValueMemory(features)
        value_prime = self.getValueMemory(features_prime)

        # Obtain delta weight
        delta_w = (self.beta * (reward + self.gamma * value_prime - value)
            * self.VFAshort.getGradient(features))
        self.VFAshort.updateWeightsDelta(delta_w)

    def TDupdateLong(self, state, action, reward, state_prime, action_prime):
        # Compute the pertinent feature vectors
        features = self.featurize.featureStateAction(state, action)
        features_prime = self.featurize.featureStateAction(state_prime, action_prime)

        # Compute the value of the features via function approximation
        value = self.VFAlong.getValue(features)
        value_prime = self.VFAlong.getValue(features_prime)

        # Obtain delta weight
        delta_w = (self.alpha * (reward + self.gamma * value_prime - value)
            * self.VFAlong.getGradient(features))
        self.VFAlong.updateWeightsDelta(delta_w)

# This function demonstrates how the above methods can be used with OpenAI gym
# environments, while also demonstrating the differences in performance between
# these methods.
def compareMethods():
    import gym
    import matplotlib.pyplot as plt
    import gym_gridworlds
    env = gym.make('Gridworld-v0')

    epsilon = 0.1
    policyVFA = EGreedyPolicyVFA(epsilon)
    policyTab = EGreedyPolicyTabular(epsilon)
    VFA = LinearVFA()
    feature = Featurize()
    init_train_model = 0 # No previous knowledge about model
    H = 20

    training_episodes = 200
    n_plot_points = 100
    eps_benchmark = 100

    # Initialize agents
    alpha1 = 0.4
    plan1 = 20
    agent1 = DynaQ(env, policyVFA, VFA, feature, init_train_model, plan1, alpha1,
        horizon = H)

    alpha4 = 0.4
    beta4 = 0.4
    plan4 = 20
    agent4 = Dyna2(env, policyVFA, LinearVFA(), VFA, feature, init_train_model,
        plan4, alpha4, beta4, horizon = H)
    agent4.model.addTerminalStates([0, 15])

    agents = [agent1, agent4]

    eps_per_point = int(training_episodes / n_plot_points)
    benchmark_data = np.zeros((4, n_plot_points))
    # Benchmark agents without training
    for agent_i in range(2): benchmark_data[agent_i][0] = agents[agent_i].benchmark(eps_benchmark)
    # Train and benchmark agents

    plt.figure(figsize=(10, 5))
    plt.ion()
    for point_i in range(1, n_plot_points):
        # for agent_i in range(2):
        #     print('Dyna ' + str(agent_i) + ', Episode ' + str((point_i+1)*eps_per_point))
        #     agents[agent_i].train(eps_per_point)
        #     benchmark_data[agent_i][point_i] = agents[agent_i].benchmark(eps_benchmark)

        print('DynaQ' + ', Episode ' + str((point_i+1)*eps_per_point))
        agents[0].train(eps_per_point)
        benchmark_data[0][point_i] = agents[0].benchmark(eps_benchmark)
        print('Dyna2' + ', Episode ' + str((point_i+1)*eps_per_point))
        agents[1].train(eps_per_point)
        benchmark_data[1][point_i] = agents[1].benchmark(eps_benchmark)


    # Plot results
    # plt.figure(figsize=(16, 10))
    # xaxis = [eps_per_point*(i+1) for i in range(n_plot_points)]
    # title1 = 'DynaQ'
    # title4 = 'Dyna2'
    # titles = [title1, title4]
    # for i in range(2):
    #     plt.subplot(221+i)
    #     plt.plot(xaxis, benchmark_data[i])
    #     plt.xlabel('Training episodes')
    #     plt.ylabel('Average reward per episode')
    #     plt.title(titles[i])
    # plt.show()
        # Plot results
        plt.clf()  # 清除之前画的图
        fig = plt.gcf()  # 获取当前图
        xaxis = [eps_per_point*(i+1) for i in range(n_plot_points)]
        title1 = 'DynaQ'
        title4 = 'Dyna2'
        titles = [title1, title4]
        for i in range(2):
            plt.subplot(121+i)
            plt.plot(xaxis, benchmark_data[i])
            plt.xlabel('Training episodes')
            plt.ylabel('Average reward per episode')
            plt.title(titles[i])
        plt.pause(0.001)  # 暂停一段时间，不然画的太快会卡住显示不出来
        plt.ioff()  # 关闭画图窗口Z
    plt.show()
compareMethods()
