import pandas as pd
import numpy as np


msme_base = pd.read_csv("fact_msme_employment_base.csv")

msme_base = msme_base.sort_values("year")

last_row = msme_base.iloc[-1].copy()

np.random.seed(42)
extended_rows = []


for year in range(int(last_row["year"]) + 1, 2023):

    # Growth logic
    if year <= 2019:
        growth_units = np.random.uniform(1.23, 1.66)
        growth_inv = np.random.uniform(1.34, 1.78)
        growth_emp = np.random.uniform(1.23, 1.66)

    elif year == 2020:
        growth_units = 0.75
        growth_inv = 0.75
        growth_emp = 0.75

    else:  # 2021–2022 recovery
        growth_units = np.random.uniform(1.45, 1.80)
        growth_inv = np.random.uniform(1.48, 2.05)
        growth_emp = np.random.uniform(1.45, 1.80)

    new_row = {
        "year": year,
        "msme_units": int(last_row["msme_units"] * growth_units),
        "investment_lakh": int(last_row["investment_lakh"] * growth_inv),
        "employment_generated": int(last_row["employment_generated"] * growth_emp)
    }

    extended_rows.append(new_row)
    last_row = new_row  # ← THIS is the key fix


msme_extended = pd.concat(
    [msme_base, pd.DataFrame(extended_rows)],
    ignore_index=True
)


msme_extended.to_csv(
    "fact_msme_employment.csv",
    index=False
)

print("fact_msme_employment.csv regenerated correctly")
print(msme_extended.tail())
