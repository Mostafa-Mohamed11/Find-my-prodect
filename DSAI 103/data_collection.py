from serpapi.google_search import GoogleSearch

def search_products(query):
    params = {
        "engine": "google_shopping",
        "q": query,
        "api_key": "b04898ef7fc37e7ba8ecde25cef286b824445d054af19d7f78d9da9a5028b76b"
    }

    search = GoogleSearch(params)
    results = search.get_dict()

    products_list = []

    categories = results.get("categorized_shopping_results")

    if categories:
        for category in categories:
            products = category.get("shopping_results", [])

            for product in products:
                title = product.get("title")
                link = product.get("product_link")

                if title and link:
                    image = product.get("serpapi_thumbnail") or product.get("thumbnail") or ""

                    products_list.append({
                        "title": title,
                        "price": product.get("price"),
                        "link": link,
                        "image": image,   
                        "source": product.get("source")
                    })

    else:
        products = results.get("shopping_results", [])

        for product in products:
            title = product.get("title")
            link = product.get("product_link") or product.get("link")

            if title and link:
                image = product.get("serpapi_thumbnail") or product.get("thumbnail") or ""

                products_list.append({
                    "title": title,
                    "price": product.get("price"),
                    "link": link,
                    "image": image,   # 👈 ده الحل
                    "source": product.get("source")
                })

    return products_list

#selenium + Bueatiful soup




def scrape_product_details(url):
    from selenium import webdriver
    from bs4 import BeautifulSoup
    import time

    driver = webdriver.Chrome()
    driver.get(url)

    time.sleep(5)

    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")

    products = []

    try:
        items = soup.find_all("div", attrs={"role": "heading"})

        for item in items:
            title = item.text.strip()

            if title and len(title) > 10 and "Color" not in title:
                products.append(title)

    except:
        print("Error")

    driver.quit()

    return products
#######################################################################################

# def scrape_product_details(url):
#     from selenium import webdriver
#     from selenium.webdriver.common.by import By
#     import time

#     driver = webdriver.Chrome()
#     driver.get(url)

#     time.sleep(5)

#     products = []

#     try:
#         items = driver.find_elements(By.XPATH, "//div[@role='heading']")

#         for item in items:
#             title = item.text.strip()

#             if title and len(title) > 10 and "Color" not in title:
#                 products.append(title)

#     except:
#         print("Error")

#     driver.quit()

#     return products