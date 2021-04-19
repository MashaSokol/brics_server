
from project.resources.consts import PATH_TO_LINKS_JOURNALS

# todo переименовать
from project.resources.csv import csv_dict_reader, csv_writer


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
    def read_links_journals_file(self):
        print('reader')
        links_journals = csv_dict_reader(PATH_TO_LINKS_JOURNALS)
        return links_journals
