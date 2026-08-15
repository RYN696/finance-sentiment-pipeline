import feedparser
import requests
from bs4 import BeautifulSoup
import json
import time
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))
from config import RAW_DIR

FLUX_PAR_TICKER = {
    "TotalEnergies": "TTE", "LVMH": "LVMUY", "Sanofi": "SNY",
    "Apple": "AAPL", "Microsoft": "MSFT", "Amazon": "AMZN",
    "Tesla": "TSLA", "Google": "GOOGL", "Meta": "META",
    "Nvidia": "NVDA", "JPMorgan": "JPM", "Johnson & Johnson": "JNJ",
    "Walmart": "WMT", "Visa": "V", "ExxonMobil": "XOM",
    "Coca-Cola": "KO", "Netflix": "NFLX", "Disney": "DIS", "Intel": "INTC"
}

HEADERS = {"User-Agent": "Mozilla/5.0"}

def recuperer_summary(url, max_caracteres=800):
    try:
        response = requests.get(url, headers=HEADERS, timeout=5)
        soup = BeautifulSoup(response.content, "html.parser")
        paragraphes = soup.find_all("p")
        texte = " ".join(p.get_text(strip=True) for p in paragraphes if len(p.get_text(strip=True)) > 40)
        return texte[:max_caracteres]
    except Exception:
        return ""

def collecter():
    tous_les_articles = []

    for entreprise, ticker in FLUX_PAR_TICKER.items():
        url_flux = f"https://feeds.finance.yahoo.com/rss/2.0/headline?s={ticker}&region=US&lang=en-US"
        feed = feedparser.parse(url_flux)
        print(f"{entreprise} ({ticker}) : {len(feed.entries)} articles trouvés dans le flux")

        for entry in feed.entries[:5]:  # limite 5 par entreprise
            titre = entry.get("title", "")
            lien = entry.get("link", "")
            summary = recuperer_summary(lien) if lien else ""

            tous_les_articles.append({
                "entreprise_cible": entreprise,
                "title": titre,
                "summary": summary,
                "source": "Yahoo Finance RSS",
                "url": lien,
                "published_at": entry.get("published", "")
            })
            time.sleep(0.3)

    print(f"\nTotal articles collectés : {len(tous_les_articles)}")

    RAW_DIR.mkdir(parents=True, exist_ok=True)
    output_path = RAW_DIR / "articles_rss.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(tous_les_articles, f, ensure_ascii=False, indent=2)

    print(f"Sauvegardé dans {output_path}")
    return tous_les_articles

if __name__ == "__main__":
    collecter()