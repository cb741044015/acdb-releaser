import argparse
import time
import datetime

DATE_FORMAT = '%Y%m%d'


def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--date', default=time.strftime(DATE_FORMAT),
                        help="date time format:YYYYMMDD default today")
    parser.add_argument('--suffix', default='_acdb', help="suffix")
    parser.add_argument('-o', '--outout')
    return parser


def verify_date(date):
    try:
        date = datetime.datetime.strptime(args.date, DATE_FORMAT).date()
    except:
        print("data fomat: YYYYYMMDD")
        exit(1)
    return date.strftime(DATE_FORMAT)


if __name__ == "__main__":
    parser = get_parser()
    args = parser.parse_args()
    date = verify_date(args.date)
