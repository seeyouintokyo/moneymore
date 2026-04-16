#!/usr/bin/env python3
"""
微信记账消息解析器 - AI增强版
支持：阿拉伯数字、中文数字、复杂表达
"""

import sys
import json
import re
from datetime import datetime

# 分类关键词映射
CATEGORY_KEYWORDS = {
    "餐饮": ["吃饭", "午餐", "晚餐", "早餐", "奶茶", "咖啡", "餐厅", "外卖", "食堂", "火锅", "烧烤", "聚餐", "火锅", "烤肉", "日料", "中餐", "西餐"],
    "交通": ["打车", "滴滴", "地铁", "公交", "车费", "加油", "停车", "高速", "高铁", "火车", "飞机", "机票", "出租车", "网约车"],
    "购物": ["买东西", "淘宝", "京东", "拼多多", "购物", "买衣服", "买鞋", "买包", "超市", "便利店", "买", "购物", "消费"],
    "娱乐": ["电影", "游戏", "KTV", "唱歌", "玩", "娱乐", "旅游", "旅行", "门票", "演出", "剧本杀", "密室"],
    "通讯": ["话费", "流量", "宽带", "手机费", "电话费", "网费", "套餐"],
    "居住": ["房租", "水电", "物业", "房贷", "租金", "住宿费", "酒店", "民宿", "电费", "水费", "燃气费"],
    "医疗": ["医院", "看病", "药", "医保", "体检", "诊所", "挂号", "医药费"],
}

# 收入关键词
INCOME_KEYWORDS = ["收入", "工资", "转账给我", "收到", "到账", "发钱", "奖金", "红包", "退款", "报销", "AA", "A", "人均", "平分"]

# 中文数字映射
CN_NUMBERS = {
    '零': 0, '一': 1, '二': 2, '两': 2, '三': 3, '四': 4, '五': 5,
    '六': 6, '七': 7, '八': 8, '九': 9, '十': 10, '百': 100,
    '千': 1000, '万': 10000, '亿': 100000000
}


def parse_chinese_number(text):
    """解析中文数字，如'八十多'->80, '一百五'->150"""
    if not text:
        return None
    
    # 清理文本
    text = text.replace('多', '').replace('左右', '').replace('大概', '').replace('差不多', '').replace('块', '').replace('元', '')
    
    # 纯阿拉伯数字
    if text.isdigit():
        return int(text)
    
    # 处理"几十"、"几百"
    if text.startswith('几'):
        unit = text[1] if len(text) > 1 else '十'
        if unit in CN_NUMBERS:
            return CN_NUMBERS[unit] * 5  # 取中间值
        return 50
    
    # 简单中文数字映射
    simple_map = {
        '一': 1, '二': 2, '两': 2, '三': 3, '四': 4, '五': 5,
        '六': 6, '七': 7, '八': 8, '九': 9, '十': 10,
        '十一': 11, '十二': 12, '十三': 13, '十四': 14, '十五': 15,
        '十六': 16, '十七': 17, '十八': 18, '十九': 19, '二十': 20,
        '二十一': 21, '二十二': 22, '二十三': 23, '二十四': 24, '二十五': 25,
        '二十六': 26, '二十七': 27, '二十八': 28, '二十九': 29, '三十': 30,
        '三十一': 31, '三十二': 32, '三十三': 33, '三十四': 34, '三十五': 35,
        '四十': 40, '五十': 50, '六十': 60, '七十': 70,
        '八十': 80, '九十': 90, '一百': 100, '两百': 200, '三百': 300,
        '一千': 1000, '两千': 2000, '一万': 10000
    }
    
    if text in simple_map:
        return simple_map[text]
    
    # 解析组合数字（如"一百五"、"八十"）
    result = 0
    temp = 0
    last_unit = 1
    
    for char in reversed(text):
        if char in CN_NUMBERS:
            num = CN_NUMBERS[char]
            if num >= 10:
                if temp == 0:
                    temp = 1
                result += temp * num
                temp = 0
                last_unit = num
            else:
                temp = temp * 10 + num if last_unit >= 10 else num
    
    result += temp
    return result if result > 0 else None


def extract_amount(text):
    """提取金额 - 支持阿拉伯数字和中文数字"""
    amount = None
    
    # 模式1: "花了XX元/块"、"消费XX"
    pattern1 = r'(?:花了|消费|支出|用了|人均|AA|a|A).*?(\d+(?:\.\d+)?)\s*(?:元|块|块钱)'
    match = re.search(pattern1, text)
    if match:
        amount = float(match.group(1))
    
    # 模式2: 直接数字+单位
    if amount is None:
        pattern2 = r'(\d+(?:\.\d+)?)\s*(?:元|块|块钱)'
        match = re.search(pattern2, text)
        if match:
            amount = float(match.group(1))
    
    # 模式3: 中文数字 + 单位
    if amount is None:
        # 匹配"八十多"、"一百五"、"两千"
        pattern3 = r'([零一二两三四五六七八九十百千万亿]+(?:多|左右|大概)?)\s*(?:元|块|块钱)'
        match = re.search(pattern3, text)
        if match:
            amount = parse_chinese_number(match.group(1))
    
    # 模式4: 纯数字
    if amount is None:
        numbers = re.findall(r'\d+(?:\.\d+)?', text)
        if numbers:
            amount = float(numbers[0])
    
    # 模式5: 中文数字（没有单位）
    if amount is None:
        pattern5 = r'([零一二两三四五六七八九十百千万亿]+(?:多|左右)?)'
        match = re.search(pattern5, text)
        if match:
            amount = parse_chinese_number(match.group(1))
    
    return amount


