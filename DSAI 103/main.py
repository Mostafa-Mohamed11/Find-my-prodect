from data_collection import search_products
from data_processing import clean_data
from graph_analysis import build_graph, draw_graph , calculat_centrality , remove_isolated_nodes
import pandas as pd
from heatmap_analysis import kde_heatmap
from model_3d import plot_3d
searched_item = input("Enter the product you want to search: ")
data = search_products(searched_item)
cleaned = clean_data(data)



for item in cleaned:
    print("Title:", item["title"])
    print("Price:", item["price"])
    print("Source:", item["source"])
    print("Link:", item["link"])
    print("-" * 50)

df = pd.DataFrame(cleaned)
df.to_csv("products.csv", index=False)

print(df)




##################################################


from data_collection import scrape_product_details

all_details = []

for item in cleaned[:3]:  
    print("Scraping:", item["link"])
    
    details = scrape_product_details(item["link"])
    
    all_details.append({
    "original_title": item["title"],
    "link": item["link"],
    "Recommended_items": details
})
for detail in all_details:
    print("*" *50,"\n","Product name:", detail["original_title"],"\n","Link:","\n",detail["link"] ,"\n","*"*50)
    print("Recommended items:")
    for d in detail["Recommended_items"]:
        print("-", d)
    print("-" * 50)

############################################

print("Total recommendations:", len(all_details[0]["Recommended_items"]))

rows = []

for detail in all_details:
    for rec in detail["Recommended_items"]:
        rows.append({
            "product_name": detail["original_title"],
            "product_link": detail["link"],
            "recommended_product": rec
        })

import pandas as pd

df_final = pd.DataFrame(rows)
df_final.to_csv("final_products.csv", index=False)

print(df_final)


#####################################################

while True:
    try:
        threshold = int(input("Enter price threshold >=200 :"))

        if threshold >= 200:
            break
        else:
            print("number shoud be >=200 :")

    except:
        print(" please enter a valid number :")
G=build_graph(cleaned, threshold)

G = remove_isolated_nodes(G)

centrality= calculat_centrality(G)
for node, value in centrality.items():
    print(node,"=>", value)
draw_graph(G)

##################################
kde_heatmap(cleaned)
#####################################
plot_3d(cleaned)