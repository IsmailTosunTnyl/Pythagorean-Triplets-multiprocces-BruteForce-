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
    # every process has a unique start point and has a same increase amount as other process which equals cpu count
    # this separate every process from each other
    for a in range(start_point, end_point, increase_amount):
        for b in range(a + 1, n):
            for c in range(b + 1, n):
                if a ** 2 + b ** 2 == c ** 2:
                    shared_pythagorean_triplets.append([a, b, c])


if __name__ == '__main__':
    timer = TicToc()
    timer.tic()

    # for the most accurate result,choose a number that is divisible by the number of processors
    n = 800
    cpu_count = os.cpu_count()

    number_per_process = int(n / cpu_count)
    shared_pythagorean_triplets = Manager().list()
    processes = list()

    for i, start_point in zip(range(1, cpu_count + 1)[::-1], range(1, cpu_count + 1)):
        end_point = n - cpu_count + i
        processes.append(Process(target=triplets,
                                 args=(start_point, end_point, n, cpu_count, shared_pythagorean_triplets)))

    for process in processes:
        process.start()

    for process in processes:
        process.join()

    for tri in shared_pythagorean_triplets:
        print(f"a:{tri[0]} , b:{tri[1]} , c:{tri[2]}")

    print("Total numbers of triplets :", len(shared_pythagorean_triplets))
    print("Number per CPU:", number_per_process)
    print("Time", timer.toc())
