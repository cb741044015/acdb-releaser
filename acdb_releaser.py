import argparse
import time
import datetime
import os.path
import shutil
import os

DATE_FORMAT = '%Y%m%d'
RELEASE = '/Release'


def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--date', default=time.strftime(DATE_FORMAT),
                        help="date time format:YYYYMMDD default today")
    parser.add_argument('--suffix', default='_acdb', help="suffix")
    parser.add_argument('-o', '--output')
    return parser


def verify_date(date):
    try:
        date = datetime.datetime.strptime(args.date, DATE_FORMAT).date()
    except:
        print("data fomat: YYYYYMMDD")
        exit(1)
    return date


def copy_dir(src, dst):
    assert isinstance(src, str)

    ## for safe...
    if not os.path.exists(src) or not os.path.isdir(src):
        print(src + "is not exists or a directory")
        return False
    try:
        shutil.copytree(src, dst)
    except:
        print("error happend, cleaning all")
        clear_for_term()
        exit(1)


def make_dirs_for_release():
    try:
        os.makedirs(RELEASE_DIR, exist_ok=True)
    except:
        print("what's wrong but exit")
        exit(1)


def clear_for_term():
    shutil.rmtree(RELEASE_DIR, ignore_errors=True)


def format_dir_name(dir, date, suffix=None):
    assert isinstance(dir, str) and isinstance(date, str)
    if not suffix:
        dir = date + "_" + dir
    else:
        dir = date + "_" + dir + suffix
    return dir


MONTHTOVER = ['1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C']


def get_version(date):
    assert isinstance(date, datetime.date)
    # safe no check
    # get tomorrow
    date = date + datetime.timedelta(days=1)
    m = MONTHTOVER[date.month - 1]
    d = date.strftime("%d")
    return 'A' + m + d + '0'


RELEASE_DIR = os.getcwd() + RELEASE

if __name__ == "__main__":
    parser = get_parser()
    args = parser.parse_args()
    date = verify_date(args.date)

    # first list dir under wd
    wd = os.getcwd()
    dirs = [d for d in os.listdir(wd) if os.path.isdir(os.path.join(wd, d))]
    print(dirs)
    print(type(date))
    print(MONTHTOVER)
    print(args.output)

    make_dirs_for_release()
    dir_prefix = date.strftime(DATE_FORMAT)

    # then copy dir to local release
    for dir in dirs:
        src = wd + '/' + dir
        dir_name = format_dir_name(dir, dir_prefix, args.suffix)
        dst = wd + RELEASE + '/' + dir + '/' + dir_name
        copy_dir(src, dst)

        # touch a empty file in release
        with open(dst + '/' + get_version(date) + '.txt', 'w+'):
            pass

        # copy releases to outptut if spec
        if args.output:
            src = dst
            print(src)
            dst = args.output + '/' + dir + '/' + dir_name
            print(dst)
            if os.path.exists(dst):
                shutil.rmtree(dst)
            shutil.copytree(src, dst)

    clear_for_term()
