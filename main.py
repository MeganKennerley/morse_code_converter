import requests
from bs4 import BeautifulSoup
import pandas as pd


def create_csv():
    url = "https://en.wikipedia.org/wiki/Morse_code"
    page = requests.get(url)

    soup = BeautifulSoup(page.content, "html.parser")

    table_rows = soup.find_all("tr", valign="top")
    data_string = []
    data_code = []

    for row in table_rows:
        title = row.find("td")
        letter = row.find("a")
        code_div = row.select("td:nth-child(3) > div > div > div > div > div.listen-file-header > a > span > span")

        if title is None:
            continue

        for element in code_div:
            code = element.get_text()

        if title.get_text() == "Letters":
            letters = letter.get_text().split()
            value = letters[0].replace(",", "")
        elif title.get_text() == "Numbers":
            value = letter.get_text()

        data_string.append(value)
        data_code.append(code)

        if value == "9":
            break

    morse_dict = {"string": data_string, "code": data_code}
    df = pd.DataFrame(morse_dict)

    return df


def convert_string():
    df = create_csv()
    string = input("Enter a string to convert into Morse Code: ").upper()
    for letter in string:
        code_value = df.loc[df["string"] == letter, "code"].values
        remove_list = str(code_value).replace("['", "").replace("']", "")
        code = remove_list.replace("\\xa0", " ")
        print(code)


def main():
    convert_string()


if __name__ == '__main__':
    main()