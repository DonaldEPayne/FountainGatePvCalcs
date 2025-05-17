import numpy as np
import pandas as pd

# Constants
discount_rate = 0.07  # annual
monthly_discount_rate = (1 + discount_rate) ** (1/12) - 1
monthly_balance_decline_rate = 0.02
# Plans
plans = {
    "80%": {
        "entrance_fee": 683400,
        "monthly_fee": 4738,
        "plateau": 0.80,
        "months_to_plateau": 0 # calculate below
    },
    "50%": {
        "entrance_fee": 530700,
        "monthly_fee": 4738,
        "plateau": 0.50,
        "months_to_plateau": 0
    },
    "0%": {
        "entrance_fee": 431700,
        "monthly_fee": 4468,
        "plateau": 0.0,
        "months_to_plateau": 0
    }
}

# Years to evaluate
years = [1, 2, 3, 4, 5, 10, 20]

# Result container
results = []

for plan_name, plan in plans.items():
    ef = plan["entrance_fee"]
    mf = plan["monthly_fee"]
    plateau = plan["plateau"]
    plan["months_to_plateau"] = (1 - plateau) / monthly_balance_decline_rate  # R%/mo until P% refund
    m_plateau = plan["months_to_plateau"]
    
    for year in years:
        months = year * 12
        
        # Refund calculation
        if months >= m_plateau:
            refund = ef * plateau
        else:
            refund = ef * max(1 - monthly_balance_decline_rate * months, plateau)
        
        net_entrance_cost = ef - refund
        
        # PV of monthly fees
        months_array = np.arange(1, months + 1)
        pv_monthly_fees = sum(mf / (1 + monthly_discount_rate) ** months_array)
        
        # PV of net entrance cost (treated as paid at time 0)
        total_pv = net_entrance_cost + pv_monthly_fees
        
        results.append({
            "Plan": plan_name,
            "Year": year,
            "PV Cost": round(total_pv, 2)
        })

# Convert to DataFrame
df_results = pd.DataFrame(results)
pivot_table = df_results.pivot(index="Year", columns="Plan", values="PV Cost")
print (pivot_table)
