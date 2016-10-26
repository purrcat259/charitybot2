import pytest
from charitybot2.reporter.purrbot_config import purrbot_config
from charitybot2.reporter.twitch import InvalidTwitchAccountException, TwitchAccount
from charitybot2.reporter.twitch_config import TwitchConfig


class TestTwitchAccount:
    def test_invalid_twitch_account_throws_exception(self):
        with pytest.raises(InvalidTwitchAccountException):
            invalid_config = TwitchConfig(account_name='ifdjgiojdfiojdoijfg', client_id='fidjgojfdg', client_secret='boo')
            TwitchAccount(twitch_config=invalid_config)

    def test_twitch_account_exists(self):
        purrbot = TwitchAccount(twitch_config=purrbot_config)
        purrbot.validate_twitch_account()