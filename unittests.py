import unittest
from EmptySolution import Error, InvalidTimeStampFormating, InvalidTimeValueException, get_time_in_hours_from_midnight, process_shifts, process_sales

class SolutionTestCase(unittest.TestCase):
    """Test for Emptysolution.py"""

    def test_get_time_for_simple_break_format(self):
        break_start, break_end = get_time_in_hours_from_midnight ('15-18', 0)

        self.assertEqual(break_start, 15)
        self.assertEqual(break_end, 18)

    def test_get_time_for_break_format_with_PM(self):
        break_start, break_end = get_time_in_hours_from_midnight ('4PM-5PM', 0)

        self.assertEqual(break_start, 16)
        self.assertEqual(break_end, 17)

    def test_get_time_with_break_format_with_minutes(self):
        break_start, break_end = get_time_in_hours_from_midnight ('4-4.30PM', 0)

        self.assertEqual(break_start, 16)
        self.assertEqual(break_end, 16.5)

    def test_get_time_for_shift_start(self):
        shift_start = get_time_in_hours_from_midnight ('10.45', 3)

        self.assertEqual(shift_start, 10.75)

    def test_get_time_for_shift_end(self):
        shift_end = get_time_in_hours_from_midnight ('5.15', 1)

        self.assertEqual(shift_end, 17.25)

    def test_get_time_raise_exception_because_of_invalid_break_start_end_separation(self):
        with self.assertRaises(InvalidTimeStampFormating) as error:
            get_time_in_hours_from_midnight ('15_18', 0)
        self.assertEqual("Please separate the start and end of the break with a '-'", str(error.exception))

    def test_get_time_raise_exception_because_of_invalid_time_stamp_format(self):
        with self.assertRaises(InvalidTimeStampFormating) as error:
            get_time_in_hours_from_midnight ('15h', 1)
        self.assertEqual("An unexpected format at the end of a shift was recieved, please use format like '22:16'", str(error.exception))

    def test_process_shifts(self):
        shifts = process_shifts("unittest_work_shifts.csv")
        shifts_check = ({'9:00': 20.0, '10:00': 20.0, '11:00': 20.0, '12:00': 20.0, '13:00': 20.0, '14:00': 20.0, '15:00': 20.0,
         '16:00': 16.666666666666643, '17:00': 20.0, '18:00': 26.0, '19:00': 32.0, '20:00': 32.0, '21:00': 32.0, '22:00': 32.0})

        self.assertEqual(shifts, shifts_check)

    def test_process_sales(self):
        sales = process_sales("unittest_transactions.csv")
        sales_check = ({'9:00': 0, '10:00': 130.88, '11:00': 300.65, '12:00': 0, '13:00': 0, '14:00': 0, '15:00': 0,
         '16:00': 0, '17:00': 0, '18:00': 0, '19:00': 0, '20:00': 0, '21:00': 0, '22:00': 0})
        print (sales)
        self.assertEqual(sales, sales_check)

#Many more tests should be included but ommited as they considered beyond the scope of current test

unittest.main()