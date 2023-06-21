import re
from datetime import datetime
from dataclasses import dataclass, asdict, field

from tweepy.models import User

SPAM_WORD_LIST: list = [
    "bit.ly",
    "tinyurl.com",
    "tiny.cc",
    "ux.nu",
    "cutt.ly",
    "はこっち→",
    "はこっち",
    "は下",
    "は下→",
    "連絡は👉",
    "セーフ",
    "カップ",
    "ホテ",
    "DMする",
    "メッセージする",
    "エロ",
    "0cm",
    "1cm",
    "2cm",
    "3cm",
    "4cm",
    "5cm",
    "6cm",
    "7cm",
    "8cm",
    "9cm",
    "裏垢",
    "裏あか",
    "裏アカ",
    "パコ",
    "家出",
    "パイ",
    "リフレ",
    "見せ合い",
    "見せあい",
]


@dataclass
class TwitterUser:
    twitter_id: int = field(init=False)
    screen_name: str = field(init=False)
    name: str = field(init=False)
    description: str = field(init=False)
    location: str = field(init=False)
    url: str = field(init=False)
    created_at: datetime = field(init=False)
    profile_img_url: str = field(init=False)
    is_spam_account: bool = field(init=False, default=False)

    def __init__(self, user: User):
        self.twitter_id = user.id
        self.screen_name = user.screen_name
        self.name = user.name or ""
        self.description = user.description or ""
        self.location = user.location or ""
        self.url = user.url or ""
        self.created_at = user.created_at
        self.profile_img_url = user.profile_image_url
        self.spam_check()

    def _check_for_spam_words(self, text: str):
        for spam_word in SPAM_WORD_LIST:
            if spam_word in text:
                self.is_spam_account = True
                break

    def _description_check(self):
        ptn = r"(\d{2})/♀/(\w+)([🌀-🗿😀-🙏]*)"
        if re.search(ptn, self.description):
            self.is_spam_account = True
        self._check_for_spam_words(self.description)

    def _url_check(self):
        self._check_for_spam_words(self.url)

    def _location_check(self):
        self._check_for_spam_words(self.location)

    def _profile_img_check(self):
        default_profiles = ["default_profile", "default_profile_images"]
        if any(dp in self.profile_img_url for dp in default_profiles):
            self.is_spam_account = True

    def _check_for_spam_screen_name(self):
        ptn = r"\w+\d{8,}"
        if re.match(ptn, self.screen_name):
            self.is_spam_account = True

    def spam_check(self):
        for check_method in [
            self._description_check,
            self._url_check,
            self._location_check,
            self._profile_img_check,
            self._check_for_spam_screen_name
        ]:
            check_method()
            if self.is_spam_account:
                break

    def check_if_spam(self) -> bool:
        return self.is_spam_account

    def to_dict(self) -> dict:
        return asdict(self)
