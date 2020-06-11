import multiprocessing
import random

import numpy

from my_pool import ProcessPool


def heavy_computation(data):
    M = 1000
    a = numpy.array([[random.randint(M * (-data), M * data)
                      for _ in range(M)] for _ in range(M)])
    b = numpy.array([[random.randint(M * (-data), M * data)
                      for _ in range(M)] for _ in range(M)])
    c = numpy.array([[random.randint(M * (-data), M * data)
                      for _ in range(M)] for _ in range(M)])
    d = numpy.array([[random.randint(M * (-data), M * data)
                      for _ in range(M)] for _ in range(M)])
    return a * b * c * d


if __name__ == '__main__':
    q = multiprocessing.Queue()
    for i in range(5):
        q.put(i * 100)

    pool = ProcessPool()
    print(pool.map(heavy_computation, q))
