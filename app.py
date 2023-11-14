from flask import Flask, render_template, request, redirect, url_for
import whoosh.index as index
from whoosh.qparser import QueryParser

app = Flask(__name__)

# Path to the Whoosh index directory
INDEX_DIR = 'woosh_index'

# Create a Whoosh index object
index_object = index.open_dir(INDEX_DIR)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Handle the form submission
        search_query = request.form.get('search_query')
        # Redirect to the search route with the search query as a parameter
        if search_query:
            return redirect(url_for('search', q=search_query))
    # Render the search form template for GET requests
    return render_template('search_form.html')

@app.route('/search', methods=['GET'])
def search():
    # Get the search query from the request parameters
    search_query = request.args.get('q', '')
    if search_query:
        #perform search using the whoosh index
        with index_object.searcher() as searcher:
            query_parser = QueryParser("content", schema=index_object.schema)
            query = query_parser.parse(search_query)
            results = searcher.search(query)
            search_results = []
             # Extract relevant information from search results
            for result in results:
                search_results.append({
                    "url": result["url"],
                    "title": result["title"],
                    "teaser": result["teaser"]
                })
             # Render the results template with the search query and results
            return render_template('results.html', search_query=search_query, search_results=search_results)
     # Render the results template with an empty search query and no results for the initial page load
    return render_template('results.html', search_query=search_query, search_results=[])

if __name__ == '__main__':
    #run the flask app
    app.run(debug=True)
