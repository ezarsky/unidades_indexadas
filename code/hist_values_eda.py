from matplotlib import pyplot as plt
import numpy as np
import pandas as pd

# TODO functionalize regression
# TODO compartmentalize personal settings
# TODO wage data and inflation

rng = np.random.default_rng(7)

# color-blind friendly bright qualitative colorscheme
# source: https://sronpersonalpages.nl/~pault/
tol_bright = {
    'blue': (68, 119, 170), 
    'cyan': (102, 204, 238),
    'green': (34, 136, 51),
    'yellow': (204, 187, 68),
    'red': (238, 102, 119),
    'purple': (170, 51, 119),
    'grey': (187, 187, 187)
    }
tol_bright = {name: (r/256, g/256, b/256) for name, (r, g, b) in tol_bright.items()}


### currency data ###
#import data
uyu_usd_data = pd.read_csv('uyu_usd_history.csv')
# drop empty rows
uyu_usd_data = uyu_usd_data.dropna()

# fill in missing usd_buy value by averaging values before and after
row = int(uyu_usd_data.loc[uyu_usd_data['usd_buy'] == ' '].index.values[0])
col = uyu_usd_data.columns.get_loc('usd_buy')
uyu_usd_data.iloc[row, col] = str(
        (float(uyu_usd_data.iloc[row-1, col]) + float(uyu_usd_data.iloc[row+1, col])) / 2
    )

# convert column datatypes
uyu_usd_data['usd_buy'] = uyu_usd_data['usd_buy'].astype(float)
uyu_usd_data['date'] = pd.to_datetime(uyu_usd_data['date'], yearfirst=True)


# plot USD-UYU buy and sell prices over time
fig, ax = plt.subplots()
ax.plot(uyu_usd_data['date'], uyu_usd_data['usd_buy'], color=tol_bright['blue'], label='Buy price')
ax.plot(uyu_usd_data['date'], uyu_usd_data['usd_sell'], color=tol_bright['green'], label='Sell price')
ax.set_xlabel('Date')
ax.set_ylabel('UYU per USD')
ax.set_title('UYU-USD Conversion Rate Over Time')
ax.legend()
plt.show()

# # plot USD-UYU buy/sell spread over time
# fig, ax = plt.subplots()
# ax.plot(uyu_usd_data['date'], uyu_usd_data['usd_sell'] - uyu_usd_data['usd_buy'], color=tol_bright['red'])
# ax.set_xlabel('Date')
# ax.set_ylabel('Buy/Sell Spread (Sell-Buy)')
# ax.set_title('UYU-USD Buy/Sell Spread Over Time')
# plt.show()




### indexed units data ###
# source: https://www.gub.uy/instituto-nacional-estadistica/datos-y-estadisticas/estadisticas/series-historicas-ui
# import data
ui_data = pd.read_csv('ui_history.csv')

# convert datatype of date column
ui_data['date'] = pd.to_datetime(ui_data['date'])

# plot UI values in UYU over time
fig, ax = plt.subplots()
ax.plot(ui_data['date'], ui_data['value'], color=tol_bright['cyan'])
ax.set_xlabel('Date')
ax.set_ylabel('Pesos per UI')
ax.set_title('Value of Unidad Indexada Over Time')
plt.show()

# create day column/variable that tracks number of days since first date
first_day = ui_data.loc[0,'date']
ui_data['days'] = ui_data['date'].apply(lambda x: (x-first_day).days)
ui_data = ui_data[['days', 'value', 'date']]

# create data matrix for training exponential regression model
ui_matrix = ui_data[['days', 'value']].to_numpy()
m = ui_matrix.shape[0]
ui_matrix = np.concatenate((np.ones((m, 1)), ui_matrix), axis=1)

# define size of training set
train_size = int(0.8 * m)

# select training and test set data points
idxs = np.arange(m)
rng.shuffle(idxs)
train_idxs = idxs[:train_size]
test_idxs = idxs[train_size:]
train_idxs.sort()
test_idxs.sort()

# define training and test set data matrices
X_train = ui_matrix[train_idxs, :-1]
y_train = ui_matrix[train_idxs, -1]
X_test = ui_matrix[test_idxs, :-1]
y_test = ui_matrix[test_idxs, -1]

