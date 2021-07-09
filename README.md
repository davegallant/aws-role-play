# aws-role-play

## Motivation

AWS CLI supports role assumption by [caching temporary credentials](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-role.html), but unfortunately does not export the temporary credentials to locations where other external applications are expecting them.

`aws-role-play` makes it easier to write and export these temporary credentials. Assuming roles eliminates the need to store and transmit privileged long-term access keys. This tool re-uses the same credentials cache as AWS CLI, and then either exports the credentials to the current shell, or puts the credentials in `~/.aws/credentials` (or `AWS_SHARED_CREDENTIALS_FILE`) so that external applications can read the credentials.

For more information on current issues:

- https://github.com/hashicorp/terraform-provider-aws/issues/10491
- https://github.com/aws/aws-cli/issues/4676

## Installation

```sh
pip install --user git+https://github.com/rewindio/aws-role-play
```

## Configuration

Configuration is read from `~/.aws/config`. Check out the [docs](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html) to learn more about how it's configured.

### Example

```
[personal]
region = ca-central-1

[profile personal-admin]
duration_seconds = 3600
mfa_serial = arn:aws:iam::555555555555:mfa/myuser
role_arn = arn:aws:iam::555555555555:role/admin
source_profile = personal

[profile personal-readonly]
duration_seconds = 28800
mfa_serial = arn:aws:iam::555555555555:mfa/myuser
role_arn = arn:aws:iam::555555555555:role/read-only
source_profile = personal
```

Having a `mfa_serial` is optional, but it's highly recommended that a policy requires one.

## Usage

## Exporting

To export the temporary credentials to the current shell:

```sh
eval $(aws-role-play assume --profile personal-admin --export)
```

## Writing

> Note: Temporary credentials will overwrite any existing credentials in the profile provided

```sh
Usage: aws-role-play [OPTIONS] COMMAND [ARGS]...

  A CLI tool that makes assuming IAM roles easier

Options:
  -v, --version
  --help         Show this message and exit.

Commands:
  assume  Assumes a role and updates session credentials
  list    List all roles defined in the aws config
```

Based on the above configuration, to assume the admin role and update your credentials:

```sh
aws-role-play assume --profile personal-admin --write
```

After assuming a role, check your identity by:

```sh
aws sts get-caller-identity --profile personal-admin
```

## Additional Resources

- If your organization has [SSO](https://aws.amazon.com/single-sign-on/), you should consider [integrating it with awscli](https://docs.aws.amazon.com/singlesignon/latest/userguide/integrating-aws-cli.html) for an easier way to switch between roles and accounts. It doesn't export credentials either, so something like [aws2-wrap](https://github.com/linaro-its/aws2-wrap) helps.

- [aws-vault](https://github.com/99designs/aws-vault) provides a secure way to store and access credentials.

- If you use Azure AD, you might want to consider [aws-azure-login](https://github.com/sportradar/aws-azure-login).

- [aws-extend-switch-roles](https://github.com/tilfinltd/aws-extend-switch-roles) is a set of browser extensions for switching roles based on aws config.
