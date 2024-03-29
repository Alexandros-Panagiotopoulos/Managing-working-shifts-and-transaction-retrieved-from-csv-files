"""
Please write you name here: Alexandros Panagiotopoulos
"""

import csv

class Error(Exception):
   """Base class for other exceptions"""
   pass

class InvalidTimeStampFormating(Error):
   """Raised when the time stamps are in unexpected format"""
   pass

class InvalidTimeValueException(Error):
   """Raised when the imported times are invalid, like shifts outside operating hours or break outside the shift"""
   pass


def clean_the_break_time_format(time_random_format):
    time_temp_format = time_random_format.replace('PM', '')
    time_temp_format = time_temp_format.replace('pm', '')
    time_temp_format = time_temp_format.replace('AM', '')
    time_temp_format = time_temp_format.replace('am', '')
    time_temp_format = time_temp_format.replace(' ', '')
    break_start_cleaned_format, break_end_cleaned_format = time_temp_format.split("-")
    return break_start_cleaned_format, break_end_cleaned_format

def format_time_in_hours_from_midnight(time_cleaned_format):
    time_temp_format = time_cleaned_format.replace('.', ':')
    if ":" in time_temp_format:     #If minutes are contained in the time format
        time_temp_format_hours, time_temp_format_min = time_temp_format.split(":")
    else:
        time_temp_format_hours = time_temp_format
        time_temp_format_min = None
    time_format_hours = int(time_temp_format_hours)
    if time_format_hours < 8:  #Assume that shift starts the earliest at 8 so any hour with lower value is at pm
        time_format_hours += 12
    if time_temp_format_min:
        time_temp_format_min = int(time_temp_format_min)
        time_temp_format_min = time_temp_format_min / 60
        time_format_hours += time_temp_format_min
    return time_format_hours

def get_time_in_hours_from_midnight(time, time_position, line):
    if time_position == 0: #Dealing with the break period
        try:
            break_start_cleaned_format, break_end_cleaned_format = clean_the_break_time_format(time)
        except:
            raise InvalidTimeStampFormating("Invalid entry in line "+str(line+1) +" of 'shifts.csv. Please separate the start and end of the break with a '-'")
        try:
            break_start_in_hours_from_midnight = format_time_in_hours_from_midnight(break_start_cleaned_format)
            break_end_in_hours_from_midnight = format_time_in_hours_from_midnight(break_end_cleaned_format)
        except:
            raise InvalidTimeStampFormating("Invalid entry in line "+str(line+1) +" of 'shifts.csv. An unexpected format at a break time stamp was recieved, please avoid any special character or letter except from '.',':' and 'pm'")
        return break_start_in_hours_from_midnight, break_end_in_hours_from_midnight
    elif time_position == 1: #Dealing with the end of the shifts
        try:
            shift_end_in_hours_from_midnight = format_time_in_hours_from_midnight(time)
        except:
            raise InvalidTimeStampFormating("Invalid entry in line "+str(line+1) +" of 'shifts.csv. An unexpected format at the end of a shift was recieved, please use format like '22:16'")
        return shift_end_in_hours_from_midnight
    else:   #Dealing with the start of the shifts
        try:
            shift_start_in_hours_from_midnight = format_time_in_hours_from_midnight(time)
        except:
            raise InvalidTimeStampFormating("Invalid entry in line "+str(line+1) +" of 'shifts.csv. An unexpected format at the beginning of a shift was recieved, please use format like '13:12'")
        return shift_start_in_hours_from_midnight

def create_dict_with_keys_per_hour_in_operating_hours(operating_hours = [9,23]):
    dictionary = dict()
    for hour in range(int(operating_hours[0]), int(operating_hours[1])):
        dictionary[hour] = 0
    return dictionary

def format_dictionary_keys(dictionary):
    formated_dictionary = dict()
    for hour in dictionary:
        new_key = str(hour) + ":00"
        formated_dictionary[new_key] = dictionary[hour]
    return formated_dictionary

def calculate_hourly_cost_of_shift(hour, start, end, rate):
    if int(start) == hour:
        cost = ((hour + 1) - start) * rate
    else:
        cost = rate
    if int(end) == hour:
        cost -= ((hour + 1) - end) * rate
    return cost

