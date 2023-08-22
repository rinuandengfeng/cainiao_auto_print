from pypinyin import pinyin, Style


def get_express_initial(express):
    """
    获取快递的首字母
    """
    if express == None:
        raise "快递公司不能为空！"
    pinyin_list = pinyin(express, style=Style.FIRST_LETTER)

    # 将拼音列表转换为字符串
    first_letters = ''.join(p[0] for p in pinyin_list)
    
    return first_letters.upper()