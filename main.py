import streamlit as st
import pandas as pd
import math
import take_home_income_components as thic
import financial_calculations as fc
import visualisation_elements as ve

#To convert salary from monthly to annual
def salaryIdentifyier(value, type):
    if type == 'monthly':
        return value * 12
    else:
        return value

#Suggestion for income needed at retirement
def pensionIncomeSuggestionGenerator(salary, type):
    if type == 'annual':
        value = salary*2/3
        return value
    elif type == '':
        value = salary * 2 / 3
        return value
    else:
        value = (salary*2/3)/12
        return value


#Allows converting needed pension income from annual to monthly
def neededIncomeTypeIdentifyier(value, type):
    if type == 'monthly':
        return value
    else:
        return value/12


#To identify method for calculation of contributions

def pensionIncomeEqualValue(income_calc_logic, fc_option_1, PV_total_fund, retirement_age):
    PV_tax_free_cash = PV_total_fund * 0.25
    if income_calc_logic == fc_option_1:
        PV_pension = (PV_total_fund - PV_tax_free_cash) / max(2, (100 - retirement_age - 1))
        return PV_tax_free_cash, PV_pension
    else:
        PV_pension = (PV_total_fund - PV_tax_free_cash) * 0.04
        return PV_tax_free_cash, PV_pension
