import math
def incomeTaxDeduct(salary):
    PA_adjustment = lambda x: 12571 if (x <= 100000) else (12571 - min(12571, math.floor((x-100000)/2)))
    personal_allowance = PA_adjustment(salary)
    tax_band_a = 50270
    tax_band_b = 125140
    upper_band_tax = max(0, salary-125140) * 0.45
    if salary < personal_allowance:
        return 0
    elif personal_allowance <= salary <= tax_band_a:
        deduct = (salary - personal_allowance) * 0.20
        return deduct
    elif salary > tax_band_a:
        deduct = (tax_band_a - personal_allowance) * 0.20 + (min(tax_band_b,salary) - tax_band_a) * 0.40 + upper_band_tax
        return deduct


def nationalInsuranceDeduct(salary):
    monthly_tax_band_a = 1048
    monthly_tax_band_b = 4189
    if (salary/12) <= monthly_tax_band_a:
        return 0
    elif (salary/12) <= monthly_tax_band_b:
        deduct = (salary/12 - monthly_tax_band_a) * 0.12
        yearly_deduct = deduct*12
        return yearly_deduct
    elif (salary/12) > monthly_tax_band_b:
        deduct = (monthly_tax_band_b-monthly_tax_band_a) * 0.12 + (salary/12-monthly_tax_band_b)*0.02
        yearly_deduct = deduct * 12
        return yearly_deduct

def pensionAutoEnrollmentClassifier(salary, personal_contribution, employer_contribution):
    lower_band = 6240
    upper_band = 50270
    max_salary = min(salary, upper_band)
    if salary < lower_band:
        employee_pen_cont = 0
        employer_pen_cont = 0
        return employee_pen_cont, employer_pen_cont
    elif salary >= lower_band:
        employee_pen_cont = (max_salary-lower_band) * personal_contribution
        employer_pen_cont = (max_salary-lower_band) * employer_contribution
        return employee_pen_cont, employer_pen_cont


def pensionContributionFullSalary(salary, personal_contribution, employer_contribution):
    employee_pen_cont = salary * personal_contribution
    employer_pen_cont = salary * employer_contribution
    return employee_pen_cont, employer_pen_cont

def studentLoanDeduct(salary, choice):
    #TODO: Student loan being paid off
    if choice == "Plan 1":
        if salary < 20195:
            deduct = 0
            return deduct
        else:
            deduct = (salary - 20195) * 0.09
            return deduct
    elif choice == "Plan 2":
        if salary < 27295:
            deduct = 0
            return deduct
        else:
            deduct = (salary - 27295) * 0.09
            return deduct
    elif choice == "None":
        deduct = 0
        return deduct