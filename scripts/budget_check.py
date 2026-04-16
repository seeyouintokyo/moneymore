#!/usr/bin/env python3
"""
预算检查器
检查当月支出是否超过预算
"""

import sys
import json

def check_budget(records, budget_limit):
    """检查预算"""
    
    total_expense = 0
    
    for record in records:
        fields = record.get("fields", {})
        amount = fields.get("金额", 0)
        record_type = fields.get("类型", "支出")
        
        if record_type == "支出":
            total_expense += amount
    
    # 计算剩余预算
    remaining = budget_limit - total_expense
    percentage = (total_expense / budget_limit * 100) if budget_limit > 0 else 0
    
    result = {
        "total_expense": total_expense,
        "budget_limit": budget_limit,
        "remaining": remaining,
        "percentage": percentage,
        "is_over_budget": total_expense > budget_limit,
        "is_warning": percentage >= 80 and percentage < 100,
    }
    
    return result


def format_budget_alert(check_result):
    """格式化预算提醒"""
    
    if check_result["is_over_budget"]:
        return f"""⚠️ 预算超支提醒

本月预算：{check_result['budget_limit']:.2f} 元
已支出：{check_result['total_expense']:.2f} 元
超支：{abs(check_result['remaining']):.2f} 元

建议控制消费！"""
    
    elif check_result["is_warning"]:
        return f"""💡 预算预警

本月预算：{check_result['budget_limit']:.2f} 元
已支出：{check_result['total_expense']:.2f} 元
剩余：{check_result['remaining']:.2f} 元
使用率：{check_result['percentage']:.1f}%

注意控制开支！"""
    
    return None


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python budget_check.py <budget_limit>", file=sys.stderr)
        sys.exit(1)
    
    budget_limit = float(sys.argv[1])
    
    # 从stdin读取JSON数据
    data = json.load(sys.stdin)
    records = data.get("records", [])
    
    result = check_budget(records, budget_limit)
    alert = format_budget_alert(result)
    
    if alert:
        print(alert)
    else:
        print(json.dumps(result, ensure_ascii=False))
