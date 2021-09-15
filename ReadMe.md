# AWS STS Tool

[![aws-sts-tool CI](https://github.com/farazmd/aws-sts-tool/actions/workflows/ci.yaml/badge.svg)](https://github.com/farazmd/aws-sts-tool/actions/workflows/ci.yaml)


A CLI tool to help assume AWS role via STS. Useful in automated environments and cross account access requirements for workflows involving AWS.

---

## Prerequisites

- A AWS user/role credentials that would be used as a trust relation with the roles that need to be assumed.
- Python >= 3.7

---

## Installation

Run the following to install the tool using pip.

```shell
pip install aws_sts_tool
```
---

## Usage

- Assuming that you have stored user/role credentials that will be used to assume roles at the locations specified by AWS, you can run the following commands.


### With default duration configured on the role to assume

```shell
aws_sts_tool account_id sessionName roleName output
```

- Where the command line arguments are as follows:
  - `account_id` - the 12 digit AWS account.
  - `sessionName` - a name to identify the session with.
  - `roleName` - the role to be assumed.
  - `output` - the output format of the credentials. Must be one of json, shell or both.

Example: 

```shell
aws_sts_tool 123456789012 test-session test-role json
```

---

### With custom duration

```shell
aws_sts_tool account_id sessionName roleName output --duration duration
```

- Where the command line arguments are as follows:
  - `account_id` - the 12 digit AWS account.
  - `sessionName` - a name to identify the session with.
  - `roleName` - the role to be assumed.
  - `output` - the output format of the credentials. Must be one of json, shell or both.
  - `duration` - the custom duration in seconds to assume the role.

Example: 

```shell
# Will fetch credentials valid for 2 hours
aws_sts_tool 123456789012 test-session test-role json --duration 7200
```

- Once the command executes successfully, it will store the credentials for the role assumed in `credentials.{ json | sh }` at the `location` from where the command is executed.