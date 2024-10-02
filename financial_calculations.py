import pandas as pd
import take_home_income_components as thic
import datetime

def TodaysYearFinder():
    today = datetime.date.today()
    year = today.year
    return year

#To identify method for calculation of contributions
def pensionContributionIdentifyier(contribution_type, salary, employee_contribution, employer_contribution):
    if contribution_type == "on your qualifying earnings":
        employee_cont_value, employer_cont_value = thic.pensionAutoEnrollmentClassifier(salary, employee_contribution,
                                                                    employer_contribution)
        return employee_cont_value, employer_cont_value


    else:
        employee_cont_value, employer_cont_value = thic.pensionContributionFullSalary(salary, employee_contribution,
                                                                      employer_contribution)
        return employee_cont_value, employer_cont_value

def pensionContributionGrowth(salary, personal_contribution, employer_contribution, contribution_type, years_until_retirement, salary_increase,today_year):

    contributions = []
    contribution_year = []

    # Loop over each year
    for y in range(years_until_retirement):
        # Contributions generated in this year
        contribution_year.append(today_year + y)
        salary = salary * (1 + salary_increase)
        employee, employer = pensionContributionIdentifyier(contribution_type, salary, personal_contribution, employer_contribution)
        contributions.append (employee + employer)
    year_with_contributions = pd.Series(data=contributions, index=contribution_year)
    return year_with_contributions

def compoundInterestPensionForecast(principal, annual_rate, years_until_retirement, contributions, today_year):
    monthly_rate = annual_rate / 12
    years = []
    interest_values = []
    fund_values =[]
    contribution_values =[]
    yearly_interest = 0
    compound_interest = 0
    total_contributions = 0

    # Loop over each year
    for y in range(years_until_retirement):
        # Compound the total amount so far for a year
        years.append(today_year + y)
        fund_interest = (principal + total_contributions + compound_interest) * annual_rate
        yearly_interest += fund_interest
        # Consider compound interest earned on contributions throughout the year
        monthly_contribution = contributions[today_year + y] / 12

        for m in range(12):
            yearly_interest += monthly_contribution * monthly_rate ** (12-m)

        compound_interest += yearly_interest
        total_contributions += contributions[today_year + y]
        fund_values.append(principal)
        interest_values.append(compound_interest)
        contribution_values.append(total_contributions)
        yearly_interest = 0
    year_with_interest = pd.Series(data=interest_values, index=years)
    year_with_fund_value = pd.Series(data=fund_values, index=years)
    year_with_contribution = pd.Series(data=contribution_values, index=years)
    FV_fund = year_with_interest.tail(1).item() + year_with_fund_value.tail(1).item() + year_with_contribution.tail(1).item()
    return FV_fund, year_with_interest, year_with_fund_value, year_with_contribution

def inflationAdjustmentPensionSeries(FV_series, average_inflation_rate):
    adjusted=[]
    cumulative_inflation = 1
    for fv in FV_series:
        cumulative_inflation = cumulative_inflation * (1 + average_inflation_rate)
        adjusted.append(fv / cumulative_inflation)
    return adjusted

def inflationAdjustmentPension (FV_series, average_inflation_rate, year):
    for index, value in FV_series.items():
        FV_series[index] = value *(1-average_inflation_rate)**(index - year + 1)
    return FV_series
