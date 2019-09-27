from request import Request
from server import Server
import urllib.request as urllib
import logging
import argparse
import csv 

def simulateOneServer(file_name):
    """
    Responsible for printing out the average wait time for a request.
    (i.e.,how long, on average, did a request stay in the server queue before being processed). The simulate function
    should return this average.
    """
    return True 

def get_data(url):
    csvData = urllib.urlopen(url).read()
    csvPayLoad = csv.reader(csvData.decode('utf-8').splitlines())
    csvResults = [row for row in csvPayLoad]

    return csvResults

def main():
    """
    The primary function of this application.

    Parameters:
        None

    Logs:
        An error if the string url is entered incorrectly.
    """

    parser = argparse.ArgumentParser()
    parser.add_argument('url')
    args = parser.parse_args()

    logging.basicConfig(filename='errors.log',
                        level=logging.ERROR, format='%(message)s')
    logging.getLogger('assignment5')

    if(args.url):
        try:
            result = get_data(args.url)
            print(result, 'RESULTS FROM URL REQUEST')
        except (ValueError, urllib.HTTPError):
            print(
                f'Something went wrong, you entered in <{args.url}>, please check your url param for errors')

            logging.error(f'Error processing <{args.url}>')
            return SystemExit


if __name__  == '__main__':
    main()