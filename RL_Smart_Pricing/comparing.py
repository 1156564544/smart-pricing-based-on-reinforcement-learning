import numpy as np
import math
import random

import training

Total=training.Total
qfunc=training.load_qfunc()
policy=training.Q_learning(qfunc)

customers=np.random.poisson(15,20)

# using policy
reward=[]
for iter in range(100):
    inventory = int(Total * 1.0)
    start_day = 0
    price = 100
    current_reward=0.0
    for day in range(start_day, 20):
        action = policy["%d_%d_%d" % (day, math.ceil(20 * inventory / Total), (price - 81) // 10)]
        price = training.update_price(action, price)

        expected_price = np.random.normal(100, 15, customers[day])
        for i in range(len(expected_price)):
            if expected_price[i] >= price:
                if inventory > 0:
                    inventory = inventory - 1
                    current_reward += price
    reward.append(current_reward)
print("Total reward(using policy):",np.mean(reward))

# randomly pricing
reward=[]
for iter in range(100):
    inventory = int(Total * 1.0)
    start_day = 0
    current_reward=0.0
    for day in range(start_day, 20):
        price = random.randint(81, 130)

        expected_price = np.random.normal(100, 15, customers[day])
        for i in range(len(expected_price)):
            if expected_price[i] >= price:
                if inventory > 0:
                    inventory = inventory - 1
                    current_reward += price
    reward.append(current_reward)
print("Total reward(randomly pricing):",np.mean(reward))

#price=100
reward=[]
for iter in range(100):
    current_reward = 0.0
    inventory = int(Total * 1.0)
    start_day = 0
    for day in range(start_day, 20):
        price = 100

        expected_price = np.random.normal(100, 15, customers[day])
        for i in range(len(expected_price)):
            if expected_price[i] >= price:
                if inventory > 0:
                    inventory = inventory - 1
                    current_reward += price
    reward.append(current_reward)
print("Total reward(price=100):",np.mean(reward))