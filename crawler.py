import requests
from bs4 import BeautifulSoup
import re
import os
import whoosh.index
from whoosh.qparser import QueryParser
from whoosh.fields import Schema, TEXT, ID, STORED

from whoosh.highlight import Highlighter, WholeFragmenter, UppercaseFormatter

# Define the schema for the Woosh index
schema = Schema(
    url=ID(stored=True),
    content=TEXT(stored=True),
    teaser=TEXT(stored=True),
    title=TEXT(stored=True),

)

# Create  the Woosh index directory
INDEX_DIR = 'woosh_index'
#if directory does not exist,create one 
if not os.path.exists(INDEX_DIR):
    os.mkdir(INDEX_DIR)
index = whoosh.index.create_in(INDEX_DIR, schema)
#define a class to crawl the pages
class Crawler:
    def __init__(self):
        #keep track of visited url
        self.visited_link = set()
        #queue to manage links to be visited
        self.to_visit = []
        self.writer = index.writer()

    def get_url_content(self, url):
        #fetch content and handle failed requests
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException:
            return None
     
    def crawl(self, start_url):
        #iniatise the starting url
        self.to_visit.append(start_url)

        while self.to_visit:

            current_url = self.to_visit.pop(0)
            #skip already visited url
            if current_url in self.visited_link:
                continue

            content = self.get_url_content(current_url)

            if content is not None:
                #extract information from the url content
                soup = BeautifulSoup(content, 'html.parser')
                page_title = soup.title.string if soup.title else ""
                page_text = soup.get_text()
                teaser_text = page_text[:200]  # Extract the first 200 characters as teaser text
                words = re.findall(r'\w+', page_text.lower())
                #add document to whoosh index
                self.writer.add_document(url=current_url, title=page_title, content=page_text, teaser=teaser_text)
                #extract all links and add to the queue
                for link in soup.find_all('a'):
                    href = link.get('href')
                    if href and href.startswith('http'):
                        self.to_visit.append(href)

                self.visited_link.add(current_url)

    def commit_index(self):
        #save the changes to the whoosh index
        self.writer.commit()

#function to search the whoosh index
    
def search(query):
    with index.searcher() as searcher:
        # Parse the search query and perform a search
        query_parser = QueryParser("content", schema=index.schema)
        query = query_parser.parse(query)
        
        # Use the WholeFragmenter to get the entire field value as a fragment
        frag = WholeFragmenter()

        # Use the UppercaseFormatter for case-insensitive highlighting
        format = UppercaseFormatter()

        # Set up a highlighter with the chosen fragmenter and formatter
        highlighter = Highlighter(fragmenter=frag,formatter=format)

        # Search and apply highlighting to the content field
        results = searcher.search(query)
        results.fragmenter = frag
        results.formatter = format

        # Extract and return the URLs of the search results with highlighted snippets
        result_data = []
        for result in results:
            # Get highlighted snippets for the "content" field
            content_highlights = highlighter.highlight_hit(result, "content")
            
            # Append the URL and highlighted content to the result_data list
            result_data.append({
                "url": result["url"],
                "highlighted_content": content_highlights
            })

        return result_data
#testing crawler.py
    #define a start url
start_url = "https://vm009.rz.uos.de/crawl/index.html"
    #initialise and run crawler
crawler = Crawler()
crawler.crawl(start_url)
    #save changes to whoosh index
crawler.commit_index()
    
    # Define a search query and perform a search
search_query = input("Enter something to searh :")
result_links = search(search_query)
print(result_links)
