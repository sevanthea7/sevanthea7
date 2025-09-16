import matplotlib.pyplot as plt
import numpy as np
plt.rcParams['font.family'] = ['SimSun']
plt.rcParams['axes.unicode_minus'] = False

def visualize_performance(before_times, after_times, labels):
    """
    可视化函数耗时对比（优化前 vs 优化后）。
    参数:
        before_times (list[float]): 优化前耗时
        after_times (list[float]): 优化后耗时
        labels (list[str]): 函数名称
    """
    x = np.arange(len(labels))
    width = 0.35  # 条形宽度

    fig, ax = plt.subplots(figsize=(12, 6))
    rects1 = ax.bar(x - width / 2, before_times, width, label='优化前', color='tomato')
    rects2 = ax.bar(x + width / 2, after_times, width, label='优化后', color='seagreen')

    # 添加文字标签
    for rects in [rects1, rects2]:
        for rect in rects:
            height = rect.get_height()
            ax.annotate(f'{height:.2f}',
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=8)

    ax.set_ylabel('耗时 (秒)')
    # ax.set_title('各函数优化前后耗时对比')
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=45)
    ax.legend()
    ax.grid(axis='y', linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.show()
labels = ['main', 'similarity_score', 'edit_dist', 'lcs', 'tokenize',
          'simhash_res', 'simhash', 'read_file', 'jaccard2', 'ngrams', 'hamming']

before_times = [34.3436976, 34.330135, 12.6729408, 8.8428592, 6.3741328,
                4.8641088, 4.839478, 1.1482112, 0.309857, 0.2579306, 0.0153954]

after_times = [17.4164386, 17.4082462, 5.6605362, 4.374025, 3.5220806,
               3.113066, 3.101691, 0.5643334, 0.1421218, 0.1152188, 0.00778]

visualize_performance(before_times, after_times, labels)
