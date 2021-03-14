import requests, json
import multiprocessing
import api_get


def mp(number_of_process=1):
    process = []
    for i in range(number_of_process):
        process.append(multiprocessing.Process(target=api_get.get_manufacturer(),
                                               kwargs=({'start': i, 'step': number_of_process})))
    return process


if __name__ == '__main__':
    # multiprocessing.cpu_count()
    cpu_count = 12
    threads = mp(number_of_process=cpu_count)
    for p in threads:
        p.start()
    for p in threads:
        p.join()