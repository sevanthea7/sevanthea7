from typing import List
import hashlib

# LCS算法，通过DP动态规划实现，计算两个token序列的最长公共子序列长度
def LCS( a, b ):
    if not a or not b:          # 如果任意一个序列为空，LCS长度为0
        return 0
    m, n = len(a), len(b)       # 获取序列长度
    prev = [0] * (n + 1)        # 初始化上一行动态规划数组，长度n+1用于处理空前缀
    for i in range(1, m + 1):
        cur = [0] * (n + 1)     # 当前行动态规划数组
        ai = a[i - 1]           # 当前a序列的元素
        for j in range(1, n + 1):
            if ai == b[j - 1]:  # 元素相同，则LCS长度加1
                cur[j] = prev[j - 1] + 1
            else:               # 否则取左或上方的最大值
                cur[j] = max(prev[j], cur[j - 1])
        prev = cur              # 当前行变成上一行，用于下一轮迭代
    return prev[n]              # 返回整个LCS长度


# 编辑距离算法，通过DP动态规划实现
def edit_dist( a, b ):
    m, n = len(a), len(b)                       # 获取序列长度
    dp = [[0] * (n + 1) for _ in range(m + 1)]  # 初始化动态规划矩阵 (m+1)*(n+1)
    # 初始化第一列，删除操作次数
    for i in range(m + 1):
        dp[i][0] = i
    # 初始化第一行，插入操作次数
    for j in range(n + 1):
        dp[0][j] = j

    # DP
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if a[i - 1] == b[j - 1]:    # 相等则不增加成本，否则替换成本为1
                cost = 0
            else:
                cost = 1
            # 对三种操作取最小值：删除、插入、替换
            dp[i][j] = min(dp[i - 1][j] + 1,  # 删除
                           dp[i][j - 1] + 1,  # 插入
                           dp[i - 1][j - 1] + cost)  # 替换
    return dp[m][n]  # 返回编辑距离

# Jaccard
# 生成tokens的n-gram集合
def ngrams( tokens, n ):
    # 如果n>0，生成长度为n的连续子序列
    if n <= 0:
        return set()

    ngram_set = set()
    for i in range(len(tokens) - n + 1):
        ngram = tuple(tokens[i:i + n])  # 取连续n个token组成一个tuple
        ngram_set.add(ngram)

    return ngram_set

def jaccard2( a, b, n = 2 ):
    A = ngrams(a, n)  # a的n-gram集合
    B = ngrams(b, n)  # b的n-gram集合

    if not A and not B:  # 两个集合都为空，定义相似度为1
        return 1.0
    if not A or not B:   # 其中一个为空，定义相似度为0
        return 0.0
    return len(A & B) / len(A | B)  # 相似度 = 交集 / 并集

# SimHash算法
# 计算tokens序列的SimHash指纹
def simhash( tokens, hashbits = 64 ):
    v = [0] * hashbits          # 初始化权重向量
    for token in tokens:
        # 将token做MD5哈希并转为整数
        h = int( hashlib.md5( token.encode('utf-8') ).hexdigest(), 16 )
        for i in range(hashbits):
            bitmask = 1 << i    # 对应bit位置的掩码
            if h & bitmask:
                v[i] += 1       # 若该位为1，权重加1
            else:
                v[i] -= 1       # 若该位为0，权重减1

    fingerprint = 0
    for i in range(hashbits):
        if v[i] >= 0:           # 权重大于等于0则该位为1，否则为0
            fingerprint |= 1 << i
    return fingerprint          # 返回SimHash指纹

# 计算两个整数的海明距离，即二进制位不同的数量
def hamming( x, y ):
    return bin(x ^ y).count('1')  # 异或后统计1的个数

# 计算两个tokens序列的SimHash相似度
def simhash_res( orig_tokens, copy_tokens, hashbits = 64 ):
    simhash1 = simhash(orig_tokens, hashbits)   # 原文指纹
    simhash2 = simhash(copy_tokens, hashbits)   # 待测文本指纹
    distance = hamming( simhash1, simhash2 )    # 计算海明距离
    return (1 - distance / hashbits)              # 转换为相似度（1-海明距离/总位数）