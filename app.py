from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import os

app = Flask(__name__)

@app.route('/scrape', methods=['POST'])
def scrape_google_maps():
    data = request.json
    country = data.get("country")
    niche = data.get("niche")
    brand = data.get("brand", "")

    query = f"{niche} {brand} in {country}".strip()

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=options)

    driver.get(f"https://www.google.com/maps/search/{query.replace(' ', '+')}")
    time.sleep(10)  # ⏳ Wait longer for listings to fully load

    results = []
    listings = driver.find_elements(By.CLASS_NAME, "Nv2PK")[:5]  # updated class

    for item in listings:
        try:
            title = item.text.split("\n")[0]
            results.append({
                "company_name": title,
                "country": country,
                "industry": niche,
                "email": "N/A",
                "phone": "N/A"
            })
        except Exception as e:
            continue

    driver.quit()
    return jsonify(results)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
