def clean_data(data):
    new_data = []

    for item in data:
        price = item['price']

        if price is not None:
            price = price.replace('$', '').replace(',', '')

            
            if "/" in price:
                price = price.split("/")[0]

            try:
                price = float(price)
            except:
                price = 0.0
        else:
            price = 0.0

        item['price'] = price
        new_data.append(item)

    return new_data