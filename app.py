from flask import Flask, request, jsonify
from bs4 import BeautifulSoup
import requests
import os

app = Flask(__name__)

@app.route('/scrape', methods=['POST'])
def yellowpages_scraper():
    data = request.json
    country = data.get("country", "Saudi Arabia").lower()
    niche = data.get("niche", "")
    brand = data.get("brand", "")
    search_query = f"{niche} {brand}".strip().replace(" ", "+")

    url = f"https://www.yellowpages.com.sa/search?q={search_query}"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")
    listings = soup.select(".business-card")[:5]  # Select top 5 listings

    results = []
    for card in listings:
        name = card.select_one(".business-name")
        phone = card.select_one(".phone-number")
        email = card.select_one(".email")
        company_name = name.get_text(strip=True) if name else "N/A"
        phone_number = phone.get_text(strip=True) if phone else "N/A"
        email_address = email.get_text(strip=True) if email else "N/A"

        results.append({
            "company_name": company_name,
            "country": country.title(),
            "industry": niche,
            "email": email_address,
            "phone": phone_number
        })

    return jsonify(results)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
