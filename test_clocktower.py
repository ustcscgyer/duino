from duino.clocktower import *
import datetime as dt

class TestWeekdayDistance:
    def test_within_one_week0(self):
        # From Tu to Fr
        t1 = dt.datetime(2017,7,11)
        t2 = dt.datetime(2017,7,13)
        assert weekday_distance(t1,t2) == 2
        assert weekday_distance(t1,t2, 'backward') == 2

    def test_in_weekend0(self):
        # From Sa to Su
        t1 = dt.datetime(2017,7,15)
        t2 = dt.datetime(2017,7,16)
        assert weekday_distance(t1,t2) == 0
        assert weekday_distance(t1,t2, 'backward') == 0

    def test_in_weekend1(self):
        # from Th to Sa
        t1 = dt.datetime(2017,7,13)
        t2 = dt.datetime(2017,7,15)
        assert weekday_distance(t1,t2) == 2
        assert weekday_distance(t1,t2, 'backward') == 1

    def test_in_weekend2(self):
        # From Sa to Mo
        t1 = dt.datetime(2017,7,15)
        t2 = dt.datetime(2017,7,17)
        assert weekday_distance(t1,t2) == 0
        assert weekday_distance(t1,t2, 'backward') == 1

    def test_in_weekend3(self):
        # From Mo to Sa
        t1 = dt.datetime(2017,7,10)
        t2 = dt.datetime(2017,7,15)
        assert weekday_distance(t1,t2) == 5
        assert weekday_distance(t1,t2, 'backward') == 4

    def test_in_weekend4(self):
        # From Tu to Su
        t1 = dt.datetime(2017,7,10)
        t2 = dt.datetime(2017,7,16)
        assert weekday_distance(t1,t2) == 5
        assert weekday_distance(t1,t2, 'backward') == 4
 
    def test_in_weekend5(self):
        # From Su to Fr
        t1 = dt.datetime(2017,7,9)
        t2 = dt.datetime(2017,7,14)
        assert weekday_distance(t1,t2) == 4
        assert weekday_distance(t1,t2, 'backward') == 5

    def test_in_weekend6(self):
        # From Sa to Fr
        t1 = dt.datetime(2017,7,8)
        t2 = dt.datetime(2017,7,14)
        assert weekday_distance(t1,t2) == 4
        assert weekday_distance(t1,t2, 'backward') == 5

    def test_in_weekend7(self):
        # From Su to Su
        t1 = dt.datetime(2017,7,9)
        t2 = dt.datetime(2017,7,16)
        assert weekday_distance(t1,t2) == 5
        assert weekday_distance(t1,t2, 'backward') == 5   

    def test_cross_weekend0(self):
        # From Tu to Mo
        t1 = dt.datetime(2017,7,11)
        t2 = dt.datetime(2017,7,17)
        assert weekday_distance(t1,t2) == 4
        assert weekday_distance(t1,t2, 'backward') == 4

    def test_cross_weekend1(self):
        # From Tu to Tu
        t1 = dt.datetime(2017,7,11)
        t2 = dt.datetime(2017,7,18)
        assert weekday_distance(t1,t2) == 5
        assert weekday_distance(t1,t2, 'backward') == 5

    def test_cross_weekend2(self):
        # From Tu to We
        t1 = dt.datetime(2017,7,11)
        t2 = dt.datetime(2017,7,19)
        assert weekday_distance(t1,t2) == 6
        assert weekday_distance(t1,t2, 'backward') == 6

    def test_cross_weekend3(self):
        # From Su to Sa
        t1 = dt.datetime(2017,7,9)
        t2 = dt.datetime(2017,7,15)
        assert weekday_distance(t1,t2) == 5
        assert weekday_distance(t1,t2, 'backward') == 5

    def test_parity(self):
        dates = [dt.datetime(2017,7,i) for i in range(9,19)]
        for i in range(len(dates)):
            for j in range(i+1, len(dates)):
                weekday_distance(dates[i], dates[j]) == \
                    - weekday_distance(dates[j], dates[i])
                weekday_distance(dates[i], dates[j], 'backward') == \
                    - weekday_distance(dates[j], dates[i], 'backward')
