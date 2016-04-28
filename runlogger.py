import os.path
import sys

LOGFILE = 'running_log.txt' 
LOGFILE_UNITS = 'miles' # change to km if you want
KM_TO_MILES = 0.62137 
MILES_TO_KM = 1.60934

CSV_HEADERS = ['date', 'time', 'notes']
ARG_ABBREVIATIONS = {
    '-d': CSV_HEADERS[0],
    '-t': CSV_HEADERS[1],
    '-n': CSV_HEADERS[3],
    '-mi': 'miles',
    '-km': 'kilometers'
}

def display_help():
    print('Simple run logger to save run details in a csv for future inspection.\n')
    print('Arguments:')
    print('-h           display help message')
    print('-d           date of run in YYYY-MM-DD format')
    print('-t           total duration of run in HH:MM format')
    print('-n           notes/comments about the run')
    print('-m           distance ran in miles')
    print('-km          distance ran in kilometers')
    print('Sample usage:')
    print('python runlogger.py -m 5 -t 35:23 -n "hard pace. felt good')
    print('python runlogger.py -km 10.6 -t 56:23 -n "long run"')

def display_error():
    print('There was an issue with one or more of the arguments supplied')
    
def convert_distance(dist, output_units):
    if output_units == 'miles':
        return dist/KM_TO_MILES
    elif output_units == 'km':
        return dist/MILES_TO_KM
    else:
        print("output_units must be km or miles")

def validate_args(args):
    if len(args)%2 != 0:
        return False
    
    for i in range(len(args)):
        if i%2 == 0 and arg[i] not in ARG_ABBREVIATIONS:
            return False

    return True

def parse_args(args):
    # returns a tuple of args and arg values 
    column_args = []
    column_vals = []
    for token in args:
        
    return (column_args, column_vals)

def write_line(file_handle, vals_lst):
    line = ', '.join(vals_lst)
    file_handle.write(line)

def log(csv_header, csv_values, fname):
    file_exists = os.path.isfile(fname)
    with open(fname, 'w') as f:
        if not file_exists:
            write_line(csv_columns)
        write_line(csv_values)

if __name__ == "__main__":
    if len(sys.argv) <= 1 or sys.argv[1] in ['-h', '--help']:
        display_help()
    else:
        args = sys.arv[1:]
        if validate_args(args):
            column_args, column_vals = parse_args(args)
            log(column_args, column_vals, LOGFILE)
        else:
            display_error() 
