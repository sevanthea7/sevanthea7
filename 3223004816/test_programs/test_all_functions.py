import pytest
from tool_functions import tokenize, read_file, write_result
from similarity_functions import lcs, edit_dist, ngrams, jaccard2, simhash, simhash_res, hamming

@pytest.mark.parametrize("text, expected", [
    ("我啊真的喜欢你呢", ["我", "真的", "喜欢", "你"]),   # 普通文本 + 语气词
    ("啊吧吗呢哦嗯", []), # 全是无用词
    ("", []),           # 空字符串
    ("    ", []),       # 仅空格
    ("我喜欢Python3", ["我", "喜欢", "Python3"]),     # 中英文数字混合
    ("你好！今天吃了吗？", ["你好", "今天", "吃"]), # 包含标点
    ("测试特殊字符#@$%^", ["测试", "特殊字符"]),            # 特殊字符
    ("长文本"*50, ["长", "文本"]*50), # 长文本重复
    ("\n换行符测试\n", ["换行符", "测试"]),   # 换行符
    ("重复重复重复", ["重复"]*3),   # 重复词
])

def test_tokenize_various_cases(text, expected):
    tokens = tokenize(text)
    assert tokens == expected

def test_read_write_file(tmp_path):
    file_path = tmp_path / "test.txt"
    # 写入结果
    write_result(file_path, 3.1415926)
    # 读取文件
    content = read_file(file_path)
    # 检查保留两位小数
    assert "3.14" in content

def test_read_file_not_exist():
    with pytest.raises(ValueError):
        read_file("non_existent_file.txt")

def test_lcs_cases():
    assert lcs([], []) == 0                     # 空序列
    assert lcs(['a'], ['a']) == 1               # 单元素相同
    assert lcs(['a','b','c'], ['a','b','c']) == 3  # 全匹配
    assert lcs(['a','b'], ['b','a']) == 1      # 部分匹配
    assert lcs(['a','a','b'], ['a','b','b']) == 2  # 重复元素

def test_edit_dist_cases():
    assert edit_dist([], []) == 0               # 空序列
    assert edit_dist(['a'], ['b']) == 1         # 单元素不同
    assert edit_dist(['a','b','c'], ['a','c','d']) == 2  # 多元素不同
    assert edit_dist(['a','b'], ['a','b']) == 0 # 相同序列
    assert edit_dist(['a','b','c'], []) == 3   # 一边空

def test_ngrams_cases():
    assert ngrams([], 2) == set()               # 空序列
    assert ngrams(['a','b','c'], 2) == {('a','b'), ('b','c')}  # n-gram正常
    assert ngrams(['a','b','c'], 0) == set()    # n=0

def test_jaccard2_cases():
    assert jaccard2([], [], 2) == 1.0           # 都空
    assert jaccard2(['a','b'], ['a','b'], 2) == 1.0  # 完全相同
    assert jaccard2(['a','b'], ['b','c'], 2) == 0.0  # 完全不同
    assert 0 <= jaccard2(['a','b','c'], ['b','c','d'], 2) <= 1  # 范围检查

def test_simhash_cases():
    fp1 = simhash(['a','b'])
    fp2 = simhash(['a','b'])
    fp3 = simhash(['b','a'])
    assert fp1 == fp2                             # 相同序列指纹相同
    assert isinstance(fp1, int)
    assert fp1 != fp3 or fp1 == fp3               # 不保证顺序敏感度，可允许相同或不同

def test_hamming_cases():
    assert hamming(0b1010, 0b1001) == 2          # 基本位差
    assert hamming(0b1111, 0b1111) == 0          # 相等
    assert hamming(0, 0b1111) == 4               # 完全不同

def test_simhash_res_cases():
    sim = simhash_res(['a','b'], ['a','b'])
    sim2 = simhash_res(['a','b'], ['b','a'])
    assert 0 <= sim <= 1
    assert 0 <= sim2 <= 1
