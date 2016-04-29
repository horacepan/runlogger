import os.path
import sys
import re
import datetime

LOGFILE = 'running_log.txt' # name it w/e you want

# TODO: Allow users to specify distance of miles or kms eventually
KM_TO_MILES = 0.62137 
MILES_TO_KM = 1.60934

ARG_DATE = '-d'
ARG_TIME = '-t'
ARG_NOTES = '-n'
ARG_MILES= '-m'
ARG_KMS = '-km'
ARG_ABBREVIATIONS = {
    ARG_DATE: 'date',
    ARG_TIME: 'time',
    ARG_NOTES: 'notes',
    ARG_MILES: 'miles',
}
CSV_HEADER_ORDER = [ARG_DATE, ARG_TIME, ARG_MILES, ARG_NOTES]
CSV_HEADER_NAMES = map(lambda x: ARG_ABBREVIATIONS.get(x, ''), CSV_HEADER_ORDER)

def display_help():
    print('Simple run logger to save run details in a csv for future inspection.\n')
    print('Arguments:')
    print('-h           display help message')
    #print('-d           date of run in YYYY-MM-DD format') # TODO: Put back in
    print('-t           total duration of run in HH:MM format')
    print('-n           notes/comments about the run')
    print('-m           distance ran in miles')
    print('-km          distance ran in kilometers')
    print('Sample usage:')
    print('python runlogger.py -m 5 -t 35:23 -n "hard pace. felt good')
    
def convert_distance(dist, output_units):
    if output_units == 'miles':
        return dist/KM_TO_MILES
    elif output_units == 'km':
        return dist/MILES_TO_KM
    else:
        print("output_units must be km or miles")

# TODO: Maybe not the best way to do this.
def validate_arg(arg_name, arg_val):
    '''
        return:
            True or False depending on whether or not given arg_val is appropriate for
            the given arg_name
        inputs:
            arg_name: a string. Should be one of the keys of ARG_ABBREVIATIONS
            arg_val: a string
    '''
    if arg_name == ARG_TIME:
        # Allow user to omit the hours since most runs will probably be less than an hour
        time_regex = re.compile("[0-2]?[0-3]:[0-5][0-9]:[0-5][0-9]|[0-5][0-9]:[0-5][0-9]")
        if not re.match(time_regex, arg_val):
            print("Incorrect time format: should be 'HH:MM:SS'")
            return False
    if arg_name == ARG_MILES or arg_name == ARG_KMS:
        try:
            float(arg_val)
        except ValueError:
            print("Incorrect distance format: should be a float")
            return False

    # No restrictions for ARG_NOTES
    return True

def validate_args(arg_names, arg_vals):
    '''
        return:
            True or False depending on whether or not every arg_val is appropriate for
            its corresponding arg_name
        inputs:
            arg_names: list of strings
            arg_vals: list of strings that should be parallel to arg_names
    '''
    # Every arg_name should have a corresponding arg_value
    if len(arg_names) != len(arg_vals):
        print("Incorrect number of arguments")
        return False
    
    for name in arg_names:
        if name not in ARG_ABBREVIATIONS:
            print("%s is not a valid argument" %name)
            return False

    for (arg_name, arg_val) in zip(arg_names, arg_vals):
        if not validate_arg(arg_name, arg_val):
            return False

    if (ARG_KMS not in arg_names or ARG_MILES not in arg_names) and ARG_TIME not in arg_names:
        print("You must supply either the distance of duration of the run")
        return False
    if ARG_KMS in arg_names and ARG_MILES in arg_names:
        print("Supply your distance in miles or in kms, but not both!")
        return False

    return True

def get_csv_vals(arg_names, arg_vals):
    '''
        return:
            a list of strings(in the desired order as determined by the csv header) to write to the log csv file 
        inputs:
            arg_names: list of strings
            arg_vals: list of strings parallel to arg_names
    '''
    csv_line = []
    # TODO: Sort of gross
    for csv_col in CSV_HEADER_ORDER:
        if csv_col not in arg_names:
            if csv_col == ARG_DATE:
                csv_line.append(str(datetime.date.today()))
            else:
                csv_line.append('')
        else:
            index = arg_names.index(csv_col)
            csv_line.append(arg_vals[index])

    return csv_line

def write_line(file_handle, vals_lst):
    line = ', '.join(vals_lst)
    line = line + '\n'
    file_handle.write(line)

# Order matters
def log(csv_values, fname):
    '''
        return:
            Nothing. Writes the csv_values to a file specified by fname
        inputs:
            csv_values: list of strings to write on a single line in a csv file
            fname: string name of the file to write the given csv values to
    '''
    file_exists = os.path.isfile(fname)
    print('does file exist: ', file_exists)
    with open(fname, 'w') as f:
        if not file_exists:
            write_line(f, CSV_HEADER_NAMES)
        write_line(f, csv_values)

if __name__ == "__main__":
    if len(sys.argv) <= 1 or sys.argv[1] in ['-h', '--help']:
        display_help()
    else:
        arg_names = sys.argv[1::2]
        arg_vals = sys.argv[2::2]
        if validate_args(arg_names, arg_vals):
            csv_vals = get_csv_vals(arg_names, arg_vals)
            log(csv_vals, LOGFILE)
