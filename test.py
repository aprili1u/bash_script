import csv

with open('run.csv', 'r') as csv_file:
    csv_reader = csv.reader(csv_file)

    with open('new_names.csv', 'w') as new_file:
        csv_writer = csv.writer(new_file)

        for line in csv_reader:
            csv_writer.writerow()

    # for line in csv_reader:
    #     pay_off_matrix = line[5:11]
    #     pay_off_matrix = [float(i) for i in pay_off_matrix]
    #     network_methode = line[-4:]
    #     network_methode[2] = int(network_methode[2])
    #     network_methode[3] = float(network_methode[3])
    #     print(network_methode)
    #     print(line)