def run_app():

    fc_option_1 = ""
    income_calc_logic = "none"

    st.write('Please enter following information:')
    #Create 2 columns for adding features
    col1, col2 = st.columns(2)

    # Hide possible choice in session state
    if "visibility" not in st.session_state:
        st.session_state.visibility = "visible"
        st.session_state.disabled = False

    # User information input
    salary_value = col1.number_input(label='Your salary:', min_value=0.0, format="%f")
    salary_type = col2.radio(label='Input type', options=["annual", "monthly"], horizontal=True)
    salary = salaryIdentifyier(salary_value, salary_type)

    with st.container():
        container_c1, container_c2 = st.columns(2)
        personal_contribution = container_c1.number_input(label='Your monthly contribution:', min_value=0.0, max_value=100.0, value=5.0, help='If your pension contribution is calculated under automatic enrolment,\nyour pension contribution will be at least 5%')*0.01
        pension_contribution_type = container_c2.radio(label='\n\nChoose how your employer makes contributions', options=["on your qualifying earnings", "on your full salary"])
        employer_contribution = container_c1.number_input(label='Your employer monthly contribution:', min_value=0.0, max_value=100.0, value=3.0, help="If your pension contribution is calculated under automatic enrolment,\nyour employer's contribution will be at least 5%")*0.01


    student_loan_choice = st.selectbox("Your student loan",("None", "Plan 1", "Plan 2"),label_visibility=st.session_state.visibility, disabled=st.session_state.disabled,)

    user_age, retirement_age = st.slider(
        'Your age and desired retirement age',
        0, 100, (25, 68))

    pension_pot = st.number_input(label='Your current pension value:')

    with st.container():
        container_c1, container_c2, container_c3 = st.columns(3)
        pension_income_type = container_c3.radio(key='12', label='Input type', options=["annual", "monthly"], horizontal=True)
        suggested_pension_income = pensionIncomeSuggestionGenerator(salary, pension_income_type)

        chosen_pension_income = container_c2.number_input(key='abc', label='Type desired pension income instead:', min_value=0.0,
                                                   help='Many expect would suggest to plan for pension income which is 2/3 of the current income.')
        container_c1.write(f'Based on your salary suggested retirement income is £{suggested_pension_income:,.2f}')

        def test_click():
            st.session_state['abc'] = suggested_pension_income

        container_c1.button(label="Use suggested income", on_click=test_click)


    user_pension_income = chosen_pension_income
    pension_income = neededIncomeTypeIdentifyier(user_pension_income,pension_income_type)

    # Financial calculation settings
    investment_return = st.number_input("Investment returns", min_value=0.0, max_value=100.0, value=4.5, help='FCA recommends using 3.5% - 5.5% for forecasting expected return on EMRP (the risk-free rate and the equity market risk premium)')*0.01
    inflation_rate = st.number_input('Inflation estimate:', min_value=0.0, max_value=100.0, value=2.5, help='FCA recommends using 2.5% inflation rate in financial forecasting')*0.01
    salary_increase = st.number_input('Salary increase:', min_value=0.0, max_value=100.0, value=3.75, help='FCA recoomends using 3.75% average earning growth in 10-15 years finnacial forecasts')*0.01

    if salary == 0:

        st.write("Please enter your details above to start.")

    else:

        # take-home salary calculations
        income_tax_deduct = thic.incomeTaxDeduct(salary)
        NI_deduct = thic.nationalInsuranceDeduct(salary)
        employee_cont, employer_cont = fc.pensionContributionIdentifyier(pension_contribution_type, salary, personal_contribution, employer_contribution)
        student_loan_repayment = thic.studentLoanDeduct(salary, student_loan_choice)
        take_home_income = (salary - income_tax_deduct - NI_deduct - employee_cont - student_loan_repayment)/12

        years_until_retirement = retirement_age - user_age
        year = fc.TodaysYearFinder()

        contributions = fc.pensionContributionGrowth(salary, personal_contribution, employer_contribution, pension_contribution_type,
                                                     years_until_retirement, salary_increase, year)
        CI_future_pension, yearly_interest_earned, yearly_FV_fund, yearly_total_contributions = fc.compoundInterestPensionForecast(pension_pot, investment_return,
                                                                                       years_until_retirement,
                                                                                       contributions, year)

        inflation_adjusted_interest_earned = fc.inflationAdjustmentPension(yearly_interest_earned,inflation_rate, year)
        inflation_adjusted_pension_pot = fc.inflationAdjustmentPension(yearly_FV_fund, inflation_rate, year)
        inflation_adjusted_total_contributions = fc.inflationAdjustmentPension(yearly_total_contributions, inflation_rate, year)
        inflation_adjusted_total_fund = inflation_adjusted_interest_earned +inflation_adjusted_pension_pot +inflation_adjusted_total_contributions
        PV_total_fund = inflation_adjusted_total_fund.tail(1).item()


        CI_pension_fund_components = pd.DataFrame({'Interest': inflation_adjusted_interest_earned, 'Contributions': inflation_adjusted_total_contributions, 'Current Fund': inflation_adjusted_pension_pot})
        CI_pension_fund_components.index.name = 'Year'

        final_fund_series = CI_pension_fund_components.iloc[-1]
        final_fund_series = final_fund_series.sort_values(ascending=False)
        final_fund_names = final_fund_series.index.values.tolist()
        final_fund_values = final_fund_series.tolist()


        if pension_income <= 0:

            figure = ve.pensionComponentsInStackedBarChart(CI_pension_fund_components)
            st.plotly_chart(figure, use_container_width=True)

            st.write("Please enter your desirable pension income for more analysis")

        else:

            with st.container():
                container_c1, container_c2 = st.columns(2)

                trace_indicator = ve.totalFundTraceIndicator(PV_total_fund, inflation_adjusted_total_fund)
                container_c1.plotly_chart(trace_indicator, use_container_width=True)

                figure = ve.pensionComponentsInStackedBarChart(CI_pension_fund_components)
                container_c2.plotly_chart(figure, use_container_width=True)


                fc_option_1 = f'equal value over remaining years between {retirement_age} and 100'
                fc_option_2 = f'4% of the total fund'

                income_calc_logic = container_c1.radio(label='And the remaining fund is withdrawn at either:',
                                                       options=[fc_option_1, fc_option_2])
                PV_tax_free_cash, PV_annual_withdrawal = pensionIncomeEqualValue(income_calc_logic, fc_option_1,
                                                                                 PV_total_fund,
                                                                                 retirement_age)


                container_c2.write(f'This program assumes you make your 25% tax-free withdrawal in the first year')
                cash_indicator = ve.displayKeyIndicator(PV_tax_free_cash)
                container_c2.plotly_chart(cash_indicator, use_container_width=True)

                pie = ve.targetCompletionPie(PV_annual_withdrawal, pension_income)
                container_c1.plotly_chart(pie, use_container_width=True)

                funnel = ve.compositionFinalPensionFunnel(final_fund_names, final_fund_values)
                container_c1.plotly_chart(funnel, use_container_width=True)

                container_c2.write(f'Your pre-tax income')
                annual_withdrawal_indicator = ve.displayKeyIndicator(PV_annual_withdrawal/12)
                container_c2.plotly_chart(annual_withdrawal_indicator, use_container_width=True)


                container_c2.write(f'Your post-tax income')
                tax_deduct = thic.incomeTaxDeduct(PV_annual_withdrawal)
                post_tax_annual_withdrawal_indicator = ve.displayKeyIndicator((PV_annual_withdrawal - tax_deduct) / 12)
                container_c2.plotly_chart(post_tax_annual_withdrawal_indicator, use_container_width=True)


            if (PV_annual_withdrawal/12) < pension_income:
                st.write(
                    f'You are off target to achieve your desired pension income.\nHere are suggestions of what you can do.')
            else:
                st.write(
                    f'Congratuations! You are on target to achieve your desired pension income.\n You can still improve your pension fund by considering the following.')

            suggestion_choice = st.radio(label='Choose from following options:', options=["Increase your contribution", "Delay your retirement", "Reconsider your desired pension income"], horizontal=True)
            if suggestion_choice == "Increase your contribution":
                revised_contribution = st.slider(
                    label='Choose your revised contribution',
                    min_value=0, max_value=100, value=math.ceil(personal_contribution/0.01+2), format="%d%%")*0.01

                #Calculating new take-home income considering revised contribution
                revised_employee_cont, revised_employer_cont = fc.pensionContributionIdentifyier(pension_contribution_type, salary,
                                                                              revised_contribution, employer_contribution)
                revised_take_home_income = (salary - income_tax_deduct - NI_deduct - revised_employee_cont - student_loan_repayment) / 12

                #Calculating new pension fund considering revised contribution
                revised_contributions = fc.pensionContributionGrowth(salary, revised_contribution, employer_contribution,
                                                             pension_contribution_type,
                                                             years_until_retirement, salary_increase, year)
                revised_CI_future_pension, revised_yearly_interest_earned, revised_yearly_FV_fund, revised_yearly_total_contributions = fc.compoundInterestPensionForecast(
                    pension_pot, investment_return,
                    years_until_retirement,
                    revised_contributions, year)

                revised_inflation_adjusted_interest_earned = fc.inflationAdjustmentPension(revised_yearly_interest_earned,
                                                                                   inflation_rate, year)
                revised_inflation_adjusted_pension_pot = fc.inflationAdjustmentPension(revised_yearly_FV_fund, inflation_rate, year)
                revised_inflation_adjusted_total_contributions = fc.inflationAdjustmentPension(revised_yearly_total_contributions,
                                                                                       inflation_rate, year)
                revised_inflation_adjusted_total_fund = revised_inflation_adjusted_interest_earned + revised_inflation_adjusted_pension_pot + revised_inflation_adjusted_total_contributions
                revised_PV_total_fund = revised_inflation_adjusted_total_fund.tail(1).item()


                revised_PV_tax_free_cash, revised_PV_annual_withdrawal = pensionIncomeEqualValue(income_calc_logic, fc_option_1,
                                                                                 revised_PV_total_fund,
                                                                                 retirement_age)

                # Visualising all indicators
                with st.container():
                    container_c1, container_c2 = st.columns(2)
                    container_c1.write('Change in your take-home income')
                    income_indicator = ve.changeInKeyIndicators(revised_take_home_income, take_home_income)
                    container_c1.plotly_chart(income_indicator, use_container_width=True)
                    total_fund_indicator = ve.changeInKeyIndicators(revised_PV_total_fund, PV_total_fund)
                    container_c2.write('Change in your total pension fund')
                    container_c2.plotly_chart(total_fund_indicator, use_container_width=True)
                    tax_free_cash_indicator = ve.changeInKeyIndicators(revised_PV_tax_free_cash, PV_tax_free_cash)
                    container_c1.write('Change in your tax-free withdrawal')
                    container_c1.plotly_chart(tax_free_cash_indicator, use_container_width=True)
                    monthly_income_indicator = ve.changeInKeyIndicators(revised_PV_annual_withdrawal / 12, PV_annual_withdrawal / 12)
                    container_c2.write('Change in your monthly retirement income')
                    container_c2.plotly_chart(monthly_income_indicator, use_container_width=True)

            elif suggestion_choice == "Delay your retirement":
                revised_retirement_age = st.slider(
                    label='Choose your revised retirement age',
                    min_value=0, max_value=130, value=(retirement_age+10))

                #Calculating new pension fund considering changed retirement age
                revised_years_until_retirement = revised_retirement_age - user_age

                revised_contributions = fc.pensionContributionGrowth(salary, personal_contribution, employer_contribution,
                                                             pension_contribution_type,
                                                             revised_years_until_retirement, salary_increase, year)
                revised_CI_future_pension, revised_yearly_interest_earned, revised_yearly_FV_fund, revised_yearly_total_contributions = fc.compoundInterestPensionForecast(
                    pension_pot, investment_return,
                    revised_years_until_retirement,
                    revised_contributions, year)

                revised_inflation_adjusted_interest_earned = fc.inflationAdjustmentPension(revised_yearly_interest_earned,
                                                                                   inflation_rate, year)
                revised_inflation_adjusted_pension_pot = fc.inflationAdjustmentPension(revised_yearly_FV_fund, inflation_rate, year)
                revised_inflation_adjusted_total_contributions = fc.inflationAdjustmentPension(revised_yearly_total_contributions,
                                                                                       inflation_rate, year)
                revised_inflation_adjusted_total_fund = revised_inflation_adjusted_interest_earned + revised_inflation_adjusted_pension_pot + revised_inflation_adjusted_total_contributions
                revised_PV_total_fund = revised_inflation_adjusted_total_fund.tail(1).item()

                revised_PV_tax_free_cash, revised_PV_annual_withdrawal = pensionIncomeEqualValue(income_calc_logic,
                                                                                                 fc_option_1,
                                                                                                 revised_PV_total_fund,
                                                                                                 revised_retirement_age)
                #Visualising all indicators
                with st.container():
                    container_c1, container_c2 = st.columns(2)

                    # Take-home income remains unchanged
                    income_indicator = ve.changeInKeyIndicators(take_home_income, take_home_income)
                    container_c1.write('Change in your take-home income')
                    container_c1.plotly_chart(income_indicator, use_container_width=True)
                    total_fund_indicator = ve.changeInKeyIndicators(revised_PV_total_fund, PV_total_fund)
                    container_c2.write('Change in your total pension fund')
                    container_c2.plotly_chart(total_fund_indicator, use_container_width=True)
                    tax_free_cash_indicator = ve.changeInKeyIndicators(revised_PV_tax_free_cash, PV_tax_free_cash)
                    container_c1.write('Change in your tax-free withdrawal')
                    container_c1.plotly_chart(tax_free_cash_indicator, use_container_width=True)
                    monthly_income_indicator = ve.changeInKeyIndicators(revised_PV_annual_withdrawal / 12, PV_annual_withdrawal / 12)
                    container_c2.write('Change in your monthly retirement income')
                    container_c2.plotly_chart(monthly_income_indicator, use_container_width=True)
            else:
                st.write(f'When planning for your retirement income, you may like to consider following:\n- Are you going to be paying off your mortgage during your retirement?\n- Would you consider downsizing or moving to less expensive area?\n- Will you have any other assets you can relly on during the retirement (e.g. buy-to-let property)?\n- Would you like to rely on your State Pension which is not considered by this program?\n- If you have a student loan, when will you pay it off and would you consider contributing the extra income towards your pension?')




if __name__ == '__main__':
    run_app()