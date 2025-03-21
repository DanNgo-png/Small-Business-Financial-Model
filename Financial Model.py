import pandas as pd
import numpy as np

def create_small_business_financial_model(years=5):
    """
    Creates a comprehensive financial model for a hypothetical small business.

    Args:
        years (int): Number of years for the forecast.

    Returns:
        dict: A dictionary containing the financial model components:
            - Income Statement (DataFrame)
            - Balance Sheet (DataFrame)
            - Cash Flow Statement (DataFrame)
            - Key Ratios (DataFrame)
    """

    # --- Assumptions ---
    initial_revenue = 100000
    revenue_growth = 0.10  # 10% annual growth
    cost_of_goods_sold_percentage = 0.40  # 40% of revenue
    operating_expenses_percentage = 0.30  # 30% of revenue
    tax_rate = 0.25  # 25% tax rate
    initial_cash = 50000
    initial_accounts_receivable = 20000
    initial_inventory = 30000
    initial_fixed_assets = 150000
    depreciation_percentage = 0.05 # 5% per year
    initial_accounts_payable = 15000
    initial_debt = 100000
    interest_rate = 0.05 # 5% interest rate
    initial_equity = initial_fixed_assets + initial_cash + initial_accounts_receivable + initial_inventory - initial_accounts_payable - initial_debt
    receivables_days = 30 # Days sales outstanding
    inventory_days = 60 # Days inventory outstanding
    payables_days = 45 # Days payable outstanding
    
    # --- Income Statement ---
    income_statement = pd.DataFrame(index=range(1, years + 1))
    income_statement['Revenue'] = [initial_revenue * (1 + revenue_growth) ** (year - 1) for year in range(1, years + 1)]
    income_statement['Cost of Goods Sold (COGS)'] = income_statement['Revenue'] * cost_of_goods_sold_percentage
    income_statement['Gross Profit'] = income_statement['Revenue'] - income_statement['Cost of Goods Sold (COGS)']
    income_statement['Operating Expenses'] = income_statement['Revenue'] * operating_expenses_percentage
    income_statement['EBIT'] = income_statement['Gross Profit'] - income_statement['Operating Expenses']  # Ensure this line is executed
    income_statement['Interest Expense'] = [initial_debt * interest_rate] * years
    income_statement['Earnings Before Taxes (EBT)'] = income_statement['EBIT'] - income_statement['Interest Expense']
    income_statement['Taxes'] = income_statement['Earnings Before Taxes (EBT)'] * tax_rate
    income_statement['Net Income'] = income_statement['Earnings Before Taxes (EBT)'] - income_statement['Taxes']

    # --- Balance Sheet ---
    balance_sheet = pd.DataFrame(index=range(1, years + 1))
    balance_sheet['Cash'] = [0] * years
    balance_sheet['Accounts Receivable'] = [income_statement['Revenue'][year] / 365 * receivables_days for year in range(1, years + 1)]
    balance_sheet['Inventory'] = [income_statement['Cost of Goods Sold (COGS)'][year] / 365 * inventory_days for year in range(1, years + 1)]
    balance_sheet['Total Current Assets'] = balance_sheet['Cash'] + balance_sheet['Accounts Receivable'] + balance_sheet['Inventory']
    balance_sheet['Fixed Assets'] = [initial_fixed_assets] * years
    balance_sheet['Accumulated Depreciation'] = [initial_fixed_assets * depreciation_percentage * year for year in range(1, years + 1)]
    balance_sheet['Net Fixed Assets'] = balance_sheet['Fixed Assets'] - balance_sheet['Accumulated Depreciation']
    balance_sheet['Total Assets'] = balance_sheet['Total Current Assets'] + balance_sheet['Net Fixed Assets']
    balance_sheet['Accounts Payable'] = [income_statement['Cost of Goods Sold (COGS)'][year] / 365 * payables_days for year in range(1, years + 1)]
    balance_sheet['Debt'] = [initial_debt] * years
    balance_sheet['Equity'] = [initial_equity] * years

    # --- Cash Flow Statement ---
    cash_flow_statement = pd.DataFrame(index=range(1, years + 1))
    cash_flow_statement['Net Income'] = income_statement['Net Income']
    cash_flow_statement['Depreciation'] = [initial_fixed_assets * depreciation_percentage] * years
    cash_flow_statement['Change in Accounts Receivable'] = [balance_sheet['Accounts Receivable'][year] - balance_sheet['Accounts Receivable'][year -1] if year > 1 else balance_sheet['Accounts Receivable'][1] - initial_accounts_receivable for year in range(1, years + 1)]
    cash_flow_statement['Change in Inventory'] = [balance_sheet['Inventory'][year] - balance_sheet['Inventory'][year -1] if year > 1 else balance_sheet['Inventory'][1] - initial_inventory for year in range(1, years + 1)]
    cash_flow_statement['Change in Accounts Payable'] = [balance_sheet['Accounts Payable'][year] - balance_sheet['Accounts Payable'][year -1] if year > 1 else balance_sheet['Accounts Payable'][1] - initial_accounts_payable for year in range(1, years + 1)]
    cash_flow_statement['Cash Flow from Operations'] = cash_flow_statement['Net Income'] + cash_flow_statement['Depreciation'] - cash_flow_statement['Change in Accounts Receivable'] - cash_flow_statement['Change in Inventory'] + cash_flow_statement['Change in Accounts Payable']
    cash_flow_statement['Cash Flow from Investing'] = [0] * years
    cash_flow_statement['Cash Flow from Financing'] = [-income_statement['Interest Expense'][1]] * years
    cash_flow_statement['Net Change in Cash'] = cash_flow_statement['Cash Flow from Operations'] + cash_flow_statement['Cash Flow from Investing'] + cash_flow_statement['Cash Flow from Financing']
    cash_flow_statement['Beginning Cash'] = [initial_cash] + list(cash_flow_statement['Net Change in Cash'][:-1])
    cash_flow_statement['Ending Cash'] = cash_flow_statement['Beginning Cash'] + cash_flow_statement['Net Change in Cash']
    balance_sheet['Cash'] = cash_flow_statement['Ending Cash']

    # Update Equity based on net income
    for year in range(1,years + 1):
        if year == 1:
            balance_sheet['Equity'][year] = initial_equity + income_statement['Net Income'][year]
        else:
            balance_sheet['Equity'][year] = balance_sheet['Equity'][year-1] + income_statement['Net Income'][year]

    # --- Key Ratios ---
    key_ratios = pd.DataFrame(index=range(1, years + 1))
    key_ratios['Gross Profit Margin'] = income_statement['Gross Profit'] / income_statement['Revenue']
    key_ratios['Net Profit Margin'] = income_statement['Net Income'] / income_statement['Revenue']
    key_ratios['Current Ratio'] = balance_sheet['Total Current Assets'] / balance_sheet['Accounts Payable']
    key_ratios['Debt-to-Equity Ratio'] = balance_sheet['Debt'] / balance_sheet['Equity']
    key_ratios['Return on Equity (ROE)'] = income_statement['Net Income'] / balance_sheet['Equity']
    key_ratios['Days Sales Outstanding (DSO)'] = balance_sheet['Accounts Receivable'] / income_statement['Revenue'] * 365
    key_ratios['Days Inventory Outstanding (DIO)'] = balance_sheet['Inventory'] / income_statement['Cost of Goods Sold (COGS)'] * 365
    key_ratios['Days Payable Outstanding (DPO)'] = balance_sheet['Accounts Payable'] / income_statement['Cost of Goods Sold (COGS)'] * 365

    return {
        'Income Statement': income_statement,
        'Balance Sheet': balance_sheet,
        'Cash Flow Statement': cash_flow_statement,
        'Key Ratios': key_ratios,
    }

# --- Example Usage ---
financial_model = create_small_business_financial_model(years=5)

print("Income Statement:")
print(financial_model['Income Statement'])
print("\nBalance Sheet:")
print(financial_model['Balance Sheet'])
print("\nCash Flow Statement:")
print(financial_model['Cash Flow Statement'])
print("\nKey Ratios:")
print(financial_model['Key Ratios'])
