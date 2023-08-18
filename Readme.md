
# Proxidize Scraper Backend


The API exposes four endpoints:
* Login
* Register
* Keyword Scrape
* List Scraped from DB

Last two endpoints expects the user to be authenticated via Token Authentication.
Scraping using static libraries that fetch the initial HTML is not suitable as the website uses VueJS to mount components after page is loaded. Headless chrome driver was used.

Dockerfile is used to utilize the selenium standalone image

# Limitations
Current scraping implementation takes at least (2 * Number of rows specified)
A maximum of 30 rows can be scraped at a time as the server's RAM is limited

Running @ [Backend](https://proxidize-scraper-backend-production.up.railway.app/)