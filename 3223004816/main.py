"""
main.py
作者: wangyq
修改日期: 2025-09-16

功能:
该模块用于计算两个文本之间的相似度，支持 LCS、编辑距离、Jaccard、Simhash 等方法，最终会输出一个综合加权的重复率分数。
"""

import argparse
from similarity_functions import lcs, edit_dist, jaccard2, simhash_res
from tool_functions import tokenize, read_file, write_result


def similarity_score(orig_path, copy_path):
    """
    计算两个文件的相似度分数。
    参数:
        orig_path (str): 原文文件路径
        copy_path (str): 待检测文件路径
    返回:
        tuple: (final_score, result)
            - final_score (float): 最终加权相似度百分比
            - result (dict): 各个相似度指标的结果
    """
    # 定义各个相似度指标的权重比例
    percent = {
        'lcs': 0.15,        # LCS
        'edit': 0.15,       # 编辑距离
        'jaccard': 0.1,     # Jaccard
        'simhash': 0.6      # Simhash
    }

    # 读取原文并分词
    orig_text = read_file(orig_path)
    orig_tokens = tokenize(orig_text)

    # 读取待检测文本并分词
    copy_text = read_file(copy_path)
    copy_tokens = tokenize(copy_text)

    # 校验输入是否为空
    if len(orig_tokens) == 0:
        raise ValueError("原文为空，无法计算重复率")
    if len(copy_tokens) == 0:
        raise ValueError("待检测文本为空，计算无效")

    # LCS 计算
    lcs_len = lcs(orig_tokens, copy_tokens)
    lcs_sim = lcs_len / len(orig_tokens)

    # 编辑距离计算
    edit_distance_val = edit_dist(orig_tokens, copy_tokens)
    edit_distance_sim = 1 - edit_distance_val / max(
        len(orig_tokens), len(copy_tokens), 1
    )

    # Jaccard 计算
    jaccard_sim = jaccard2(orig_tokens, copy_tokens, 2)

    # Simhash 计算
    simhash_sim = simhash_res(orig_tokens, copy_tokens)

    # 加权计算最终相似度得分
    final_score = (
        percent['lcs'] * lcs_sim
        + percent['edit'] * edit_distance_sim
        + percent['jaccard'] * jaccard_sim
        + percent['simhash'] * simhash_sim
    ) * 100

    result = {
        'lcs': lcs_sim,
        'edit': edit_distance_sim,
        'jaccard': jaccard_sim,
        'simhash': simhash_sim
    }

    return final_score, result


def main():
    """
    主函数，解析命令行参数并计算相似度。
    """
    parser = argparse.ArgumentParser(description="计算两个文本文件的相似度")
    parser.add_argument('orig_path', help='原文文件路径')
    parser.add_argument('copy_path', help='待测试文件路径')
    parser.add_argument('output_path', help='输出结果文件路径')
    args = parser.parse_args()

    # 计算相似度
    score, _ = similarity_score(args.orig_path, args.copy_path)

    # 将最终得分写入输出文件
    write_result(args.output_path, score)

    print(f"重复率: {score:.2f} %")


if __name__ == '__main__':
    main()
