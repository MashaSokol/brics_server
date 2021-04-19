
import csv

# читаем файл со ссылками
def csv_dict_reader(file_obj):
    with open(file_obj, "r", newline="") as file:
        reader = csv.reader(file)
        links = {}
        for row in reader:
            links[row[0]] = row[1]
    return links


# сохранение ссылок в файл
def csv_writer(path, fieldnames, data):
    with open(path, "w", newline='') as out_file:
        if str(type(data)) != "<class 'numpy.ndarray'>":
            writer = csv.DictWriter(out_file, delimiter=',', fieldnames=fieldnames)
            for row in data:
                print(row)
                writer.writerow(row)
        else:
            writer = csv.writer(out_file)
            writer.writerows(zip(data))

