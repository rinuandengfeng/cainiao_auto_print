from pypinyin import pinyin, Style

# 定义一个汉字字符串
chinese_text = "kt"

# 使用 pinyin 方法将汉字转换为拼音，style 参数设置为 Style.FIRST_LETTER 表示获取首字母
pinyin_list = pinyin(chinese_text, style=Style.FIRST_LETTER)

# 将拼音列表转换为字符串
first_letters = ''.join(p[0] for p in pinyin_list)

