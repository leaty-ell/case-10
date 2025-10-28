from data_importer import import_financial_data
from transaction_classifier import categorize_all_transactions
from financial_analyst import calculate_basic_stats, calculate_by_category, analyze_by_time
from budget_planner import analyze_historical_spending, create_budget_template, compare_budget_vs_actual
import ru_local as ru

def main():
    """
    Main application pipeline - integrates all modules.
    """
    filename = input(f"📁 {ru.ENTER_FILENAME}")
    transactions = import_financial_data(filename)
    
    if not transactions:
        print(f"❌ {ru.PROGRAM_COMPLETED}")
        return
    
    categorized_transactions = categorize_all_transactions(transactions)
    
    stats = calculate_basic_stats(categorized_transactions)
    category_stats = calculate_by_category(categorized_transactions)
    time_analysis = analyze_by_time(categorized_transactions)
    
    spending_analysis = analyze_historical_spending(categorized_transactions)
    budget = create_budget_template(spending_analysis, categorized_transactions)
    
    print_financial_report(stats, category_stats, budget, categorized_transactions, time_analysis)

def print_financial_report(stats: dict, category_stats: dict, budget: dict, transactions: list, time_analysis: dict):
    """
    Print comprehensive financial report.
    Args:
        stats: Basic statistics from calculate_basic_stats
        category_stats: Category statistics from calculate_by_category
        budget: Budget from create_budget_template
        transactions: Transactions for additional analysis
        time_analysis: Time-based analysis from analyze_by_time
    """
    print("\n" + "="*60)
    print(f"💰 {ru.FINANCIAL_REPORT}")
    print("="*60)
    
    print(f"\n📊 {ru.BASIC_INDICATORS}")
    print(f"│   💵 {ru.INCOME}:     {stats.get('total_income', 0):>12,.0f} руб.".replace(',', ' '))
    print(f"│   💸 {ru.EXPENSES}:    {stats.get('total_expenses', 0):>12,.0f} руб.".replace(',', ' '))
    print(f"│   ⚖️ {ru.BALANCE}:     {stats.get('balance', 0):>12,.0f} руб.".replace(',', ' '))
    print(f"│   📈 {ru.TRANSACTION_COUNT}:   {stats.get('transaction_count', 0):>12}".replace(',', ' '))
    
    if category_stats:
        print(f"\n  {ru.CATEGORY_SPENDING}:")
        for category, data in category_stats.items():
            amount = data.get('total_amount', 0)
            percentage = data.get('percentage', 0)
            count = data.get('transaction_count', 0)
            print(f"│     {category:<15} {amount:>8,.0f} {ru.RUBLES} ({percentage:>5.1f}%) {count:>3} {ru.OPERATIONS}".replace(',', ' '))
    
    if budget:
        print(f"\n🎯 {ru.NEXT_MONTH_BUDGET}:")
        
        spending_analysis = analyze_historical_spending(transactions)
        budget_comparison = compare_budget_vs_actual(budget, transactions)
        
        for category, planned in budget.items():
            if category == {ru.SAVINGS_CATEGORY}:
                print(f"│   💰 {ru.SAVINGS}:{planned:>12,.0f} {ru.RUBLES}".replace(',', ' '))
            else:
                historical = spending_analysis.get(category, {}).get('avg_monthly', 0)
                if historical > 0:
                    change = ((planned - historical) / historical) * 100
                    trend = f"📉 {ru.DECREASE_TREND}" if change < 0 else f"📈 {ru.INCREASE_TREND}"
                    print(f"│     {category:<15} {planned:>8,.0f} {ru.RUBLES} ({trend} {ru.ON} {abs(change):>3.0f}%)".replace(',', ' '))
                else:
                    print(f"│     {category:<15} {planned:>8,.0f} {ru.RUBLES}".replace(',', ' '))
        
        print(f"\n💡 {ru.RECOMMENDATIONS}:")
        exceeded = [cat for cat, data in budget_comparison.items() 
                   if data.get('status') == 'exceeded']
        
        if exceeded:
            print(f"│   ⚠️  {ru.FOCUS_SPENDING}: {', '.join(exceeded[:2])}")
        else:
            print(f"│   ✅ {ru.BUDGET_MAINTAINED}")
            
        monthly_income = stats.get('total_income', 0)
        if monthly_income > 0:
            savings_goal = monthly_income * 0.1
            print(f"│   🎯 {ru.SAVINGS_GOAL}: {savings_goal:>8,.0f} {ru.RUBLES_IN_MONTH}".replace(',', ' '))
    
    if time_analysis:
        print(f"\n📅 {ru.TIME_ANALYSIS}:")
        for month, data in list(time_analysis.items())[-3:]:
            print(f"│   📆 {month}:  {data['income']:>8,.0f} {ru.RUBLES}  {data['expenses']:>8,.0f} {ru.RUBLES}".replace(',', ' '))
    
    print("\n" + "="*60)
    print(f"🎉 {ru.ANALYSIS_COMPLETED} 😊")
    print("="*60)

if __name__ == "__main__":
    main()