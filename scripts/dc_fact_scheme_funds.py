import pandas as pd
import numpy as np


benef = pd.read_csv("fact_scheme_beneficiaries.csv")
dim_scheme = pd.read_csv("dim_scheme.csv")

benef = benef.merge(
    dim_scheme[["scheme_id", "avg_benefit_amount"]],
    on="scheme_id",
    how="left"
)

if benef["avg_benefit_amount"].isna().any():
    raise ValueError("Missing avg_benefit_amount for some schemes")

yearly = (
    benef
    .groupby(["scheme_id", "district_id", "year"], as_index=False)
    .agg({"beneficiaries": "sum", "avg_benefit_amount": "first"})
)


yearly["funds_allocated"] = (
    yearly["beneficiaries"] * yearly["avg_benefit_amount"]
)


np.random.seed(42)

def utilization_factor(year):
    if year == 2020:
        return np.random.uniform(0.80, 0.88)  # COVID pain
    return np.random.uniform(0.90, 0.97)

yearly["funds_utilized"] = yearly.apply(
    lambda r: int(r["funds_allocated"] * utilization_factor(r["year"])),
    axis=1
)

fact_scheme_funds = yearly[[
    "scheme_id",
    "district_id",
    "year",
    "funds_allocated",
    "funds_utilized"
]]


fact_scheme_funds.to_csv(
    "fact_scheme_funds.csv",
    index=False
)

print("fact_scheme_funds.csv created")
print("Rows:", len(fact_scheme_funds))
print(fact_scheme_funds.head())
