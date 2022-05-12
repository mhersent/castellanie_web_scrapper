import requests
from bs4 import BeautifulSoup
import shutil
import os

def get_accounts_url():
    URL = "http://www.castellanie.net/acces.php"
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, "html.parser")

# refactorisation possible ? sauter l'étape de trouver les li dans les ul => récupérer directement tous les li ?
    lists = soup.find_all("ul", class_="", id="")
    urls = []

    for list in lists:

        list_items = list.find_all("li")

        for list_item in list_items:

            a = list_item.find("a")
            urls.append("http://www.castellanie.net/% s" % a.get('href'))

    return urls

def get_account_pictures(account_url):
    page = requests.get(account_url)
    soup = BeautifulSoup(page.content, "html.parser")

    links = soup.find_all("a")
    pictures_url = []
    
    for link in links:
        temp_url = link.get("href")
        # print(type(temp_url))
        if isinstance(temp_url, str) and temp_url.__contains__("/archives"):
            # print(temp_url)
            # on supprime le "./" en début de temp_url
            temp_url = temp_url[2:]
            pictures_url.append("http://www.castellanie.net/%s" % temp_url)

    for picture_url in pictures_url:
        dest_folder = picture_url.split("/")[-2]

        if not os.path.exists(dest_folder):
            os.makedirs(dest_folder)  # create folder if it does not exist

        filename = picture_url.split("/")[-1]
        filepath = os.path.join(dest_folder, filename)

        print(filepath)

        img = requests.get(picture_url, stream = True)

        # Check if the image was retrieved successfully
        if img.status_code == 200:
            # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
            img.raw.decode_content = True

            # Open a local file with wb ( write binary ) permission.
            with open(filepath,'wb') as f:
                shutil.copyfileobj(img.raw, f)
                
            print('Image sucessfully Downloaded: ',filename)
        else:
            print('Image Couldn\'t be retrieved')


def main():
    urls = get_accounts_url()

    # print(urls)
    for url in urls:
        get_account_pictures(url)

if __name__ == "__main__":
    main()
