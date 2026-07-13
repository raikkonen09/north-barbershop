#!/usr/bin/env python3
"""Regenerate QA screenshots for North Barbershop landing page."""
import os
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
URL = "http://localhost:8004"
QA = ROOT / "qa"


def scroll_to(page, ratio):
    """Scroll to a ratio of the scroll-world track height."""
    y = page.evaluate("""(ratio) => {
      const track = document.querySelector('.sw-track');
      return track ? Math.round(track.offsetHeight * ratio) : 0;
    }""", ratio)
    page.evaluate(f"window.scrollTo(0, {y})")
    return y


def main():
    if not QA.exists():
        QA.mkdir(parents=True)

    with sync_playwright() as p:
        browser = p.chromium.launch()

        # Desktop services section
        page = browser.new_page(viewport={"width": 1440, "height": 900})
        page.goto(URL, wait_until="networkidle")
        page.wait_for_timeout(1500)
        scroll_to(page, 1.12)
        page.wait_for_timeout(1200)
        page.screenshot(path=str(QA / "qa-desktop-services.png"))
        page.close()

        # Mobile hero
        page = browser.new_page(viewport={"width": 390, "height": 844})
        page.goto(URL, wait_until="networkidle")
        page.wait_for_timeout(1500)
        page.evaluate("window.scrollTo(0, 0)")
        page.wait_for_timeout(1000)
        page.screenshot(path=str(QA / "qa-mobile-hero.png"))
        page.close()

        # Mobile mid-scroll (around scene 3)
        page = browser.new_page(viewport={"width": 390, "height": 844})
        page.goto(URL, wait_until="networkidle")
        page.wait_for_timeout(1500)
        scroll_to(page, 0.45)
        page.wait_for_timeout(1000)
        page.screenshot(path=str(QA / "qa-mobile-mid.png"))
        page.close()

        # Mobile services section
        page = browser.new_page(viewport={"width": 390, "height": 844})
        page.goto(URL, wait_until="networkidle")
        page.wait_for_timeout(1500)
        scroll_to(page, 1.12)
        page.wait_for_timeout(1200)
        page.screenshot(path=str(QA / "qa-mobile-services.png"))
        page.close()

        # Mobile modal
        page = browser.new_page(viewport={"width": 390, "height": 844})
        page.goto(URL, wait_until="networkidle")
        page.wait_for_timeout(1000)
        page.click("text=Programează-te >> visible=true")
        page.wait_for_timeout(600)
        page.screenshot(path=str(QA / "qa-modal-mobile.png"))
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
    for f in sorted(QA.glob("qa-*.png")):
        print(" -", f.name)


if __name__ == "__main__":
    main()
