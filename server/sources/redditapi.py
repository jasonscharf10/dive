from aiohttp import ClientSession
from sources.base import DataSource
import settings
import praw
import datetime


class RedditAPI(DataSource):
    def __init__(self):
        self.client_id = settings.REDDIT_CLIENT_ID
        self.client_secret = settings.REDDIT_CLIENT_SECRET
        self.password = settings.REDDIT_PASSWORD
        self.user_agent = settings.REDDIT_USER_AGENT
        self.username = settings.REDDIT_USERNAME

    async def request_data(self):
        # session = ClientSession(trust_env=True)
        reddit = praw.Reddit(
            client_id=self.client_id,
            client_secret=self.client_secret,
            password=self.password,
            # requestor_kwargs={"session": session},  # pass the custom Session instance
            user_agent=self.user_agent,
            username=self.username,
        )
        search_params = []
        titles = []
        urls = []
        publishedAts = []
        sources = []
        for submission in reddit.subreddit("all").search(self._search_param):
            search_params.append(self._search_param)
            titles.append(submission.title)
            urls.append(submission.permalink)
            publishedAts.append(
                datetime.datetime.fromtimestamp(submission.created_utc).date()
            )
            sources.append("RedditAPI")

        self._data = [
            {
                "search_param": search_param,
                "title": title,
                "url": f"https://reddit.com{url}",
                "publishedAt": publishedAt,
                "source": source,
            }
            for search_param, title, url, publishedAt, source in zip(
                search_params, titles, urls, publishedAts, sources
            )
        ]
