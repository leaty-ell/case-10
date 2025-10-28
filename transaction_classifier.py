"""
Module for automatic categorization of financial transactions.
Responsible for determining spending categories based on transaction descriptions.
"""

from typing import Dict, List, Any
import ru_local as ru


def create_categories() -> Dict[str, List[str]]:
    """
    Returns a dictionary of categories for transaction classification.
    
    Returns:
        Dictionary where keys are category names, values are lists of keywords.
    """
    categories = {
    ru.FOOD: ru.FOOD_KEYWORDS,
    ru.TRANSPORT: ru.TRANSPORT_KEYWORDS,
    ru.ENTERTAINMENT: ru.ENTERTAINMENT_KEYWORDS,
    ru.HEALTH: ru.HEALTH_KEYWORDS,
    ru.UTILITIES: ru.UTILITIES_KEYWORDS,
    ru.COMMUNICATION: ru.COMMUNICATION_KEYWORDS,
    ru.CLOTHING: ru.CLOTHING_KEYWORDS,
    ru.EDUCATION: ru.EDUCATION_KEYWORDS,
    ru.SALARY: ru.SALARY_KEYWORDS,
    ru.OTHER: []
}
    
    return categories


def categorize_transaction(description: str, categories: Dict[str, List[str]]) -> str:
    """
    Determines transaction category based on its description.
    
    Args:
        description: Transaction description from bank statement.
        categories: Dictionary of categories with keywords.
        
    Returns:
        Category name or ru.SALARY if category not found.
    """
    if not description or not isinstance(description, str):
        return ru.OTHER
    
    description_lower = description.lower()
    
    for category, keywords in categories.items():
        if category == ru.OTHER:
            continue
            
        for keyword in keywords:
            if keyword in description_lower:
                return category
    
    return ru.OTHER


def categorize_all_transactions(transactions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Adds 'category' field to each transaction in the list.
    
    Args:
        transactions: List of transactions in UNIFIED FORMAT.
            
    Returns:
        List of transactions with added 'category' field.
    """
    if not transactions:
        return []
    
    required_fields = {"date", "amount", "description", "type"}
    for transaction in transactions:
        missing_fields = required_fields - set(transaction.keys())
        if missing_fields:
            raise ValueError(f"Transaction missing fields: {missing_fields}")
    
    categories = create_categories()
    categorized_transactions = []
    
    for transaction in transactions:
        categorized_transaction = transaction.copy()
        description = transaction["description"]
        
        if transaction["amount"] > 0:
            category = categorize_transaction(description, categories)
            if category == ru.OTHER:
                category = ru.SALARY
            categorized_transaction["category"] = category
        else:
            category = categorize_transaction(description, categories)
            categorized_transaction["category"] = category
        
        categorized_transactions.append(categorized_transaction)
    
    return categorized_transactions