# personal-finance-app
Personal finance app to show total assets / liabilities and help budget for income and expenses.
This was started from the following Claude AI prompts
```
create a python project that receives transaction data from an API and passes it to a streamlit budget planning app.
```
```
Can you give it some HTML styling and generate some fake data for the app.
```

# Features to build
- Select historical time periods, month, quarter and year (financial and calendar) to show acutal income and expenses over the period. (COMPLETE)
- Remove certain categories and subcategories from expenses and income.
- Break down historical time periods by the expense category, and select the spending category to show a timeseries over the last year.
- Generate a monthly forecast for expected expenses that can be overwritten.
- Add the ability to add in income manually (Maybe forecast too? income is generally stable and known).
- Add config to allow adding multiple people to the budget.

# Refactor steps
- Change the structure of the code to make it easier to change and extend.
    - Separate creatation from use. Move the `TransactionGenerator` instances outside of the `BudgetPlanner` class and `app` function. This makes it easier to test and swap the transaction data for our real transaction data.
    - Dependecy injection. Pass the mock data as an input to the `BudgetPlanner` class and `app` function.
    - Move the streamlit config and date input widget to the top so they can be used by `TransactionGenerator`.
    - Create some validation for the mock data using `pandantic`. This ensures the schema of the data frame we pass the budget app is as we expect.
    - Move the dashboard components into different functions so they can be moved around and modified in isolation.
    - Remove CSS styling or change to black background, I want to use native Streamlit functions that work with dark mode.

- Start building historical income and expenditure features.
    - Change the hero metrics to total income, total expenses, difference.
    - Add spending and income to the line chart.
    - Remove Category Budgets and convert the Progress charts to Category Actuals. Exclude income from the charts.
    - Make the trend a rolling period.
    - Fix the rolling period and make the rolling days configurable in the UI.
    - Purchase breakdown, Order categories by highest spend.
    - Purchase breakdown, ability to change from category to subcategory.
    - Add category breakdown of income

- Add additinal data sources.
    - Add UP transaction data. (partially complete).
    - Add dropdown to select from accounts.
    - Implement the date range for UP.