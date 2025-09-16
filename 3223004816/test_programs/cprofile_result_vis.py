import pstats
import matplotlib.pyplot as plt

# 全局设置字体为宋体
plt.rcParams['font.family'] = ['SimSun']
plt.rcParams['axes.unicode_minus'] = False

# 读取 cProfile 结果
p = pstats.Stats('prof2.out')
p.strip_dirs()
p.sort_stats('cumulative')

funcs = []
times = []

# 遍历函数
for func, stat in p.stats.items():
    filename, lineno, funcname = func
    if filename.endswith('similarity_functions.py') or filename.endswith('tool_functions.py') or filename.endswith('main_for_test.py'):
        funcs.append(funcname)
        avg_time_ms = (stat[3] / 500) * 1000  # 平均每次similarity_score调用耗时
        times.append(avg_time_ms)

if not funcs:
    print("没有匹配到函数，请检查文件名或路径")
else:
    # 按耗时从大到小排序
    funcs_times = sorted(zip(funcs, times), key=lambda x: x[1], reverse=True)
    funcs_sorted, times_sorted = zip(*funcs_times)

    plt.figure(figsize=(10,6))
    bars = plt.barh(funcs_sorted, times_sorted, color='skyblue')
    for i in range( len(funcs_sorted) ):
        print(funcs_sorted[i], times_sorted[i])

    # 显示条形上的数值
    for bar, time in zip(bars, times_sorted):
        plt.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height()/2,
                 f'{time:.2f} ms', va='center', fontsize=10)

    plt.xlabel('每次调用平均耗时 (毫秒)', fontsize=12)
    plt.ylabel('函数名称', fontsize=12)
    # plt.title('每次调用的函数平均执行时间', fontsize=14)

    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.show()
