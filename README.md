# Rwanda Web Crawler

A Python web crawler that discovers `.rw` websites by following links across the web, then reports each site's server location and page response time.

## What it does

Starting from a seed URL, the crawler:

1. Downloads the page and records its response time
2. Extracts every link on the page
3. Pulls the domain out of each link and keeps the ones ending in `.rw`
4. Follows the links it finds to discover more pages
5. Looks up the server location (country, city, hosting provider) for each `.rw` site found

Results are saved to `rw_sites.txt`.

## The assignment, and what is actually possible

The task asked for four things: the number of viewers of a site, their region, the time they spend viewing, and all `.rw` websites on the internet. Three of these cannot be obtained by crawling:

- **Number of viewers**, **viewer region**, and **time spent viewing** are private analytics. Only the site owner can see them, through tools like Google Analytics or server logs. They are not part of the public page, so no crawler can read them from the outside. Third-party services such as SimilarWeb publish *estimates*, but those are estimates, not actual figures.

What the crawler does instead, using only publicly available information:

- **Server region** (not visitor region): looks up where each site's server is hosted, via IP geolocation
- **Response time** (not time spent viewing): measures how fast each page responds

## Built with

- **Python**
- **requests** | fetches web pages and calls the geolocation service
- **BeautifulSoup** (bs4) | reads the HTML and extracts links
- **urllib.parse (urlparse)** | extracts the domain from each URL
- **ip-api.com** | free service that maps a domain's IP to a server location

## Setup

```bash
pip install requests beautifulsoup4
```

## Usage

```bash
python crawler.py
```

Enter a starting URL when prompted (for example `https://www.gov.rw`). The crawler prints each page it visits with its response time, saves the discovered `.rw` sites to `rw_sites.txt`, then prints the server location for each one.

## How it avoids problems

- A page limit (`max_pages = 30`) stops it from crawling indefinitely
- A `visited` set ensures no page is crawled twice, preventing infinite loops
- Each request is wrapped in `try/except`, so a site that is down or blocks the crawler is skipped rather than crashing the run
