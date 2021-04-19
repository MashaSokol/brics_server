COUNTRY = "India"
# todo заменить на относительный путь
PATH_TO_LINKS_JOURNALS = fr'C:\Users\misss\Desktop\brics-project\brics_server\project\data_csv\links-journals-{COUNTRY}.csv'
# PATH_TO_JOURNALS_FUNCTIONS = f'../data_csv/journals-functions.csv'
PATH_TO_GECKODRIVER = r'../driver/geckodriver.exe'
PATH_TO_CHROMEDRIVER = r'../driver/chromedriver.exe'
DB_POSTGRES_URL = 'pq://postgres:1234@localhost/brics_test'

ALL_COUNTRIES = ['Brazil', 'Russia', 'India', 'China', 'South Africa']

JOURNALS_FUNCTIONS = {
    'Nano Letters': 'get_art_meta_acspub',
    'ACS Nano': 'get_art_meta_acspub',
    'Environmental Science and Technology': 'get_art_meta_acspub',
    'Analytical Chemistry': 'get_art_meta_acspub',
    'The Journal of Physical Chemistry Letters': 'get_art_meta_acspub',
    'Inorganic Chemistry': 'get_art_meta_acspub',
    'Journal of the American Chemical Society': 'get_art_meta_acspub',
    'Macromolecules': 'get_art_meta_acspub',
    'Organic Letters': 'get_art_meta_acspub',
    'Advanced Functional Materials': 'get_art_meta_wiley',
    'Advanced Materials': 'get_art_meta_wiley',
    'Geophysical Research Letters': 'get_art_meta_wiley',
    'Journal of Geophysical Research: Atmospheres': 'get_art_meta_wiley',
    'Journal of Geophysical Research: Solid Earth': 'get_art_meta_wiley',
    'Ecology Letters': 'get_art_meta_wiley',
    'Angewandte Chemie International Edition': 'get_art_meta_wiley',
    'Nature': 'get_art_meta_springer',
    'Nature Communications': 'get_art_meta_springer',
    'Nature Materials': 'get_art_meta_springer',
    'Nature Methods"' : 'get_art_meta_springer',
    'Nature Photonics': 'get_art_meta_springer',
    'Nature Physics': 'get_art_meta_springer',
    'Molecular Psychiatry': 'get_art_meta_springer',
    'Nature Geoscience': 'get_art_meta_springer',
    'Nature Chemical Biology': 'get_art_meta_springer',
    'Nature Climate Change': 'get_art_meta_springer',
    'Nature Genetics': 'get_art_meta_springer',
    'Nature Immunology': 'get_art_meta_springer',
    'Nature Medicine': 'get_art_meta_springer',
    'The ISME Journal: Multidisciplinary Journal of Microbial Ecology': 'get_art_meta_springer',
    'European Physical Journal C': 'get_art_meta_springer',
    'Journal of High Energy Physics': 'get_art_meta_springer',
    'Proceedings of the National Academy of Sciences of the United States of America': 'get_art_meta_pnasorg',
    'Earth and Planetary Science Letters': 'get_art_meta_sciencedirect',
    'Geochimica et Cosmochimica Acta': 'get_art_meta_sciencedirect',
    'Water Research': 'get_art_meta_sciencedirect',
    'Science': 'get_art_meta_advancesscience',
    'Science Advances': 'get_art_meta_advancesscience',
    'Science Translational Medicine': 'get_art_meta_advancesscience',
    'American Journal of Human Genetics': 'get_art_metaCellajhg',
    'Cancer Cell': 'get_art_metaCellajhg',
    'Developmental Cell': 'get_art_metaCellajhg',
    'Neuron': 'get_art_metaCellajhg',
    'Cell': 'get_art_meta_cellfulltext',
    'Cell Host & Microbe': 'get_art_metaCellajhg',
    'Cell Metabolism': 'get_art_metaCellajhg',
    'Cell Stem Cell': 'get_art_metaCellajhg',
    'Current Biology': 'get_art_metaCellajhg',
    'Immunity': 'get_art_metaCellajhg',
    'Physical Review A': 'get_art_meta_journalsaps',
    'Physical Review B': 'get_art_meta_journalsaps',
    'Physical Review D': 'get_art_meta_journalsaps',
    'Physical Review Letters': 'get_art_meta_journalsaps',
    'Physical Review X': 'get_art_meta_journalsaps',
    'Genome Research': 'get_art_meta_genomecshlp',
    'Geology': 'get_art_meta_geoscienceworld',

    # 'The Plant Cell': 'get_art_meta_planetcell',
    'The Plant Cell': 'get_art_meta_academicoup',

    'eLife': 'get_art_meta_elifescience',
    'Chemical Communications': 'get_art_meta_pubsrsc',
    'Chemical Science': 'get_art_meta_pubsrsc',
    'Journal of Biological Chemistry': 'get_art_meta_jbcorg',
    'Journal of Clinical Investigation': 'get_art_meta_jciorg',
    'Journal of Experimental Medicine': 'get_art_meta_rupress',
    'Applied Physics Letters': 'get_art_meta_aipscitation',
    'Astronomy & Astrophysics': 'get_art_meta_aanda',
    'Journal of Neuroscience': 'get_art_meta_jneurosciorg',
    'PLOS Biology': 'get_art_meta_journalsplos',
    'PLOS Genetics': 'get_art_meta_journalsplos',
    'Cancer Research': 'get_art_meta_jneurosciorg',
    'Proceedings of the Royal Society B': 'get_art_meta_royal',
    'The Astrophysical Journal Letters': 'get_art_meta_iopsciense',
    'Monthly Notices of the Royal Astronomical Society: Letters': 'get_art_meta_academicoup',
    'Journal of Cell Biology': 'get_art_meta_rupress',
    'Molecular Cell': 'get_art_metaCellajhg',
    'Nature Biotechnology': 'get_art_meta_springer',
    'Nature Cell Biology': 'get_art_meta_springer',
    'Nature Chemistry': 'get_art_meta_springer',
    'Nature Nanotechnology': 'get_art_meta_springer',
    'Nature Neuroscience': 'get_art_meta_springer',
    'Nature Structural & Molecular Biology': 'get_art_meta_springer',

    'Nature Methods': 'get_art_meta_springer',

    'The EMBO Journal': 'get_art_meta_embojournal'
}

CSS = 'css_selector'
XPATH = 'xpath'
ID = 'id'
NAME = 'name'
