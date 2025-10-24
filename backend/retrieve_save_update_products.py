from kroger_api import get_access_token, search_products
from save_products import save_products_to_db
from update_calories import update_product_calories


if __name__ == "__main__":
    token = get_access_token()
    products = search_products("bananas", token)
    save_products_to_db(products)
    update_product_calories()
