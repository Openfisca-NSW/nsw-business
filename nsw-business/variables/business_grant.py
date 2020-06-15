# -*- coding: utf-8 -*-

# This file defines variables for the modelled legislation.
# A variable is a property of an Entity such as a Person, an Organisation…
# See https://openfisca.org/doc/key-concepts/variables.html

# Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_nsw_base.entities import *


# This is used to calculate whether an organisation is eligible for the COVID-19 small business grant.
class eligible_for_covid_19_business_grant(Variable):
    value_type = bool
    entity = Organisation
    definition_period = MONTH
    label = "Is the organisation a business?"

    def formula(organisation, period, parameters):
        return (
            (organisation('is_small_business', period))
            * (organisation('has_abn', period))
            * (organisation('highly_impacted', period))
            * (organisation('number_of_fte', period) > 0.5)
            * (organisation('number_of_fte', period) < 20)
            * (organisation('annual_turnover', period) > 75000)
            * (organisation('based_in_nsw', period))
            * (organisation('payroll', period) < parameters(period).payroll_threshold)
            * (organisation('turnover_calculations') > 0.75))


class is_small_business(Variable):
    value_type = bool
    entity = Organisation
    definition_period = MONTH
    label = "Is the organisation a small business?"
    reference = "holds an Australian Business Number (ABN) and employs more than 1 and less than 20 full-time employees. That is, the sum total of all standard hours worked by all employees (whether full-time or part-time) is less than the number of standard hours which would be worked by 20 full-time employees, as defined by the Australian Bureau of Statistics."


class has_abn(Variable):
    value_type = bool
    entity = Organisation
    definition_period = MONTH
    label = "Is the organisation a business?"


class highly_impacted(Variable):
    value_type = bool
    entity = Organisation
    definition_period = MONTH
    label = "Has the business been highly impacteed due to the Public Health (COVID-19 Restrictions on Gathering and Movement) Order 2020 effective on 30 March 2020?"


class based_in_nsw(Variable):
    value_type = bool
    entity = Organisation
    definition_period = MONTH
    label = "Is the organisation a business?"


class annual_turnover(Variable):
    value_type = int
    entity = Organisation
    definition_period = MONTH
    label = "What is the annual turnover of the business?"


class number_of_fte(Variable):
    value_type = int
    entity = Organisation
    definition_period = MONTH
    label = "What is the total number of FTEs employed the business?"


class payroll(Variable):
    value_type = int
    entity = Organisation
    definition_period = MONTH
    label = "What is the payroll amount for the business for the year 2019-2020?"


class lowest_turnover_for_two_weeks(Variable):
    value_type = bool
    entity = Organisation
    definition_period = MONTH
    default_value = True
    label = "What was the lowest turnover for your business after COVID restrictions have been placed?"


class corresponding_turnover_last_year(Variable):
    value_type = bool
    entity = Organisation
    definition_period = MONTH
    default_value = True
    label = "What was the lowest turnover for your business for the corresponding week a year earlier?"


class turnover_calculations(Variable):
    value_type = float
    entity = Organisation
    definition_period = MONTH
    default_value = True
    label = "By how much was the current year's turnover lesser than the previous year during the same two week period?"

    def formula(organisation, period, parameters):
        current_turnover = organisation('lowest_turnover_for_two_weeks', period)
        last_year_turnover = organisation('corresponding_turnover_last_year', period)
        turnover_diff = ((current_turnover - last_year_turnover / last_year_turnover))
        return turnover_diff
