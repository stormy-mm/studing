from selenium import webdriver

browser = webdriver.Firefox()
browser.get("https://localshot:8000")

assert "Django" in browser.title
