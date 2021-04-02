import time
import requests
from bs4 import BeautifulSoup as BfSoup
from Emailer import Email

div_class = 'condd'
anchor_class = 'cona'

show_names = []
links = []
shows_and_links = {}


class Anime:
    def __init__(self):
        while True:
            try:
                search_name = self.anime_request()
                search_result = requests.get(f'https://animeheaven.ru/search?q={search_name}', timeout=3)
                self.result = search_result.text
            except:
                print('Request Timeout. Try Again.')
            else:
                break

        self.soup = BfSoup(self.result, 'lxml')
        self.available_anime(div_class, anchor_class, self.soup)

        # USER INPUT FOR SHOW CHOICE
        num_range = len(show_names)
        in_range = False
        while not in_range:
            user_choice = int(input('Enter the number of the show you want to get notified about: '))
            if 1 <= user_choice <= num_range:
                print('Searching...')
                in_range = True
            else:
                print('Please enter one of the given numbers.')

        user_link = self.user_show_link(user_choice)  # link to provide to user
        self.anime_name = show_names[user_choice - 1]

        # EPISODE INFORMATION
        self.result2 = requests.get(user_link)
        self.epi_soup = BfSoup(self.result2.text, 'lxml')

    def get_latest_epi_link(self):
        epi_link = self.epi_soup.select('.infovanr')
        for w in epi_link:
            self.latest_episode_link = w['href']

        return self.latest_episode_link

    def get_anime_name(self):
        return self.anime_name

    def get_latest_epi(self):
        for x in self.epi_soup.select('.infoept2r .centerv'):
            Anime.latest_episode = x.text
        return self.latest_episode

    # Returns formatted anime name provided by user
    def anime_request(self):
        anime_name = input('Enter Anime Name: ')
        split_name = anime_name.split()
        formatted_name = ''

        for i in range(len(split_name)):
            if len(split_name) > 1:
                formatted_name += split_name[i] + "+"
            else:
                formatted_name += split_name[i]

        if '+' in formatted_name:
            formatted_name = formatted_name[:-1]

        return formatted_name

    # Returns dictionary of available anime
    def available_anime(self, class1, class2, soup):
        counter = 1

        # Look for all links with specific anchor class
        for div in soup.find_all("div", {"class": class1}):
            for link in div.select("a." + class2):
                links.append(link['href'])

        # Look for all text with specific div class
        for item in soup.select('.' + class1 + ' .' + class2):
            print(str(counter) + ': ' + item.text)
            show_names.append(item.text)
            shows_and_links.update({counter: {item.text: links[counter - 1]}})
            counter += 1

        return shows_and_links

    # Return the link of the show the user is looking for
    def user_show_link(self, user_choice):
        link = shows_and_links.get(user_choice, {}).get(show_names[user_choice - 1])
        return link


user_anime = Anime()
anime_name = user_anime.get_anime_name()
anime_link = user_anime.get_latest_epi_link()
episode_number = user_anime.get_latest_epi()

print(anime_name)
print('Latest EP: ' + episode_number)
print('Link: ' + anime_link)

new_email = Email()

is_new_episode = False
current_episode = user_anime.get_latest_epi()

while not is_new_episode:
    new_episode = user_anime.get_latest_epi()
    msg = new_email.format_mail(user_anime.get_anime_name(), user_anime.get_latest_epi_link())
    if current_episode == new_episode:
        pass
    else:
        new_email.send_mail(msg)
        print("Message Sent!")
        is_new_episode = True
    time.sleep(3)
