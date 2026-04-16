#!/usr/bin/env python3
"""
月末自动报表生成器
生成当月收支统计并推送
"""

import sys
import json
from datetime import datetime, timedelta

def generate_monthly_report(records):
    """生成月度报表"""
    
    # 统计
    total_expense = 0
    total_income = 0
    category_stats = {}
    
    for record in records:
        fields = record.get("fields", {})
        amount = fields.get("金额", 0)
        record_type = fields.get("类型", "支出")
        category = fields.get("分类", "其他")
        
        if record_type == "支出":
            total_expense += amount
            category_stats[category] = category_stats.get(category, 0) + amount
        else:
            total_income += amount
    
    # 分类排序
    sorted_categories = sorted(category_stats.items(), key=lambda x: x[1], reverse=True)
    
    # 生成报表文本
    report = f"""📊 本月记账报表

💰 收支总览
━━━━━━━━━━━━━━━━
收入：{total_income:.2f} 元
支出：{total_expense:.2f} 元
结余：{total_income - total_expense:.2f} 元

📈 支出分类 TOP5
━━━━━━━━━━━━━━━━"""
    
    for i, (cat, amount) in enumerate(sorted_categories[:5], 1):
        percentage = (amount / total_expense * 100) if total_expense > 0 else 0
        report += f"\n{i}. {cat}：{amount:.2f} 元 ({percentage:.1f}%)"
    
    report += "\n\n💡 记账小贴士：\n"
    
    # 根据数据给建议
    if total_expense > total_income:
        report += "本月支出超过收入，建议控制消费"
    else:
        report += "本月有结余，继续保持！"
    
    return report


if __name__ == "__main__":
    # 从stdin读取JSON数据
    data = json.load(sys.stdin)
    records = data.get("records", [])
    
    report = generate_monthly_report(records)
    print(report)
