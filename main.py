from report_parser import ReportParser, AwakeWithoutAsleepException, FallAsleepException, GuardNotAwakeException, InvalidTimeFlowException
import os.path
import unittest


class Tests(unittest.TestCase):
    # Test 1 - Classic example
    def test_1(self):
        rp = ReportParser('{}{}'.format(os.path.dirname(__file__), '/reports/report1'))
        result = rp.get_most_sleepy_guard()
        assert result == 'Guard #10 is most likely to be asleep in 00:24', 'Should be: Guard #10 is most likely to be asleep in 00:24'

    # Test 2 - No sleeping guards
    def test_2(self):
        rp = ReportParser('{}{}'.format(os.path.dirname(__file__), '/reports/report2'))
        result = rp.get_most_sleepy_guard()
        assert result == 'Guards are doing their job', 'Should be: Guards are doing their job'

    # Test 3 - Two 'falls asleep' in a row
    def test_3(self):
        rp = ReportParser('{}{}'.format(os.path.dirname(__file__), '/reports/report3'))
        with self.assertRaises(FallAsleepException):
            rp.get_most_sleepy_guard()

    # Test 4 - 'wakes up' without prior 'falls asleep'
    def test_4(self):
        rp = ReportParser('{}{}'.format(os.path.dirname(__file__), '/reports/report4'))
        with self.assertRaises(AwakeWithoutAsleepException):
            rp.get_most_sleepy_guard()

    # Test 5 - no wake up right after falls asleep
    def test_5(self):
        rp = ReportParser('{}{}'.format(os.path.dirname(__file__), '/reports/report5'))
        with self.assertRaises(AwakeWithoutAsleepException):
            rp.get_most_sleepy_guard()

    # Test 6 - guard remains asleep
    def test_6(self):
        rp = ReportParser('{}{}'.format(os.path.dirname(__file__), '/reports/report6'))
        with self.assertRaises(GuardNotAwakeException):
            rp.get_most_sleepy_guard()

    # Test 7 - another classic run, this time guard #99 is most sleepy one
    def test_7(self):
        rp = ReportParser('{}{}'.format(os.path.dirname(__file__), '/reports/report7'))
        result = rp.get_most_sleepy_guard()
        assert result == 'Guard #99 is most likely to be asleep in 00:36', 'Should be: Guard #99 is most likely to be asleep in 00:36'

    # Test 8 - Invalid time flow
    def test_8(self):
        rp = ReportParser('{}{}'.format(os.path.dirname(__file__), '/reports/report8'))
        with self.assertRaises(InvalidTimeFlowException):
            rp.get_most_sleepy_guard()
