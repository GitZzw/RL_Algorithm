import gym
id = "SkullAndTreasure-v0" # 设置环境id

env = gym.make(id) # 构建环境对象

env.reset() # 重置环境

env.render() # 绘制环境

Input("press any key to continue...")

env.close() # 关闭环境
