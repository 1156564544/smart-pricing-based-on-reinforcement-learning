import numpy as np
import random
import math
import tqdm
import pickle
import os

actions = ["plus", "decrease", "unchanged"]
Total=200

# load qfunc from 'my.pickl.pkl'
def load_qfunc():
    if not os.path.exists('my_pickle.pkl') or not os.path.getsize('my_pickle.pkl') :
        pickle_file = open('my_pickle.pkl', "wb")
        qfunc = dict()
        for i in range(21):
            for j in range(21):
                for k in range(5):
                    for action in actions:
                        qfunc["%d_%d_%d_%s" % (i, j, k, action)] = random.random() * 100
                        if i == 20 or j == 0:
                            qfunc["%d_%d_%d_%s" % (i, j, k, action)] = 0.0
    else:
        pickle_file = open('my_pickle.pkl', "rb")
        qfunc = pickle.load(pickle_file)
    pickle_file.close()

    return qfunc

def epsilon_greedy(qfunc,day,price,inventory,epsilon):
    # find the maximum action
    amax=0
    ratio=math.ceil(20*inventory/Total)
    qmax=qfunc["%d_%d_%d_%s"%(day,ratio,(price-81)//10,actions[0])]
    for i in range(len(actions)):
        q=qfunc["%d_%d_%d_%s"%(day,ratio,(price-81)//10,actions[i])]
        if qmax<q:
            qmax=q
            amax=i

    # probability part
    pro=[0.0 for i in range(len(actions))]
    pro[amax]+=1-epsilon
    for i in range(len(actions)):
        pro[i]+=epsilon/len(actions)

    # choose action and return
    r=random.random()
    s=0.0
    for i in range(len(actions)):
        s+=pro[i]
        if s>=r:
            return actions[i]
    return actions[len(actions)-1]

def update_price(action,price):
    if action=="plus":
        price=price*1.1
        if price>130:
            price=130
        return price

    if action=="decrease":
        price=price*0.9
        if price<81:
            price=81
        return price
    if action=="unchanged":
        return price

def Q_learning(qfunc,episodes=0):
    # learning parameters
    epsilon = 0.15
    alpha = 0.05

    # start learning
    for iter in tqdm.tqdm(range(episodes)):
        # initialize customers model
        customers = np.random.poisson(15, 20)

        # randomly initialize start state
        price = random.randint(81, 130)
        inventory = random.randint(0, Total)
        start_day = random.randint(0, 19)

        # episode
        for day in range(start_day, 20):
            ratio1 = math.ceil(20 * inventory / Total)
            action = epsilon_greedy(qfunc, day, price, inventory, epsilon)
            if ratio1 == 0:
                qfunc["%d_%d_%d_%s" % (day, ratio1, (price - 81) // 10, action)] = 0.0
                break
            old_price = price
            price = update_price(action, price)
            expected_price = np.random.normal(100, 15, customers[day])
            reward = 0.0
            for i in range(len(expected_price)):
                if expected_price[i] >= price:
                    if inventory > 0:
                        inventory = inventory - 1
                        reward += price
            ratio2 = math.ceil(20 * inventory / Total)
            qmax = qfunc["%d_%d_%d_%s" % (day + 1, ratio2, (price - 81) // 10, actions[0])]
            for i in range(len(actions)):
                if qmax < qfunc["%d_%d_%d_%s" % (day + 1, ratio2, (price - 81) // 10, actions[i])]:
                    qmax = qfunc["%d_%d_%d_%s" % (day + 1, ratio2, (price - 81) // 10, actions[i])]
            qfunc["%d_%d_%d_%s" % (day, ratio1, (old_price - 81) // 10, action)] += alpha * (
                        reward + qmax - qfunc["%d_%d_%d_%s" % (day, ratio1, (old_price - 81) // 10, action)])

    #dump qfunc to 'my_pickle.pkl'
    pickle_file = open('my_pickle.pkl', 'wb')
    pickle.dump(qfunc, pickle_file)
    pickle_file.close()

    # generate policy
    policy = dict()
    for i in range(20):
        for j in range(21):
            for l in range(5):
                qmax = qfunc["%d_%d_%d_%s" % (i, j, l, actions[0])]
                item = 0
                for k in range(len(actions)):
                    if qmax < qfunc["%d_%d_%d_%s" % (i, j, l, actions[k])]:
                        qmax = qfunc["%d_%d_%d_%s" % (i, j, l, actions[k])]
                        item = k
                policy["%d_%d_%d" % (i, j, l)] = actions[item]

    #return policy
    return policy

def output_qfunc(qfunc):
    # print qfunc
    for i in range(21):
        for j in range(21):
            for k in range(5):
                print("day:%d ratio:%d price:%d" % (i, j, k))
                for action in actions:
                    print(qfunc["%d_%d_%d_%s" % (i, j, k, action)], end=" ")
                print(" ")

def output_policy(qfunc):
    # generate policy
    policy = dict()
    for i in range(20):
        for j in range(21):
            for l in range(5):
                qmax = qfunc["%d_%d_%d_%s" % (i, j, l, actions[0])]
                item = 0
                for k in range(len(actions)):
                    if qmax < qfunc["%d_%d_%d_%s" % (i, j, l, actions[k])]:
                        qmax = qfunc["%d_%d_%d_%s" % (i, j, l, actions[k])]
                        item = k
                policy["%d_%d_%d" % (i, j, l)] = actions[item]

    # print policy
    for i in range(20):
        for j in range(21):
            print("day:%d,ratio:%d: " % (i, j * 5))
            for k in range(5):
                print(policy["%d_%d_%d" % (i, j, k)], end=" ")
            print("")


