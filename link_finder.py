from html.parser import HTMLParser
from urllib import parse
import re

class LinkFinder(HTMLParser):

    def __init__(self, base_url, page_url):
        super().__init__()
        self.base_url = base_url
        self.page_url = page_url
        self.links = set()
        self.emails_list = []
        
        
    # When we call HTMLParser feed() this function is called when it encounters an opening tag <a>
    def handle_starttag(self, tag, attrs):
        
        if tag == 'a':
            for (attribute, value) in attrs:
                if attribute == 'href':
                    url = parse.urljoin(self.base_url, value)
                    self.links.add(url)
                    
    
    def handle_data(self, data):
    
        match = re.findall(r'[\w\.-]+@[\w\.-]+', data)
        for emails in match:
            self.emails_list.append(emails)
    
    
    def page_links(self):
        return self.links

    def email_list(self):
        return self.emails_list

    def error(self, message):
        pass









