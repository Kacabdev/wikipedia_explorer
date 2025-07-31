import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for
import requests
from urllib.parse import quote

# Load environment variables (Vercel handles this in production)
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Supported languages and default language for Wikipedia API
SUPPORTED_LANGUAGES = {
    'en': 'English',
    'so': 'Somali',
    'ar': 'العربية',
    'es': 'Español',
    'fr': 'Français',
    'de': 'Deutsch',
    'it': 'Italiano'
}
DEFAULT_LANGUAGE = 'en'

# Helper function to construct Wikipedia RESTBase API URL for a given language
def get_wikipedia_base_url(lang_code):
    if lang_code not in SUPPORTED_LANGUAGES:
        lang_code = DEFAULT_LANGUAGE
    return f"https://{lang_code}.wikipedia.org/api/rest_v1/page/"

# Helper function to construct Wikipedia MediaWiki API URL for a given language
def get_mediawiki_base_url(lang_code):
    if lang_code not in SUPPORTED_LANGUAGES:
        lang_code = DEFAULT_LANGUAGE
    return f"https://{lang_code}.wikipedia.org/w/api.php"


# Home route: Displays a random Wikipedia page
@app.route('/')
def home():
    # Get language from URL parameters, default to English
    lang = request.args.get('lang', DEFAULT_LANGUAGE)
    if lang not in SUPPORTED_LANGUAGES:
        lang = DEFAULT_LANGUAGE

    wikipedia_api_url = get_wikipedia_base_url(lang) + "random/summary"

    try:
        response = requests.get(wikipedia_api_url)
        response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)
        article_data = response.json()

        title = article_data.get('title', 'No Title Found')
        summary = article_data.get('extract', 'No summary available.')
        full_page_url = article_data.get('content_urls', {}).get('desktop', {}).get('page', '#')

        return render_template("index.html", 
                               random_article={'title': title, 'summary': summary, 'full_page_url': full_page_url},
                               current_lang=lang,
                               supported_languages=SUPPORTED_LANGUAGES)

    except requests.exceptions.RequestException as e:
        # Handle API connection/response errors
        error_message = f"Error fetching from Wikipedia API: {e}"
        print(error_message)
        return render_template("index.html", error=error_message, current_lang=lang, supported_languages=SUPPORTED_LANGUAGES)
    except Exception as e:
        # Handle any other unexpected errors
        error_message = f"An unexpected error occurred: {e}"
        print(error_message)
        return render_template("index.html", error=error_message, current_lang=lang, supported_languages=SUPPORTED_LANGUAGES)

# Route to fetch another random page
@app.route('/random')
def get_random_page():
    lang = request.args.get('lang', DEFAULT_LANGUAGE)
    return redirect(url_for('home', lang=lang))

# Search route: Displays search results from Wikipedia
@app.route('/search')
def search():
    query = request.args.get('q')
    lang = request.args.get('lang', DEFAULT_LANGUAGE)
    if lang not in SUPPORTED_LANGUAGES:
        lang = DEFAULT_LANGUAGE

    if not query:
        return redirect(url_for('home', lang=lang))

    encoded_query = quote(query) # URL-encode the query
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
        error_message = f"Error searching Wikipedia API: {e}"
        print(error_message)
        return render_template("index.html", error=error_message, current_lang=lang, supported_languages=SUPPORTED_LANGUAGES)
    except Exception as e:
        error_message = f"An unexpected error occurred during search: {e}"
        print(error_message)
        return render_template("index.html", error=error_message, current_lang=lang, supported_languages=SUPPORTED_LANGUAGES)

# This is the WSGI application entry point for Vercel
# Vercel expects a callable named 'app'
# No app.run() here as Vercel handles the server
