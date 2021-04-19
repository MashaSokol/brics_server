from project.resources.CSVWriter import CSVWriter
from .Parser import Parser
from .models import Article
from .Service import Service
from .cache import Cache


class Agent:
    def __init__(self):
        self.service = Service()
        self.cache = Cache()
        self.csv_writer = CSVWriter()
        self.parser = Parser()
        self.test_link = ""

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            print('creating new agent')
            cls.instance = super(Agent, cls).__new__(cls)
        return cls.instance

    def fill_db_for_country(self, country):
        # links, links_journals = self.parser.get_btns_links_and_journals()
        # self.csv_writer.write_links_journals_functions_files(links, links_journals)

        links_journals = self.csv_writer.read_links_journals_file()
        for link_to_button in links_journals:
            try:
                Article.objects.get(link_to_btn=link_to_button)
            except Article.DoesNotExist:
                try:
                    journal_name = links_journals[link_to_button]
                    article_info = self.parser.get_article_information(link_to_button, journal_name)
                    if article_info is not None:
                        self.service.save_article_info(article_info)
                except KeyError:
                    my_file = open("exceptions.txt", "a")
                    my_file.write('\n we do not know what journal of ' + link_to_button + " is\n ")
                    my_file.close()
                    continue

        # для тестирования: выбираем журнал

        # ! springer
        # if 'Nature' in journal_name:

        # ! sciencedirect
        # if 'Earth and Planetary Science Letters' in journal_name or 'Geochimica et Cosmochimica Acta' in journal_name or 'Water Research' in journal_name:

        # ! acs
        # if 'Organic Letters' in journal_name or 'Macromolecules' in journal_name or 'Journal of the American Chemical Society' in journal_name or 'Inorganic Chemistry' in journal_name or 'The Journal of Physical Chemistry Letters' in journal_name or 'Analytical Chemistry' in journal_name or 'Environmental Science and Technology' in journal_name or 'ACS Nano' in journal_name or 'Nano Letters' in journal_name:
        #
        # ! rsc
        # if 'Chemical Communications' in journal_name or 'Chemical Science' in journal_name:
        #
        # ! pnasorg
        # if 'Proceedings of the National Academy of Sciences of the United States of America' in journal_name:
        #
        # ! advances science
        # if 'Science' == journal_name or 'Science Advances' == journal_name or 'Science Translational Medicine' == journal_name:
        #
        # ! journalsplos
        # if 'PLOS Biology' == journal_name or 'PLOS Genetics' == journal_name:
        #
        # ! jneurosci
        # if 'Journal of Neuroscience' == journal_name or 'Cancer Research' == journal_name:
        #
        # ! jbcorg
        # if 'Journal of Biological Chemistry' == journal_name:
        #
        #  ! jciorg
        #  if 'Journal of Clinical Investigation' == journal_name:
        #
        #  ! cell
        #  if 'Cell' == journal_name:
        #
        #  ! royal
        #  if 'Proceedings of the Royal Society B' == journal_name:
        #
        #  ! meta aip scitation
        #  if 'Applied Physics Letters' == journal_name:
        #
        #         # ? academic oup
        #         # if 'Monthly Notices of the Royal Astronomical Society: Letters' == journal_name:
        #
        #         # ? iop science
        #         # if 'The Astrophysical Journal Letters' == journal_name:
        #
        # ! meta ru press
        # if 'Journal of Experimental Medicine' == journal_name or 'Journal of Cell Biology' == journal_name:
        #
        # ! genome
        # if 'Genome Research' == journal_name:
        #
        #         # ? planet cell
        #         # if 'The Plant Cell' == journal_name:
        #
        #         # ? aanda
        #         # if 'Astronomy & Astrophysics' in journal_name:
        #
        # ! pubs geo science world
        #  https: // www.natureindex.com / article / 10.1130 / g47008.1
        #  https: // www.natureindex.com / article / 10.1130 / g46740.1
        #  https: // www.natureindex.com / article / 10.1130 / g46923.1
        #  https: // www.natureindex.com / article / 10.1130 / g46180.1
        #  if 'Geology' in journal_name:
        #
        # ! wiley
        #  if 'Advanced Functional Materials' == journal_name or 'Advanced Materials' == journal_name or 'Geophysical Research Letters' == journal_name or 'Journal of Geophysical Research: Atmospheres' == journal_name or 'Journal of Geophysical Research: Solid Earth' == journal_name or 'Ecology Letters' == journal_name or 'Angewandte Chemie International Edition' == journal_name:
        #
        # ! journals aps
        # if 'Physical Review' in journal_name:
        #
        # ! elife
        # if 'eLife' == journal_name:
        #
        # ! cell ajhg
        #  if 'American Journal of Human Genetics' == journal_name or 'Cancer Cell' == journal_name or 'Neuron' == journal_name or 'Cell Metabolism ' == journal_name or 'Cell Host & Microbe' == journal_name or 'Cell Stem Cell' == journal_name or 'Current Biology' == journal_name or 'Immunity' == journal_name:

        # self.update_cache(self.parser)

    def update_cache(self, parser):
        # todo заменить
        for country in ['Brazil', 'Russia', 'India', 'China', 'South Africa']:
            self.cache.cache_unis_top(parser.get_top_unis_names(country), country)

    def country_unis_top(self, country):
        if self.cache.is_unis_empty(country):
            # с сайта, нужно парсить - долго
            unis = self.parser.get_top_unis_names(country)
            # из БД согласно данным в ней, тоже долго:
            # unis = self.service.get_top_unis_names(country)
            self.cache.cache_unis_top(unis, country)
        return self.cache.get_unis_top(country)

    def country_keywords_top(self, country):
        if self.cache.is_keywords_empty(country):
            # из БД согласно данным в ней:
            kwds = self.service.get_top_keywords_names(country)
            self.cache.cache_keywords_top(kwds, country)
        return self.cache.get_keywords_top(country)

    def get_limit_organizations(self, country, page):
        return self.service.get_limit_organizations(country, page)
