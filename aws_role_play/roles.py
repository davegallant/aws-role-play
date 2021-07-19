def get_list_of_roles(config):
    roles = []
    for section in config.sections():
        for (key, value) in config.items(section):
            if key == "role_arn":
                roles.append((value, f"{' '.join(section.split(' ')[1:])}"))

    return roles
