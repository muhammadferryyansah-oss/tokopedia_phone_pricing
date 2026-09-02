
import os
import time
import pandas as pd
from playwright.sync_api import sync_playwright

# 40 target kata kunci spesifik lintas merek & segmen harga
TARGET_KEYWORDS = [
    # Apple iPhone
    "iphone 11", "iphone 12", "iphone 13", "iphone 14", "iphone 15", "iphone 16",
    "iphone 13 pro", "iphone 15 pro",
    # Samsung Flagship & Foldable
    "samsung galaxy s22", "samsung galaxy s23", "samsung galaxy s24",
    "samsung galaxy z flip", "samsung galaxy z fold",
    # Samsung Mid-Range & Entry
    "samsung galaxy a05s", "samsung galaxy a15", "samsung galaxy a25",
    "samsung galaxy a35", "samsung galaxy a55",
    # Xiaomi & Redmi
    "redmi 13c", "redmi note 12", "redmi note 13", "xiaomi 13t", "xiaomi 14",
    # Poco Series
    "poco m6 pro", "poco x6", "poco x6 pro", "poco f5", "poco f6",
    # Infinix & Tecno & itel
    "infinix hot 40 pro", "infinix note 30", "infinix note 40", "infinix gt 20 pro",
    "tecno spark 20", "tecno pova 6", "itel s23",
    # Oppo & Vivo & Realme
    "oppo a78", "oppo reno 11", "vivo y27", "vivo v30", "vivo v40",
    "realme c67", "realme 12", "iqoo z9", "asus rog phone"
]

BLACKLIST = [
    "tripod", "mic", "microphone", "gimbal", "stabilizer", "holder",
    "monopod", "cable", "kabel", "case", "casing", "charger",
    "powerbank", "power station", "lens", "lensa", "lighting",
    "battery", "v-mount", "mount", "touchscreen", "strap", "adaptor",
    "tempered glass", "hydrogel", "screen protector", "tws", "earphone", "headset"
]

def is_valid_phone(title: str) -> bool:
    t = title.lower()
    return not any(bad in t for bad in BLACKLIST)

def scrape_1000_smartphones():
    os.makedirs("Data", exist_ok=True)
    all_products = []
    seen_identifiers = set()

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False,
            args=["--disable-blink-features=AutomationControlled", "--start-maximized"]
        )
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            no_viewport=True
        )
        page = context.new_page()

        print(f"Target: Minimal 1.000 data produk.")
        print(f"Total kata kunci yang disiapkan: {len(TARGET_KEYWORDS)}\n")

        for idx, kw in enumerate(TARGET_KEYWORDS, 1):
            url = f"https://www.tokopedia.com/search?q={kw.replace(' ', '%20')}&pmin=1000000&ob=5"
            print(f"[{idx}/{len(TARGET_KEYWORDS)}] Mencari: '{kw}'")

            try:
                page.goto(url, wait_until="domcontentloaded", timeout=60000)
                time.sleep(2)

                # Auto-scroll bertahap sampai seluruh kartu ter-render
                for _ in range(8):
                    page.mouse.wheel(0, 850)
                    time.sleep(0.5)

                cards = page.locator('a:has-text("Rp")').all()

                new_items_count = 0
                for card in cards:
                    try:
                        text = card.inner_text().strip()
                        lines = [l.strip() for l in text.split("\n") if l.strip()]

                        price = next((l for l in lines if l.startswith("Rp")), None)
                        if not price:
                            continue

                        title = next((l for l in lines if len(l) > 12 and not l.startswith("Rp") and "terjual" not in l.lower()), None)
                        if not title or not is_valid_phone(title):
                            continue

                        # Identifikasi unik agar data tidak kembar
                        unique_id = f"{title.strip().lower()}_{price.strip()}"
                        if unique_id in seen_identifiers:
                            continue

                        sold = next((l for l in lines if "terjual" in l.lower()), None)
                        rating = next((l for l in lines if l.replace(".", "", 1).isdigit() and len(l) <= 3 and float(l) <= 5.0), None)

                        seen_identifiers.add(unique_id)
                        all_products.append({
                            "search_keyword": kw,
                            "title": title.strip(),
                            "price": price.strip(),
                            "rating": rating,
                            "sold_count": sold
                        })
                        new_items_count += 1
                    except Exception:
                        continue

                print(f"   + Menambahkan {new_items_count} data baru | Total data unik saat ini: {len(all_products)}")
                time.sleep(1)

            except Exception as e:
                print(f"   x Error pada kata kunci '{kw}': {e}")
                continue

        browser.close()

    # Ekspor akhir ke CSV
    df = pd.DataFrame(all_products)
    output_path = "Data/raw_tokopedia_smartphone.csv"
    df.to_csv(output_path, index=False)

    print("\n" + "=" * 55)
    print(f"SELESAI! Total {len(df)} unit ponsel unik tersimpan di '{output_path}'.")
    print("=" * 55)

if __name__ == "__main__":
    scrape_1000_smartphones()