"""
Module for financial analysis and statistics calculation.
Provides basic stats, category analysis, and time-based analytics.
"""

import ru_local as ru

def calculate_basic_stats(transactions):
    """
    Calculate basic financial statistics.
    Args:
        transactions: List of transactions in UNIFIED FORMAT
    Returns:
        Dictionary with basic statistics
    """
    if not transactions:
        return {
            'total_income': 0,
            'total_expenses': 0,
            'balance': 0,
            'transaction_count': 0
        }

    total_income = 0
    total_expenses = 0

    for transaction in transactions:
        amount = transaction['amount']
        if amount > 0:
            total_income += amount
        else:
            total_expenses += abs(amount)

    balance = total_income - total_expenses

    return {
        'total_income': round(total_income, 2),
        'total_expenses': round(total_expenses, 2),
        'balance': round(balance, 2),
        'transaction_count': len(transactions)
    }


def calculate_by_category(transactions):
    """
    Calculate statistics by category.
    Args:
        transactions: List of transactions with categories
    Returns:
        Dictionary with category statistics
    """
    if not transactions:
        return {}

    category_stats = {}

    for transaction in transactions:
        amount = transaction['amount']
        if amount < 0: 
            category = transaction.get('category', ru.OTHER)
            abs_amount = abs(amount)

            if category not in category_stats:
                category_stats[category] = {
                    'total_amount': 0,
                    'transaction_count': 0
                }

            category_stats[category]['total_amount'] += abs_amount
            category_stats[category]['transaction_count'] += 1

    total_expenses = sum(stats['total_amount'] for stats in category_stats.values())

    for category, stats in category_stats.items():
        if total_expenses > 0:
            percentage = (stats['total_amount'] / total_expenses) * 100
        else:
            percentage = 0
        stats['percentage'] = round(percentage, 2)
        stats['total_amount'] = round(stats['total_amount'], 2)

    return category_stats


def analyze_by_time(transactions):
    """
    Analyze transactions by time periods.
    Args:
        transactions: List of transactions
    Returns:
        Dictionary with time-based analysis
    """
    if not transactions:
        return {}

    monthly_stats = {}

    for transaction in transactions:
        date_str = transaction['date']
        month = date_str[:7] 

        if month not in monthly_stats:
            monthly_stats[month] = {
                'income': 0,
                'expenses': 0,
                'categories': {}
            }

        amount = transaction['amount']
        category = transaction.get('category', ru.OTHER)

        if amount > 0:
            monthly_stats[month]['income'] += amount
        else:
            monthly_stats[month]['expenses'] += abs(amount)

            if category not in monthly_stats[month]['categories']:
                monthly_stats[month]['categories'][category] = 0
            monthly_stats[month]['categories'][category] += abs(amount)

    for month, stats in monthly_stats.items():
        stats['income'] = round(stats['income'], 2)
        stats['expenses'] = round(stats['expenses'], 2)
        
        if stats['categories']:
            sorted_categories = sorted(
                stats['categories'].items(),
                key=lambda x: x[1],
                reverse=True
            )
            stats['top_categories'] = sorted_categories[:3]
        else:
            stats['top_categories'] = []

    return monthly_stats