"""
tool_functions.py
作者: wangyq
修改日期: 2025-09-16

功能:
提供中文文本的分词方法、文件读写与结果写入功能
"""

import jieba
import re
# 停用词（常见语气词）
USELESS_WORDS = {"的", "了", "啊", "吧", "吗", "呢", "哦", "嗯"}

def tokenize(text):
    """
    对输入文本进行分词，并去掉无用词和标点符号。
    参数:
        text (str): 待分词的文本
    返回:
        list[str]: 过滤后的分词结果
    """
    if not text:
        return []
    text = text.strip()
    if not text:
        return []
    # 中文分词
    tokens = [t for t in jieba.cut(text) if t.strip()]
    # 过滤无意义词
    tokens = [t for t in tokens if t not in USELESS_WORDS]
    # 过滤标点符号
    filtered_tokens = []
    for t in tokens:
        # 去掉标点
        t = re.sub(r'[^\w\u4e00-\u9fff]', '', t)  # 保留中文、字母、数字
        if t:  # 非空才保留
            filtered_tokens.append(t)
    return filtered_tokens


def read_file(path):
    """
    读取指定路径的文本文件内容。
    参数:
        path (str): 文件路径
    返回:
        str: 文件内容
    异常:
        ValueError: 当文件不存在时抛出
    """
    try:
        with open(path, "r", encoding="utf-8") as file_handle:
            return file_handle.read()
    except FileNotFoundError as exc:
        raise ValueError(f"文件 {path} 不存在！") from exc


def write_result(path, value):
    """
    将结果写入指定路径的文件，保留两位小数。
    参数:
        path (str): 输出文件路径
        value (float): 需要写入的数值
    """
    with open(path, "w", encoding="utf-8") as file_handle:
        file_handle.write(f"{value:.2f}\n")
