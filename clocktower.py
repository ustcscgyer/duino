from pandas.tseries.holiday import *
from pandas.tseries.offsets import CustomBusinessDay, CustomBusinessHour

class USFinancialHolidayCalendar(USFederalHolidayCalendar):
    """
    US Financial Calendar
    """
    def __init__(self):
        self.rules = [
            Holiday('New Years Day', month=1, day=1, observance=nearest_workday),
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
us_bd = CustomBusinessDay(calendar = USFederalHolidayCalendar())
# US financial business day
fi_bd = CustomBusinessDay(calendar = USFinancialHolidayCalendar())
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
        t1: datetime
        t2: datetime
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
        wd_map = [1,2,3,4,5,0,0]

    n1 = wd_map[wd2]-wd_map[wd1]
    if n1 < 0: n1 += 5

    return n0 + n1

def cbday_distance(t1, t2, cbd = None, convention = 'forward'):
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
    cbd: CustomBusinessDay
    convention: str, 'forward' or 'backward'
    """
    pass