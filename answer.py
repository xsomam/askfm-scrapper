import datetime
from locators import *


class SinglePost:
    def __init__(self, question):

        #ca³e pojedyncze zapytanie w HTML
        self.post = question

    def __repr__(self):
        return f'<{self.likes} | {self.date} | {self.answer} | {self.question}>'

    @property
    def question(self) -> str:
        locator = PostLocator.question
        question = self.post.select_one(locator)
        string = question.string

        return string

    @property
    def date(self):
        locator = PostLocator.date
        time = self.post.select_one(locator)
        get_attrs = time.attrs['datetime'].split('T')
        time_and_date = datetime.datetime.strptime(get_attrs[0]+' ' + get_attrs[1], '%Y-%m-%d %H:%M:%S')

        return str(time_and_date)

    @property
    def link(self) -> str:
        locator = PostLocator.link
        link = self.post.select_one(locator)
        link_attrs = link.attrs['href']

        return 'https://ask.fm' + link_attrs


    @property
    def answer(self):
        locator = PostLocator.answer
        answer = self.post.select_one(locator)
        if answer:
            extract = [q for q in answer][:-1]
            return str(extract[0])
        else:
            return None

    @property
    def likes(self) -> int:
        locator = PostLocator.likes
        likes = self.post.select_one(locator)
        integer = int(likes.string)

        return integer

    @property
    def image(self):
        locator = PostLocator.img
        image = self.post.select_one(locator)
        if image:
            self.image_link = image.attrs['src']
            self.image_extension = self.image_link.split('.')[-1]
            return True
        else:
            return None

    @property
    def asker(self):
        locator = PostLocator.asker_url
        locate_url = self.post.select_one(locator)

        if locate_url:
            locate_url_attrs = locate_url.attrs['href']
            return 'https://ask.fm' + locate_url_attrs
        else:
            return 'Anonymous'
