"""
Please write you name here: Alexandros Panagiotopoulos
"""

import csv

def clean_the_break_time_format(time_random_format):
    time_temp_format = time_random_format.replace('PM', '')
    time_temp_format = time_temp_format.replace('pm', '')
    time_temp_format = time_temp_format.replace('AM', '')
    time_temp_format = time_temp_format.replace('am', '')
    time_temp_format = time_temp_format.replace(' ', '')
    break_start_cleaned_format, break_end_cleaned_format = time_temp_format.split("-")
    return break_start_cleaned_format, break_end_cleaned_format

def get_time_in_hours_from_midnight(time_random_format, time_position):
    if time_position == 0: #Dealing with the break period
        break_start_cleaned_format, break_end_cleaned_format = clean_the_break_time_format(time_random_format)
        print(break_start_cleaned_format, break_end_cleaned_format)
        return break_start_cleaned_format, break_end_cleaned_format
        

    

def process_shifts(path_to_csv):

    with open (path_to_csv) as shifts_path:
        reader = csv.reader(shifts_path)
        header_row = next(reader)
        
        time_positions = [0, 1, 3]
        for shift in reader:
            for time_position in time_positions:
                if time_position == 0:
                    break_start, break_end = get_time_in_hours_from_midnight(shift[time_position], time_position)
                elif time_position == 1:
                    shift_end = get_time_in_hours_from_midnight(shift[time_position], time_position)
                else:
                    shift_start = get_time_in_hours_from_midnight(shift[time_position], time_position)
                

    """

    :param path_to_csv: The path to the work_shift.csv
    :type string:
    :return: A dictionary with time as key (string) with format %H:%M
        (e.g. "18:00") and cost as value (Number)
    For example, it should be something like :
    {
        "17:00": 50,
        "22:00: 40,
    }
    In other words, for the hour beginning at 17:00, labour cost was
    50 pounds
    :rtype dict:
    """
    return None


def process_sales(path_to_csv):
    """

    :param path_to_csv: The path to the transactions.csv
    :type string:
    :return: A dictionary with time (string) with format %H:%M as key and
    sales as value (string),
    and corresponding value with format %H:%M (e.g. "18:00"),
    and type float)
    For example, it should be something like :
    {
        "17:00": 250,
        "22:00": 0,
    },
    This means, for the hour beginning at 17:00, the sales were 250 dollars
    and for the hour beginning at 22:00, the sales were 0.

    :rtype dict:
    """
    return None

def compute_percentage(shifts, sales):
    """

    :param shifts:
    :type shifts: dict
    :param sales:
    :type sales: dict
    :return: A dictionary with time as key (string) with format %H:%M and
    percentage of labour cost per sales as value (float),
    If the sales are null, then return -cost instead of percentage
    For example, it should be something like :
    {
        "17:00": 20,
        "22:00": -40,
    }
    :rtype: dict
    """
    return None

def best_and_worst_hour(percentages):
    """

    Args:
    percentages: output of compute_percentage
    Return: list of strings, the first element should be the best hour,
    the second (and last) element should be the worst hour. Hour are
    represented by string with format %H:%M
    e.g. ["18:00", "20:00"]

    """

    return

def main(path_to_shifts, path_to_sales):
    """
    Do not touch this function, but you can look at it, to have an idea of
    how your data should interact with each other
    """

    shifts_processed = process_shifts(path_to_shifts)
    sales_processed = process_sales(path_to_sales)
    # percentages = compute_percentage(shifts_processed, sales_processed)
    # best_hour, worst_hour = best_and_worst_hour(percentages)
    return None, None #best_hour, worst_hour

if __name__ == '__main__':
    # You can change this to test your code, it will not be used
    path_to_sales = "c:/Users/alex/code/python/Tenzo_coding_test/transactions.csv"
    path_to_shifts = "c:/Users/alex/code/python/Tenzo_coding_test/work_shifts.csv"
    best_hour, worst_hour = main(path_to_shifts, path_to_sales)


# Please write you name here:
