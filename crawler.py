# --- Rwanda Web Crawler ---
# Starts at a website, follows the links it finds, and collects every
# ".rw" website it discovers. Reports each page's response time, and
# looks up where each .rw site's server is hosted (its region).

import requests                      # fetches web pages and talks to the location api
from bs4 import BeautifulSoup        # reads html and lets us pull out the links
from urllib.parse import urlparse    # breaks a url apart so we can grab just the domain

# ask the user which website to start from
start_url = input("Enter a website to start crawling from (e.g. https://igihe.com): ")

# --- our three lists (the heart of how a crawler works) ---
to_visit = [start_url]   # pages we still need to visit
visited = set()          # pages we've already done (a set, so we never repeat one)
rw_sites = set()         # the .rw sites we find (a set, so no duplicates)

max_pages = 30           # safety limit so it doesn't run forever

while to_visit and len(visited) < max_pages:
    current = to_visit.pop(0)

    if current in visited:
        continue

    try:
        response = requests.get(current, timeout=5)
    except:
        continue

    visited.add(current)

    # how long the server took to respond, in seconds
    response_time = response.elapsed.total_seconds()
    print("Visited:", current, "-", response_time, "seconds")

    soup = BeautifulSoup(response.text, "html.parser")
    for link in soup.find_all("a"):
        href = link.get("href")
        if not href or not href.startswith("http"):
            continue

        domain = urlparse(href).netloc

        # skip junk domains with brackets or weird characters
        if not all(c.isalnum() or c in ".-" for c in domain):
            continue

        if domain.endswith(".rw"):
            rw_sites.add(domain)

        if href not in visited:
            to_visit.append(href)

# --- crawling finished ---
print("\n=== FINISHED CRAWLING ===")
print("Visited", len(visited), "pages")
print("Found", len(rw_sites), "unique .rw sites")

# save the list of sites to a file
with open("rw_sites.txt", "w") as f:
    for site in sorted(rw_sites):
        f.write(site + "\n")
print("Site list saved to rw_sites.txt")

# --- look up where each .rw site's server is hosted (its region) ---
# we ask a free service (ip-api.com) for each domain's location
print("\n=== SERVER LOCATIONS ===")
for site in sorted(rw_sites):
    try:
        # ask ip-api.com where this domain's server is
        info = requests.get("http://ip-api.com/json/" + site, timeout=5).json()

        # the service replies "success" if it found the location
        if info["status"] == "success":
            country = info["country"]     # e.g. "Rwanda" or "United States"
            city = info["city"]           # e.g. "Kigali"
            host = info["isp"]            # the hosting company
            print(site, "->", city + ",", country, "(" + host + ")")
        else:
            print(site, "-> location not found")
    except:
        print(site, "-> lookup failed")
