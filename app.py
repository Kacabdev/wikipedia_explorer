import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for
import requests
from urllib.parse import quote # Waxaan u baahanahay tan si aan u encode-no query-ga URL-ka

# Load environment variables (haddii aan u baahano mustaqbalka)
load_dotenv()

app = Flask(__name__)

# Route-ka ugu muhiimsan ee soo bandhigaya bogga random-ka ah ee Wikipedia
@app.route('/')
def home():
    wikipedia_api_url = "https://en.wikipedia.org/api/rest_v1/page/random/summary"

    try:
        response = requests.get(wikipedia_api_url)
        response.raise_for_status() # Wuxuu soo saaraa HTTPError haddii jawaabtu tahay 4xx/5xx
        article_data = response.json()

        title = article_data.get('title', 'No Title Found')
        summary = article_data.get('extract', 'No summary available.')
        full_page_url = article_data.get('content_urls', {}).get('desktop', {}).get('page', '#')

        # Ku gudbi macluumaadka template-ka. Halkan waxaan ku gudbinaynaa hal article.
        return render_template("index.html", random_article={'title': title, 'summary': summary, 'full_page_url': full_page_url})

    except requests.exceptions.RequestException as e:
        error_message = f"Cilad ka timid Wikipedia API: {e}"
        print(error_message)
        return render_template("index.html", error=error_message)
    except Exception as e:
        error_message = f"Cilad aan la filayn: {e}"
        print(error_message)
        return render_template("index.html", error=error_message)

# Route-ka loogu talagalay inuu soo qaado bog kale oo random ah
@app.route('/random')
def get_random_page():
    return redirect(url_for('home')) # Dib ugu celi home route-ka si uu u soo qaado mid cusub

# Route-ka cusub ee raadinta
@app.route('/search')
def search():
    query = request.args.get('q') # Soo qaado query-ga ka yimid URL-ka (?q=your_query)

    if not query:
        # Haddii uusan jirin query, dib ugu celi bogga hore ama soo bandhig fariin
        return redirect(url_for('home'))

    # Wikipedia API endpoint for search
    # Waxaan isticmaalaynaa MediaWiki API, kaasoo siiya natiijooyin raadin oo faahfaahsan
    # 'opensearch' waa mid fudud, laakin 'action=query&list=search' ayaa ka awood badan
    # encode-garaynta query-ga si uu ugu habboonaado URL-ka
    encoded_query = quote(query)
    search_api_url = f"https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch={encoded_query}&format=json&srlimit=10" # limit to 10 results

    try:
        response = requests.get(search_api_url)
        response.raise_for_status()
        search_results = response.json()

        articles = []
        # Falanqaynta natiijooyinka raadinta
        if 'query' in search_results and 'search' in search_results['query']:
            for item in search_results['query']['search']:
                # Soo qaado summary for each search result (tani waxay u baahan tahay codsi kale)
                # Si loo fududeeyo, marka hore waxaan kaliya soo bandhigaynaa title iyo snippet
                articles.append({
                    'title': item.get('title'),
                    'snippet': item.get('snippet'),
                    'full_page_url': f"https://en.wikipedia.org/wiki/{quote(item.get('title'))}" # Dhis URL-ka bogga oo buuxa
                })
        
        # Ku gudbi natiijooyinka raadinta template-ka
        return render_template("index.html", search_query=query, search_results=articles)

    except requests.exceptions.RequestException as e:
        error_message = f"Cilad ka timid Wikipedia API inta la raadinayay: {e}"
        print(error_message)
        return render_template("index.html", error=error_message)
    except Exception as e:
        error_message = f"Cilad aan la filayn inta la raadinayay: {e}"
        print(error_message)
        return render_template("index.html", error=error_message)


if __name__ == '__main__':
    app.run(debug=True)
