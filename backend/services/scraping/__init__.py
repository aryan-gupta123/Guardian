"""
Web scraping services for financial scam detection.
"""
from .brightdata_scraper import BrightDataScraper
from .scam_detector import FinancialScamDetector

__all__ = ['BrightDataScraper', 'FinancialScamDetector']
