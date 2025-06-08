import sympy
import random
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter
import math

def logistic(x,n,a):
    if a <= 3.57 or a >= 4:
        raise ValueError("Parameter 'a' must be in the certain range")
    for i in range(n):
        y=a*x*(1-x)
        x=y
    return x

def singer(x,n,a):
    if a < 0.9 or a > 1.08:
        raise ValueError("Parameter 'a' must be in the certain range")
    for i in range(n):
        y=a*(7.86*x-23.31*x**2+28.75*x**3-13.302875*x**4)
        x=y
    return y

def pwlcm(x,n,a):
    if a <= 0 or a >= 1:
        raise ValueError("Parameter 'a' must be in the certain range")
    for i in range(n):
        if x < a:
            y=x/a
        else:
            y=(1-a)*(1-x)
        x=y
    return y

def create_table(func, x0, n, a, N):
    if func not in [logistic, singer, pwlcm]:
        raise ValueError("Function must be one of the defined functions: logistic, singer, PWLCM")
    if a is None:
        raise ValueError("Parameter 'a' must be provided")
    seq = []
    x = x0
    for i in range(N):
        x = func(x, n, a)
        seq.append(x)
    idx = np.argsort(seq)
    return idx

def analyze_cycles(perm):
    n = len(perm)
    visited = [False] * n
    cycle_lengths = []
    for i in range(n):
        if not visited[i]:
            cnt = 0
            j = i
            while not visited[j]:
                visited[j] = True
                j = perm[j]
                cnt += 1
            if cnt > 0:
                cycle_lengths.append(cnt)
    # 统计每种长度的循环圈数量
    
    length_count = Counter(cycle_lengths)
    # 阶为所有循环长度的lcm
    order = 1
    for l in cycle_lengths:
        order = math.lcm(order, l)
    return length_count, order

def average_order_vs_N(func, a, n, N_list, seeds_per_N):
    avg_orders = []
    for N in N_list:
        orders = []
        for seed in range(seeds_per_N):
            random.seed(seed)
            np.random.seed(seed)
            x0 = random.random()
            perm = create_table(func, x0, n, a, N)
            _, order = analyze_cycles(perm)
            orders.append(order)
        avg_orders.append(np.mean(orders))
    return avg_orders

def main():
    print("请选择功能：")
    print("1. 生成置乱表")
    print("2. 计算平均阶并绘制平均阶-N曲线")
    choice = input("请输入功能编号（1或2）：").strip()
    func = input("Enter the function name (logistic, singer, PWLCM): ").strip().lower()
    n = int(input("Enter the number of iterations (n): "))
    if func == "logistic":
        a = float(input("Enter the parameter 'a' (must be in range (3.57, 4)): "))
        func = logistic
    elif func == "singer":
        a = float(input("Enter the parameter 'a' (must be in range (0.9, 1.08)): "))
        func = singer
    elif func == "pwclm":
        a = float(input("Enter the parameter 'a' (must be in range (0, 1)): "))
        func = pwlcm
    else:
        raise ValueError("Invalid function name. Must be one of: logistic, singer, PWLCM.")
    if choice == "1":
        N = int(input("请输入置乱表长度N："))
        x0 = random.random()
        table = create_table(func, x0, n, a, N)
        print("生成的置乱表：")
        print(table)
        print("置乱表的循环圈分析：")
        length_count, order = analyze_cycles(table)
        print("循环圈长度统计：", length_count)
        print("置乱表的阶：", order)
    elif choice == "2":
        N_list = list(range(10, 31, 1))
        seeds_per_N = 100
        avg_orders = average_order_vs_N(func, a, n, N_list, seeds_per_N)
        print("N值及对应平均阶：")
        for N, avg_order in zip(N_list, avg_orders):
            print(f"N={N}, 平均阶={avg_order:.2f}")
        plt.figure()
        plt.plot(N_list, avg_orders, marker='o')
        plt.xlabel('N')
        plt.ylabel('average order')
        plt.title('average order-N')
        plt.grid(True)
        plt.show()
        
    else:
        print("无效选择。")

if __name__ == "__main__":
    main()
