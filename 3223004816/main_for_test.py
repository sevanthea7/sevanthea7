import argparse
import similarity_functions
import tool_functions

def similarity_score(orig_path, copy_path):
    # 定义各个相似度指标的权重比例
    percent = {
        'lcs': 0.15,      # LCS
        'edit': 0.15,     # 编辑距离
        'j2': 0.1,        # Jaccard
        'simhash': 0.6    # simhash
    }

    # 处理原文
    orig_text = tool_functions.read_file(orig_path)
    orig_tokens = tool_functions.tokenize(orig_text)

    # 处理待检测文本
    copy_text = tool_functions.read_file(copy_path)
    copy_tokens = tool_functions.tokenize(copy_text)

    # 如果原文空，抛出异常
    if len(orig_tokens) == 0:
        raise ValueError("原文为空，无法计算重复率")
    # 如果待检测文本为空，也出异常
    if len(copy_tokens) == 0:
        raise ValueError("待检测文本为空，计算无效")

    # LSC计算
    lcs_len = similarity_functions.LCS(orig_tokens, copy_tokens)
    lcs_sim = lcs_len / len(orig_tokens)    # LCS相似度 = LCS长度 / 原文长度

    # 编辑距离计算
    ed = similarity_functions.edit_dist(orig_tokens, copy_tokens)
    ed_sim = 1 - ed / max(len(orig_tokens), len(copy_tokens), 1)    # 编辑距离相似度 = 1 - 编辑距离 / 最大文本长度或1（防止除以零）

    # Jaccard计算
    j2 = similarity_functions.jaccard2(orig_tokens, copy_tokens, 2)

    # Simhash计算
    simhash_sim = similarity_functions.simhash_res(orig_tokens, copy_tokens)

    # 加权计算最终相似度得分
    final_score = (percent['lcs'] * lcs_sim +
                   percent['edit'] * ed_sim +
                   percent['j2'] * j2 +
                   percent['simhash'] * simhash_sim) * 100

    result = {
        'lcs': lcs_sim,
        'edit': ed_sim,
        'j2': j2,
        'simhash': simhash_sim
    }

    return final_score, result


def main():
    for _ in range(500):
        similarity_score('test_files/orig.txt', 'test_files/copy.txt')

if __name__ == '__main__':
    import cProfile
    import pstats

    cProfile.run('main()', 'prof.out')

    p = pstats.Stats('prof.out')
    p.strip_dirs()
    p.sort_stats('cumulative')
    p.print_stats('3223004816')