def check_if_time_stamps_are_valid(shift_start, shift_end, break_start, break_end, operating_hours, line):
    if (shift_start < operating_hours[0] or
        shift_end > operating_hours[1] or
        shift_start > shift_end or
        break_start < shift_start or
        break_end > shift_end or
        break_start >  break_end):
        raise InvalidTimeValueException ("Invalid entry in line "+str(line+1) +" of 'shifts.csv. Please make sure shifts periods are inside operating hours and break periods inside\
                             shifts periods. Also in high PM hours please use 24 hour format like '22:10'")

def process_shifts(path_to_csv):
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
    operating_hours = [9, 23]    #Assume operating hours for the restaurant from 9 to 23
    # The above should have been in a higher level function but there are istruction not to change the main
    shifts = create_dict_with_keys_per_hour_in_operating_hours(operating_hours) 
    with open (path_to_csv) as shifts_path:
        reader = csv.reader(shifts_path)
        next(reader)    #skip the header
        time_positions = [0, 1, 3]
        for line, shift in enumerate(reader):
            rate = float(shift[2])
            for time_position in time_positions:
                if time_position == 0:
                    break_start, break_end = get_time_in_hours_from_midnight(shift[time_position], time_position, line)
                elif time_position == 1:
                    shift_end = get_time_in_hours_from_midnight(shift[time_position], time_position, line)
                else:
                    shift_start = get_time_in_hours_from_midnight(shift[time_position], time_position, line)
            check_if_time_stamps_are_valid(shift_start, shift_end, break_start, break_end, operating_hours, line)
            for hour in shifts:
                if int(shift_start) <= hour <= shift_end:
                    cost = calculate_hourly_cost_of_shift(hour, shift_start, shift_end, rate)
                    if int(break_start) <= hour <= break_end:
                        cost -= calculate_hourly_cost_of_shift(hour, break_start, break_end, rate) #reduce the cost amount while on a break
                    shifts[hour] += cost
    shifts = format_dictionary_keys(shifts)
    return shifts

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
    sales = create_dict_with_keys_per_hour_in_operating_hours() 
    with open (path_to_csv) as sales_path:
        reader = csv.reader(sales_path)
        next(reader)    #skip the header
        for sale in reader:
            hour = int(sale[1][0:2])
            sales[hour] += float(sale[0])
    sales = format_dictionary_keys(sales)
    return sales

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
    percentages = create_dict_with_keys_per_hour_in_operating_hours() 
    percentages = format_dictionary_keys(percentages)
    for hour in percentages:
        if sales[hour] != 0:
            percentages[hour] = sales[hour] / shifts[hour]
        else:
            percentages [hour] = -shifts[hour]
    return percentages

def best_and_worst_hour(percentages):
    """
    Args:
    percentages: output of compute_percentage
    Return: list of strings, the first element should be the best hour,
    the second (and last) element should be the worst hour. Hour are
    represented by string with format %H:%M
    e.g. ["18:00", "20:00"]
    """
    best_hour = max(percentages, key=percentages.get)
    worst_hour = min(percentages, key=percentages.get)
    return best_hour, worst_hour

def main(path_to_shifts, path_to_sales):
    """
    Do not touch this function, but you can look at it, to have an idea of
    how your data should interact with each other
    """

    shifts_processed = process_shifts(path_to_shifts)
    sales_processed = process_sales(path_to_sales)
    percentages = compute_percentage(shifts_processed, sales_processed)
    best_hour, worst_hour = best_and_worst_hour(percentages)
    # print (shifts_processed)
    # print (sales_processed)
    # print (percentages)
    # print(best_hour, worst_hour)
    return best_hour, worst_hour #best_hour, worst_hour

if __name__ == '__main__':
    # You can change this to test your code, it will not be used
    path_to_sales = "transactions.csv"
    path_to_shifts = "work_shifts.csv"
    best_hour, worst_hour = main(path_to_shifts, path_to_sales)

# Please write you name here: Panagiotopoulos Alexandros
