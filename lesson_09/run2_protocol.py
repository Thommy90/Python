from datetime import datetime, timedelta
from dataclasses import dataclass
from typing import Protocol

class SocialChannelProvider(Protocol):
    def post_message(self, message: str) -> None:
        ...

class YouTubeProvider:
    def post_message(self, message: str) -> None:
        print(f"Posting to YouTube: {message}")


class FacebookProvider:
    def post_message(self, message: str) -> None:
        print(f"Posting to Facebook: {message}")


class TwitterProvider:
    def post_message(self, message: str) -> None:
        print(f"Posting to Twitter: {message}")


@dataclass
class SocialChannel:
    provider: SocialChannelProvider
    followers: int = 1

    def post_message(self, message: str) -> None:
        self.provider.post_message(message)


@dataclass
class Post:
    message: str
    timestamp: datetime

def process_schedule(posts: list[Post], channels: list[SocialChannel]) -> None:
    sorted_posts = sorted(posts, key=lambda post: post.timestamp)
    current_time = datetime.now()
    for post in sorted_posts:
        if post.timestamp <= current_time:
            for channel in channels:
                channel.post_message(post.message)


if __name__ == "__main__":

    youtube_channel = SocialChannel(YouTubeProvider())
    facebook_channel = SocialChannel(FacebookProvider())
    twitter_channel = SocialChannel(TwitterProvider())

    posts = [
        Post(message="first message, datetime.now()", timestamp=datetime.now()),
        Post(message="second message, timestamp=datetime.now() + timedelta(days=1)", timestamp=datetime.now() + timedelta(days=1)),
        Post(message="third message, timestamp=datetime.now() - timedelta(days=1)", timestamp=datetime.now() - timedelta(days=1)),
        Post(message="fourth message, timestamp=datetime.now()", timestamp=datetime.now()),
    ]

    channels = [youtube_channel, facebook_channel, twitter_channel]
    process_schedule(posts, channels)
