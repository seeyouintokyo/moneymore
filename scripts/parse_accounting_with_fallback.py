#!/usr/bin/env python3
"""
统一解析入口 - 规则 + AI 兜底
先走规则解析，低置信度时调用 AI 兜底
"""

import json
import logging
from datetime import datetime

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('accounting_parse.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# 导入现有规则解析器
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from parse_accounting import parse_accounting_message as rule_parse
from ai_parse_accounting import ai_parse_accounting as ai_parse


def calculate_rule_confidence(rule_result, text):
    """
    计算规则解析的置信度
    返回 0~1 之间的值
    """
    confidence = 1.0
    
    if not rule_result.get("is_accounting"):
        return 0.0
    
    # 金额是否提取成功
    amount = rule_result.get("amount")
    if amount is None:
        confidence -= 0.4
    elif amount <= 0:
        confidence -= 0.3
    
    # 分类是否为"其他"
    category = rule_result.get("category")
    if category == "其他":
        # 检查文本是否明显包含消费语义
        spending_keywords = ["买", "吃", "花", "用", "消费", "支出", "花了", "买了", "吃了"]
        if any(kw in text for kw in spending_keywords):
            confidence -= 0.2  # 可能是分类失败
        else:
            confidence -= 0.1
    
    # 多笔记录检查
    multi_records = rule_result.get("multi_records", [])
    if multi_records:
        # 检查多笔是否完整
        expected_amounts = len(multi_records)
        actual_amounts = len([r for r in multi_records if r.get("amount")])
        if expected_amounts != actual_amounts:
            confidence -= 0.2
    
    # 检查文本长度（过短可能信息不足）
    if len(text) < 5:
        confidence -= 0.1
    
    return max(0.0, min(1.0, confidence))


def should_use_ai_fallback(rule_result, text, confidence_threshold=0.7):
    """
    判断是否需要 AI 兜底
    
    触发条件：
    1. is_accounting 为 false，但消息看起来可能是记账
    2. 金额提取失败
    3. 分类为 "其他" 且文本明显包含消费语义
    4. 多笔记录拆分失败或明显不完整
    5. 规则结果存在冲突或低置信度
    """
    
    # 计算置信度
    confidence = calculate_rule_confidence(rule_result, text)
    
    logger.info(f"规则解析置信度: {confidence:.2f}")
    
    # 条件1: 低置信度
    if confidence < confidence_threshold:
        logger.info("触发 AI 兜底: 置信度低于阈值")
        return True, confidence
    
    # 条件2: is_accounting 为 false，但可能是记账
    if not rule_result.get("is_accounting"):
        # 检查是否包含金额相关关键词
        amount_indicators = ["块", "元", "钱", "花了", "买了", "吃了", "消费", "支出", "收入"]
        if any(ind in text for ind in amount_indicators):
            logger.info("触发 AI 兜底: 可能是记账但规则未识别")
            return True, confidence
    
    # 条件3: 金额为 None
    if rule_result.get("amount") is None:
        logger.info("触发 AI 兜底: 金额提取失败")
        return True, confidence
    
    # 条件4: 分类为"其他"且包含消费语义
    if rule_result.get("category") == "其他":
        spending_keywords = ["买", "吃", "花", "用", "消费", "花了", "买了", "吃了", "喝"]
        if any(kw in text for kw in spending_keywords):
            logger.info("触发 AI 兜底: 分类为其他但含消费语义")
            return True, confidence
    
    # 条件5: 多笔记录不完整
    multi_records = rule_result.get("multi_records", [])
    if multi_records:
        incomplete = any(r.get("amount") is None or r.get("category") == "其他" 
                        for r in multi_records)
        if incomplete:
            logger.info("触发 AI 兜底: 多笔记录不完整")
            return True, confidence
    
    return False, confidence


def merge_rule_and_ai(rule_result, ai_result, text):
    """
    合并规则结果和 AI 结果
    
    策略：
    - 规则高置信度时优先规则
    - 规则缺失字段时可用 AI 补齐
    - AI 与规则冲突时，默认保守：不自动记账，返回确认提示
    """
    
    merged = {
        "is_accounting": False,
        "type": None,
        "amount": None,
        "category": None,
        "note": text,
        "date": datetime.now().strftime("%Y-%m-%d"),
        "time": datetime.now().strftime("%H:%M"),
        "multi_records": [],
        "confidence": 0.0,
        "source": "merged"
    }
    
    # 如果 AI 也无法识别
    if not ai_result.get("is_accounting"):
        # 检查是否需要确认
        if ai_result.get("need_confirmation"):
            return {
                "is_accounting": False,
                "need_confirmation": True,
                "reason": ai_result.get("reason", "无法可靠判断")
            }
        # 否则返回规则结果（即使可能不准确）
        rule_result["confidence"] = calculate_rule_confidence(rule_result, text)
        rule_result["source"] = "rule"
        return rule_result
    
    # 金额决策
    rule_amount = rule_result.get("amount")
    ai_amount = ai_result.get("amount")
    
    if rule_amount is not None and ai_amount is not None:
        # 冲突：金额不一致
        if abs(rule_amount - ai_amount) > 0.01:
            logger.warning(f"金额冲突: 规则={rule_amount}, AI={ai_amount}")
            # 保守策略：需要确认
            return {
                "is_accounting": False,
                "need_confirmation": True,
                "reason": f"金额不确定（规则:{rule_amount}, AI:{ai_amount}）",
                "rule_result": rule_result,
                "ai_result": ai_result
            }
        # 一致，使用规则
        merged["amount"] = rule_amount
    elif rule_amount is not None:
        merged["amount"] = rule_amount
    elif ai_amount is not None:
        merged["amount"] = ai_amount
    else:
        # 都失败
        return {
            "is_accounting": False,
            "need_confirmation": True,
            "reason": "无法提取金额"
        }
    
    # 类型决策
    rule_type = rule_result.get("type", "支出")
    ai_type = ai_result.get("type", "支出")
    
    if rule_type == ai_type:
        merged["type"] = rule_type
    else:
        # 冲突：保守策略，使用支出（更常见）
        logger.warning(f"类型冲突: 规则={rule_type}, AI={ai_type}")
        merged["type"] = "支出"
        merged["need_confirmation"] = True
        merged["reason"] = f"收支类型不确定（规则:{rule_type}, AI:{ai_type}）"
    
    # 分类决策
    rule_category = rule_result.get("category", "其他")
    ai_category = ai_result.get("category", "其他")
    
    if rule_category != "其他":
        # 规则有明确分类，优先
        merged["category"] = rule_category
    elif ai_category != "其他":
        # 规则为"其他"，AI 有分类，使用 AI
        merged["category"] = ai_category
    else:
        # 都是"其他"
        merged["category"] = "其他"
    
    # 多笔记录
    rule_multi = rule_result.get("multi_records", [])
    ai_multi = ai_result.get("multi_records", [])
    
    if rule_multi and ai_multi:
        # 都有多笔，优先规则（更可靠）
        merged["multi_records"] = rule_multi
    elif ai_multi:
        # 只有 AI 有多笔
        merged["multi_records"] = ai_multi
    elif rule_multi:
        merged["multi_records"] = rule_multi
    
    # 计算最终置信度
    if merged.get("need_confirmation"):
        merged["confidence"] = 0.5
    else:
        rule_conf = calculate_rule_confidence(rule_result, text)
        # AI 兜底通常意味着规则不够可靠，降低置信度
        merged["confidence"] = max(0.5, rule_conf * 0.9)
    
    merged["is_accounting"] = True
    
    return merged


def parse_accounting_with_fallback(text):
    """
    统一解析入口
    先走规则，低置信度时调用 AI 兜底
    """
    
    logger.info(f"开始解析: '{text}'")
    
    # Step 1: 规则解析
    rule_result = rule_parse(text)
    logger.info(f"规则解析结果: {json.dumps(rule_result, ensure_ascii=False)}")
    
    # Step 2: 判断是否需要 AI 兜底
    need_ai, confidence = should_use_ai_fallback(rule_result, text)
    
    if not need_ai:
        # 规则解析足够可靠
        rule_result["confidence"] = confidence
        rule_result["source"] = "rule"
        logger.info(f"使用规则结果，置信度: {confidence:.2f}")
        return rule_result
    
    # Step 3: 调用 AI 兜底
    logger.info("调用 AI 兜底解析")
    ai_result = ai_parse(text)
    logger.info(f"AI 解析结果: {json.dumps(ai_result, ensure_ascii=False)}")
    
    # Step 4: 合并结果
    merged_result = merge_rule_and_ai(rule_result, ai_result, text)
    logger.info(f"合并结果: {json.dumps(merged_result, ensure_ascii=False)}")
    
    return merged_result


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python parse_accounting_with_fallback.py '消息内容'", file=sys.stderr)
        sys.exit(1)
    
    message = sys.argv[1]
    result = parse_accounting_with_fallback(message)
    print(json.dumps(result, ensure_ascii=False, indent=2))