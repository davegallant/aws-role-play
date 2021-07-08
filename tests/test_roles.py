import configparser
import pytest

from aws_role_play.roles import get_list_of_roles


@pytest.fixture
def role_admin():
    return "arn:aws:iam::555555555555:role/admin"


@pytest.fixture
def role_readonly():
    return "arn:aws:iam::555555555555:role/read-only"


@pytest.fixture
def aws_config(role_admin, role_readonly):
    config = configparser.ConfigParser()
    config.add_section("profile admin")
    config["profile admin"]["role_arn"] = role_admin
    config.add_section("profile readonly")
    config["profile readonly"]["role_arn"] = role_readonly
    config.add_section("user")
    config["user"]["aws_account_id"] = "555555555555"
    return config


def test_get_list_of_roles(
    aws_config,
):

    roles = get_list_of_roles(aws_config)

    assert roles == [
        ("arn:aws:iam::555555555555:role/admin", "admin"),
        ("arn:aws:iam::555555555555:role/read-only", "readonly"),
    ]
