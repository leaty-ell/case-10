"""
Module for budget planning and analysis.
Includes historical spending analysis and budget vs actual comparison.
"""

import ru_local as ru

def analyze_historical_spending(transactions: list) -> dict:
    """
    Analyzes historical spending data by categories.
    Args:
        transactions (list): List of transactions in unified format
    Returns:
        Dictionary with spending analysis by categories
    """
    category_data = {}
    months = set() 
    
    for transaction in transactions:
        if transaction['amount'] < 0:  
            category = transaction['category']
            amount = abs(transaction['amount'])
            month = transaction['date'][:7]  
            months.add(month)
            
            if category not in category_data:
                category_data[category] = {
                    'total': 0,
                    'count': 0,
                    'max': 0
                }
            
            category_data[category]['total'] += amount
            category_data[category]['count'] += 1
            
            if amount > category_data[category]['max']:
                category_data[category]['max'] = amount
    
    result = {}
    num_months = len(months) if months else 1
    
    for category, data in category_data.items():
        avg_monthly = data['total'] / num_months  
        result[category] = {
            'avg_monthly': round(avg_monthly, 2),
            'max': data['max'],
            'count': data['count'],
            'total_months': num_months 
        }
    
    return result


def create_budget_template(analysis: dict, transactions: list) -> dict:
    """
    Creates budget template based on spending analysis.
    Args:
        analysis (dict): Result from analyze_historical_spending
        transactions (list): Transactions for income calculation
    Returns:
        Dictionary with budget limits by categories
    """
    budget = {}
    
    monthly_income = calculate_monthly_income(transactions)
    
    for category, data in analysis.items():
        avg_spending = data['avg_monthly'] 
        
        if avg_spending > 3000:
            budget[category] = round(avg_spending * 0.85) 
        else:
            budget[category] = round(avg_spending * 0.95) 
    
    budget[ru.SAVINGS_CATEGORY] = round(monthly_income * 0.1)
    return budget


def calculate_monthly_income(transactions: list) -> float:
    """
    Calculates average monthly income from transactions.
    Args:
        transactions (list): List of transactions
    Returns:
        Average monthly income as float
    """
    monthly_totals = {}
    
    for transaction in transactions:
        if transaction['amount'] > 0:  
            month = transaction['date'][:7] 
            amount = transaction['amount']
            
            if month not in monthly_totals:
                monthly_totals[month] = 0
            monthly_totals[month] += amount
    
    if monthly_totals:
        return sum(monthly_totals.values()) / len(monthly_totals)
    else:
        return 0


def compare_budget_vs_actual(budget: dict, transactions: list, target_month: str = None) -> dict:
    """
    Compares budget with actual spending.
    Args:
        budget (dict): Budget from create_budget_template
        transactions (list): Actual transactions to compare
        target_month (str): Specific month to analyze (optional)
    Returns:
        Dictionary with budget comparison results
    """
    actual_spending = {}
    
    for transaction in transactions:
        if transaction['amount'] < 0:
            if target_month and not transaction['date'].startswith(target_month):
                continue
                
            category = transaction['category']
            amount = abs(transaction['amount'])
            
            if category not in actual_spending:
                actual_spending[category] = 0
            actual_spending[category] += amount
    
    comparison = {}
    for category, planned_amount in budget.items():
        if category == ru.SAVINGS_CATEGORY:
            continue
            
        actual_amount = actual_spending.get(category, 0)
        
        if actual_amount <= planned_amount:
            status = 'within_budget'
        else:
            status = 'exceeded'
        
        comparison[category] = {
            'planned': planned_amount,
            'actual': round(actual_amount, 2),
            'status': status,
            'percent_over': round(((actual_amount - planned_amount) / planned_amount * 100), 1) if planned_amount > 0 else 0
        }
    
    return comparison