# calculate exponetial regression weights
inv = np.linalg.inv(np.dot(X_train.T, X_train))
right = np.dot(X_train.T, np.log(y_train))
betas = np.dot(inv, right)
a, b = np.exp(betas)
ann_inf_factor = b**365.25
print(f'Approximate annual inflation (UI): {round((ann_inf_factor-1)*100, 4)}%')

preds_train = np.exp(np.dot(X_train, betas))
preds_test = np.exp(np.dot(X_test, betas))

MSE_train = np.mean((y_train-preds_train)**2)
MSE_test = np.mean((y_test-preds_test)**2)

all_preds = np.zeros(m)
all_preds[train_idxs] = preds_train
all_preds[test_idxs] = preds_test

ui_data['pred_value'] = all_preds
ui_data = ui_data[['date', 'days', 'value', 'pred_value']]

fig, ax = plt.subplots()
ax.scatter(ui_data['date'], ui_data['value'] - ui_data['pred_value'], 
           s=3.0, color=tol_bright['cyan'])
ax.set_xlabel('Date')
ax.set_ylabel('Residual')
ax.set_title('UI Model Residuals')
plt.show()

fig, ax = plt.subplots()
ax.plot(ui_data['date'], ui_data['value'], color=tol_bright['cyan'], label='True')
ax.plot(ui_data['date'], ui_data['pred_value'], color=tol_bright['purple'], label='Predicted')
ax.set_xlabel('Date')
ax.set_ylabel('UYU per UI')
ax.set_title('True and Predicted Values of Unidad Indexada Over Time')
ax.legend()
plt.show()

#TODO: better fit might be piecewise - 2002 to 2020, 2020 to 2024, 2024 to present


### consumer price index (IPC) data ###
# source: https://www.gub.uy/instituto-nacional-estadistica/datos-y-estadisticas/estadisticas/series-historicas-ipc-base-octubre-2022100
# import data
ipc_data = pd.read_csv('ipc_history_base2022.csv')

# create date column set to first day of each month
ipc_data['date'] = ipc_data.apply(
    lambda row: f"{str(int(row['year']))}-{str(int(row['month'])).zfill(2)}-01",
    axis=1
    )
ipc_data['date'] = pd.to_datetime(ipc_data['date'], yearfirst=True)

# filter out months where UI doesn't exist
ipc_data = ipc_data[ipc_data['date'] >= pd.to_datetime('2002-06-01', yearfirst=True)]
ipc_data = ipc_data.reset_index(drop=True)
ipc_data = ipc_data.reset_index().rename(columns={'index': 'months'})

# plot IPC over time
fig, ax = plt.subplots()
ax.plot(ipc_data['date'], ipc_data['ipc'], color=tol_bright['yellow'])
ax.set_xlabel('Date')
ax.set_ylabel('IPC')
ax.set_title('Consumer Price Index (IPC) Over Time')
plt.show()

# normalize IPC so that June 1, 2002 IPC = 1
new_ipc_base = ipc_data.loc[ipc_data['months'] == 0, 'ipc'].values[0]
ipc_data['normed_ipc'] = ipc_data['ipc']/new_ipc_base


# select only UI data from the first of the month each month
first_uis = ui_data[ui_data['date'].dt.day == 1]

# merge into dataframe of inflation indices
inflation_idxs = pd.merge(ipc_data, first_uis, on='date')
inflation_idxs = inflation_idxs[['date', 'value', 'normed_ipc']]
inflation_idxs = inflation_idxs.rename(columns={'value': 'ui'})

# plot normalized IPC and UI over time
fig, ax = plt.subplots()
ax.plot(inflation_idxs['date'], inflation_idxs['ui'], color=tol_bright['cyan'], label='UI Value')
ax.plot(inflation_idxs['date'], inflation_idxs['normed_ipc'], color=tol_bright['yellow'], label='Normed IPC Value')
ax.set_xlabel('Date')
ax.set_ylabel('Index Value')
ax.set_title('Indexed Units (UI) and Consumer Price Index (IPC) Over Time')
ax.legend()
plt.show()

