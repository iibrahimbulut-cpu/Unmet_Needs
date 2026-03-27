Unmet Needs Finder: AI-Driven Market Insight Tool
Unmet Needs Finder is a strategic intelligence tool that bridges the gap between raw social media chatter and actionable business strategy. It scrapes real-time consumer complaints from Twitter (X) and uses Google Gemini AI to synthesize them into a professional market gap report.

Key Features
Integrated Scraper & Analyst: Combines Selenium-based data collection with LLM-based strategic reasoning in a single workflow.
Stealth Scraping: Connects to an authenticated Chrome session (Port 9222) to gather authentic user tweets without triggering bot defenses.
AI Strategic Reporting: Once data is collected, the script feeds the top 100 unique tweets into Gemini Flash to generate:
The top 3 recurring industry complaints.
Two specific "Unmet Needs" (product/service ideas customers are wishing for).
A concise "Market Gap" summary for entrepreneurs and product managers.
Dual Output: Saves the raw data to Excel (.xlsx) and the AI-generated strategy report to a Text (.txt) file.
Language Focused: Specifically tuned to analyze Turkish consumer sentiment and market dynamics.

Setup & Requirements
Browser Preparation: Launch Chrome in remote debugging mode:
Bash
chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\selenum\ChromeProfile"
API Configuration: Add your Gemini API Key to the GEMINI_API_KEY variable in the script.

Dependencies:
Bash
pip install google-generativeai selenium webdriver-manager pandas openpyxl

How to Use
Set Keywords: Update the keywords list with your industry terms (e.g., "teslimat sorunu").
Run: Execute python "Unmet Needs.py".
Review: * Watch the live terminal for the "GEMINI STRATEGIC ANALYSIS" output.
Check pazar_analiz_raporu.txt for the final professional report.
Open hazir_yemek_sikayet_analizi.xlsx for the supporting raw data.

The "Unmet Needs" Logic
The script follows a 3-step intelligence cycle:
Listen: Scrape raw, unfiltered human emotions and complaints from social media.
Filter: Clean the data and remove duplicates to find unique voices.
Synthesize: Use AI to answer the question: "Based on these frustrations, what is the market failing to provide?"

Technologies
Google Gemini (Flash): For lightning-fast text synthesis and market analysis.
Selenium: For navigating complex web structures.
Pandas: For data structuring and Excel exportation.
