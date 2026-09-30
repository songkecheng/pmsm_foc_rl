import gym_electric_motor as gem  # 导入 gym-electric-motor 仿真库，并用 gem 作为简短别名，后续通过 gem.make() 创建电机环境。

# 创建 PMSM（永磁同步电机）电流控制环境；环境 ID 指定连续动作空间（Cont）的电流控制（CC）任务。
# 未额外传入参数，因此使用该环境预设的电机、控制器和仿真配置。
env = gem.make("Cont-CC-PMSM-v0")  # 得到环境对象；之后用 reset() 初始化、用 step() 推进仿真。

# 开始一局仿真，并获取初始观测 observation 和附加信息字典 info。
# 新版 Gym/Gymnasium 的 reset() 返回值是 (observation, info) 这两个元素。
observation, info = env.reset()  # observation 通常包含电机状态和参考目标；info 用于提供额外诊断信息。

# 将观测拆成电机状态 state 与参考目标 reference，方便分别查看或交给控制算法使用。
state, reference = observation  # 此环境的观测结构为二元组；两项的具体维度由环境配置决定。

print("状态数量：", len(state))  # 打印状态向量的元素个数，可用于了解观测状态的维数。
print("参考目标：", reference)  # 打印当前控制目标，例如电流参考值。
print("动作空间：", env.action_space)  # 打印动作空间定义，查看动作的类型、范围和形状。

# 随机给出 5 个动作，演示如何与环境交互；随机动作只用于试运行，并非有效控制策略。
for step in range(5):  # 循环执行 5 次；step 从 0 开始计数。
    action = env.action_space.sample()  # 从环境允许的动作空间中随机采样一个动作。

    observation, reward, terminated, truncated, info = env.step(action)  # 执行动作并推进一步仿真，返回新观测、奖励、结束标志和附加信息。
    state, reference = observation  # 从本步的新观测中取出电机状态和参考目标。

    print(f"\n第 {step + 1} 步")  # 显示当前步数；加 1 是因为循环变量从 0 开始。
    print("动作（三相电压指令）：", action)  # 打印本步施加的动作；动作含义以该环境的动作空间定义为准。
    print("当前参考目标：", reference)  # 打印本步观测中的控制参考目标。
    print("奖励：", reward)  # 打印环境根据本步表现计算的奖励，可用于强化学习反馈。

    if terminated or truncated:  # 若任务自然结束（terminated）或达到时间/步数限制（truncated），就重置环境。
        observation, info = env.reset()  # 重新开始一局，获得新一局的初始观测和附加信息。

env.close()  # 关闭并释放环境占用的资源；仿真结束后调用。
