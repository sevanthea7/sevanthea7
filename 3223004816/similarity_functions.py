"""
similarity_functions.py
作者: wangyq
修改日期: 2025-09-16

功能: 提供多种文本相似度计算方法，包括：最长公共子序列 (LCS)、编辑距离 (Edit Distance)、Jaccard 相似度、SimHash 与海明距离。
"""
import hashlib
import numpy as np

def lcs(a, b):
    """
    通过动态规划计算两个序列的最长公共子序列长度（LCS）。
    参数:
        a (list[str]): 序列 A
        b (list[str]): 序列 B
    返回:
        int: LCS 的长度
    """
    if not isinstance(a, list) or not isinstance(b, list):
        raise TypeError("输入必须为列表")
    if not all(isinstance(x, str) for x in a + b):
        raise TypeError("列表元素必须为字符串")
    if not a or not b:
        return 0  # 空序列直接返回0
    if not a or not b:  # 如果任意序列为空，LCS 长度为 0
        return 0

    m, n = len(a), len(b)

    # 仅保留两行 DP，prev 为上一行，cur 为当前行
    prev = [0] * (n + 1)
    cur = [0] * (n + 1)

    for i in range(1, m + 1):
        ai = a[i - 1]  # 当前 a 序列的元素
        for j in range(1, n + 1):
            if ai == b[j - 1]:  # 元素相同，LCS 长度加 1
                cur[j] = prev[j - 1] + 1
            else:  # 否则取左或上方的最大值
                cur[j] = max(prev[j], cur[j - 1])
        # 当前行更新为上一行，供下一轮使用
        prev, cur = cur, prev  # 交换引用，避免复制

    return prev[n]  # 返回 LCS 长度


def edit_dist(a, b):
    """
    通过动态规划计算两个序列的编辑距离。
    参数:
        a (list[str]): 序列 A
        b (list[str]): 序列 B
    返回:
        int: 编辑距离
    """
    if not isinstance(a, list) or not isinstance(b, list):
        raise TypeError("输入必须为列表")
    if not all(isinstance(x, str) for x in a + b):
        raise TypeError("列表元素必须为字符串")
    m, n = len(a), len(b)

    # 仅保留两行 DP，prev 为上一行，cur 为当前行
    prev = list(range(n + 1))
    cur = [0] * (n + 1)

    for i in range(1, m + 1):
        cur[0] = i  # 当前行第 0 列初始化为删除操作次数
        for j in range(1, n + 1):
            cost = 0 if a[i - 1] == b[j - 1] else 1  # 相等不增加成本，不等替换成本为 1
            # 当前单元格取三种操作的最小值：删除、插入、替换
            cur[j] = min(
                prev[j] + 1,  # 删除
                cur[j - 1] + 1,  # 插入
                prev[j - 1] + cost  # 替换
            )
        prev, cur = cur, prev  # 交换引用，下一轮使用上一行

    return prev[n]  # 返回编辑距离


def ngrams( tokens, n ):
    """
    生成指定序列的 n-gram 集合。
    参数:
        tokens (list[str]): 输入序列
        n (int): n-gram 的长度
    返回:
        set[tuple]: n-gram 集合
    """
    if not isinstance(tokens, list):
        raise TypeError("tokens 必须为列表")
    if not isinstance(n, int):
        raise TypeError("n 必须为整数")
    if n <= 0:
        raise ValueError("n-gram 长度必须大于0")
    if n <= 0:
        return set()

    ngram_set = set()
    for i in range(len(tokens) - n + 1):
        ngram = tuple(tokens[i:i + n])  # 取连续n个token组成一个tuple
        ngram_set.add(ngram)

    return ngram_set

def jaccard2( a, b, n = 2 ):
    """
    计算两个序列的 Jaccard 相似度（基于 n-gram）。
    参数:
        a (list[str]): 序列 A
        b (list[str]): 序列 B
        n (int): n-gram 的长度，默认 2
    返回:
        float: Jaccard 相似度
    """
    if not isinstance(n, int):
        raise TypeError("n 必须为整数")
    ngrams_a = ngrams(a, n)
    ngrams_b = ngrams(b, n)

    if not ngrams_a and not ngrams_b:   # 两个集合都为空，定义相似度为1
        return 1.0
    if not ngrams_a or not ngrams_b:    # 其中一个为空，定义相似度为0
        return 0.0
    return len(ngrams_a & ngrams_b) / len(ngrams_a | ngrams_b)  # 相似度 = 交集 / 并集


def simhash( tokens, hashbits = 64 ):
    """
   计算序列的 SimHash 指纹。
   参数:
       tokens (list[str]): 输入序列
       hashbits (int): 指纹长度（默认 64 位）
   返回:
       int: SimHash 指纹
   """
    if not isinstance(tokens, list):
        raise TypeError("tokens 必须为列表")
    if not all(isinstance(x, str) for x in tokens):
        raise TypeError("tokens 中所有元素必须为字符串")
    if hashbits <= 0:
        raise ValueError("hashbits 必须大于0")
    v = np.zeros(hashbits, dtype=int)  # 初始化权重向量（numpy数组，便于向量化）

    for token in tokens:
        # 将 token 做 MD5 哈希并转换为整数
        h = int(hashlib.md5(token.encode("utf-8")).hexdigest(), 16)
        # 将整数转换为二进制数组 0/1，长度为 hashbits
        bits = np.array([(h >> i) & 1 for i in range(hashbits)], dtype=int)
        # 更新权重向量：1 -> +1, 0 -> -1
        v += np.where(bits == 1, 1, -1)

    # 根据权重向量生成最终指纹：权重大于等于0为1，否则为0
    fingerprint = 0
    for i in range(hashbits):
        if v[i] >= 0:
            fingerprint |= 1 << i
    return fingerprint

# 计算两个整数的海明距离，即二进制位不同的数量
def hamming( x, y ):
    """
    计算两个整数的海明距离。
    参数:
        x (int): 整数 X
        y (int): 整数 Y
    返回:
        int: 海明距离（两个数二进制表示中不同位的数量）
    """
    if not isinstance(x, int) or not isinstance(y, int):
        raise TypeError("hamming 输入必须为整数")
    return bin(x ^ y).count('1')  # 异或后统计1的个数


def simhash_res( orig_tokens, copy_tokens, hashbits = 64 ):
    """
    计算两个序列的 SimHash 相似度。
    参数:
        orig_tokens (list[str]): 原文分词序列
        copy_tokens (list[str]): 待测文本分词序列
        hashbits (int): SimHash 指纹位数，默认 64
    返回:
        float: 相似度，取值范围 [0,1]
    """
    if not isinstance(hashbits, int) or hashbits <= 0:
        raise ValueError("hashbits 必须为正整数")
    simhash1 = simhash(orig_tokens, hashbits)   # 原文指纹
    simhash2 = simhash(copy_tokens, hashbits)   # 待测文本指纹
    distance = hamming( simhash1, simhash2 )    # 计算海明距离
    return 1 - distance / hashbits              # 转换为相似度（1-海明距离/总位数）
