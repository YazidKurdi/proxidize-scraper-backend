
# Proxidize Scraper Backend


The API exposes four endpoints:
* Login
* Register
* Keyword Scrape
* List Scraped from DB

Last two endpoints expects the user to be authenticated via Token Authentication.
Scraping using static libraries that fetch the initial HTML is not suitable as the website uses VueJS to mount components after page is loaded. Headless chrome driver was used.

Running @ [Backend](https://proxidize-scraper-backend-production.up.railway.app/)