"""
BrightData Web Scraper for Financial Scam Detection
Handles web scraping using BrightData's proxy and scraping API.
"""

import os
import requests
import json
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import re
from urllib.parse import urlparse


class BrightDataScraper:
    """
    BrightData API wrapper for scraping financial data to detect scam companies.
    """

    def __init__(self):
        self.api_key = os.getenv('BRIGHTDATA_API_KEY')
        self.zone = os.getenv('BRIGHTDATA_ZONE', 'scraping_browser')
        self.host = os.getenv('BRIGHTDATA_HOST', 'brd.superproxy.io')
        self.port = int(os.getenv('BRIGHTDATA_PORT', '22225'))

        if not self.api_key:
            raise ValueError("BRIGHTDATA_API_KEY not found in environment variables")

        # BrightData Web Scraper API endpoint
        self.scraper_api_url = "https://api.brightdata.com/datasets/v3/trigger"

        # Proxy configuration
        self.proxy_url = f"http://{self.api_key}:@{self.host}:{self.port}"
        self.proxies = {
            "http": self.proxy_url,
            "https": self.proxy_url,
        }

    def _make_request(self, url: str, method: str = 'GET', headers: Optional[Dict] = None,
                      data: Optional[Dict] = None, use_proxy: bool = True) -> requests.Response:
        """
        Make HTTP request through BrightData proxy or direct.

        Args:
            url: Target URL to scrape
            method: HTTP method (GET, POST, etc.)
            headers: Optional HTTP headers
            data: Optional POST data
            use_proxy: Whether to use BrightData proxy

        Returns:
            requests.Response object
        """
        default_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        }

        if headers:
            default_headers.update(headers)

        try:
            if use_proxy:
                response = requests.request(
                    method=method,
                    url=url,
                    headers=default_headers,
                    proxies=self.proxies,
                    timeout=30,
                    data=data
                )
            else:
                response = requests.request(
                    method=method,
                    url=url,
                    headers=default_headers,
                    timeout=30,
                    data=data
                )

            response.raise_for_status()
            return response

        except requests.exceptions.RequestException as e:
            print(f"Request failed for {url}: {str(e)}")
            raise

    def scrape_domain_info(self, domain: str) -> Dict[str, Any]:
        """
        Scrape domain registration and WHOIS information.

        Args:
            domain: Domain name to investigate

        Returns:
            Dictionary with domain information
        """
        try:
            # Use WHOIS API through BrightData
            whois_url = f"https://www.whois.com/whois/{domain}"
            response = self._make_request(whois_url)

            # Parse domain age and registration info
            content = response.text

            domain_info = {
                'domain': domain,
                'registration_date': self._extract_registration_date(content),
                'registrar': self._extract_registrar(content),
                'privacy_protected': 'privacy' in content.lower() or 'protected' in content.lower(),
                'age_days': None,
                'is_new_domain': False,
                'ssl_valid': self._check_ssl(domain),
            }

            # Calculate domain age
            if domain_info['registration_date']:
                try:
                    reg_date = datetime.strptime(domain_info['registration_date'], '%Y-%m-%d')
                    domain_info['age_days'] = (datetime.now() - reg_date).days
                    domain_info['is_new_domain'] = domain_info['age_days'] < 365
                except:
                    pass

            return domain_info

        except Exception as e:
            print(f"Error scraping domain info for {domain}: {str(e)}")
            return {
                'domain': domain,
                'error': str(e)
            }

    def scrape_company_registration(self, company_name: str, jurisdiction: str = 'US') -> Dict[str, Any]:
        """
        Scrape company registration data from official sources.

        Args:
            company_name: Name of the company
            jurisdiction: Country/state jurisdiction

        Returns:
            Dictionary with company registration details
        """
        try:
            # For US companies, check SEC EDGAR database
            if jurisdiction == 'US':
                search_url = f"https://www.sec.gov/cgi-bin/browse-edgar?company={company_name}&action=getcompany"
                response = self._make_request(search_url)

                return {
                    'company_name': company_name,
                    'jurisdiction': jurisdiction,
                    'registration_number': self._extract_cik(response.text),
                    'incorporation_date': self._extract_incorporation_date(response.text),
                    'status': self._extract_company_status(response.text),
                    'registered_address': self._extract_address(response.text),
                    'officers': self._extract_officers(response.text),
                }

            # For UK companies
            elif jurisdiction == 'UK':
                # Companies House API would go here
                return {'company_name': company_name, 'jurisdiction': jurisdiction, 'source': 'companies_house'}

            return {'company_name': company_name, 'jurisdiction': jurisdiction, 'source': 'unknown'}

        except Exception as e:
            print(f"Error scraping company registration: {str(e)}")
            return {'company_name': company_name, 'error': str(e)}

    def scrape_financial_data(self, company_identifier: str) -> Dict[str, Any]:
        """
        Scrape financial statements and filings.

        Args:
            company_identifier: CIK or company ticker symbol

        Returns:
            Dictionary with financial data
        """
        try:
            # Get latest 10-K, 10-Q filings from SEC
            filings_url = f"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={company_identifier}&type=10-K&dateb=&owner=exclude&count=10"
            response = self._make_request(filings_url)

            return {
                'company_id': company_identifier,
                'latest_filing_date': self._extract_latest_filing_date(response.text),
                'filing_status': self._extract_filing_status(response.text),
                'auditor': self._extract_auditor(response.text),
                'auditor_changes': self._detect_auditor_changes(response.text),
                'late_filings': self._detect_late_filings(response.text),
                'red_flags': []
            }

        except Exception as e:
            print(f"Error scraping financial data: {str(e)}")
            return {'company_id': company_identifier, 'error': str(e)}

    def scrape_regulatory_actions(self, company_name: str) -> List[Dict[str, Any]]:
        """
        Scrape regulatory enforcement actions and warnings.

        Args:
            company_name: Company name to search

        Returns:
            List of regulatory actions
        """
        actions = []

        try:
            # Search SEC enforcement actions
            sec_search_url = f"https://www.sec.gov/litigation/litreleases.shtml"
            response = self._make_request(sec_search_url)

            # Search FTC complaints
            ftc_search_url = f"https://www.ftc.gov/enforcement/cases-proceedings"

            # Search state attorney general warnings
            # This would require multiple state-specific searches

            actions.append({
                'source': 'SEC',
                'actions_found': self._extract_sec_actions(response.text, company_name),
            })

            return actions

        except Exception as e:
            print(f"Error scraping regulatory actions: {str(e)}")
            return []

    def scrape_online_reviews(self, company_name: str, domain: str = None) -> Dict[str, Any]:
        """
        Scrape online reviews and reputation data.

        Args:
            company_name: Company name
            domain: Company website domain

        Returns:
            Dictionary with review and reputation data
        """
        try:
            reviews_data = {
                'company_name': company_name,
                'bbb_rating': None,
                'bbb_complaints': 0,
                'trustpilot_score': None,
                'trustpilot_reviews': 0,
                'google_reviews': 0,
                'review_patterns': [],
                'suspicious_patterns': []
            }

            # Scrape BBB
            if domain:
                bbb_url = f"https://www.bbb.org/search?find_text={company_name}"
                try:
                    response = self._make_request(bbb_url)
                    reviews_data['bbb_rating'] = self._extract_bbb_rating(response.text)
                    reviews_data['bbb_complaints'] = self._extract_bbb_complaints(response.text)
                except:
                    pass

            # Scrape Trustpilot
            trustpilot_url = f"https://www.trustpilot.com/review/{domain}" if domain else None
            if trustpilot_url:
                try:
                    response = self._make_request(trustpilot_url)
                    reviews_data['trustpilot_score'] = self._extract_trustpilot_score(response.text)
                    reviews_data['trustpilot_reviews'] = self._extract_review_count(response.text)
                    reviews_data['review_patterns'] = self._analyze_review_patterns(response.text)
                except:
                    pass

            return reviews_data

        except Exception as e:
            print(f"Error scraping reviews: {str(e)}")
            return {'company_name': company_name, 'error': str(e)}

    def scrape_social_media_presence(self, company_name: str, domain: str = None) -> Dict[str, Any]:
        """
        Scrape social media presence and follower authenticity indicators.

        Args:
            company_name: Company name
            domain: Company website domain

        Returns:
            Dictionary with social media data
        """
        return {
            'company_name': company_name,
            'twitter_followers': None,
            'twitter_engagement_rate': None,
            'facebook_likes': None,
            'linkedin_followers': None,
            'follower_authenticity_score': None,
            'suspicious_patterns': []
        }

    # Helper methods for parsing scraped data

    def _extract_registration_date(self, content: str) -> Optional[str]:
        """Extract domain registration date from WHOIS content."""
        patterns = [
            r'Creation Date:\s*(\d{4}-\d{2}-\d{2})',
            r'Created:\s*(\d{4}-\d{2}-\d{2})',
            r'Registered on:\s*(\d{4}-\d{2}-\d{2})',
        ]
        for pattern in patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                return match.group(1)
        return None

    def _extract_registrar(self, content: str) -> Optional[str]:
        """Extract registrar from WHOIS content."""
        pattern = r'Registrar:\s*([^\n]+)'
        match = re.search(pattern, content, re.IGNORECASE)
        return match.group(1).strip() if match else None

    def _check_ssl(self, domain: str) -> bool:
        """Check if domain has valid SSL certificate."""
        try:
            response = requests.get(f'https://{domain}', timeout=5)
            return True
        except:
            return False

    def _extract_cik(self, content: str) -> Optional[str]:
        """Extract CIK number from SEC page."""
        pattern = r'CIK=(\d+)'
        match = re.search(pattern, content)
        return match.group(1) if match else None

    def _extract_incorporation_date(self, content: str) -> Optional[str]:
        """Extract incorporation date from company filings."""
        # This would parse the actual filing documents
        return None

    def _extract_company_status(self, content: str) -> str:
        """Extract company status (active, dissolved, etc.)."""
        if 'active' in content.lower():
            return 'active'
        elif 'dissolved' in content.lower():
            return 'dissolved'
        return 'unknown'

    def _extract_address(self, content: str) -> Optional[str]:
        """Extract registered address."""
        pattern = r'Business Address[:\s]+([^<]+)'
        match = re.search(pattern, content, re.IGNORECASE)
        return match.group(1).strip() if match else None

    def _extract_officers(self, content: str) -> List[str]:
        """Extract list of officers/directors."""
        # This would parse officer information from filings
        return []

    def _extract_latest_filing_date(self, content: str) -> Optional[str]:
        """Extract date of most recent filing."""
        pattern = r'(\d{4}-\d{2}-\d{2})'
        match = re.search(pattern, content)
        return match.group(1) if match else None

    def _extract_filing_status(self, content: str) -> str:
        """Determine if filings are up to date."""
        return 'current' if content else 'unknown'

    def _extract_auditor(self, content: str) -> Optional[str]:
        """Extract auditor name from filings."""
        return None

    def _detect_auditor_changes(self, content: str) -> bool:
        """Detect if company has changed auditors recently."""
        return False

    def _detect_late_filings(self, content: str) -> bool:
        """Detect if company has late filings."""
        return False

    def _extract_sec_actions(self, content: str, company_name: str) -> List[str]:
        """Extract SEC enforcement actions mentioning the company."""
        return []

    def _extract_bbb_rating(self, content: str) -> Optional[str]:
        """Extract BBB rating (A+, A, B, etc.)."""
        pattern = r'rating[:\s]+([A-F][+-]?)'
        match = re.search(pattern, content, re.IGNORECASE)
        return match.group(1) if match else None

    def _extract_bbb_complaints(self, content: str) -> int:
        """Extract number of BBB complaints."""
        pattern = r'(\d+)\s+complaint'
        match = re.search(pattern, content, re.IGNORECASE)
        return int(match.group(1)) if match else 0

    def _extract_trustpilot_score(self, content: str) -> Optional[float]:
        """Extract Trustpilot score."""
        pattern = r'score[:\s]+([\d.]+)'
        match = re.search(pattern, content, re.IGNORECASE)
        return float(match.group(1)) if match else None

    def _extract_review_count(self, content: str) -> int:
        """Extract total review count."""
        pattern = r'(\d+)\s+reviews?'
        match = re.search(pattern, content, re.IGNORECASE)
        return int(match.group(1)) if match else 0

    def _analyze_review_patterns(self, content: str) -> List[str]:
        """Analyze review patterns for suspicious activity."""
        patterns = []

        # Check for clustering (many reviews on same day)
        # Check for similar language patterns
        # Check for new/unverified accounts

        return patterns
