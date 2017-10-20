"""
Author: Giovanni Ge
Created: 2017/03/30
Last Modification: 2017/09/12

This module provides various of objects and methods related to time
"""
import datetime as dt, pandas as pd
from pandas.tseries.offsets import CustomBusinessDay, Easter, Day
from pandas.tseries.holiday import AbstractHolidayCalendar, sunday_to_monday, \
    nearest_workday, Holiday, USFederalHolidayCalendar
from pandas import DateOffset
import warnings
import pdb

from pandas.tseries.holiday import *
from pandas.tseries.offsets import CustomBusinessDay, CustomBusinessHour

now = dt.datetime.now
today = dt.date.today

class USFinancialHolidayCalendar(AbstractHolidayCalendar):
    """
    US Financial Calendar
    https://www.nyse.com/markets/hours-calendars
    """
    rules = [
        # New Years have difference observance method because the preceeding 
        # Friday is year end and exchange is open
        Holiday('New Years Day', month=1, day=1, observance=sunday_to_monday),
        USMartinLutherKingJr,
        USPresidentsDay,
        USMemorialDay,
        Holiday('July 4th', month=7, day=4, observance=nearest_workday),
        USLaborDay,
        GoodFriday,
        USThanksgivingDay,
        Holiday('Christmas', month=12, day=25, observance=nearest_workday)
    ]

# US business day
us_bd = CustomBusinessDay(calendar=USFederalHolidayCalendar())
# US financial business day
fi_bd = CustomBusinessDay(calendar=USFinancialHolidayCalendar())
fi_holidays = USFinancialHolidayCalendar().holidays
_ = fi_holidays('19500101', '20500101') # Activate the holiday for better efficiency

# US Exchange bussiness hour
fi_bh = CustomBusinessHour(calendar=USFederalHolidayCalendar(), start='9:30', end='16:30')

def weekday_distance(t1, t2, convention='forward'):
    """ Number of weekdays between t1 and t2: t2 - t1
    Rolling forward convention: from 0 am+ to 0 am+
    example: Friday to Saturday is 1
             Sunday to Monday is 0
    Rolling back convention: from 0 am- to 0 am -
    example: Friday to Saturday is 0
             Sunday to Monday is 1
    Parameters
    -------------
        t1: datetime.date
        t2: datetime.date
    convention: str, 'forward' or 'backward'
    """
    if t2 < t1:
        return -1 * weekday_distance(t2, t1, convention)

    # Portions that is more than one week
    n0 = (t2.toordinal() - t1.toordinal()) // 7 * 5
    # Portions that is smaller than one week
    wd1, wd2 = t1.weekday(), t2.weekday()
    # Mathematical magic
    if convention == 'forward':
        wd_map = [0,1,2,3,4,5,5]
    elif convention == 'backward':
        wd_map = [0,1,2,3,4,4,4]
    else:
        raise ValueError('wrong convetion')
    if wd2 >= wd1:
        n1 = wd_map[wd2]-wd_map[wd1]
    else:
        n1 = 5 + wd_map[wd2]-wd_map[wd1]

    return n0 + n1

def cbday_distance(t1, t2, holidays=fi_holidays, convention='forward'):
    """ Number of custom business days between t1 and t2: t2 - t1
    Rolling forward convention: from 0 am+ to 0 am+
    example: Friday to Saturday is 1
             Sunday to Monday is 0
    Rolling back convention: from 0 am- to 0 am -
    example: Friday to Saturday is 0
             Sunday to Monday is 1
    Parameters
    -------------
    t1: datetime
    t2: datetime
    holidays: list of holidays
    convention: str, 'forward' or 'backward'
    """
    # First calculate number of weekdays
    if t1 > t2:
        return -1 * cbday_distance(t2, t1, holidays, convention)

    wkd_dis = weekday_distance(t1, t2, convention)
    if holidays is None: return wkd_dis

    # Calculate number of holidays that is not weekends
    dates = holidays(t1, t2)

    # if convention == 'forward':
    #     # dates = holidays[(holidays >= t1) & (holidays < t2)]
    #     dates = holidays(t1,t2)
    # elif convention == 'backward':
    #     dates = holidays(t1,t2)
    #     # dates = holidays[(holidays > t1) & (holidays <= t2)]
    # else:
    #     raise ValueError('wrong convetion')

    nh = len([d for d in dates if d.weekday() <= 4])
    
    return wkd_dis - nh
    
