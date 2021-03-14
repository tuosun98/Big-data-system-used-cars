from src.cars_spider import *
from multiprocessing import Pool
# TODO(tuosun): This file should not be a Executable Python files.
#               This python file should be changed into a function and be merged into get_car_url_list.py

if __name__ == '__main__':
    # TODO(tuosun): The following variables should be changed into parameters or arguments in a function
    start_year = 2000
    end_year = 2021
    number_of_process = 10
    batchs_size = 100
    directory = 'car_url/'

    url_list = list()
    for i in range(start_year, end_year+1):
        with open('{directory}car_url_list_{year}.txt'.format(directory=directory, year=i)) as f:
            lines = f.readline()
            url_list += lines.split('-')
    pool = Pool(processes=number_of_process)
    batches = split_list(url_list, batchs_size)
    pool.map(get_info_from_list, batches)