import configparser
from collections import namedtuple

import pytest

from aws_role_play.sts import update_session_credentials

Credentials = namedtuple("Credentials", ["access_key", "secret_key", "token"])


def credentials_config_empty():
    return configparser.ConfigParser()


def credentials_config_populated():
    config = configparser.ConfigParser()
    config.add_section("test-profile")
    config["test-profile"]["aws_access_key_id"] = "OLD_ACCESS_KEY"
    config["test-profile"]["aws_secret_access_key"] = "OLD_SECRET"
    config["test-profile"]["aws_session_token"] = "OLD_TOKEN"
    return config


@pytest.fixture
def session_token():
    return Credentials("ACCESS_KEY", "SECRET", "TOKEN")


@pytest.mark.parametrize(
    "credentials_config", [credentials_config_empty(), credentials_config_populated()]
)
def test_update_session_credentials(credentials_config, session_token):

    config = update_session_credentials(
        credentials_config, session_token, "test-profile"
    )

    assert config["test-profile"]["aws_access_key_id"] == session_token.access_key
    assert config["test-profile"]["aws_secret_access_key"] == session_token.secret_key
    assert config["test-profile"]["aws_session_token"] == session_token.token
