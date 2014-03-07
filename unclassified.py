import os
import sys
import subprocess
import time

months = {'01': 'JAN', '02': 'FEB', '03': 'MAR', '04': 'APR', '05': 'MAY',
          '06': 'JUN', '07': 'JUL', '08': 'AUG', '09': 'SEP', '10': 'OCT',
          '11': 'NOV', '12': 'DEC'}

def get_creation_time(path):
    if sys.platform.startswith('linux'):
        flag = '-c %Y'
    else:  # OS X
        flag = '-f %B'

    p = subprocess.Popen(['stat', flag, path],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if p.wait():
        raise OSError(p.stderr.read().rstrip())
    else:
        return int(p.stdout.read())

def parse_date_tstamp(fname):
    """extract date info from file timestamp"""

    # time of last modification
    if os.name == 'nt':  # windows allows direct access to creation date
        creation_time = os.path.getctime(fname)
    else:
        creation_time = get_creation_time(fname)

    date = time.gmtime(creation_time)
    year = str(date.tm_year)
    month = '{0:02d}'.format(date.tm_mon)
    month += '-' + months[month]
    day = '{0:02d}'.format(date.tm_mday)

    return year, month, day


if __name__ == '__main__':
    try:
        s = os.path.basename(sys.argv[1])
        d = sys.argv[2]
        if s.startswith('IMG_'):
            s = s[4:]
        Y = int(s[0:4])
        M = int(s[4:6])
        D = int(s[6:8])
        if Y > 2000 and M >= 1 and M <= 12 and D >= 1 and D <= 31:
            Y = str(Y)
            M = '{0:02d}'.format(M)
            M += '-' + months[M]
            D = '{0:02d}'.format(D)
            year, month, day = parse_date_tstamp(sys.argv[1])
            # print Y, M, D, year, month, day
            if Y != year or M != month or D != day:
                dst = os.path.join(d, Y, M, D, os.path.basename(sys.argv[1]))
                if not os.path.exists(dst):
                    print 'mv ' + sys.argv[1] + ' ' + dst
    except ValueError as e:
        print "# "+ sys.argv[1]