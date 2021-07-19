def update_session_credentials(config, session_credentials, profile):

    if not config.has_section(profile):
        config.add_section(profile)

    config.set(profile, "aws_access_key_id", session_credentials.access_key)
    config.set(profile, "aws_secret_access_key", session_credentials.secret_key)
    config.set(profile, "aws_session_token", session_credentials.token)

    return config


def write_session_credentials(config, credentials_path):

    with open(credentials_path, "w") as configfile:
        config.write(configfile)


def export_session_credentials(session_credentials, profile):
    print(f"export AWS_ACCESS_KEY_ID={session_credentials.access_key}")
    print(f"export AWS_SECRET_ACCESS_KEY={session_credentials.secret_key}")
    print(f"export AWS_SESSION_TOKEN={session_credentials.token}")
    print(f"export AWS_PROFILE={profile}")
