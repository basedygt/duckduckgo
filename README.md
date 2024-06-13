## DuckDuckGo

```python3
# Import the scraper class
from engines import DuckDuckGoScraper

# Create an instance of the scraper
scraper = DuckDuckGoScraper(browser="Firefox", timeout=10)

# Perform a search
query = "python programming"
pages = 2  # Number of pages to scrape
scraper.perform_search(query, pages)

# Extract links from the search results
links = scraper.extract_links()
print("Extracted Links:")
for link in links:
    print(link)

# Close the scraper
scraper.close()
```
