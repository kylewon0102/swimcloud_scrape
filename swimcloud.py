import requests as req
from bs4 import BeautifulSoup

#class order: swimmer -> url -> html

# ---- class swimmer ----
class swimmer_class:
  def __init__(self, url):
    self.name = ""
    self.url = url_class(url)
    self.hometown = ""
    self.university = ""
    self.sns = ""
    self.events_list = []

  def update_info(self):
    self.name = self.url.html.get_name(self.url.html.soup)
    self.hometown, self.university, self.sns = self.url.html.get_info(self.url.html.soup)
    self.events_list = self.url.html.get_events_list(self.url.html.soup)

  def save_info_as_file(self, filename):
    with open(filename, 'w', encoding='utf-8') as file:
      file.write(self.name + "\n")
      file.write(self.hometown + " ")
      file.write(self.university + " ")
      for sns in self.sns:
        file.write(str(sns) + "\n")
      for event in self.events_list:
        file.write(str(event) + "\n")

  def search_event(self, event_name):
    for event in self.events_list:
      if event_name in event:
        return event
    return "Error: {} not found".format(event_name)

# ---- class url ----
class url_class:
  def __init__(self, url):
    self.url = url
    self.headers = {
      "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
      "Accept-Language": "en-US,en;q=0.9",
      "Referer": "https://swimcloud.com",
    }
    self.html = html_class(self.set_soup())

  def get_url(self):
    return self.url

  def get_http_status(self):
    status = req.get(self.url)
    response = req.get(self.url, headers=self.headers)

    if response.status_code == 200:
        print("connection OK")
    else:
        print(f"Failed to retrieve page. Status code: {response.status_code}")

  def set_soup(self):
    response = req.get(self.url, headers=self.headers)
    if response.status_code == 200:
      return response
    else:
      print(f"Failed to retrieve page. Status code: {response.status_code}")
      return None

  def get_soup(self):
    return self.html.get_soup()

# ---- class html ----
class html_class:
  def __init__(self, html):
    self.unorganized_content = html
    self.soup = self.set_soup()

  """
    Methods - Soup formatting
  """
  def set_soup(self):
    soup = BeautifulSoup(self.unorganized_content.text, "html.parser")
    return soup

  def save_soup_to_file(self, filename):
    with open(filename, 'w', encoding='utf-8') as file:
      file.write(str(self.soup))

  def get_soup(self):
    return self.soup

  def remove_newlines_from_soup(self, soup):
    for element in soup.find_all(text=True):
        cleaned_text = element.strip()
        if cleaned_text:
            cleaned_text = "\n".join(line.strip() for line in cleaned_text.splitlines() if line.strip())
            element.replace_with(cleaned_text)

  """
  Methods - Info gathering
  """
  def get_name(self, soup):
      name = soup.find('title')
      if name is not None:
          title = name.string
          title = title.replace(" | Swimcloud", "").strip()
          return title
      else:
          print("Error: Title tag not found in HTML.")
          return None

  def get_info(self, soup):
    info_meta = soup.find("div", class_="c-toolbar__meta hidden-print")

    hometown, university = None, None
    if info_meta:
      hometown = info_meta.find('li').get_text()
      university = info_meta.find('a').get_text()
      sns = info_meta.find_all('a', class_='btn-icon-plain')

    twitter, instagram = None, None

    for link in sns:
      title = link.get('title')
      if 'Twitter' in title:
        twitter = link['href']
      elif 'Instagram' in title:
        instagram = link['href']

    sns = []
    if twitter:
      sns.append(twitter)
    if instagram:
      sns.append(instagram)

    return hometown, university, sns

  def get_events_list(self, soup):
    rows = soup.select('#js-swimmer-profile-times-container tbody tr')

    results = []
    for row in rows:
        event_name = row.select_one('td:nth-of-type(1)').text.strip()
        time = row.select_one('td:nth-of-type(2) a').text.strip()
        results.append(f'{event_name}: {time}')

    return results
