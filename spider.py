from urllib.request import urlopen
from link_finder import LinkFinder
from domain import *
from general import *
from random_useragent.random_useragent import Randomize
from urllib.request import urlopen, Request


def Random_agent_generator():
    
    r_agent = Randomize()
    agent = r_agent.random_agent('desktop','windows') # returns 'Desktop / Linux'
    
    return agent 


class Spider:

    project_name = ''
    base_url = ''
    domain_name = ''
    queue_file = ''
    crawled_file = ''
    email_file = ''
    queue = set()
    crawled = set()
    email_list = set() #set of emails fetched

    def __init__(self, project_name, base_url, domain_name):
        Spider.project_name = project_name
        Spider.base_url = base_url
        Spider.domain_name = domain_name
        Spider.queue_file = Spider.project_name + '/queue.txt'
        Spider.crawled_file = Spider.project_name + '/crawled.txt'
        Spider.email_file = Spider.project_name + '/email_list.txt'
        self.boot()
        self.crawl_page('First spider', Spider.base_url)
        
        
        
    @staticmethod
    def Random_agent_generator():
        
        r_agent = Randomize()
        agent = r_agent.random_agent('desktop','windows') # returns 'Desktop / Linux'
        
        return agent 

    # Creates directory and files for project on first run and starts the spider
    @staticmethod
    def boot():
        create_project_dir(Spider.project_name)
        create_data_files(Spider.project_name, Spider.base_url)
        Spider.queue = file_to_set(Spider.queue_file)
        Spider.crawled = file_to_set(Spider.crawled_file)
        Spider.email_list = file_to_set(Spider.email_file)

    # Updates user display, fills queue and updates files
    @staticmethod
    def crawl_page(thread_name, page_url):
        if page_url not in Spider.crawled:
            print(thread_name + ' now crawling ' + page_url)
            print('Queue ' + str(len(Spider.queue)) + ' | Crawled  ' + str(len(Spider.crawled)))
            Spider.add_links_to_queue(Spider.gather_links(page_url))
            Spider.queue.remove(page_url)
            Spider.crawled.add(page_url)
            Spider.update_files()

    # Converts raw response data into readable information and checks for proper html formatting
    @staticmethod
    def gather_links(page_url):
        html_string = ''
        try:
            string_random_user_agent = Random_agent_generator()
            headers = {'User-Agent': string_random_user_agent}
            req = Request(url=page_url, headers=headers)
            response = urlopen(req)
            
            
            if 'text/html' in response.getheader('Content-Type'):
                html_bytes = response.read()
                html_string = html_bytes.decode("utf-8")
                
                
            finder = LinkFinder(Spider.base_url, page_url)
            finder.feed(html_string)
            
    
            list_tmp = finder.email_list()
            for email in list_tmp:
                Spider.email_list.add(email)
            
        except Exception as e:
            print(str(e))
            return set()
        return finder.page_links()
    
    

    # Saves queue data to project files
    @staticmethod
    def add_links_to_queue(links):
        for url in links:
            if (url in Spider.queue) or (url in Spider.crawled):
                continue
            if Spider.domain_name != get_domain_name(url):
                continue
            Spider.queue.add(url)

    @staticmethod
    def update_files():
        set_to_file(Spider.queue, Spider.queue_file)
        set_to_file(Spider.crawled, Spider.crawled_file)
        set_to_file(Spider.email_list, Spider.email_file)
