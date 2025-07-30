import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for
import requests
from urllib.parse import quote

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Dejinta luqadaha la taageerayo iyo luqadda asalka ah
SUPPORTED_LANGUAGES = {
    'en': 'English',
    'so': 'Somali',
    'ar': 'العربية', # Arabic
    'es': 'Español', # Spanish
    'fr': 'Français', # French
    'de': 'Deutsch', # German
    'it': 'Italiano' # Italian
}
DEFAULT_LANGUAGE = 'en' # Luqadda asalka ah

# Function caawiya oo dhisaya base URL-ka Wikipedia API-ga luqadda
def get_wikipedia_base_url(lang_code):
    if lang_code not in SUPPORTED_LANGUAGES:
        lang_code = DEFAULT_LANGUAGE # Haddii luqadda aan la taageerin, ku laabo default
    return f"https://{lang_code}.wikipedia.org/api/rest_v1/page/"

# Function caawiya oo dhisaya base URL-ka Wikipedia MediaWiki API-ga luqadda
def get_mediawiki_base_url(lang_code):
    if lang_code not in SUPPORTED_LANGUAGES:
        lang_code = DEFAULT_LANGUAGE
    return f"https://{lang_code}.wikipedia.org/w/api.php"


# Route-ka ugu muhiimsan ee soo bandhigaya bogga random-ka ah ee Wikipedia
@app.route('/')
def home():
    # Soo qaado luqadda ka yimid URL-ka, haddii kale isticmaal default
    lang = request.args.get('lang', DEFAULT_LANGUAGE)
    if lang not in SUPPORTED_LANGUAGES:
        lang = DEFAULT_LANGUAGE # Hubi mar kale in luqadda la taageerayo

    wikipedia_api_url = get_wikipedia_base_url(lang) + "random/summary"

    try:
        response = requests.get(wikipedia_api_url)
        response.raise_for_status()
        article_data = response.json()

        title = article_data.get('title', 'No Title Found')
        summary = article_data.get('extract', 'No summary available.')
        full_page_url = article_data.get('content_urls', {}).get('desktop', {}).get('page', '#')

        return render_template("index.html", 
                               random_article={'title': title, 'summary': summary, 'full_page_url': full_page_url},
                               current_lang=lang, # Ku gudbi luqadda hadda jirta template-ka
                               supported_languages=SUPPORTED_LANGUAGES) # Ku gudbi luqadaha la taageerayo

    except requests.exceptions.RequestException as e:
        error_message = f"Cilad ka timid Wikipedia API: {e}"
        print(error_message)
        return render_template("index.html", error=error_message, current_lang=lang, supported_languages=SUPPORTED_LANGUAGES)
    except Exception as e:
        error_message = f"Cilad aan la filayn: {e}"
        print(error_message)
        return render_template("index.html", error=error_message, current_lang=lang, supported_languages=SUPPORTED_LANGUAGES)

# Route-ka loogu talagalay inuu soo qaado bog kale oo random ah
@app.route('/random')
def get_random_page():
    lang = request.args.get('lang', DEFAULT_LANGUAGE) # Soo qaado luqadda hadda jirta
    return redirect(url_for('home', lang=lang)) # Dib ugu celi home route-ka oo leh luqadda

# Route-ka cusub ee raadinta
@app.route('/search')
def search():
    query = request.args.get('q')
    lang = request.args.get('lang', DEFAULT_LANGUAGE) # Soo qaado luqadda hadda jirta
    if lang not in SUPPORTED_LANGUAGES:
        lang = DEFAULT_LANGUAGE

    if not query:
        return redirect(url_for('home', lang=lang))

    encoded_query = quote(query)
    search_api_url = get_mediawiki_base_url(lang) + f"?action=query&list=search&srsearch={encoded_query}&format=json&srlimit=10"

    try:
        response = requests.get(search_api_url)
        response.raise_for_status()
        search_results = response.json()

        articles = []
        if 'query' in search_results and 'search' in search_results['query']:
            for item in search_results['query']['search']:
                articles.append({
                    'title': item.get('title'),
                    'snippet': item.get('snippet'),
                    'full_page_url': f"https://{lang}.wikipedia.org/wiki/{quote(item.get('title'))}"
                })
        
        return render_template("index.html", 
                               search_query=query, 
                               search_results=articles,
                               current_lang=lang,
                               supported_languages=SUPPORTED_LANGUAGES)

    except requests.exceptions.RequestException as e:
        error_message = f"Cilad ka timid Wikipedia API inta la raadinayay: {e}"
        print(error_message)
        return render_template("index.html", error=error_message, current_lang=lang, supported_languages=SUPPORTED_LANGUAGES)
    except Exception as e:
        error_message = f"Cilad aan la filayn inta la raadinayay: {e}"
        print(error_message)
        return render_template("index.html", error=error_message, current_lang=lang, supported_languages=SUPPORTED_LANGUAGES)


if __name__ == '__main__':
    app.run(debug=True)
