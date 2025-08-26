# https://www.bls.gov/news.release/empsit.t01.htm
NUM_WORKERS = 170_000_000

BASE_TAX_RATE = 0.15

HIGH_INFLATION_DICT = {
    2022: 0.08
}

# https://www.irs.gov/newsroom/irs-releases-tax-inflation-adjustments-for-tax-year-2025
INCOME_TAX_RATES = [
    0.1, 0.12, 0.22, 0.24, 0.32, 0.35, 0.37
]

if __name__ == "__main__":
    tax_revenue_dict = dict()

    curr_net_worth = 0
    date = None

    # Wealth distribution data from the Federal Reserve
    # https://www.federalreserve.gov/releases/z1/dataviz/dfa/distribute/table/
    # https://www.federalreserve.gov/releases/z1/dataviz/download/zips/dfa.zip
    NET_WORTH_DATA_CSV = "dfa/dfa-networth-levels.csv"

    # Step 1: Calculate total wealth gains tax per quarter
    with open(NET_WORTH_DATA_CSV) as csv_file:
        for line in csv_file:
            if "TopPt1" in line or "RemainingTop1" in line:
                columns = line.split(',')
                date = columns[0]
                net_worth = int(columns[6]) * 1_000_000  # Number in millions
                curr_net_worth += net_worth
            else:
                if date is not None:
                    year = int(date.split(":")[0])
                    if year in HIGH_INFLATION_DICT:
                        dividend_yield = HIGH_INFLATION_DICT[year]
                    else:
                        dividend_yield = 0.05
                    dividend_tax_rate = dividend_yield * INCOME_TAX_RATES[-1]

                    annualized_tax_revenue = curr_net_worth * dividend_tax_rate
                    quarterly_tax_revenue = annualized_tax_revenue / 4
                    tax_revenue_dict[date] = quarterly_tax_revenue

                    curr_net_worth = 0
                    date = None
    with open("1-tax_revenue_dict.csv", 'w') as csv_file:
        for quarter in sorted(tax_revenue_dict.keys()):
            csv_file.write(f"{quarter},{tax_revenue_dict[quarter]}\n")

    # Step 2: Calculate annual tax relief per capita, assuming tax relief is uniformly applied across the workforce
    annual_tax_relief_dict = dict()
    annual_tax_revenue = 0
    curr_date = ""
    for date, revenue in tax_revenue_dict.items():
        annual_tax_revenue += revenue
        if "Q1" in date:
            curr_date = date
        elif curr_date and "Q4" in date:
            year = int(curr_date.split(':')[0])
            annual_tax_relief_dict[year] = round(annual_tax_revenue / NUM_WORKERS, 2)
            annual_tax_revenue = 0
    with open("2-annual_tax_relief.csv", 'w') as csv_file:
        for year in sorted(annual_tax_relief_dict.keys()):
            csv_file.write(f"{year},{annual_tax_relief_dict[year]}\n")
