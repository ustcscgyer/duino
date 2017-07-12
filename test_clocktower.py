from duino.clocktower import *
import datetime as dt

class TestWeekdayDistance:
    def test_within_one_week0(self):
        t1 = dt.datetime(2017,7,11)
        t2 = dt.datetime(2017,7,13)
        assert weekday_distance(t1,t2) == 2
        assert weekday_distance(t1,t2, 'backward') == 2

    def test_in_weekend0(self):
        t1 = dt.datetime(2017,7,15)
        t2 = dt.datetime(2017,7,16)
        assert weekday_distance(t1,t2) == 0
        assert weekday_distance(t1,t2, 'backward') == 0

    def test_in_weekend1(self):
        t1 = dt.datetime(2017,7,13)
        t2 = dt.datetime(2017,7,15)
        assert weekday_distance(t1,t2) == 2
        assert weekday_distance(t1,t2, 'backward') == 1

    def test_in_weekend2(self):
        t1 = dt.datetime(2017,7,15)
        t2 = dt.datetime(2017,7,17)
        assert weekday_distance(t1,t2) == 0
        assert weekday_distance(t1,t2, 'backward') == 1

    def test_in_weekend3(self):
        t1 = dt.datetime(2017,7,10)
        t2 = dt.datetime(2017,7,16)
        assert weekday_distance(t1,t2) == 5
        assert weekday_distance(t1,t2, 'backward') == 4
 
    def test_in_weekend4(self):
        t1 = dt.datetime(2017,7,9)
        t2 = dt.datetime(2017,7,14)
        assert weekday_distance(t1,t2) == 4
        assert weekday_distance(t1,t2, 'backward') == 5

    def test_in_weekend4(self):
        t1 = dt.datetime(2017,7,9)
        t2 = dt.datetime(2017,7,16)
        assert weekday_distance(t1,t2) == 5
        assert weekday_distance(t1,t2, 'backward') == 5   