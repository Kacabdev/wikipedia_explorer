import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for
import requests

# Load environment variables (haddii aan u baahano mustaqbalka)
load_dotenv()

app = Flask(__name__)

# Route-ka ugu muhiimsan ee soo bandhigaya bogga random-ka ah ee Wikipedia
@app.route('/')
def home():
    # Wikipedia API endpoint for a random page summary
    # Tani waxay soo celisaa JSON leh cinwaan iyo sharraxaad kooban
    wikipedia_api_url = "https://en.wikipedia.org/api/rest_v1/page/random/summary"

    try:
        response = requests.get(wikipedia_api_url)
        response.raise_for_status() # Wuxuu soo saaraa HTTPError haddii jawaabtu tahay 4xx/5xx
        article_data = response.json()

        # Soo qaado macluumaadka muhiimka ah
        title = article_data.get('title', 'No Title Found')
        summary = article_data.get('extract', 'No summary available.')
        full_page_url = article_data.get('content_urls', {}).get('desktop', {}).get('page', '#')

        # Ku gudbi macluumaadka template-ka
        return render_template("index.html", title=title, summary=summary, full_page_url=full_page_url)

    except requests.exceptions.RequestException as e:
        # Maamul ciladaha xiriirka ama API-ga
        error_message = f"Cilad ka timid Wikipedia API: {e}"
        print(error_message) # Ku daabac terminalka si aad u aragto
        return render_template("index.html", error=error_message)
    except Exception as e:
        # Maamul ciladaha kale ee aan la filayn
        error_message = f"Cilad aan la filayn: {e}"
        print(error_message)
        return render_template("index.html", error=error_message)

# Route-ka loogu talagalay inuu soo qaado bog kale oo random ah
@app.route('/random')
def get_random_page():
    return redirect(url_for('home')) # Dib ugu celi home route-ka si uu u soo qaado mid cusub

if __name__ == '__main__':
    app.run(debug=True)
