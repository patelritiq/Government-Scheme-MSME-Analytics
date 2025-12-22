import pandas as pd
msme_raw = pd.read_csv("MSME_Units_Investment_Employment_2004_2014.csv")


msme = msme_raw.rename(columns={
    "year": "year_raw",
    "unit number": "msme_units",
    "Investment (Rs in Lakh)": "investment_lakh",
    "employment": "employment_generated"
})


msme = msme.dropna(subset=["year_raw"])
msme["year"] = pd.to_numeric(msme["year_raw"].str.split("-").str[1], errors='coerce')
# Drop rows where year conversion failed
msme = msme.dropna(subset=["year"])
msme["year"] = msme["year"].astype(int)


numeric_cols = [
    "msme_units",
    "investment_lakh",
    "employment_generated"
]

for col in numeric_cols:
    msme[col] = (
        msme[col]
        .astype(str)
        .str.replace(",", "")
        .astype(float)
    )


fact_msme_employment = msme[[
    "year",
    "msme_units",
    "investment_lakh",
    "employment_generated"
]]


fact_msme_employment.to_csv(
    "fact_msme_employment_base.csv",
    index=False
)

print("fact_msme_employment_base.csv created")
print(fact_msme_employment.head())