def detect_type(text):
    """检测类型：收入或支出"""
    text_lower = text.lower()
    
    # 收入关键词
    for keyword in ["收入", "工资", "收到", "到账", "发钱", "奖金", "红包", "退款", "报销"]:
        if keyword in text_lower:
            return "收入"
    
    # 特殊：AA制、人均，通常是支出
    if "AA" in text or "人均" in text or "A" in text:
        return "支出"
    
    return "支出"


def detect_category(text):
    """检测分类"""
    for category, keywords in CATEGORY_KEYWORDS.items():
        for keyword in keywords:
            if keyword in text:
                return category
    return "其他"


def is_accounting_message(text):
    """判断是否是记账消息"""
    # 必须有金额
    amount = extract_amount(text)
    if amount is None:
        return False
    
    # 排除纯问候
    greetings = ["你好", "您好", "哈喽", "在吗", "在不在", "在么", "嗨", "hello", "hi"]
    if text.strip() in greetings:
        return False
    
    # 排除纯数字（可能是验证码等）
    if text.strip().isdigit():
        return False
    
    return True


def extract_all_amounts(text):
    """提取所有金额，返回列表"""
    amounts = []
    
    # 阿拉伯数字 + 单位（元/块）
    pattern1 = r'(\d+(?:\.\d+)?)\s*(?:元|块|块钱)'
    matches = re.findall(pattern1, text)
    for m in matches:
        amounts.append(float(m))
    
    # 纯数字（没有单位的）
    if not amounts:
        numbers = re.findall(r'\d+(?:\.\d+)?', text)
        amounts = [float(n) for n in numbers]
    else:
        # 如果有带单位的，也看看有没有纯数字
        numbers = re.findall(r'(?<![\d])(\d+)(?![\d元块])', text)
        for n in numbers:
            val = float(n)
            if val not in amounts:
                amounts.append(val)
    
    # 中文数字
    if not amounts:
        pattern2 = r'([零一二两三四五六七八九十百千万亿]+(?:多|左右|大概)?)\s*(?:元|块|块钱)'
        matches = re.findall(pattern2, text)
        for m in matches:
            val = parse_chinese_number(m)
            if val:
                amounts.append(val)
    
    return amounts


def parse_accounting_message(text):
    """解析记账消息 - 支持多笔记录"""
    result = {
        "is_accounting": False,
        "type": None,
        "amount": None,
        "category": None,
        "note": text,
        "date": datetime.now().strftime("%Y-%m-%d"),
        "time": datetime.now().strftime("%H:%M"),
        "multi_records": [],  # 多笔记录
    }
    
    # 判断是否是记账消息
    if not is_accounting_message(text):
        return result
    
    # 提取所有金额
    amounts = extract_all_amounts(text)
    if not amounts:
        return result
    
    # 如果只找到一个金额，按原来的逻辑
    if len(amounts) == 1:
        result["is_accounting"] = True
        result["amount"] = amounts[0]
        result["type"] = detect_type(text)
        result["category"] = detect_category(text)
        return result
    
    # 如果找到多个金额，尝试拆分多笔
    result["is_accounting"] = True
    result["multi_records"] = []
    
    # 简单拆分：按逗号、顿号、分号、"和"、"以及"分割
    import re
    segments = re.split(r'[，,、；;]|以及|和', text)
    
    # 为每个段落匹配对应的金额
    for segment in segments:
        segment = segment.strip()
        if not segment:
            continue
        
        # 在这个段落中找金额
        seg_amounts = extract_all_amounts(segment)
        if seg_amounts:
            seg_amount = seg_amounts[0]  # 取第一个
            seg_category = detect_category(segment)
            seg_type = detect_type(segment)
            
            result["multi_records"].append({
                "amount": seg_amount,
                "category": seg_category,
                "type": seg_type,
                "note": segment,
            })
    
    # 主记录用第一个
    if result["multi_records"]:
        result["amount"] = result["multi_records"][0]["amount"]
        result["category"] = result["multi_records"][0]["category"]
        result["type"] = result["multi_records"][0]["type"]
    
    return result


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python parse_accounting.py '消息内容'", file=sys.stderr)
        sys.exit(1)
    
    message = sys.argv[1]
    result = parse_accounting_message(message)
    print(json.dumps(result, ensure_ascii=False, indent=2))
