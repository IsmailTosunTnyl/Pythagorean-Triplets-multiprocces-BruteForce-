import time
import os
from multiprocessing import Process, Manager


class TicToc:
    def __init__(self):
        self.t1 = 0
        self.t2 = 0

    def tic(self):
        self.t1 = time.time()

    def toc(self):
        self.t2 = time.time()
        return self.t2 - self.t1


def triplets(start_point, end_point, n, increase_amount, shared_pythagorean_triplets):
    for a in range(start_point, end_point, increase_amount):
        for b in range(a, n):
            for c in range(b+1, n):
                if a ** 2 + b ** 2 == c ** 2:
                    shared_pythagorean_triplets.append([a, b, c])


if __name__ == '__main__':
    n = 100
    number_per_process = int(n / os.cpu_count())
    print(number_per_process)
    shared_pythagorean_triplets = Manager().list()
    shared_pythagorean_triplets.append(1)

    processes = list()

    for i, start_point in zip(range(1, os.cpu_count() + 1)[::-1], range(1, os.cpu_count() + 1)):
        end_point = n - os.cpu_count() + i
        processes.append(Process(target=triplets,
                                 args=(start_point, end_point, n, number_per_process, shared_pythagorean_triplets)))

    for process in processes:
        process.start()
    for process in processes:
        process.join()

    for ar in shared_pythagorean_triplets:
        print(ar)

    print(len(shared_pythagorean_triplets))
