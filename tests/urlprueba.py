from bs4 import BeautifulSoup

def extract_product_info(html_file_path: str) -> dict:
    with open(html_file_path, encoding="utf-8") as file:
        soup = BeautifulSoup(file, "html.parser")

    # Título desde <title>
    title = soup.title.string.strip() if soup.title else "Título no encontrado"

    # Buscar span con clase customer-price
    price_span = soup.find("span", class_="customer-price")
    price = price_span.get_text(strip=True) if price_span else "Precio no encontrado"

    return {"title": title, "price": price}


# Ejemplo de uso
if __name__ == "__main__":
    info = extract_product_info("WHILE ON EARTH MOVE TRAINER _ Fittest Freakest - Ropa, accesorios y calzado para Training.html")
    print("Producto:", info["title"])
    print("Precio:", info["price"])
