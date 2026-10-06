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

## The assignment, and why parts of it cannot be done by crawling

The task asked for four things: the number of viewers of a website, their region, the time they spend viewing, and all `.rw` websites on the internet.

### Viewer count, viewer region, and time spent viewing | not possible by crawling

These three are private analytics. They exist only in the website owner's own tools, such as Google Analytics, or in the server's logs. They are never part of the public page that a crawler downloads, so no crawler can read them from the outside, no matter how it is built. A crawler only sees what the site sends to the public: the HTML, the links, and the text.

Third-party services such as SimilarWeb publish traffic *estimates*, but those are modelled guesses from their own sample data, not the site's actual figures, and would have to be clearly labelled as estimates.

What the crawler does instead, using only publicly available information:

- **Server region** (not visitor region): looks up where each site's server is hosted, via IP geolocation
- **Response time** (not time spent viewing): measures how fast each page responds

These are the honest, measurable versions of what was asked. Note the distinction: server location is where the site is hosted, which is not the same as where its visitors are; response time is how fast the page replies, which is not the same as how long a visitor stays.

### Finding all `.rw` websites | only partly possible by crawling

Crawling finds `.rw` sites that are *linked* from the pages it visits, so it returns a sample, not the complete set. A domain that nothing links to is never reached by a crawler, so crawling alone can never guarantee *every* `.rw` site.

To enumerate *every* registered `.rw` domain, the correct source is RICTA, the registry that manages the `.rw` country-code domain, queried through its official RDAP/WHOIS service (also done in code). That is the authoritative database of registered `.rw` names. This crawler demonstrates the discovery method; integrating RICTA would give the complete list.

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

- A page limit (`max_pages = 50`) stops it from crawling indefinitely
- A `visited` set ensures no page is crawled twice, preventing infinite loops
- Each request is wrapped in `try/except`, so a site that is down or blocks the crawler is skipped rather than crashing the run

## Author

Elsie Irakoze Karangwa
