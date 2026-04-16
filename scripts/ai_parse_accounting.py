#!/usr/bin/env python3
"""
AI 兜底解析器
当规则解析失败或低置信度时，调用 AI 进行补充解析
"""

import json
import re
from datetime import datetime

# 模拟 LLM 调用（实际项目中替换为真实 API）
def call_llm_parse(text):
    """
    调用 LLM 解析消息
    实际实现应调用 OpenAI/Claude/Kimi 等 API
    这里用模拟逻辑演示
    """
    
    # 构造 prompt
    system_prompt = """你是一个中文记账消息解析器。你的任务是从用户一句话中提取是否记账、金额、收支类型、分类、备注、多笔记录。

只输出 JSON，不输出解释。若信息不足，不要猜测；将 need_confirmation 设为 true。

分类仅允许：餐饮、交通、购物、娱乐、通讯、居住、医疗、其他。
收支类型仅允许：支出、收入。

输出格式：
{
  "is_accounting": true/false,
  "need_confirmation": true/false,
  "amount": 数字或null,
  "type": "支出"/"收入"/null,
  "category": "分类"/null,
  "note": "备注",
  "multi_records": [{"amount": 数字, "type": "支出"/"收入", "category": "分类", "note": "备注"}],
  "reason": "若无法判断，说明原因"
}"""
    
    # TODO: 实际调用 LLM API
    # response = openai.ChatCompletion.create(...)
    
    # 模拟解析逻辑（用于演示）
    result = simulate_llm_parse(text)
    return result


def simulate_llm_parse(text):
    """
    模拟 LLM 解析（实际项目中删除此函数，改用真实 API）
    """
    result = {
        "is_accounting": False,
        "need_confirmation": False,
        "amount": None,
        "type": None,
        "category": None,
        "note": text,
        "multi_records": [],
        "reason": ""
    }
    
    # 尝试提取金额（更灵活的方式）
    import re
    
    # 匹配各种金额表达
    amount_patterns = [
        r'(\d+(?:\.\d+)?)\s*(?:元|块|块钱|圆)',
        r'(?:花了|用了|消费|支出|收入)?\s*(\d+(?:\.\d+)?)',
    ]
    
    amounts = []
    for pattern in amount_patterns:
        matches = re.findall(pattern, text)
        for m in matches:
            try:
                amounts.append(float(m))
            except:
                pass
    
    # 中文数字（简单处理）
    cn_numbers = {
        '一': 1, '二': 2, '两': 2, '三': 3, '四': 4, '五': 5,
        '六': 6, '七': 7, '八': 8, '九': 9, '十': 10,
        '二十': 20, '三十': 30, '四十': 40, '五十': 50,
        '六十': 60, '七十': 70, '八十': 80, '九十': 90,
        '一百': 100, '两百': 200, '一千': 1000
    }
    
    for cn, num in cn_numbers.items():
        if cn in text and '元' in text:
            # 检查是否已提取
            if num not in amounts:
                amounts.append(num)
    
    if not amounts:
        result["need_confirmation"] = True
        result["reason"] = "无法提取金额"
        return result
    
    # 判断类型
    if any(kw in text for kw in ["收入", "工资", "收到", "到账", "退款", "报销"]):
        record_type = "收入"
    else:
        record_type = "支出"
    
    # 判断分类
    category_keywords = {
        "餐饮": ["吃饭", "午餐", "晚餐", "早餐", "奶茶", "咖啡", "餐厅", "火锅", "烧烤", "聚餐"],
        "交通": ["打车", "滴滴", "地铁", "公交", "车费", "加油", "停车", "高速"],
        "购物": ["买东西", "淘宝", "京东", "拼多多", "买", "购物", "超市", "衣服", "鞋", "包"],
        "娱乐": ["电影", "游戏", "KTV", "唱歌", "玩", "娱乐", "旅游", "旅行"],
        "通讯": ["话费", "流量", "宽带", "手机费", "电话费"],
        "居住": ["房租", "水电", "物业", "房贷", "租金"],
        "医疗": ["医院", "看病", "药", "医保", "体检"],
    }
    
    category = "其他"
    for cat, keywords in category_keywords.items():
        if any(kw in text for kw in keywords):
            category = cat
            break
    
    # 构建结果
    result["is_accounting"] = True
    result["amount"] = amounts[0] if len(amounts) == 1 else None
    result["type"] = record_type
    result["category"] = category
    result["note"] = text
    
    # 多笔记录
    if len(amounts) > 1:
        result["multi_records"] = []
        # 简单拆分
        segments = re.split(r'[，,、；;]|以及|和', text)
        for i, amount in enumerate(amounts):
            if i < len(segments):
                seg = segments[i]
                seg_category = "其他"
                for cat, keywords in category_keywords.items():
                    if any(kw in seg for kw in keywords):
                        seg_category = cat
                        break
                
                result["multi_records"].append({
                    "amount": amount,
                    "type": record_type,
                    "category": seg_category,
                    "note": seg.strip()
                })
    
    return result


def ai_parse_accounting(text):
    """
    AI 兜底解析入口
    返回标准格式结果
    """
    try:
        result = call_llm_parse(text)
        
        # 确保返回格式正确
        if not isinstance(result, dict):
            return {
                "is_accounting": False,
                "need_confirmation": True,
                "reason": "AI 返回格式错误"
            }
        
        # 添加时间信息
        result["date"] = datetime.now().strftime("%Y-%m-%d")
        result["time"] = datetime.now().strftime("%H:%M")
        
        return result
        
    except Exception as e:
        return {
            "is_accounting": False,
            "need_confirmation": True,
            "reason": f"AI 解析异常: {str(e)}"
        }


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python ai_parse_accounting.py '消息内容'", file=sys.stderr)
        sys.exit(1)
    
    message = sys.argv[1]
    result = ai_parse_accounting(message)
    print(json.dumps(result, ensure_ascii=False, indent=2))
