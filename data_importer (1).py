"""
Module for importing financial data from various file formats.
Supports CSV and JSON formats with data normalization.
"""

import csv
import json
import os.path
import ru_local as ru

def read_csv_file(filename: str) -> list[dict]:
    """
    Read CSV file and convert it to list of dictionaries.
    Args:
        filename (str): Name of the CSV file
    Returns:
        List of transactions in UNIFIED FORMAT
    """
    transactions = []
    
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            
            for row in reader:
                try:
                    amount = float(row['amount'])
                except (ValueError, KeyError):
                    print(f"{ru.INVALID_AMOUNT}: {row}")
                    continue
                
                transaction_type = ru.EXPENSE_TYPE if amount < 0 else ru.INCOME_TYPE
                
                transaction = {
                    "date": row.get('date', ''),
                    "amount": amount,
                    "description": row.get('description', ''),
                    "type": transaction_type
                }
                transactions.append(transaction)
                
    except FileNotFoundError:
        print(ru.FILE_NOT_FOUND)
        return []
    except Exception as e:
        print(f"{ru.CSV_READ_ERROR}: {e}")
        return []
    
    return transactions

def read_json_file(filename: str) -> list[dict]:
    """
    Read JSON file and convert it to list of dictionaries.
    Args:
        filename (str): Name of the JSON file
    Returns:
        List of transactions in UNIFIED FORMAT
    """
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            data = json.load(file)
            
            if isinstance(data, list):
                normalized_transactions = []
                for item in data:
                    transaction = {
                        "date": item.get("date", ""),
                        "amount": float(item.get("amount", 0)),
                        "description": item.get("description", ""),
                        "type": item.get("type", ru.EXPENSE_TYPE if float(item.get("amount", 0)) < 0 else ru.INCOME_TYPE)
                    }
                    normalized_transactions.append(transaction)
                return normalized_transactions
            else:
                print(ru.JSON_NOT_LIST)
                return []
                
    except FileNotFoundError:
        print(ru.FILE_NOT_FOUND)
        return []
    except json.JSONDecodeError:
        print(ru.JSON_INVALID)
        return []
    except Exception as e:
        print(f"{ru.JSON_READ_ERROR}: {e}")
        return []

def import_financial_data(filename: str) -> list[dict]:
    """
    Universal function for importing financial data.
    Returns data in UNIFIED FORMAT for the entire system.
    Args:
        filename (str): Name of data file (.csv or .json)
    Returns:
        List of transactions in UNIFIED FORMAT:
    """
    if not os.path.exists(filename):
        print(ru.FILE_NOT_EXIST)
        return []
    
    if filename.lower().endswith('.csv'):
        transactions = read_csv_file(filename)
    elif filename.lower().endswith('.json'):
        transactions = read_json_file(filename)
    else:
        print(f"{ru.UNSUPPORTED_FORMAT} {filename}")
        return []
    
    validated_transactions = []
    required_fields = ['date', 'amount', 'description', 'type']
    
    for transaction in transactions:
        if all(field in transaction for field in required_fields):
            validated_transactions.append(transaction)
        else:
            print(f"{ru.INCOMPLETE_DATA}: {transaction}")
    
    print(f"{ru.IMPORT_SUCCESS} {len(validated_transactions)} {ru.TRANSACTION_FORMAT}")
    return validated_transactions