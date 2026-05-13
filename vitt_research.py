import yfinance as yf
import google.generativeai as genai
import os

# ==========================================
# VITT WIRE: VERIFIED RESEARCH & SCRIPTING
# ==========================================

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-pro')

def fetch_morning_intelligence():
    """Fetches verified US Market and Crypto data."""
    nasdaq = yf.Ticker("^IXIC").history(period="2d")
    btc = yf.Ticker("BTC-USD").history(period="2d")

    nas_change = ((nasdaq['Close'].iloc[-1] - nasdaq['Close'].iloc[-2]) / nasdaq['Close'].iloc[-2]) * 100
    btc_change = ((btc['Close'].iloc[-1] - btc['Close'].iloc[-2]) / btc['Close'].iloc[-2]) * 100
    
    return {
        "nasdaq_pc": round(nas_change, 2),
        "btc_price": round(btc['Close'].iloc[-1], 2),
        "btc_pc": round(btc_change, 2)
    }

def generate_hinglish_script(data):
    """Converts raw market data into your philosophical brand voice."""
    prompt = f"""
    Context: You are a professional Strategist.
    Data: US Nasdaq changed {data['nasdaq_pc']}%, Bitcoin is at ${data['btc_price']} ({data['btc_pc']}%).
    Task: Write a 30-second broadcast script (approx 70 words).
    Tone: Philosophical, Authoritative, Calm. 
    Language: Mix of professional English and natural Hindi (Hinglish).
    """
    response = model.generate_content(prompt)
    with open("daily_script.txt", "w", encoding="utf-8") as f:
        f.write(response.text)
    return response.text

if __name__ == "__main__":
    raw_data = fetch_morning_intelligence()
    generate_hinglish_script(raw_data)