def bizday_distance(t1, t2, offset=fi_bd):
    """ For given two datetime, this module calculates their difference in number of bussiness
    days.
    i.g.: bizday_diff(dt.datetime(2017,1,4), dt.datetime(2017,1,5)) = 1
    """
    warnings.warn('Depreciated. Use cbday_distance instead')
    if t1 < t2:
        dday = max(len(pd.bdate_range(t1, t2, freq=offset)) - 1, 0)
    else:
        dday = min(1 - len(pd.bdate_range(t2, t1, freq=offset)),0)
    return dday

def intra_time_diff(t1, t2, mrkt_open_time=dt.time(9,30), mrkt_close_time=dt.time(16,0), holidays=fi_holidays):
    """ For given two datetime, this module calculates their difference in minutes, 
    if two inputs are from different days, each day if treated as number of minutes between 
    mrkt_open_time and mrkt_close_time. 
    The time difference is adjusted for weekends and holidays
    i.g.: intra_time_diff(dt.datetime(2017,1,4,9), dt.datetime(2017,1,5,10)) = 450
        (1day == 390 + 1 hour == 60 ==> 450)

    This new imiplementation is 100 times faster than the previous one!!! 
    """
    # Just for convenience
    if not isinstance(t1, pd.Series):
        t1 = pd.Series(t1)
    if not isinstance(t2, pd.Series):
        t2 = pd.Series(t2)

    t1 = pd.concat([t1.rename('datetime'), t1.dt.time.rename('time'), t1.dt.date.rename('date'), 
                t1.dt.hour.rename('hour'), t1.dt.minute.rename('minute')], axis=1)
    t2 = pd.concat([t2.rename('datetime'), t2.dt.time.rename('time'), t2.dt.date.rename('date'), 
                t2.dt.hour.rename('hour'), t2.dt.minute.rename('minute')], axis=1)

    t1.loc[t1.time < mrkt_open_time, ['time', 'hour', 'minute']] = \
        [mrkt_open_time, mrkt_open_time.hour, mrkt_open_time.minute]
    t1.loc[t1.time > mrkt_close_time, ['time', 'hour', 'minute']] = \
        [mrkt_close_time, mrkt_close_time.hour, mrkt_close_time.minute]
    t2.loc[t2.time < mrkt_open_time, ['time', 'hour', 'minute']] = \
        [mrkt_open_time, mrkt_open_time.hour, mrkt_open_time.minute]
    t2.loc[t2.time > mrkt_close_time, ['time', 'hour', 'minute']] = \
        [mrkt_close_time, mrkt_close_time.hour, mrkt_close_time.minute]

    if len(t1) == 1: t1 = t1.iloc[0]
    if len(t2) == 1: t2 = t2.iloc[0]

    minutes_of_day = 60*(mrkt_close_time.hour - mrkt_open_time.hour) + \
        (mrkt_close_time.minute - mrkt_open_time.minute)

    if isinstance(t1, pd.Series) & isinstance(t2, pd.Series):
        input_table = pd.DataFrame({'date1':t1.date, 'date2':t2.date}, index=[0])
    else:
        input_table = pd.DataFrame({'date1':t1.date, 'date2':t2.date})

    # Use Unique table to boost efficiency
    unique_input_table = input_table.drop_duplicates().copy()
    # fi_holidays(unique_input_table.min().min(), unique_input_table.max().max()) #Activate for better performance

    # dday = input_table.apply(lambda x: cbday_distance(x.date1, x.date2, holidays), axis=1)
    unique_input_table['dday'] = unique_input_table.apply(lambda x: cbday_distance(x.date1, x.date2, holidays), axis=1)

    dday = pd.merge(input_table.assign(order=input_table.index), 
        unique_input_table, on=['date1', 'date2']).set_index('order').dday

    result = minutes_of_day*dday + 60*(t2.hour - t1.hour) + (t2.minute - t1.minute)

    if len(result) == 1:
        result = result.iloc[0]
        
    return result
