# aws-role-play

## Motivation

Storing unencrypted credentials in `~/.aws/credentials` can be risky, but is often the simplest way to setup access to AWS. If the computer is compromised, a bad actor could gain access to the AWS account. If a user is required to assume a role that requires MFA, the security risk is reduced.

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
[foo]
region = ca-central-1

[profile foo-admin]
duration_seconds = 3600
mfa_serial = arn:aws:iam::555555555555:mfa/myuser
role_arn = arn:aws:iam::555555555555:role/admin
source_profile = foo

[profile foo-readonly]
duration_seconds = 28800
mfa_serial = arn:aws:iam::555555555555:mfa/myuser
role_arn = arn:aws:iam::555555555555:role/read-only
source_profile = foo
```

Having a `mfa_serial` is optional, but it's good practice that a policy requires one.

## Usage

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

### Exporting Credentials

To export the temporary credentials to the current shell:

```sh
eval $(aws-role-play assume --profile foo-admin --export)
```

### Writing Credentials

> Note: Temporary credentials will overwrite any existing credentials in the profile provided

Based on the above configuration, to assume the admin role and update your credentials:

```sh
aws-role-play assume --profile foo-admin --write
```

After assuming a role, check your identity by:

### Checking Identity

```sh
aws sts get-caller-identity --profile foo-admin
```

## Additional Resources

- [aws-vault](https://github.com/99designs/aws-vault) provides a secure way to store and access credentials.

- [leapp](https://github.com/Noovolari/leapp) also provides a secure way to store and access cloud credentials (with a GUI).

- [aws-extend-switch-roles](https://github.com/tilfinltd/aws-extend-switch-roles) is a set of browser extensions for switching roles based on aws config.
