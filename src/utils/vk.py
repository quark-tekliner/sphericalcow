import re
import requests
from bs4 import BeautifulSoup


class VkApiException(Exception):
    pass


class Vk(object):
    API_URL = "https://api.vk.com/method/%s?access_token=%s"

    @classmethod
    def call(cls, method, token, **kwargs):
        url = cls.API_URL % (method, token, )
        for key, value in kwargs.iteritems():
            url += "&%s=%s" % (key, value, )
        response = requests.get(url)
        parsed_response = response.json()
        error = parsed_response.get('error')
        if error is not None:
            raise VkApiException(error.get('error_msg'))
        return parsed_response.get('response')

    @classmethod
    def get_polls_from_wall(cls, token, owner_id):
        response = cls.call('wall.get', token, owner_id=owner_id)
        if len(response) < 1:
            raise StopIteration()
        for post in response[1:]:
            poll = cls._parse_one_poll(post, owner_id)
            if poll is not None:
                yield poll

    @classmethod
    def _parse_one_poll(cls, post, owner_id):
        poll = filter(lambda attachment: attachment.get('type') == 'poll', post.get('attachments', []))
        if len(poll) == 0:
            return
        post_id = post.get('id')
        date = post.get('date')
        poll_content = poll[0].get('poll')
        id = poll_content.get('poll_id')
        text = poll_content.get('question')
        answers = cls.get_poll_answers(owner_id, post_id)
        return {'id': id, 'text': text, 'date': date, 'answers': answers, 'post_id': post_id}

    @classmethod
    def get_poll_answers(cls, owner_id, post_id):
        """
        Ugly polls.getById replacement, because the method has strange permissions issue.
        """
        #@todo: try catch
        parsed_page = BeautifulSoup(requests.get("https://vk.com/wall%s_%s" % (owner_id, post_id, )).text)
        poll = parsed_page.find('div', {'id': "post_poll%s_%s" % (owner_id, post_id, )})
        options = poll.find_all('tr')
        options_with_count = options[1::2]
        for i, option in enumerate(options[::2]):
            id = re.search(ur'\s(\d+)\)$', option.get('onmouseover')).group(1)
            text = option.find('td', {'class': 'page_poll_text'}).get_text()
            votes_count = options_with_count[i].find('div', {'class': 'page_poll_row_count'}).get_text()
            #remove space between digits
            votes_count = ''.join(re.split(ur'\s', votes_count))
            yield {'id': id, 'text': text, 'votes_count': int(votes_count)}
