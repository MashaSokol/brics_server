import time
from accessify import private
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import ElementClickInterceptedException, TimeoutException, NoSuchElementException
from bricsagentapplication.model.PublicationInformation import PublicationInformation
from Project.resources.consts import JOURNALS_FUNCTIONS, CSS, XPATH, ID, NAME
from Project.classes.text_functions import delete_first_nums, get_first_nums


class Parser:

    def __init__(self):
        self.driver = None
        self.current_parsing_function = ''

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Parser, cls).__new__(cls)
        return cls.instance

    @private
    def try_finding_element_by(self, ways_params_dict):
        for way in ways_params_dict:
            for parameter in ways_params_dict[way]:
                try:
                    return eval('self.driver.find_element_by_' + way + '("' + parameter + '")')
                except NoSuchElementException:
                    continue

    @private
    def try_finding_elements_by(self, ways_params_dict):
        for way in ways_params_dict:
            for parameter in ways_params_dict[way]:
                try:
                    return eval('self.driver.find_elements_by_' + way + '("' + parameter + '")')
                except NoSuchElementException:
                    continue

    # нажатие на каждый элемент принятого списка
    @private
    def click_elements(self, elements):
        for element in elements:
            try:
                element.click()
            except ElementClickInterceptedException:
                time.sleep(2)
                self.driver \
                    .find_element_by_css_selector('.optanon-alert-box-button-middle.accept-cookie-container') \
                    .click()
                time.sleep(1)
                element.click()

    # сбор всех ссылок на страницы с кнопками GoToArticle
    def get_btns_links_and_journals(self, country):
        print('In parsers function')
        # переход по ссылке сайта natureindex.com
        self.driver.get("https://www.natureindex.com/country-outputs/" + country)
        # поиск всех тем
        themes = self.driver.find_elements_by_css_selector('.subject-link')
        # нажатие на каждую тему
        self.click_elements(themes)
        # поиск всех журналов
        journals = self.driver.find_elements_by_css_selector('.journal')
        # нажатие на каждый журнал
        self.click_elements(journals)
        n = 3
        k = 2
        i = 1
        links_to_btn_to_pubs = []
        journals_of_publications = []
        while True:
            try:
                WebDriverWait(self.driver, 1).until(EC.presence_of_element_located(
                    (By.XPATH, "//*[@id='research']/table/tbody/tr[" + str(n)
                     + "]/td/table/tbody/tr[2]/td/table/tbody/tr[1]/td[1]/a")))
                try:
                    WebDriverWait(self.driver, 1).until(EC.presence_of_element_located(
                        (By.XPATH, "//*[@id='research']/table/tbody/tr[" + str(n)
                         + "]/td/table/tbody/tr[" + str(k) + "]/td/table/tbody/tr[1]/td[1]/a")))
                    try:
                        links_to_btn_to_pubs.append(str(WebDriverWait(self.driver, 1).until(EC.presence_of_element_located(
                            (By.XPATH, "//*[@id='research']/table/tbody/tr[" + str(n)
                             + "]/td/table/tbody/tr[" + str(k) + "]/td/table/tbody/tr[" + str(i)
                             + "]/td[1]/a"))).get_attribute("href")))
                        j = self.driver.find_element_by_xpath(
                            '//*[@id="research"]/table/tbody/tr[' + str(n) + ']/td/table/tbody/tr[' + str(
                                k - 1) + ']/td[1]'
                        ).text
                        print('link found')
                        journals_of_publications.append(j)
                        i = i + 1
                    except TimeoutException:
                        k = k + 2
                        i = 1
                except TimeoutException:
                    n = n + 2
                    k = 2
                    i = 1
            except TimeoutException:
                return links_to_btn_to_pubs, journals_of_publications

    def get_publication_information(self, link_to_button, journal_name):
        try:
            self.driver.get(link_to_button)
        except Exception:
            return None
        link_to_publication = self.driver.find_element_by_css_selector('.btn.btn-primary').get_attribute('href')

        if link_to_publication is not None and link_to_publication != 'https://www.natureindex.com/signup':
            self.current_parsing_function = JOURNALS_FUNCTIONS[journal_name]

            pubdate = self.try_finding_element_by({CSS: ['.pubdate']}).get_attribute('textContent').replace('Published:', '').strip()

            try:
                self.driver.get(link_to_publication)  # иногда time out exception
            except TimeoutException:
                return None
            d = self.try_finding_element_by({XPATH: ["//*[contains(text(), 'DOI Not Found')]"]})
            recaptcha = self.try_finding_element_by({CSS: ['.explanation-message']})
            # bubble = self.try_finding_elements_by({CSS: ['.bubbles']})
            if d is None and recaptcha is None:  # and bubble is None
                try:
                    publication_info = eval("self." + self.current_parsing_function + '()')
                    if publication_info is not None:
                        publication_info.journal_name = journal_name
                        publication_info.link = link_to_publication
                        publication_info.date = pubdate
                        publication_info.link_to_btn = link_to_button
                        return publication_info
                except Exception as e:
                    my_file = open("exceptions.txt", "a")
                    my_file.write(link_to_publication + ": " + str(e) + '\n')
                    my_file.close()
            else:
                my_file = open("failed_links.txt", "a")
                my_file.write("Can not get information from " + link_to_publication)
                if d is not None:
                    my_file.write(", reason: NOT FOUND\n")
                if recaptcha is not None:
                    my_file.write(", reason: RECAPTCHA\n")
                # if bubble is not None:
                #     my_file.write(", reason: BROWSER CHECKING\n")
                my_file.close()

    # def get_top_orgs_names(self, country, additional_driver):
    #     # new_driver = webdriver.Firefox(executable_path=r'/bricsagentapplication/driver/geckodriver.exe')
    #     # opts = Options()
    #     # opts.headless = True
    #     # new_driver = webdriver.Firefox(options=opts, executable_path=GeckoDriverManager().install())
    #     link = "https://www.natureindex.com/country-outputs/" + country
    #     additional_driver.get(link)
    #     table = additional_driver.find_element_by_css_selector('.table.table-condensed.rank-table')
    #     orgs = table.find_elements_by_css_selector('.institution-profile')
    #     names = [u.text for u in orgs]
    #     return names

    # функции для каждого журнала

    def get_art_meta_springer(self):
        publication_info = PublicationInformation()
        publication_info.name = self.try_finding_element_by({CSS: ['.c-article-title.u-h1', '.c-article-title']}).text
        publication_info.abstract = self.try_finding_element_by({CSS: ['.c-article-section']}).text.replace('Abstract', '')
        publication_info.keywords = [k.text for k in self.try_finding_elements_by({CSS: ['.c-article-subject-list__subject']})]

        i = 1
        while True:
            augroup = self.try_finding_element_by({ID: ['Aff' + str(i)]})
            if augroup is None:
                break
            orgs = augroup.find_elements_by_css_selector('.c-article-author-affiliation__address')
            authors_array = augroup.find_elements_by_css_selector('.c-article-author-affiliation__authors-list')[0].text.replace(' & ', ', ').split(', ')
            for u in orgs:
                publication_info.org_authors[u.text] = [a for a in authors_array]
            i = i + 1

        return publication_info

    def get_art_meta_embojournal(self):
        publication_info = PublicationInformation()
        publication_info.name = self.try_finding_element_by({CSS: ['.citation__title']}).text
        publication_info.abstract = self.try_finding_element_by({CSS: ['.article-section.article-section__abstract']}).text.replace('Abstract', '').strip()

        self.try_finding_element_by({CSS: ['.accordion__control.general-link']}).click()
        authors_array = self.try_finding_element_by({CSS: ['.contributor-list.rlist.rlist--inline']}).text.replace(' and', ';').split('\n')
        orgs_array = self.try_finding_element_by({CSS: ['.affiliation-list.rlist']}).text.replace('These authors contributed equally to this work', '').split('\n')
        a_dict = {}
        u_dict = {}
        for a in authors_array:
            if len(a) > 1:
                first_symbol = ''
                for symbol in a:
                    if (not symbol.isalpha()) and (symbol != ' ') and (symbol != '`'):
                        first_symbol = symbol
                        break
                a_dict[a[:a.find(first_symbol)]] = [s for s in a[a.find(first_symbol):].split(',') if len(s) > 0]
        for u in orgs_array:
            for symbol in u.strip():
                if symbol.isalpha():
                    u_dict[u[u.find(symbol):].strip()] = u[:u.find(symbol)]
                    break
        for u in u_dict:
            publication_info.org_authors[u] = [a for a in a_dict if u_dict[u] in a_dict[a]]

        self.try_finding_element_by({ID: ['pane-pcw-detailscon']}).click()
        publication_info.keywords = [k.text for k in WebDriverWait(self.driver, 50).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.badge-type')))]

        return publication_info

    def get_art_meta_sciencedirect(self):  # 'https://linkinghub.elsevier.com/retrieve/pii/S0012821X19307368'
        time.sleep(5)
        publication_info = PublicationInformation()
        publication_info.name = self.try_finding_element_by({XPATH: ["//*[@id='screen-reader-main-title']"]}).text
        i = 1
        while True:
            k = self.try_finding_element_by({XPATH: [f"//*[@id='kw00{str(i)}0']/span"]})
            if k is None:
                break
            publication_info.keywords.append(k.text)
            i = i + 1
        publication_info.abstract = self.try_finding_element_by({CSS: ['.abstract.author']}).text.replace('Abstract', '')

        authors = self.try_finding_elements_by({CSS: [".author.size-m.workspace-trigger"]})
        for a in authors:
            a.click()
            time.sleep(3)
            orgs = self.try_finding_elements_by({CSS: [".affiliation"]})
            for u in orgs:
                if len(u.get_attribute('textContent')) > 3:
                    if u.text not in publication_info.org_authors:
                        publication_info.org_authors[u.text] = []
                    author = self.try_finding_element_by({CSS: ['.author.u-h4']}).text
                    publication_info.org_authors[u.text].append(author)

        return publication_info

    def get_art_meta_acspub(self):
        publication_info = PublicationInformation()
        publication_info.name = self.try_finding_element_by({CSS: ['.article_header-title']}).text
        publication_info.abstract = self.try_finding_element_by({CSS: ['.articleBody_abstractText'], XPATH: ['//*[@id="pb-page-content"]/div/main/article/div[3]/div/div/div[1]/div/div/div[1]/p[1]']}).text
        publication_info.keywords = self.try_finding_element_by({CSS: ['.rlist--inline.loa']}).text.split(',')

        authors = self.try_finding_elements_by({CSS: ['.hlFld-ContribAuthor']})
        cards = self.try_finding_elements_by({CSS: ['.loa-info.hlFld-Affiliation']})
        for c in cards:
            orgs = c.find_elements_by_css_selector('.loa-info-affiliations-info')
            for uni in orgs:
                uni = uni.get_attribute('textContent')
                if uni not in publication_info.org_authors:
                    publication_info.org_authors[uni] = []
                publication_info.org_authors[uni].append(authors[0].text)
            authors.pop(0)

        return publication_info

    def get_art_meta_pubsrsc(self):
        publication_info = PublicationInformation()
        publication_info.name = self.try_finding_element_by({CSS: ['.capsule__title.fixpadv--m']}).text
        # article.pubdate = self.try_finding_element_by({CSS: ['.c__14']}).text
        publication_info.abstract = self.try_finding_element_by({CSS: ['.capsule__text']}).text

        authors = self.try_finding_elements_by({CSS: ['.article__author-link']})
        k = 1
        AuStr = ''
        for a in authors:
            name = self.try_finding_element_by({XPATH: [f"//*[@id='maincontent']/div/div/div[1]/section/article/div[2]/span[{str(k)}]/a"]}).text
            a_name = name + '-' + a.text[a.text.find(name) + len(name):]
            AuStr = AuStr + a_name + ';'
            k = k + 1
        self.try_finding_element_by({CSS: ['.drawer__handle']}).click()
        orgs = self.try_finding_elements_by({CSS: ['.article__author-affiliation']})
        uni = ''
        for u in orgs:
            uni = uni + u.text + ';'
        a = [[AuStr]]
        u = [[uni.replace('* Corresponding authorsa', '')]]
        for i in range(0, len(a)):
            for aa in a[i][0].replace('  and  ', '   ').split(';'):
                if len(aa) > 0:
                    num = aa[aa.rfind('-'):].replace(',', '').replace('*', '').replace('-', '').strip().replace(' and', '').replace('‡', '')
                    nums = []
                    for s in num.strip():
                        nums.append(s)
                    aa = aa[:aa.rfind('-')]
                    for n in nums:
                        for uu in u[i][0].split(';'):
                            if 'Corresponding authors' not in uu and len(uu) > 0 and uu.strip()[0] == n:
                                uu = uu[uu.find(' ') + 1:]
                                uu = uu[:uu.find('E-mail')].strip()
                                if uu not in publication_info.org_authors:
                                    publication_info.org_authors[uu] = []
                                publication_info.org_authors[uu].append(aa)

        return publication_info

    def get_art_meta_pnasorg(self):
        publication_info = PublicationInformation()
        publication_info.name = self.try_finding_element_by({CSS: ['.highwire-cite-title']}).text
        publication_info.abstract = self.try_finding_element_by({CSS: ['.section.abstract']}).text.replace('Abstract', '')
        publication_info.keywords = [k.text for k in self.try_finding_elements_by({CSS: ['.kwd']})]

        i = 1
        while True:
            tooltips = self.driver.find_elements_by_css_selector(f'.author-tooltip-{str(i)}')
            if len(tooltips) == 0:
                break
            for tooltip in tooltips:
                author_name = tooltip.find_element_by_css_selector('.author-tooltip-name').get_attribute('textContent')
                author_orgs = tooltip.find_elements_by_css_selector('.author-affiliation')
                for u in author_orgs:
                    u_str = u.get_attribute('textContent').replace(';', '')
                    for s in u_str:
                        if s.islower():
                            u_str = u_str[1:]
                        else:
                            break
                    if u_str not in publication_info.org_authors:
                        publication_info.org_authors[u_str] = []
                    publication_info.org_authors[u_str].append(author_name)
            i = i + 1

        return publication_info

    def get_art_meta_advancesscience(self):
        publication_info = PublicationInformation()
        publication_info.name = self.try_finding_element_by({CSS: ['.highwire-cite-title']}).text
        publication_info.abstract = self.try_finding_element_by({CSS: ['.section.abstract']}).text.replace('Abstract', '').strip()

        b = self.try_finding_element_by({CSS: ['.collapsed-text']})
        try:
            b.click()
        except ElementClickInterceptedException:
            time.sleep(1)
            self.try_finding_element_by({XPATH: ['//*[@id="wb_cookie_setting_ok"]']}).click()
            time.sleep(1)
            b.click()

        authors = [a.text.replace('View ORCID Profile', '').replace('and', '').strip() for a in self.try_finding_elements_by({CSS: ['.contributor']})]
        universities = [u.text.replace('and', '').strip() for u in self.try_finding_elements_by({CSS: ['.aff']})]
        numbers = []
        for i in range(0, len(authors)):
            numbers.append(i)
            numbers[i] = []
        for i in range(0, len(authors)):
            for l in range(0, len(authors[i])):
                if authors[i][l].isdigit():
                    numbers[i].append(authors[i][l:])
                    authors[i] = authors[i][:l]
                    break
        for i in range(0, len(universities)):
            string = ''
            for s in range(0, len(universities[i])):
                if universities[i][s].isdigit():
                    string = string + universities[i][s]
                else:
                    break
            for l in range(0, len(numbers)):
                if string == numbers[l][0][:numbers[l][0].find(',')] or ',' + string + ',' in numbers[l][0]:
                    u = universities[i][universities[i].find(string) + len(string):-1]
                    if u not in publication_info.org_authors:
                        publication_info.org_authors[u] = []
                    publication_info.org_authors[u].append(authors[l])
        return publication_info

    def get_art_meta_journalsplos(self):
        publication_info = PublicationInformation()
        publication_info.name = self.try_finding_element_by({ID: ['artTitle']}).text
        publication_info.abstract = self.try_finding_element_by({CSS: ['.abstract.toc-section']}).text.replace('Abstract', '')  # driver.find_element_by_css_selector('.abstract.toc-section').text
        publication_info.keywords = self.try_finding_element_by({ID: ['subjectList']}).text.split('\n')

        authors = [a.get_attribute('textContent').replace(',', '').strip() for a in self.try_finding_elements_by({CSS: ['.author-name']})]
        for i in range(0, len(authors)):
            orgs = [u.strip() for u in self.try_finding_element_by({ID: [f'authAffiliations-{str(i)}']}).get_attribute('textContent').replace('Affiliations', '').replace('Affiliation', '').strip().split('\n')]
            for u in orgs:
                if u[-1] == ',':
                    u = u[:-1]
                if u not in publication_info.org_authors:
                    publication_info.org_authors[u] = []
                publication_info.org_authors[u].append(authors[i])

        return publication_info

    def get_art_meta_jneurosciorg(self):
        publication_info = PublicationInformation()
        publication_info.name = self.try_finding_element_by({ID: ['page-title']}).text
        publication_info.abstract = self.try_finding_element_by({CSS: ['.section.abstract']}).text.replace('Abstract', '').strip()
        publication_info.keywords = [k.text for k in self.try_finding_elements_by({CSS: ['.kwd']})]

        authors = [a.get_attribute('textContent') for a in self.try_finding_elements_by({CSS: ['.author-tooltip-name']})]
        for i in range(0, len(authors)):
            tooltip = self.try_finding_element_by({CSS: [f'.author-tooltip-{str(i)}']})
            orgs = [u.get_attribute('textContent').replace(', and ', '').strip() for u in tooltip.find_elements_by_css_selector('.author-affiliation')]
            for u in orgs:
                for s in u:
                    if s.isdigit():
                        u = u[1:]
                    else:
                        break
                if not u[-1].isalpha():
                    u = u[:-1]
                if u not in publication_info.org_authors:
                    publication_info.org_authors[u] = []
                publication_info.org_authors[u].append(authors[i])

        return publication_info

    def get_art_meta_jbcorg(self):
        publication_info = PublicationInformation()
        try:
            publication_info.name = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "article-title-1"))).text
        except TimeoutException:
            try:
                publication_info.name = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".article-header__title.smaller"))).text
            except TimeoutException:
                publication_info.name = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".article-header__title"))).text
        publication_info.abstract = self.try_finding_element_by({ID: ['abstract-1'], CSS: ['.section-paragraph']}).text.replace('Abstract', '')

        keywords = [k.text for k in self.try_finding_elements_by({CSS: ['.kwd']})]
        if len(keywords) < 1:
            keywords = [k.strip() for k in self.try_finding_element_by({CSS: ['.rlist.keywords-list.inline-bullet-list']}).text.split(' ')]
        for k in keywords:
            if '\n' in k:
                kk = k.split('\n')
                for kkk in kk:
                    publication_info.keywords.append(kkk)
            else:
                publication_info.keywords.append(k)

        cards = self.try_finding_elements_by({CSS: ['.article-header__info__scrollable']})
        authors = self.try_finding_elements_by({CSS: ['.article-header__info__label']})
        all_orgs = set([u.get_attribute('content') for u in self.try_finding_elements_by({NAME: ['citation_author_institution']})])
        if len(all_orgs) == 0:
            all_orgs = set([u.get_attribute('textContent') for u in self.try_finding_elements_by({CSS: ['.affiliation']})])
        for i in range(0, len(cards)):
            author_info = cards[i].get_attribute('textContent')
            orgs = [u for u in all_orgs if u in author_info]
            for u in orgs:
                if u not in publication_info.org_authors:
                    publication_info.org_authors[u] = []
                publication_info.org_authors[u].append(authors[i].get_attribute('textContent'))

        return publication_info

    def get_art_meta_jciorg(self):
        publication_info = PublicationInformation()
        publication_info.name = self.try_finding_element_by({CSS: ['.article-title']}).text
        publication_info.abstract = self.try_finding_element_by({ID: ['section-abstract']}).text
        publication_info.keywords = [k.text for k in self.try_finding_elements_by({CSS: ['.label-specialty']})]
        # article.pubdate = self.try_finding_element_by({CSS: ['.publication_date']}).text.replace('Published', '')
        # article.pubdate = article.pubdate[:article.pubdate.find('-')]

        authors = [a.get_attribute('textContent').replace('and', '').strip() for a in self.try_finding_elements_by({CSS: ['.author-affiliation.show-more']})]
        orgs = [u.get_attribute('textContent') for u in self.try_finding_element_by({ID: [f'author-affiliation-0']}).find_elements_by_css_selector('.affiliations')]
        for author in authors:
            nums = author[author.find(',') + 1:].split(',')
            author_orgs = [u[u.find(get_first_nums(u)) + len(get_first_nums(u)):-1] for u in orgs if   get_first_nums(u) in nums]
            for u in author_orgs:
                if u not in publication_info.org_authors:
                    publication_info.org_authors[u] = []
                publication_info.org_authors[u].append(author[:author.find(',')])

        return publication_info

    def get_art_meta_cellfulltext(self):
        publication_info = PublicationInformation()
        publication_info.name = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.article-header__title'))).get_attribute('textContent')
        publication_info.abstract = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.section-paragraph'))).text
        if len(publication_info.abstract) < 30:
            try:
                publication_info.abstract = WebDriverWait(self.driver, 50).until(EC.presence_of_element_located((By.XPATH, "//*[@id='pb-page-content']/div/div[1]/div/div/div/main/article/div[2]/div[3]/div/div[2]/section[1]/div/div"))).text
            except TimeoutException:
                publication_info.abstract = WebDriverWait(self.driver, 50).until(EC.presence_of_element_located((By.XPATH, '//*[@id="pb-page-content"]/div/div[1]/div/div/div/main/article/div[2]/div[3]/div/div[2]/section[2]/div/div'))).text
        publication_info.keywords = self.try_finding_element_by({CSS: ['.rlist.keywords-list.inline-bullet-list']}).text.split('\n')
        b = self.try_finding_element_by({CSS: ['.loa__item__name.show-hide__authors.faded.read-more']})
        if b is not None:
            b.click()

        cards = self.try_finding_elements_by({CSS: ['.article-header__info__scrollable']})
        all_uni = set([u.get_attribute('content') for u in self.try_finding_elements_by({NAME: ['citation_author_institution']})])
        for c in cards:
            author = c.find_element_by_css_selector('.article-header__info__label').get_attribute('textContent')
            aff = c.find_elements_by_css_selector('.article-header__info__group__body')
            for af in aff:
                for u in all_uni:
                    if u in af.get_attribute('textContent'):
                        if u not in publication_info.org_authors:
                            publication_info.org_authors[u] = []
                        publication_info.org_authors[u].append(author)
        return publication_info

    def get_art_meta_royal(self):
        publication_info = PublicationInformation()
        publication_info.name = self.try_finding_element_by({CSS: ['.citation__title']}).text
        publication_info.abstract = self.try_finding_element_by(
            {CSS: ['.abstractSection.abstractInFull'], XPATH: ["//*[@id='pb-page-content']/div/main/div[2]/div/div/article/div/div[1]/div/div[2]/div[4]/div[2]/p[1]"]}).text.replace('Abstract', '')
        publication_info.keywords = self.try_finding_element_by({CSS: ['.rlist.rlist--inline']}).text.split('\n')
        # article.pubdate = self.try_finding_element_by({CSS: ['.epub-section__date']}).text

        i = 1
        while True:
            author = self.try_finding_element_by({XPATH: [f"//*[@id='pb-page-content']/div/main/div[2]/div/div/article/div/div[1]/div/div[2]/div[1]/ul/div[{str()}]/div/p[3]"]})
            if author is None:
                break
            k = 4
            while True:
                uni = self.try_finding_element_by({XPATH: [f"//*[@id='pb-page-content']/div/main/div[2]/div/div/article/div/div[1]/div/div[2]/div[1]/ul/div[{str(i)}]/div/p[{str(k)}]"]}).get_attribute('textContent')
                if uni is None or 'Google' in uni or 'http' in uni or '@' in uni or len(uni) < 5:
                    break
                if uni not in publication_info.org_authors:
                    publication_info.org_authors[uni] = []
                publication_info.org_authors[uni].append(author.get_attribute('textContent'))
                k = k + 1
            i = i + 1
        return publication_info

    def get_art_meta_aipscitation(self):
        publication_info = PublicationInformation()
        publication_info.name = self.try_finding_element_by({CSS: ['.publicationContentTitle']}).text
        publication_info.abstract = self.try_finding_element_by({CSS: ['.NLM_paragraph']}).text.replace('Abstract', '').replace('\n', '')
        publication_info.keywords = [k.text for k in self.try_finding_elements_by({CSS: ['.topicTags']})]

        orgs1 = [u.get_attribute('textContent') for u in self.try_finding_elements_by({CSS: ['.author-affiliation']})]
        orgs2 = {}
        for i in range(1, len(orgs1) + 1):
            number = self.try_finding_element_by({XPATH: [
                f"//*[@id='pb-page-content']/div/div[2]/div/div/div[2]/div/div/div/div/div[4]/div[5]/div/div[2]/ul/li[{str(i)}]/sup",
                f"//*[@id='pb-page-content']/div/div[2]/div/div/div[2]/div/div/div/div/div[2]/div[5]/div/div[2]/ul/li[{str(i)}]/sup"]})
            if number is None:
                number = '1'
            else:
                number = number.get_attribute('textContent')
            orgs2[number] = orgs1[i - 1][orgs1[i - 1].find(number) + len(number):]
        authors = [a.get_attribute('textContent')[:a.get_attribute('textContent').find(',')] for a in self.try_finding_elements_by({CSS: ['.contrib-author']})]
        for i in range(1, len(authors)):
            numbers = self.try_finding_element_by({XPATH: [
                f"//*[@id='pb-page-content']/div/div[2]/div/div/div[2]/div/div/div/div/div[4]/div[5]/div/div[1]/span[{str(i)}]/sup",
                f"//*[@id='pb-page-content']/div/div[2]/div/div/div[2]/div/div/div/div/div[4]/div[5]/div/div[1]/span[{str(i)}]/sup[1]",
                f"//*[@id='pb-page-content']/div/div[2]/div/div/div[2]/div/div/div/div/div[2]/div[5]/div/div[1]/span[{str(i)}]/sup",
                f"//*[@id='pb-page-content']/div/div[2]/div/div/div[2]/div/div/div/div/div[2]/div[5]/div/div[1]/span[{str(i)}]/sup[1]"]})
            if numbers is None:
                numbers = '1'
            else:
                numbers = numbers.get_attribute('textContent')
            for num in numbers.split(','):
                if num in orgs2 and not orgs2[num][0].isdigit():
                    if orgs2[num] not in publication_info.org_authors:
                        publication_info.org_authors[orgs2[num]] = []
                    publication_info.org_authors[orgs2[num]].append(authors[i - 1][:authors[i - 1].find(numbers)])
        return publication_info

    def get_art_meta_academicoup(self):
        publication_info = PublicationInformation()
        publication_info.name = self.try_finding_element_by({CSS: ['.wi-article-title.article-title-main', '.publicationContentTitle']}).text
        publication_info.abstract = self.try_finding_element_by({CSS: ['.abstract']}).text.replace('Abstract', '')
        publication_info.keywords = [k.text for k in self.try_finding_elements_by({CSS: ['.kwd-part.kwd-main']})]

        authors = self.try_finding_element_by({CSS: ['.al-authors-list']}).find_elements_by_css_selector('.al-author-name-more.js-flyout-wrap')
        for a in authors:
            if len(a.strip()) > 3:
                author = a.find_element_by_css_selector('.info-card-name').get_attribute('textContent').replace('*', '').strip()
                orgs = [u.get_attribute('textContent') for u in a.find_elements_by_css_selector('.aff')]
                for uni in orgs:
                    uni = delete_first_nums(uni)
                    if uni[0].islower():
                        uni = uni[1:]
                    if uni not in publication_info.org_authors:
                        publication_info.org_authors[uni] = []
                    publication_info.org_authors[uni].append(author)

        return publication_info

    def get_art_meta_iopsciense(self):
        publication_info = PublicationInformation()
        publication_info.name = self.try_finding_element_by({CSS: ['.wd-jnl-art-title']}).text
        publication_info.abstract = self.try_finding_element_by({CSS: ['.article-text.wd-jnl-art-abstract.cf']}).text
        publication_info.keywords = self.try_finding_element_by({CSS: ['.col-no-break.wd-jnl-aas-keywords']}).text.replace('Keywords', '').split('\n|\r')
        # article.pubdate = self.try_finding_element_by({CSS: ['.wd-jnl-art-pub-date']}).text.replace('Published', '')

        all_orgs = [u.get_attribute('textContent') for u in self.try_finding_element_by({CSS: ['.wd-jnl-art-author-affiliations']}).find_elements_by_css_selector('.mb-05')]
        orgs_dict = {}
        for uni in all_orgs:
            num = self.get_first_nums(uni)
            orgs_dict[num] = uni[uni.find(num) + len(num):].strip()
        authors = [a.get_attribute('textContent') for a in self.try_finding_element_by({CSS: ['.da1.ta1.article-head']}).find_element_by_css_selector('.mb-0').find_elements_by_css_selector('.nowrap')]
        for author in authors:
            nums = ""
            for s in author:
                if s.isdigit():
                    nums = author[author.find(s):]
                    break
            for n in nums.split(','):
                if n in orgs_dict:
                    if orgs_dict[n] not in publication_info.org_authors:
                        publication_info.org_authors[orgs_dict[n]] = []

                    publication_info.org_authors[orgs_dict[n]].append(author.replace(nums, ''))

        return publication_info

    def get_art_meta_rupress(self):
        publication_info = PublicationInformation()
        publication_info.name = self.try_finding_element_by({CSS: ['.wi-article-title.article-title-main']}).text
        publication_info.abstract = self.try_finding_element_by({CSS: ['.abstract']}).text
        publication_info.keywords = [k.strip() for k in self.try_finding_element_by({CSS: ['.content-metadata-subjects']}).text.replace('Subjects:', '').split(',')]

        cards = self.try_finding_elements_by({CSS: ['.info-card-author.authorInfo_ArticleTopInfo_SplitView']})
        for c in cards:
            author = c.find_element_by_css_selector('.info-card-name').get_attribute('textContent').strip().replace('*', '')
            orgs = [u.get_attribute('textContent').strip() for u in c.find_elements_by_css_selector('.institution')]
            for u in orgs:
                if u not in publication_info.org_authors:
                    publication_info.org_authors[u] = []
                publication_info.org_authors[u].append(author)

        return publication_info

    def get_art_meta_genomecshlp(self):  # нет ключевых слов
        publication_info = PublicationInformation()
        publication_info.name = self.try_finding_element_by({ID: ['article-title-1']}).text
        publication_info.abstract = self.try_finding_element_by({CSS: ['.section.abstract']}).text.replace('Abstract', '')

        orgs = self.try_finding_elements_by({CSS: ['.aff']})
        orgs_dict = {}
        for i in range(1, len(orgs) + 1):
            num = self.try_finding_element_by({XPATH: [f"//*[@id='content-block']/div[2]/div[1]/ol[2]/li[{str(i)}]/address/sup"]}).get_attribute('textContent')
            uni = orgs[i - 1].get_attribute('textContent').strip()
            orgs_dict[num] = uni[uni.find(num) + len(num):].replace(';', '').replace('\n', '')
        authors = self.try_finding_elements_by({CSS: ['.contributor']})
        for a in authors:
            name = a.find_element_by_css_selector('.name').get_attribute('textContent')
            nums = [n.text for n in a.find_elements_by_css_selector('.xref-aff')]
            for n in nums:
                if n in orgs_dict:
                    if orgs_dict[n] not in publication_info.org_authors:
                        publication_info.org_authors[orgs_dict[n]] = []
                    publication_info.org_authors[orgs_dict[n]].append(name)
        return publication_info

    def get_art_meta_planetcell(self):
        publication_info = PublicationInformation()
        publication_info.name = self.try_finding_element_by({ID: ['page-title']}).text
        publication_info.abstract = self.try_finding_element_by({CSS: ['.section.abstract']}).text.replace('Abstract', '')
        publication_info.keywords = [k.text for k in self.try_finding_elements_by({CSS: ['.kwd']})]

        i = 1
        while True:
            card = self.try_finding_element_by({CSS: [f'.author-tooltip-{str(i)}']})
            if card is None:
                break
            author = card.find_element_by_css_selector('.author-tooltip-name').get_attribute('textContent')
            orgs = card.find_elements_by_css_selector('.author-affiliation')
            for u in orgs:
                num = u.find_element_by_css_selector('.nlm-sup').get_attribute('textContent')
                u = u.get_attribute('textContent')
                u = u[u.find(num) + len(num):]
                if u not in publication_info.org_authors:
                    publication_info.org_authors[u] = []
                publication_info.org_authors[u].append(author)
            i += 1

        return publication_info

    # единственная ссылка в списке ведет к 404
    # def get_art_meta_aanda(self):
    #     publication_info = ArticleInformation()
    #     publication_info.name = self.try_finding_element_by({CSS: ['.title']}).text
    #     annotation = ''
    #     k = 5
    #     while annotation is not None:
    #         annotation = annotation + self.try_finding_element_by({XPATH: ['//*[@id="head"]/p[' + str(k) + ']']}).get_attribute('textContent')
    #         k = k + 1
    #     publication_info.keywords = self.try_finding_element_by({CSS: ['.kword']}).get_attribute('textContent').replace('Key words: ', '').split(';')
    #
    #     return publication_info

    def get_art_meta_geoscienceworld(self):
        publication_info = PublicationInformation()
        publication_info.name = self.try_finding_element_by({CSS: ['.wi-article-title.article-title-main']}).text
        publication_info.abstract = self.try_finding_element_by({CSS: ['.abstract']}).text
        publication_info.keywords = [k.get_attribute('textContent').strip() for k in self.try_finding_elements_by({CSS: ['.geoRef-indexterm']})]
        # article.pubdate = self.try_finding_element_by({CSS: ['.ii-pub-date', '.article-date']}).get_attribute('textContent')

        authors = self.try_finding_element_by({CSS: ['.al-authors-list']}).find_elements_by_css_selector('.al-author-name')
        for a in authors:
            author = a.find_element_by_css_selector('.info-card-name').get_attribute('textContent').replace('*', '').strip()
            orgs = [u.get_attribute('textContent') for u in a.find_elements_by_css_selector('.aff')]
            for uni in orgs:
                uni = delete_first_nums(uni)
                if uni not in publication_info.org_authors:
                    publication_info.org_authors[uni] = []
                publication_info.org_authors[uni].append(author)

        return publication_info

    def get_art_meta_wiley(self):
        publication_info = PublicationInformation()
        publication_info.name = self.try_finding_element_by({CSS: ['.citation__title']}).text
        publication_info.abstract = self.try_finding_element_by({CSS: ['.article-section.article-section__abstract']}).text.replace('Abstract', '')
        publication_info.keywords = [k.get_attribute('textContent').strip() for k in self.try_finding_elements_by({CSS: ['.badge-type']})]

        cards = self.try_finding_elements_by({CSS: ['.accordion-tabbed__tab-mobile.accordion__closed']})
        i = 1
        for c in cards:
            author = c.find_element_by_css_selector('.author-name.accordion-tabbed__control').get_attribute('textContent')
            k = 1
            while True:
                uni = self.try_finding_element_by({XPATH: [f"//*[@id='am{str(i)}']/p[{str(k)}]"]})
                if uni is None:
                    if k == 1:
                        k = 'error'
                    break
                uni = uni.get_attribute('textContent')
                if 'E‐mail:' not in uni and '@' not in uni and 'Correspond' not in uni and len(uni) > 40:
                    if uni not in publication_info.org_authors:
                        publication_info.org_authors[uni] = []
                    publication_info.org_authors[uni].append(author)
                k += 1
            if k == 'error':
                break
            i += 1

        return publication_info

    def get_art_meta_journalsaps(self):
        publication_info = PublicationInformation()
        publication_info.name = self.try_finding_element_by({XPATH: ["//*[@id='title']/div/large-12/div[1]/div[2]/div[1]/h3", "//*[@id='title']/div/large-12/div[1]/div/div[1]/h3"]}).get_attribute('textContent')
        publication_info.abstract = self.try_finding_element_by({XPATH: ["//*[@id='article-content']/section[1]/div/p[1]"]}).text.replace('\n', ' ')
        publication_info.keywords = [k.text for k in self.try_finding_elements_by({CSS: ['.physh-concept']})]

        b = self.try_finding_element_by({CSS: ['.article.authors']})
        if b is not None:
            try:
                b.click()
                time.sleep(4)
            except ElementClickInterceptedException:
                self.try_finding_element_by({CSS: ['.app__cookie-footer__button___34uYQ']}).click()
                b.click()
                time.sleep(4)
        l = 1
        orgs_dict = {}
        while True:
            uni = self.try_finding_element_by({XPATH: [
                f"//*[@id='article-content']/section[3]/div[1]/ul[1]/li[{str(l)}]",
                f"//*[@id='article-content']/section[2]/div[1]/ul[1]/li[{str(l)}]",
                f"//*[@id='article-content']/section[2]/div[1]/div/div/ul[1]/li[{str(l)}]",
                f"//*[@id='article-content']/section[3]/div[1]/div/div/ul[1]/li[{str(l)}]"]})
            if uni is None:
                break
            num = self.try_finding_element_by({XPATH: [
                f"//*[@id='article-content']/section[3]/div[1]/ul[1]/li[{str(l)}]/sup",
                f"//*[@id='article-content']/section[2]/div[1]/ul[1]/li[{str(l)}]/sup",
                f"//*[@id='article-content']/section[2]/div[1]/div/div/ul[1]/li[{str(l)}]/sup",
                f"//*[@id='article-content']/section[3]/div[1]/div/div/ul[1]/li[{str(l)}]/sup"]}).text.strip()
            uni = uni.get_attribute('textContent')
            orgs_dict[num] = uni[uni.find(num) + len(num):]
            l += 1
        print('UNIS_DICT: ', orgs_dict)

        i = 1
        k = 1
        while True:
            a = self.try_finding_element_by({XPATH: [f"//*[@id='article-content']/section[3]/div[1]/p[1]/a[{str(i)}]",
                                                     f"//*[@id='article-content']/section[2]/div[1]/p[1]/a[{str(i)}]",
                                                     f"//*[@id='article-content']/section[2]/div[1]/div/div/p[1]/a[{str(i)}]",
                                                     f"//*[@id='article-content']/section[3]/div[1]/div/div/p[1]/a[{str(i)}]"]})
            if a is None:
                break
            if len(a.text) > 1:
                nums = self.try_finding_element_by(
                    {XPATH: [f"//*[@id='article-content']/section[3]/div[1]/p[1]/sup[{str(k)}]",
                             f"//*[@id='article-content']/section[2]/div[1]/p[1]/sup[{str(k)}]",
                             f"//*[@id='article-content']/section[2]/div[1]/div/div/p[1]/sup[{str(k)}]",
                             f"//*[@id='article-content']/section[3]/div[1]/div/div/p[1]/sup[{str(k)}]"]})
                if nums is None:
                    if orgs_dict[''] not in publication_info.org_authors:
                        publication_info.org_authors[orgs_dict['']] = []
                    publication_info.org_authors[orgs_dict['']].append(a.text)
                    break
                nums = nums.text.split(',')
                k += 1
                for n in nums:
                    if n in orgs_dict:
                        if orgs_dict[n] not in publication_info.org_authors:
                            publication_info.org_authors[orgs_dict[n]] = []
                        publication_info.org_authors[orgs_dict[n]].append(a.text)
            i += 1

        return publication_info

    def get_art_meta_elifescience(self):
        publication_info = PublicationInformation()
        publication_info.name = self.try_finding_element_by({CSS: ['.content-header__title']}).text
        publication_info.abstract = self.try_finding_element_by({CSS: ['.article-section__body']}).text
        # article.pubdate = self.try_finding_element_by({CSS: ['.date']}).text

        for k in self.try_finding_elements_by({CSS: ['.article-meta__link_list_item']}):
            publication_info.keywords.append(k.text)
        for author in self.try_finding_elements_by({CSS: ['.author-details']}):
            orgs = author.text[:author.text.find('Contribution')].split('\n')
            for k in range(1, len(orgs)):
                if len(orgs[k]) > 2:
                    if orgs[k] not in publication_info.org_authors:
                        publication_info.org_authors[orgs[k]] = []
                    publication_info.org_authors[orgs[k]].append(orgs[0])

        return publication_info

    def get_art_metaCellajhg(self):
        time.sleep(10)
        publication_info = PublicationInformation()
        publication_info.name = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.article-header__title'))).get_attribute('textContent')
        publication_info.abstract = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.section-paragraph'))).text
        if '•' in publication_info.abstract:
            publication_info.abstract = self.try_finding_element_by({XPATH: ["//*[@id='pb-page-content']/div/div[1]/div/div/div/main/article/div[2]/div[3]/div/div[2]/section[2]/div/div"]}).text
        i = 1
        while True:
            k = self.try_finding_element_by({XPATH: [f"//*[@id='pb-page-content']/div/div[1]/div/div/div/main/article/div[2]/div[3]/div/div[2]/section[2]/ul/li[{str(i)}]",
                                                     f"//*[@id='pb-page-content']/div/div[1]/div/div/div/main/article/div[2]/div[3]/div/div[2]/section[4]/ul/li[{str(i)}]",
                                                     f"//*[@id='pb-page-content']/div/div[1]/div/div/div/main/article/div[2]/div[3]/div/div[2]/section[3]/ul/li[{str(i)}]"]})
            if k is None:
                break
            else:
                publication_info.keywords.append(k.text)
                i += 1

        cards = self.try_finding_elements_by({CSS: ['.article-header__info__scrollable']})
        authors = self.try_finding_elements_by({CSS: ['.article-header__info__label']})
        all_orgs = set([u.get_attribute('content') for u in self.try_finding_elements_by({NAME: ['citation_author_institution']})])
        if len(all_orgs) == 0:
            all_orgs = set([u.get_attribute('textContent') for u in self.try_finding_elements_by({CSS: ['.affiliation']})])
        for i in range(0, len(cards)):
            author_info = cards[i].get_attribute('textContent')
            orgs = [u for u in all_orgs if u in author_info]
            for u in orgs:
                if u not in publication_info.org_authors:
                    publication_info.org_authors[u] = []
                publication_info.org_authors[u].append(authors[i].get_attribute('textContent'))

        return publication_info