fig, ax = plt.subplots()
ax.scatter(inflation_idxs['ui'], inflation_idxs['normed_ipc'], color=tol_bright['purple'])
ax.set_xlabel('UI')
ax.set_ylabel('IPC')
ax.set_title('Indexed Units (UI) vs. Consumer Price Index (IPC)')
plt.show()

ipc_matrix = ipc_data[['months', 'ipc']].to_numpy()
m = ipc_matrix.shape[0]
ipc_matrix = np.concatenate((np.ones((m, 1)), ipc_matrix), axis=1)

train_size = int(0.8 * m)

idxs = np.arange(m)
rng.shuffle(idxs)
train_idxs = idxs[:train_size]
test_idxs = idxs[train_size:]
train_idxs.sort()
test_idxs.sort()

X_train = ipc_matrix[train_idxs, :-1]
y_train = ipc_matrix[train_idxs, -1]
X_test = ipc_matrix[test_idxs, :-1]
y_test = ipc_matrix[test_idxs, -1]


inv = np.linalg.inv(np.dot(X_train.T, X_train))
right = np.dot(X_train.T, np.log(y_train))
betas = np.dot(inv, right)

a, b = np.exp(betas)
ann_inf_factor = b**12
print(f'Approximate annual inflation (IPC): {round((ann_inf_factor-1)*100, 4)}%')

preds_train = np.exp(np.dot(X_train, betas))
preds_test = np.exp(np.dot(X_test, betas))

MSE_train = np.mean((y_train-preds_train)**2)
MSE_test = np.mean((y_test-preds_test)**2)

all_preds = np.zeros(m)
all_preds[train_idxs] = preds_train
all_preds[test_idxs] = preds_test

ipc_data['pred_value'] = all_preds
ipc_data = ipc_data[['date', 'months', 'ipc', 'pred_value']]

fig, ax = plt.subplots()
ax.scatter(ipc_data['date'], ipc_data['ipc'] - ipc_data['pred_value'], 
           s=3.0, color=tol_bright['cyan'])
ax.set_xlabel('Date')
ax.set_ylabel('Residual')
ax.set_title('IPC Model Residuals')
plt.show()

fig, ax = plt.subplots()
ax.plot(ipc_data['date'], ipc_data['ipc'], color=tol_bright['cyan'], label='True')
ax.plot(ipc_data['date'], ipc_data['pred_value'], color=tol_bright['purple'], label='Predicted')
ax.set_xlabel('Date')
ax.set_ylabel('IPC')
ax.set_title('True and Predicted Values of IPC Over Time')
ax.legend()
plt.show()





# define function to calculate daily indexed unit (UI) values for a given
# year and a given month from UI and consumer price index (IPC) data 
# (note: rounding in IPC likely to be causing small errors toward the 
# end of the month)
def calc_ui(year: int, month: int) -> list:
    date_string = f'{year}-{str(month).zfill(2)}-05'
    month_1 = month - 1
    month_2 = month - 2
    year_1 = year
    year_2 = year

    # adjust for January
    if month_2 == -1:
        month_1 += 12
        month_2 += 12
        year_1 -= 1
        year_2 -= 1
    # adjust for February
    if month_2 == 0:
        month_2 += 12
        year_2 -= 1

    # define UI formula parameters    
    D_M = pd.to_datetime(date_string, yearfirst=True).days_in_month
    UI_start = ui_data.loc[ui_data['date'] == date_string, 'value'].values[0]    
    UI_end = UI_start
    IPC_1 = ipc_data.loc[(ipc_data['year'] == year_1) & (ipc_data['month'] == month_1), 'ipc'].values[0]
    IPC_2 = ipc_data.loc[(ipc_data['year'] == year_2) & (ipc_data['month'] == month_2), 'ipc'].values[0]
    daily_factor = (IPC_1/IPC_2)**(1/D_M)
    
    # calculate UI values for current month
    month_uis = []    
    for d in range(D_M):
        # calculate each day's UI based on the previous day's UI
        UI_end *= (daily_factor)
        day = (d+5) % D_M + 1
        if day <= 5:
            date = f'{year}-{str(month+1).zfill(2)}-{str(day).zfill(2)}'
        else:
            date = f'{year}-{str(month).zfill(2)}-{str(day).zfill(2)}'
        month_uis.append((date, round(UI_end, 4)))
    return month_uis

test = calc_ui(2026, 4)


