"""
Financial Scam Detector
Analyzes multiple data sources to detect potential scam companies.
"""

from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import re
from .brightdata_scraper import BrightDataScraper


class FinancialScamDetector:
    """
    Comprehensive financial scam detection system.
    Analyzes company data from multiple sources and calculates risk scores.
    """

    # Risk score weights for different categories
    WEIGHTS = {
        'company_registration': 0.15,
        'financial_data': 0.25,
        'domain_info': 0.15,
        'regulatory_actions': 0.20,
        'online_reputation': 0.15,
        'business_model': 0.10,
    }

    # Risk thresholds
    RISK_LEVELS = {
        'low': (0, 0.3),
        'medium': (0.3, 0.6),
        'high': (0.6, 0.8),
        'critical': (0.8, 1.0),
    }

    def __init__(self):
        self.scraper = BrightDataScraper()

    def analyze_company(self, company_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Comprehensive analysis of a company for scam indicators.

        Args:
            company_data: Dictionary containing:
                - company_name: str (required)
                - domain: str (optional)
                - jurisdiction: str (optional, default 'US')
                - company_identifier: str (optional, CIK or ticker)
                - business_description: str (optional)
                - promised_returns: float (optional)
                - payment_methods: List[str] (optional)

        Returns:
            Dictionary with comprehensive analysis results
        """
        company_name = company_data.get('company_name')
        domain = company_data.get('domain')
        jurisdiction = company_data.get('jurisdiction', 'US')
        company_id = company_data.get('company_identifier')

        # Initialize results
        results = {
            'company_name': company_name,
            'analysis_date': datetime.now().isoformat(),
            'overall_risk_score': 0.0,
            'risk_level': 'unknown',
            'red_flags': [],
            'green_flags': [],
            'category_scores': {},
            'detailed_findings': {},
            'recommendations': [],
        }

        # 1. Analyze Company Registration & Legal Data
        registration_score = self._analyze_company_registration(
            company_name, jurisdiction, results
        )
        results['category_scores']['company_registration'] = registration_score

        # 2. Analyze Financial Data
        if company_id:
            financial_score = self._analyze_financial_data(company_id, results)
            results['category_scores']['financial_data'] = financial_score
        else:
            results['category_scores']['financial_data'] = 0.5  # Unknown = moderate risk

        # 3. Analyze Domain & Online Presence
        if domain:
            domain_score = self._analyze_domain(domain, results)
            results['category_scores']['domain_info'] = domain_score
        else:
            results['category_scores']['domain_info'] = 0.7  # No domain = higher risk

        # 4. Check Regulatory Actions
        regulatory_score = self._analyze_regulatory_actions(company_name, results)
        results['category_scores']['regulatory_actions'] = regulatory_score

        # 5. Analyze Online Reputation
        if domain:
            reputation_score = self._analyze_online_reputation(company_name, domain, results)
            results['category_scores']['online_reputation'] = reputation_score
        else:
            results['category_scores']['online_reputation'] = 0.6

        # 6. Analyze Business Model
        business_score = self._analyze_business_model(company_data, results)
        results['category_scores']['business_model'] = business_score

        # Calculate overall risk score
        results['overall_risk_score'] = self._calculate_overall_score(
            results['category_scores']
        )

        # Determine risk level
        results['risk_level'] = self._get_risk_level(results['overall_risk_score'])

        # Generate recommendations
        results['recommendations'] = self._generate_recommendations(results)

        return results

    def _analyze_company_registration(self, company_name: str, jurisdiction: str,
                                       results: Dict) -> float:
        """
        Analyze company registration data for red flags.
        Returns risk score (0-1, higher = more risky).
        """
        risk_score = 0.0
        findings = {}

        try:
            reg_data = self.scraper.scrape_company_registration(company_name, jurisdiction)
            findings['registration_data'] = reg_data

            # Check if company exists
            if reg_data.get('error'):
                risk_score += 0.5
                results['red_flags'].append({
                    'category': 'registration',
                    'severity': 'high',
                    'message': 'Unable to verify company registration',
                })

            # Check company status
            status = reg_data.get('status', '').lower()
            if status in ['dissolved', 'inactive', 'suspended']:
                risk_score += 0.8
                results['red_flags'].append({
                    'category': 'registration',
                    'severity': 'critical',
                    'message': f'Company status: {status}',
                })
            elif status == 'active':
                risk_score += 0.0
                results['green_flags'].append({
                    'category': 'registration',
                    'message': 'Company is actively registered',
                })

            # Check incorporation date
            inc_date = reg_data.get('incorporation_date')
            if inc_date:
                try:
                    inc_datetime = datetime.fromisoformat(inc_date)
                    age_days = (datetime.now() - inc_datetime).days

                    if age_days < 365:
                        risk_score += 0.3
                        results['red_flags'].append({
                            'category': 'registration',
                            'severity': 'medium',
                            'message': f'Company is very new ({age_days} days old)',
                        })
                    elif age_days > 1825:  # 5 years
                        results['green_flags'].append({
                            'category': 'registration',
                            'message': f'Established company ({age_days // 365} years old)',
                        })
                except:
                    pass

            # Check for valid registered address
            address = reg_data.get('registered_address')
            if not address or len(address) < 10:
                risk_score += 0.2
                results['red_flags'].append({
                    'category': 'registration',
                    'severity': 'medium',
                    'message': 'No valid registered address found',
                })

            # Check for officers/directors
            officers = reg_data.get('officers', [])
            if len(officers) == 0:
                risk_score += 0.3
                results['red_flags'].append({
                    'category': 'registration',
                    'severity': 'medium',
                    'message': 'No officers or directors listed',
                })

        except Exception as e:
            risk_score = 0.6  # Unknown = moderate-high risk
            findings['error'] = str(e)

        results['detailed_findings']['company_registration'] = findings
        return min(risk_score, 1.0)

    def _analyze_financial_data(self, company_id: str, results: Dict) -> float:
        """
        Analyze financial statements and filings for red flags.
        Returns risk score (0-1, higher = more risky).
        """
        risk_score = 0.0
        findings = {}

        try:
            financial_data = self.scraper.scrape_financial_data(company_id)
            findings['financial_data'] = financial_data

            # Check for late filings
            if financial_data.get('late_filings'):
                risk_score += 0.4
                results['red_flags'].append({
                    'category': 'financial',
                    'severity': 'high',
                    'message': 'Company has history of late filings',
                })

            # Check for auditor changes
            if financial_data.get('auditor_changes'):
                risk_score += 0.3
                results['red_flags'].append({
                    'category': 'financial',
                    'severity': 'medium',
                    'message': 'Frequent auditor changes detected',
                })

            # Check filing status
            if financial_data.get('filing_status') == 'delinquent':
                risk_score += 0.5
                results['red_flags'].append({
                    'category': 'financial',
                    'severity': 'high',
                    'message': 'Delinquent financial filings',
                })
            elif financial_data.get('filing_status') == 'current':
                results['green_flags'].append({
                    'category': 'financial',
                    'message': 'Financial filings are current',
                })

        except Exception as e:
            risk_score = 0.5
            findings['error'] = str(e)

        results['detailed_findings']['financial_data'] = findings
        return min(risk_score, 1.0)

    def _analyze_domain(self, domain: str, results: Dict) -> float:
        """
        Analyze domain registration and SSL for red flags.
        Returns risk score (0-1, higher = more risky).
        """
        risk_score = 0.0
        findings = {}

        try:
            domain_data = self.scraper.scrape_domain_info(domain)
            findings['domain_data'] = domain_data

            # Check domain age
            if domain_data.get('is_new_domain'):
                risk_score += 0.5
                results['red_flags'].append({
                    'category': 'domain',
                    'severity': 'high',
                    'message': f'Domain is less than 1 year old',
                })
            elif domain_data.get('age_days', 0) > 1825:  # 5 years
                results['green_flags'].append({
                    'category': 'domain',
                    'message': f'Established domain ({domain_data["age_days"] // 365} years old)',
                })

            # Check privacy protection
            if domain_data.get('privacy_protected'):
                risk_score += 0.3
                results['red_flags'].append({
                    'category': 'domain',
                    'severity': 'medium',
                    'message': 'Domain registration uses privacy protection',
                })

            # Check SSL certificate
            if not domain_data.get('ssl_valid'):
                risk_score += 0.4
                results['red_flags'].append({
                    'category': 'domain',
                    'severity': 'high',
                    'message': 'No valid SSL certificate found',
                })
            else:
                results['green_flags'].append({
                    'category': 'domain',
                    'message': 'Valid SSL certificate',
                })

        except Exception as e:
            risk_score = 0.5
            findings['error'] = str(e)

        results['detailed_findings']['domain_info'] = findings
        return min(risk_score, 1.0)

    def _analyze_regulatory_actions(self, company_name: str, results: Dict) -> float:
        """
        Check for regulatory enforcement actions and warnings.
        Returns risk score (0-1, higher = more risky).
        """
        risk_score = 0.0
        findings = {}

        try:
            regulatory_data = self.scraper.scrape_regulatory_actions(company_name)
            findings['regulatory_actions'] = regulatory_data

            # Check for SEC actions
            for action_source in regulatory_data:
                actions = action_source.get('actions_found', [])
                if len(actions) > 0:
                    risk_score += 0.9
                    results['red_flags'].append({
                        'category': 'regulatory',
                        'severity': 'critical',
                        'message': f'{len(actions)} regulatory action(s) found from {action_source["source"]}',
                    })

            # No regulatory actions is a green flag
            if risk_score == 0:
                results['green_flags'].append({
                    'category': 'regulatory',
                    'message': 'No regulatory enforcement actions found',
                })

        except Exception as e:
            risk_score = 0.3  # Unknown = slight risk
            findings['error'] = str(e)

        results['detailed_findings']['regulatory_actions'] = findings
        return min(risk_score, 1.0)

    def _analyze_online_reputation(self, company_name: str, domain: str, results: Dict) -> float:
        """
        Analyze online reviews and reputation.
        Returns risk score (0-1, higher = more risky).
        """
        risk_score = 0.0
        findings = {}

        try:
            review_data = self.scraper.scrape_online_reviews(company_name, domain)
            findings['review_data'] = review_data

            # Check BBB rating
            bbb_rating = review_data.get('bbb_rating')
            if bbb_rating:
                if bbb_rating.startswith('F') or bbb_rating.startswith('D'):
                    risk_score += 0.6
                    results['red_flags'].append({
                        'category': 'reputation',
                        'severity': 'high',
                        'message': f'Poor BBB rating: {bbb_rating}',
                    })
                elif bbb_rating.startswith('A'):
                    results['green_flags'].append({
                        'category': 'reputation',
                        'message': f'Good BBB rating: {bbb_rating}',
                    })

            # Check BBB complaints
            complaints = review_data.get('bbb_complaints', 0)
            if complaints > 50:
                risk_score += 0.4
                results['red_flags'].append({
                    'category': 'reputation',
                    'severity': 'high',
                    'message': f'{complaints} BBB complaints filed',
                })

            # Check Trustpilot score
            trustpilot_score = review_data.get('trustpilot_score')
            if trustpilot_score:
                if trustpilot_score < 2.5:
                    risk_score += 0.5
                    results['red_flags'].append({
                        'category': 'reputation',
                        'severity': 'high',
                        'message': f'Low Trustpilot score: {trustpilot_score}/5',
                    })
                elif trustpilot_score > 4.0:
                    results['green_flags'].append({
                        'category': 'reputation',
                        'message': f'Good Trustpilot score: {trustpilot_score}/5',
                    })

            # Check for suspicious review patterns
            suspicious_patterns = review_data.get('suspicious_patterns', [])
            if len(suspicious_patterns) > 0:
                risk_score += 0.3
                results['red_flags'].append({
                    'category': 'reputation',
                    'severity': 'medium',
                    'message': f'Suspicious review patterns detected: {", ".join(suspicious_patterns)}',
                })

        except Exception as e:
            risk_score = 0.4
            findings['error'] = str(e)

        results['detailed_findings']['online_reputation'] = findings
        return min(risk_score, 1.0)

    def _analyze_business_model(self, company_data: Dict, results: Dict) -> float:
        """
        Analyze business model for common scam indicators.
        Returns risk score (0-1, higher = more risky).
        """
        risk_score = 0.0
        findings = {}

        # Check promised returns
        promised_returns = company_data.get('promised_returns')
        if promised_returns:
            findings['promised_returns'] = promised_returns
            if promised_returns > 20:  # Annual returns over 20%
                risk_score += 0.7
                results['red_flags'].append({
                    'category': 'business_model',
                    'severity': 'critical',
                    'message': f'Unrealistic return promises: {promised_returns}% annually',
                })
            elif promised_returns > 10:
                risk_score += 0.3
                results['red_flags'].append({
                    'category': 'business_model',
                    'severity': 'medium',
                    'message': f'High return promises: {promised_returns}% annually',
                })

        # Check payment methods
        payment_methods = company_data.get('payment_methods', [])
        findings['payment_methods'] = payment_methods

        risky_payment_methods = ['cryptocurrency', 'wire_transfer', 'gift_cards', 'cash']
        detected_risky = [pm for pm in payment_methods if pm.lower() in risky_payment_methods]

        if len(detected_risky) > 0:
            risk_score += 0.4 * len(detected_risky)
            results['red_flags'].append({
                'category': 'business_model',
                'severity': 'high',
                'message': f'Risky payment methods: {", ".join(detected_risky)}',
            })

        # Check business description for MLM/pyramid keywords
        business_desc = company_data.get('business_description', '').lower()
        if business_desc:
            findings['business_description'] = business_desc

            mlm_keywords = ['recruit', 'downline', 'upline', 'multi-level', 'network marketing',
                           'unlimited income', 'passive income', 'financial freedom']
            detected_keywords = [kw for kw in mlm_keywords if kw in business_desc]

            if len(detected_keywords) > 2:
                risk_score += 0.6
                results['red_flags'].append({
                    'category': 'business_model',
                    'severity': 'high',
                    'message': f'MLM/pyramid scheme indicators detected',
                })

        results['detailed_findings']['business_model'] = findings
        return min(risk_score, 1.0)

    def _calculate_overall_score(self, category_scores: Dict[str, float]) -> float:
        """
        Calculate weighted overall risk score from category scores.
        """
        overall = 0.0

        for category, score in category_scores.items():
            weight = self.WEIGHTS.get(category, 0.0)
            overall += score * weight

        return round(overall, 3)

    def _get_risk_level(self, risk_score: float) -> str:
        """
        Determine risk level based on overall score.
        """
        for level, (min_score, max_score) in self.RISK_LEVELS.items():
            if min_score <= risk_score < max_score:
                return level
        return 'critical'

    def _generate_recommendations(self, results: Dict) -> List[str]:
        """
        Generate actionable recommendations based on analysis.
        """
        recommendations = []
        risk_level = results['risk_level']
        red_flags = results['red_flags']

        if risk_level == 'critical':
            recommendations.append('AVOID: This company shows critical scam indicators')
            recommendations.append('DO NOT invest or provide personal/financial information')
            recommendations.append('Report to appropriate regulatory authorities (SEC, FTC, etc.)')

        elif risk_level == 'high':
            recommendations.append('HIGH RISK: Exercise extreme caution')
            recommendations.append('Conduct thorough due diligence before any engagement')
            recommendations.append('Consult with a financial advisor or attorney')

        elif risk_level == 'medium':
            recommendations.append('MODERATE RISK: Proceed with caution')
            recommendations.append('Verify company credentials independently')
            recommendations.append('Research thoroughly before making decisions')

        else:  # low risk
            recommendations.append('LOW RISK: Standard due diligence recommended')
            recommendations.append('Still verify key claims independently')

        # Specific recommendations based on red flags
        for flag in red_flags:
            if flag['category'] == 'regulatory' and flag['severity'] == 'critical':
                recommendations.append('Review regulatory enforcement actions in detail')

            if flag['category'] == 'business_model':
                if 'unrealistic return' in flag['message'].lower():
                    recommendations.append('Unrealistic returns are a major red flag - extremely high risk')

            if flag['category'] == 'domain' and 'ssl' in flag['message'].lower():
                recommendations.append('Never enter sensitive information on sites without valid SSL')

        return recommendations
