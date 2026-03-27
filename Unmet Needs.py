import google.generativeai as genai
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time
import random
import urllib.parse

GEMINI_API_KEY = "apı key"
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-flash-latest')

def analyze_with_gemini(tweets_text):
    """Toplanan verileri analiz ederek pazar fırsatlarını çıkarır."""
    if not tweets_text.strip():
        return "Analiz edilecek veri bulunamadı."

    prompt = f"""
    Aşağıda hazır yemek sektörüyle ilgili tüketicilerin gerçek tweetleri yer alıyor:
    ---
    {tweets_text}
    ---
    Yukarıdaki verilere dayanarak, bir pazar analisti gibi şu analizi yap:
    1. Sektörde en çok dile getirilen 3 temel şikayet nedir?
    2. Tüketicilerin "keşke olsa" dediği, karşılanmayan 2 spesifik ürün veya hizmet fikri nedir?
    3. Girişimciler için kısa bir 'pazar boşluğu' özeti yaz.
    Yanıtı profesyonel bir rapor formatında Türkçe olarak ver.
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Gemini Analiz Hatası: {str(e)}"

def connect_and_scrape_safe(keywords):
    results = []
    print("--- TWITTER TARAMASI VE GEMINI ANALİZİ BAŞLIYOR ---")
    print("Not: Chrome'un '9222' portunda açık olması gerekir.\n")
    
    options = webdriver.ChromeOptions()
    options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    
    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        
        for index, word in enumerate(keywords):
            print(f"[{index+1}/{len(keywords)}] --> '{word}' aranıyor...")
            
            try:
                query = f"{word} lang:tr"
                encoded_query = urllib.parse.quote(query)
                search_url = f"https://twitter.com/search?q={encoded_query}&src=typed_query&f=live"
                driver.get(search_url)
                
                time.sleep(random.uniform(6, 15))
                
                found_tweets_in_loop = set()
                for _ in range(10): 
                    tweets = driver.find_elements(By.CSS_SELECTOR, '[data-testid="tweetText"]')
                    for t in tweets:
                        text = t.text
                        if len(text) > 20 and text not in found_tweets_in_loop:
                            results.append({"Konu": word, "Tweet": text})
                            found_tweets_in_loop.add(text)
                    
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(random.uniform(6,15))
                
                print(f"    ✓ {len(found_tweets_in_loop)} tweet toplandı.")

            except Exception as e:
                print(f"    ! Hata oluştu: {e}")

            if index < len(keywords) - 1:
                wait_time = random.randint(6,20)
                print(f"\n>> Güvenlik Modu: Bir sonraki keyword öncesi {wait_time} saniye bekleniyor...")
                time.sleep(wait_time)
                print("-" * 30)

    except Exception as e:
        print(f"\n!!! BAĞLANTI HATASI: {e}")

    finally:
        if results:
            df = pd.DataFrame(results)
            unique_tweets = list(df['Tweet'].unique())
            all_tweets_combined = "\n".join(unique_tweets[:100]) 
            
            print("\n" + "="*50)
            print("GEMINI YAPAY ZEKA STRATEJİK ANALİZİ:")
            analiz_notu = analyze_with_gemini(all_tweets_combined)
            print(analiz_notu)
            print("="*50 + "\n")

            df.to_excel("hazir_yemek_sikayet_analizi.xlsx", index=False)
            with open("pazar_analiz_raporu.txt", "w", encoding="utf-8") as f:
                f.write(analiz_notu)
            print("İşlem tamamlandı. Veriler Excel'e, analiz rapora kaydedildi.")
        else:
            print("Analiz edilecek veri toplanamadı.")

keywords = [
    "keyword1",
    "key word2"
]

if __name__ == "__main__":
    connect_and_scrape_safe(keywords)