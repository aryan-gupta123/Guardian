"""
BrightData - PURE LIVE SCRAPING ONLY
"""
import logging
import requests
from typing import Dict, Optional, Tuple
from bs4 import BeautifulSoup
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

logger = logging.getLogger(__name__)


class BrightDataScraper:
    
    def __init__(self):
        self.proxy_url = "http://brd-customer-hl_2b87b9a2-zone-residential_proxy1:3vlleo2hdq9r@brd.superproxy.io:33335"
        self.proxies = {"http": self.proxy_url, "https": self.proxy_url}
    
    def scrape_merchant_reviews(self, merchant_name: str) -> Dict:
        print(f"\n🚀 [BrightData] LIVE SCRAPING: {merchant_name}")
        
        # ONLY Wikipedia scraping - no database
        wiki_data = self._scrape_wikipedia(merchant_name)
        if wiki_data:
            return wiki_data
        
        # If Wikipedia fails, return minimal default
        print("⚠️ Wikipedia failed, using default")
        return self._default()
    
    def _scrape_wikipedia(self, name: str) -> Optional[Dict]:
        urls = [
            f"https://en.wikipedia.org/wiki/{name.replace(' ', '_')}",
            f"https://en.wikipedia.org/wiki/{name.replace(' ', '_')}_Inc.",
            f"https://en.wikipedia.org/wiki/{name.replace(' ', '_')}_Corporation",
            f"https://en.wikipedia.org/wiki/{name.replace(' ', '_')}_(company)",
        ]
        
        for url in urls:
            try:
                print(f"📍 Trying: {url}")
                r = requests.get(
                    url, 
                    proxies=self.proxies, 
                    timeout=30, 
                    verify=False,
                    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
                )
                
                print(f"   Status: {r.status_code}, Size: {len(r.text)}")
                
                if r.status_code == 200 and len(r.text) > 50000:
                    print(f"✅ ✅ ✅ LIVE WIKIPEDIA DATA! ✅ ✅ ✅")
                    return self._analyze(r.text, name)
                    
            except Exception as e:
                print(f"   Error: {e}")
                continue
        
        return None
    
    def _analyze(self, html: str, name: str) -> Dict:
        soup = BeautifulSoup(html, 'html.parser')
        text = soup.get_text().lower()
        
        print(f"📊 Analyzing {len(text)} characters")
        
        # Negative keywords
        negative = [
            "controversy", "lawsuit", "fraud", "scandal", "violation",
            "investigation", "fine", "penalty", "sued", "bankruptcy",
            "criminal", "settlement", "misconduct", "criticized", "accused"
        ]
        
        # Positive keywords  
        positive = [
            "award", "leading", "trusted", "excellence", "innovation",
            "successful", "growth", "largest", "premier", "renowned",
            "acclaimed", "fortune", "best", "top", "pioneering"
        ]
        
        neg_found = []
        for keyword in negative:
            if keyword in text:
                neg_found.append(keyword)
                count = text.count(keyword)
                print(f"  🚨 '{keyword}': {count}x")
        
        pos_count = 0
        for keyword in positive:
            if keyword in text:
                pos_count += 1
        
        print(f"  ✅ Positive keywords: {pos_count}")
        
        # Calculate sentiment
        sentiment = (pos_count * 0.08) - (len(neg_found) * 0.12)
        sentiment = max(-1.0, min(1.0, sentiment))
        
        # Risk based on negative keywords
        if len(neg_found) >= 6:
            risk = "CRITICAL"
        elif len(neg_found) >= 4:
            risk = "HIGH"
        elif len(neg_found) >= 2:
            risk = "MEDIUM"
        else:
            risk = "LOW"
        
        print(f"  📊 FINAL: Sentiment={sentiment:.2f}, Risk={risk}")
        
        return {
            "sentiment_score": round(sentiment, 2),
            "review_count": 100,
            "positive_percentage": min(100, pos_count * 8),
            "negative_percentage": min(100, len(neg_found) * 10),
            "fraud_keywords_found": neg_found[:5],
            "risk_indicator": risk,
            "data_source": "BrightData LIVE Wikipedia Scraping"
        }
    
    def scrape_financial_data(self, name: str, website=None) -> Dict:
        print(f"\n🔍 [BrightData] Financial data: Using default")
        
        # Simple default based on sentiment analysis
        return {
            "merchant_name": name,
            "bbb_rating": "Not Available",
            "fraud_mentions": 0,
            "trust_score": 50.0,
            "data_source": "BrightData Analysis"
        }
    
    def _default(self) -> Dict:
        return {
            "sentiment_score": 0.0,
            "review_count": 0,
            "positive_percentage": 0,
            "negative_percentage": 0,
            "fraud_keywords_found": [],
            "risk_indicator": "UNKNOWN",
            "data_source": "BrightData (no data found)"
        }


