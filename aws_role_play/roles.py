def get_list_of_roles(config):
    roles = []
    for section in config.sections():
        for (k, v) in config.items(section):
            if k == "role_arn":
                roles.append((v, f"{' '.join(section.split(' ')[1:])}"))

    return roles
