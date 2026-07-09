#!/usr/bin/env python3
"""Regenerate QA screenshots for North Barbershop landing page."""
import os
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
URL = "http://localhost:8004"
QA = ROOT / "qa"


def main():
    if not QA.exists():
        QA.mkdir(parents=True)

    with sync_playwright() as p:
        browser = p.chromium.launch()

        # Desktop services section
        page = browser.new_page(viewport={"width": 1440, "height": 900})
        page.goto(URL, wait_until="networkidle")
        page.wait_for_timeout(1500)
        page.evaluate("window.scrollTo(0, 9300)")
        page.wait_for_timeout(1200)
        page.screenshot(path=str(QA / "qa-desktop-services.png"))
        page.close()

        # Mobile services section
        page = browser.new_page(viewport={"width": 390, "height": 844})
        page.goto(URL, wait_until="networkidle")
        page.wait_for_timeout(1500)
        page.evaluate("window.scrollTo(0, 8200)")
        page.wait_for_timeout(1200)
        page.screenshot(path=str(QA / "qa-mobile-services.png"))
        page.close()

        # Desktop modal
        page = browser.new_page(viewport={"width": 1440, "height": 900})
        page.goto(URL, wait_until="networkidle")
        page.wait_for_timeout(1000)
        page.click("text=Programează-te >> visible=true")
        page.wait_for_timeout(600)
        page.screenshot(path=str(QA / "qa-modal-desktop.png"))
        page.close()

        browser.close()
    print("QA screenshots regenerated:")
    for f in sorted(QA.glob("qa-*-services.png")) + [QA / "qa-modal-desktop.png"]:
        print(" -", f.name)


if __name__ == "__main__":
    main()