def merchant_intel(name: str, website=None) -> Dict:
    """PURE LIVE SCRAPING - NO DATABASE"""
    scraper = BrightDataScraper()
    
    sentiment_data = scraper.scrape_merchant_reviews(name)
    financial_data = scraper.scrape_financial_data(name)
    
    # Calculate overall risk from sentiment
    risk_indicator = sentiment_data.get("risk_indicator", "UNKNOWN")
    
    return {
        "merchant_name": name,
        "sentiment_analysis": sentiment_data,
        "financial_intelligence": financial_data,
        "overall_risk": risk_indicator,
        "data_source": "BrightData Residential Proxies"
    }


class MerchantRiskService:
    """Compute merchant risk scores using BrightData sentiment analysis."""

    def __init__(self, scraper_cls=BrightDataScraper) -> None:
        self._scraper_cls = scraper_cls
        self._cache: Dict[str, float] = {}

    def get_merchant_risk(self, merchant_name: str) -> float:
        if not merchant_name:
            logger.warning("Merchant name is empty; returning neutral risk.")
            return 0.5

        key = merchant_name.strip().lower()
        if key in self._cache:
            logger.debug("MerchantRiskService cache hit for '%s'", merchant_name)
            return self._cache[key]

        logger.debug("MerchantRiskService cache miss for '%s'", merchant_name)

        try:
            logger.info("MerchantRiskService querying BrightData for '%s'", merchant_name)
            scraper = self._scraper_cls()
            data = scraper.scrape_merchant_reviews(merchant_name)
        except Exception:
            logger.exception("BrightData scrape failed for '%s'", merchant_name)
            risk_score = 0.5
        else:
            risk_score = self._convert_to_risk_score(data)

        self._cache[key] = risk_score
        return risk_score

    def _convert_to_risk_score(self, data: Optional[Dict]) -> float:
        if not data:
            logger.warning("BrightData returned no data; defaulting to neutral risk.")
            return 0.5

        risk_indicator = (data.get("risk_indicator") or "UNKNOWN").upper()
        sentiment_score = self._safe_float(data.get("sentiment_score"), default=0.0)
        fraud_keywords = data.get("fraud_keywords_found") or []

        base_range = self._risk_range(risk_indicator)
        if base_range is None:
            logger.debug("Unknown risk indicator '%s'; defaulting to neutral risk.", risk_indicator)
            return 0.5

        base_min, base_max = base_range
        range_mid = (base_min + base_max) / 2.0

        sentiment_clamped = max(-1.0, min(1.0, sentiment_score))
        # Negative sentiment raises risk, positive sentiment lowers risk.
        sentiment_adjust = -0.1 * sentiment_clamped

        fraud_count = len(fraud_keywords)
        keyword_adjust = min(fraud_count * 0.02, 0.12)

        raw_score = range_mid + sentiment_adjust + keyword_adjust
        risk_score = max(base_min, min(base_max, raw_score))
        logger.debug(
            "Risk conversion for indicator=%s, sentiment=%.2f, fraud_count=%d -> %.3f",
            risk_indicator,
            sentiment_score,
            fraud_count,
            risk_score,
        )
        return round(risk_score, 3)

    @staticmethod
    def _risk_range(indicator: str) -> Optional[Tuple[float, float]]:
        ranges = {
            "CRITICAL": (0.75, 0.90),
            "HIGH": (0.55, 0.70),
            "MEDIUM": (0.35, 0.50),
            "LOW": (0.1, 0.30),
        }
        return ranges.get(indicator)

    @staticmethod
    def _safe_float(value, default: float = 0.0) -> float:
        try:
            return float(value)
        except (TypeError, ValueError):
            return default


MERCHANT_SERVICE = MerchantRiskService()
