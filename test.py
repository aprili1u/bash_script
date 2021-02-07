import multiprocessing as mp
from time import sleep


def do_job(i):
    "The greater i is, the shorter the function waits before returning."
    # with lock:
    sleep(1-(i/10.))
    return i


def init_child(lock_):
    global lock
    lock = lock_


def main():
    lock = mp.Lock()
    poolsize = 4
    with mp.Pool(poolsize, initializer=init_child, initargs=(lock,)) as pool:
        results = pool.map(do_job, range(poolsize))
        print(list(results))


if __name__ == "__main__":
    main()

# import csv

# with open('memo_test.csv', 'r') as csv_file:
#     csv_reader = csv.reader(csv_file)

#     with open('new_names.csv', 'a') as new_file:
#         csv_writer = csv.writer(new_file)

#         for line in csv_reader:
#             if line[0] == '3':
#                 csv_writer.writerow(line)

#     # for line in csv_reader:
#     #     pay_off_matrix = line[5:11]
#     #     pay_off_matrix = [float(i) for i in pay_off_matrix]
#     #     network_methode = line[-4:]
#     #     network_methode[2] = int(network_methode[2])
#     #     network_methode[3] = float(network_methode[3])
#     #     print(network_methode)
#     #     print(line)
