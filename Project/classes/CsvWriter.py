import csv
from Project.resources.consts import PATH_TO_LINKS_JOURNALS

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


class CSVWriter:

    # prepare links array and journals array for writing into csv
    def _data_prepare(self, links, links_journals):
        new_array = [['link', 'journal']]
        for i in range(0, len(links)):
            new_array.append([links[i], links_journals[i]])
        my_list = []
        fieldnames = new_array[0]
        cell = new_array[1:]
        for values in cell:
            inner_dict = dict(zip(fieldnames, values))
            my_list.append(inner_dict)
        return my_list

    # writing links and journals into csv
    def write_links_journals_functions_files(self, links, links_journals):
        print('in writer')
        links_journals_list = self._data_prepare(links, links_journals)
        csv_writer(PATH_TO_LINKS_JOURNALS, ['link', 'journal'], links_journals_list)
        # csv_writer(PATH_TO_JOURNALS_FUNCTIONS, ['journal'], np.unique(links_journals))

    # reading links and journals from csv
    def read_links_journals_file(self, country):
        print('reader')
        links_journals = csv_dict_reader(str(PATH_TO_LINKS_JOURNALS) + country + '.csv')
        return links_journals
