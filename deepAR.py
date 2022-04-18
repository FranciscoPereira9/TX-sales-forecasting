import numpy as np
import pandas as pd

# Read data
# Read Data
train = pd.read_csv("data/sales_train_validation_afcs2021.csv",index_col=0, header=None, low_memory=False).T
calendar = pd.read_csv("data/calendar_afcs2021.csv")
prices = pd.read_csv("data/sell_prices_afcs2021.csv")
test = pd.read_csv("data/sales_test_validation_afcs2021.csv",index_col=0, header=None, low_memory=False).T
# Calendar Pre-Processing
event_names_1 = list(calendar.event_name_1.unique())
event_names_2 = list(calendar.event_name_2.unique())
event_names = event_names_1 + [i for i in event_names_2 if i not in event_names_1]
event_names = event_names[1:]
event_type_1 = list(calendar.event_type_1.unique())
event_type_2 = list(calendar.event_type_2.unique())
event_type = event_type_1 + [i for i in event_type_2 if i not in event_type_1]
event_type = event_type[1:]
# One Hot Encode
calendar = pd.get_dummies(calendar, columns=['event_name_1', 'event_type_1'], prefix='one', prefix_sep='_')
calendar = pd.get_dummies(calendar, columns=['event_name_2', 'event_type_2'], prefix='two', prefix_sep='_')
# Event Types
calendar['Religious'] = calendar['one_Religious'] | calendar['two_Religious']
calendar['Cultural'] = calendar['one_Cultural'] | calendar['two_Cultural']
calendar['Sporting'] = calendar['one_Sporting']
calendar['National'] = calendar['one_National']
# Event Names
for event in event_names:
    one_event = "one_"+event
    two_event = "two_"+event
    if one_event in calendar.columns and two_event in calendar.columns:
        calendar[event] = calendar[one_event] | calendar [two_event]
    elif one_event in calendar.columns and two_event not in calendar.columns:
        calendar[event] = calendar[one_event]
    else:
        calendar[event] = calendar[two_event]
# Drop Columns
to_drop = [col for col in calendar.columns if (col.startswith("one_")) or col.startswith("two_")]
calendar.drop(columns=to_drop, inplace=True)
# Train Dataframe
# Assert Columns as Intergers
food_columns = [col for col in train.columns if col.startswith("FOODS")]
map_types = {}
for c in food_columns:
    train[c] = train[c].astype('int64')
    test[c] = test[c].astype('int64')
# Merge Train Dataframe with Calendar
train = train.merge(calendar, left_on="id", right_on="d", suffixes=["","_right"])
train["date"] = pd.DatetimeIndex(train['date'])
# Merge Test Dataframe with Calendar
test = test.merge(calendar, left_on="id", right_on="d", suffixes=["","_right"])
test["date"] = pd.DatetimeIndex(test['date'])
# Get Cumulative Sum on FOODS
#train[food_columns] = train[food_columns].cumsum()

