#!/usr/bin/env python3
"""
测试用例 - 覆盖各种场景
"""

import json
from parse_accounting_with_fallback import parse_accounting_with_fallback

# 测试用例
test_cases = [
    {
        "name": "纯规则可解析 - 标准格式",
        "text": "午餐 35",
        "expected_source": "rule",
        "expected_confidence_high": True
    },
    {
        "name": "规则失败但 AI 可解析 - 模糊表达",
        "text": "中午跟同事AA制吃了顿火锅人均八十多",
        "expected_is_accounting": True,
        "expected_amount": 80
    },
    {
        "name": "多笔记录 - 标准",
        "text": "鼠标98，椰子水10块",
        "expected_multi_count": 2,
        "expected_total": 108
    },
    {
        "name": "模糊表达 - 中文数字",
        "text": "买杯奶茶花了二十五块",
        "expected_amount": 25,
        "expected_category": "餐饮"
    },
    {
        "name": "应拒绝自动记账 - 无金额",
        "text": "今天吃了火锅",
        "expected_is_accounting": False,
        "expected_need_confirmation": True
    },
    {
        "name": "应拒绝自动记账 - 纯数字（验证码）",
        "text": "123456",
        "expected_is_accounting": False
    },
    {
        "name": "分类歧义 - 需要 AI 辅助",
        "text": "买了个鼠标垫花了十五",
        "expected_category": "购物"
    },
    {
        "name": "收入识别",
        "text": "今天发工资了收入8500",
        "expected_type": "收入",
        "expected_amount": 8500
    },
    {
        "name": "复杂多笔 - 混合表达",
        "text": "早上地铁4块，中午吃饭30，晚上打车25",
        "expected_multi_count": 3
    },
    {
        "name": "极低置信度 - 需要确认",
        "text": "花了一些钱",
        "expected_is_accounting": False,
        "expected_need_confirmation": True
    }
]


def run_tests():
    """运行测试"""
    print("=" * 60)
    print("阿星微信记账助手 - AI 兜底解析测试")
    print("=" * 60)
    
    passed = 0
    failed = 0
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n测试 {i}: {test['name']}")
        print(f"输入: '{test['text']}'")
        print("-" * 40)
        
        result = parse_accounting_with_fallback(test['text'])
        
        print(f"结果: {json.dumps(result, ensure_ascii=False, indent=2)}")
        
        # 验证
        success = True
        errors = []
        
        if 'expected_is_accounting' in test:
            if result['is_accounting'] != test['expected_is_accounting']:
                success = False
                errors.append(f"is_accounting 期望 {test['expected_is_accounting']}, 实际 {result['is_accounting']}")
        
        if 'expected_amount' in test:
            if result.get('amount') != test['expected_amount']:
                success = False
                errors.append(f"amount 期望 {test['expected_amount']}, 实际 {result.get('amount')}")
        
        if 'expected_type' in test:
            if result.get('type') != test['expected_type']:
                success = False
                errors.append(f"type 期望 {test['expected_type']}, 实际 {result.get('type')}")
        
        if 'expected_category' in test:
            if result.get('category') != test['expected_category']:
                success = False
                errors.append(f"category 期望 {test['expected_category']}, 实际 {result.get('category')}")
        
        if 'expected_multi_count' in test:
            actual_count = len(result.get('multi_records', []))
            if actual_count != test['expected_multi_count']:
                success = False
                errors.append(f"multi_records 数量期望 {test['expected_multi_count']}, 实际 {actual_count}")
        
        if 'expected_total' in test:
            multi = result.get('multi_records', [])
            if multi:
                actual_total = sum(r['amount'] for r in multi)
            else:
                actual_total = result.get('amount', 0)
            if actual_total != test['expected_total']:
                success = False
                errors.append(f"总金额期望 {test['expected_total']}, 实际 {actual_total}")
        
        if 'expected_source' in test:
            if result.get('source') != test['expected_source']:
                success = False
                errors.append(f"source 期望 {test['expected_source']}, 实际 {result.get('source')}")
        
        if 'expected_need_confirmation' in test:
            if result.get('need_confirmation') != test['expected_need_confirmation']:
                success = False
                errors.append(f"need_confirmation 期望 {test['expected_need_confirmation']}, 实际 {result.get('need_confirmation')}")
        
        if success:
            print("✅ 通过")
            passed += 1
        else:
            print("❌ 失败")
            for error in errors:
                print(f"   - {error}")
            failed += 1
    
    print("\n" + "=" * 60)
    print(f"测试结果: 通过 {passed}/{len(test_cases)}, 失败 {failed}/{len(test_cases)}")
    print("=" * 60)
    
    return failed == 0


if __name__ == "__main__":
    success = run_tests()
    exit(0 if success else 1)
