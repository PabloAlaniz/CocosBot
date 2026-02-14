"""
Endpoint Discovery Script for CocosBot.

Logs into Cocos Capital, crawls all pages via BFS, and captures
every API call the frontend makes. Outputs a JSON report with
discovered pages and API endpoints.

Usage:
    python scripts/discover_endpoints.py
"""

import json
import logging
import os
import sys
import time
from datetime import datetime
from urllib.parse import urlparse

# Add project root to path so we can import CocosBot
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from CocosBot.core.cocos_capital import CocosCapital
from CocosBot.config.urls import WEB_APP_URLS

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

BASE_DOMAIN = "app.cocos.capital"
API_DOMAIN = "api.cocos.capital"
WAIT_PER_PAGE = 3  # seconds to wait on each page for API calls to fire

# URLs to skip (would log us out or are not useful to crawl)
SKIP_PATTERNS = ["/login", "/logout", "/register", "/forgot-password"]

OUTPUT_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "discovered_endpoints.json")


def get_credentials():
    """Load credentials from environment variables."""
    required = ["COCOS_USERNAME", "COCOS_PASSWORD", "GMAIL_USER", "GMAIL_APP_PASS"]
    creds = {key: os.environ.get(key) for key in required}
    missing = [k for k, v in creds.items() if not v]
    if missing:
        logger.error("Missing environment variables: %s", ", ".join(missing))
        logger.info("Set them before running: export COCOS_USERNAME=... etc.")
        sys.exit(1)
    return creds


def should_skip(url: str) -> bool:
    """Check if a URL should be skipped."""
    parsed = urlparse(url)
    return any(pattern in parsed.path for pattern in SKIP_PATTERNS)


def normalize_url(url: str) -> str:
    """Strip query params and fragments for dedup purposes."""
    parsed = urlparse(url)
    return f"{parsed.scheme}://{parsed.netloc}{parsed.path}".rstrip("/")


def discover_endpoints():
    creds = get_credentials()

    cocos = CocosCapital(
        username=creds["COCOS_USERNAME"],
        password=creds["COCOS_PASSWORD"],
        gmail_user=creds["GMAIL_USER"],
        gmail_app_pass=creds["GMAIL_APP_PASS"],
        headless=False,
    )

    try:
        # --- Login ---
        logger.info("Logging in...")
        cocos.login()
        logger.info("Login successful.")
        time.sleep(2)  # let dashboard load

        # --- Setup ---
        visited = set()
        # Seed with all known WEB_APP_URLS (except login)
        to_visit = set()
        for name, url in WEB_APP_URLS.items():
            if not should_skip(url):
                to_visit.add(normalize_url(url))

        results = {
            "timestamp": datetime.now().isoformat(),
            "discovered_pages": [],
            "pages": {},
            "all_api_endpoints": [],
        }

        current_page_calls = []

        def capture_api_call(response):
            if API_DOMAIN in response.url:
                current_page_calls.append({
                    "url": response.url,
                    "method": response.request.method,
                    "status": response.status,
                    "content_type": response.headers.get("content-type", ""),
                })

        cocos.page.on("response", capture_api_call)

        # --- BFS Crawl ---
        all_api_endpoints = set()

        while to_visit:
            url = to_visit.pop()
            normalized = normalize_url(url)

            if normalized in visited:
                continue
            visited.add(normalized)

            logger.info("--- Visiting: %s ---", normalized)
            current_page_calls.clear()

            try:
                cocos.page.goto(normalized, wait_until="domcontentloaded", timeout=15000)
            except Exception as e:
                logger.warning("Failed to navigate to %s: %s", normalized, e)
                results["pages"][normalized] = {"error": str(e), "api_calls": [], "links_found": []}
                continue

            # Wait for API calls to fire
            time.sleep(WAIT_PER_PAGE)

            # Extract links from the same domain
            try:
                links = cocos.page.eval_on_selector_all(
                    "a[href]",
                    "els => els.map(e => e.href).filter(h => h.includes('app.cocos.capital'))"
                )
            except Exception:
                links = []

            new_links = set()
            for link in links:
                parsed = urlparse(link)
                if parsed.netloc == BASE_DOMAIN and not should_skip(link):
                    new_links.add(normalize_url(link))

            to_visit.update(new_links - visited)

            # Record results for this page
            page_calls = list(current_page_calls)
            results["pages"][normalized] = {
                "api_calls": page_calls,
                "links_found": sorted(new_links),
            }

            # Collect unique API endpoints
            for call in page_calls:
                endpoint_key = f"{call['method']} {call['url'].split('?')[0]}"
                all_api_endpoints.add(endpoint_key)

            logger.info(
                "  Found %d API calls, %d links on this page",
                len(page_calls),
                len(new_links),
            )

        # --- Build final output ---
        results["discovered_pages"] = sorted(visited)
        results["all_api_endpoints"] = sorted(all_api_endpoints)

        # --- Print summary ---
        print("\n" + "=" * 70)
        print("ENDPOINT DISCOVERY REPORT")
        print("=" * 70)

        print(f"\nPages visited: {len(visited)}")
        print(f"Unique API endpoints: {len(all_api_endpoints)}")

        print("\n--- Discovered Pages ---")
        for page in sorted(visited):
            print(f"  {page}")

        print("\n--- API Endpoints by Page ---")
        for page_url, page_data in sorted(results["pages"].items()):
            if page_data.get("api_calls"):
                print(f"\n  {page_url}")
                for call in page_data["api_calls"]:
                    status_marker = "OK" if call["status"] == 200 else f"ERR:{call['status']}"
                    print(f"    [{status_marker}] {call['method']} {call['url']}")

        print("\n--- All Unique API Endpoints ---")
        for ep in sorted(all_api_endpoints):
            print(f"  {ep}")

        # --- Save JSON ---
        with open(OUTPUT_FILE, "w") as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        logger.info("Results saved to %s", OUTPUT_FILE)

        print(f"\nFull report saved to: {OUTPUT_FILE}")
        print("=" * 70)

    finally:
        cocos.close_browser()


if __name__ == "__main__":
    discover_endpoints()
