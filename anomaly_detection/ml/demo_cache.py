"""
Demo cache utilities for pre-loading merchant risk scores.

This module provides functions to pre-populate the MERCHANT_SERVICE cache
with commonly used merchants for smooth demo performance.
"""

import time

from .merchant_service import MERCHANT_SERVICE


def preload_demo_merchants():
    high_risk = [
        "Enron",
        "Theranos",
        "FTX",
        "Lehman Brothers",
        "WorldCom",
        "Tyco",
        "Bernie Madoff",
        "HealthSouth",
        "Adelphia",
        "Wirecard",
    ]
    low_risk = [
        "Apple",
        "Microsoft",
        "Google",
        "Amazon",
        "Walmart",
        "Target",
        "Costco",
        "Best Buy",
        "Home Depot",
        "CVS",
    ]
    neutral = [
        "Bob's Hardware",
        "Local Coffee Shop",
        "Mike's Auto Repair",
        "Downtown Diner",
        "City Pharmacy",
    ]

    print("\n🚀 PRE-LOADING MERCHANT CACHE FOR DEMO...")
    start = time.perf_counter()
    fetch_risk = MERCHANT_SERVICE.get_merchant_risk
    total_merchants = 0

    for group in (high_risk, low_risk, neutral):
        for merchant_name in group:
            print(f"  Caching {merchant_name}...")
            risk_score = fetch_risk(merchant_name)
            print(f"    ✅ Risk: {risk_score:.2f}")
            total_merchants += 1

    elapsed = time.perf_counter() - start
    print(f"\n✅ CACHE LOADED! {total_merchants} merchants in {elapsed:.1f} seconds")
    return None

def clear_cache():
    MERCHANT_SERVICE.cache.clear()
    print("🗑️  Cache cleared! Ready for live scraping demo.")
    return None

def get_cache_stats():
    cache = getattr(MERCHANT_SERVICE, "cache", None)
    if cache is None:
        cache = getattr(MERCHANT_SERVICE, "_cache", {})

    merchants = tuple(cache.keys())
    size = len(merchants)

    if size:
        print(f"📊 Cache size: {size} merchants -> {', '.join(merchants)}")
    else:
        print("📊 Cache empty. Run preload_demo_merchants() to warm it up.")

    return {"size": size, "merchants": merchants}

