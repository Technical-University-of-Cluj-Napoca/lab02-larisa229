import sys
from bs4 import BeautifulSoup
import requests

def get_definition(word, lang="en"):
    headers = {"User-Agent": "Mozilla/5.0"}

    if lang == "en":
        url = f"https://www.oxfordlearnersdictionaries.com/definition/english/{word}"
    elif lang == "ro":
        url = f"https://dexonline.ro/definitie/{word}"
    else:
        raise ValueError("Language not supported")

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    if lang == "en":
        definition = soup.find("span", class_='def')
        if definition:
            return definition.text.strip()
        else:
            return "Definition not found"
    else:
        definition = soup.find("span", class_="def") or soup.find("p", class_="def")
        if not definition:
            definition = soup.find("div", class_="defWrapper")
        if definition:
            return definition.get_text(strip=True)
        else:
            return "Definiție negăsită"

def main():
    if len(sys.argv) < 2:
        print("Usage: python define.py <word> [lang]")
        sys.exit(1)

    word = sys.argv[1]
    lang = sys.argv[2].lower() if len(sys.argv) == 3 else "en"

    definition = get_definition(word, lang)
    print(definition)

if __name__ == "__main__":
    main()
