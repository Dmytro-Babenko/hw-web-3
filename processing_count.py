import logging
from multiprocessing import cpu_count, Pool, current_process
from datetime import datetime

def factorize(num):
    return [i for i in range(1, num+1) if not num % i]

if __name__ == '__main__':
    st = datetime.now()
    numbers = [128, 255, 99999, 10651060]
    with Pool(processes=cpu_count()) as pool:
        pool.map(factorize, numbers)
    print(datetime.now() - st)
