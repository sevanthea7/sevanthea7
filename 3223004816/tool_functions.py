import jieba

useless_words = set( ["的","了","啊","吧","吗","呢","哦","嗯"] )
def tokenize( text ):
    text = text.strip()
    if not text:
        return []
    tokens = [t for t in jieba.cut(text) if t.strip()]          # 中文分词
    filtered = [t for t in tokens if t not in useless_words]    # 去掉语气词
    return filtered

# 文件IO
def read_file( path ):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        raise ValueError(f"文件{path}不存在！")


def write_result( path, value ):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(f"{value:.2f}\n")   # 保留两位小数
