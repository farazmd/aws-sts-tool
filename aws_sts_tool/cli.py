import boto3
import sys
import os
import argparse
import json
from botocore.exceptions import ClientError, NoCredentialsError
from helpers.datetimeencoder import DateTimeEncoder
from _version import __version__

def getVersion():
    '''Returns version of package'''
    return __version__

def createParser():
    '''
        Parser to parse arguments passed to program.
    '''
    parser = argparse.ArgumentParser(prog='aws_sts_tool',
    description='Program to fetch temporary AWS credentials.',
    usage='aws-sts-tool.py account_id sessionName roleName [duration]')
    parser.add_argument('account_id',help='12 digit AWS account ID.')
    parser.add_argument('sessionName',help='Session name to use.')
    parser.add_argument('roleName',help='Role to assume.')
    parser.add_argument('output',help='Output format.\nMust be one of json, shell or both')
    parser.add_argument('-v','--version',action='version',version='aws_sts_tool: v{}'.format(getVersion()),help='Displays version.')
    parser.add_argument('--duration',
    help='The duration in seconds to assume.\nDefaults to 1 hr or the duration configured on the role.')
    
    return parser

def createSTSClient():
    try:
        return boto3.client('sts')
    except Exception:
        raise ClientError

def createRoleARN(account,roleName):
    if(len(account)!=12):
        raise AttributeError("Account number is not valid")
    return f"arn:aws:iam::{account}:role/{roleName}"

def getPath():
    return os.path.abspath(os.path.curdir)

def writeCredentialsToJson(credentials):
    path = getPath()
    try:
        with open(f"{path}{os.path.sep}credentials.json",'w') as f:
            f.write(json.dumps({
                "AWS_ACCESS_KEY_ID": credentials['AccessKeyId'],
                "AWS_SECRET_ACCESS_KEY": credentials['SecretAccessKey'],
                "AWS_SESSION_TOKEN": credentials['SessionToken']
            },cls=DateTimeEncoder))
            f.close()
        print("Credentials stored in file: credentials.json")
    except Exception as e:
        print(f'Could not write credentials to file: {path}{os.path.sep}credentials.json')
        sys.exit()

def writeCredentialsToShell(credentials):
    path = getPath()
    try:
        with open(f"{path}{os.path.sep}credentials.sh",'w') as f:
            f.write("AWS_ACCESS_KEY_ID={}".format(credentials['AccessKeyId']))
            f.write("AWS_SECRET_ACCESS_KEY={}".format(credentials['SecretAccessKey']))
            f.write("AWS_SESSION_TOKEN={}".format(credentials['SessionToken']))
            f.close()
        print("Credentials stored in file: credentials.sh")
    except Exception as e:
        print(f'Could not write credentials to file: {path}{os.path.sep}credentials.sh')
        sys.exit()

def writeCredentials(credentials,output):
    if output == "both":
        writeCredentialsToJson(credentials)
        writeCredentialsToShell(credentials)
    elif output == "json":
        writeCredentialsToJson(credentials)
    elif output == "shell":
        writeCredentialsToShell(credentials)
    else:
        raise ValueError("Invalid output format. Must be one of json | shell | both.")

def fetchCredentials(roleArn,sessionName,duration,output,sts):
    credentials = None
    if duration == None:
        try:
            credentials = sts.assume_role(
                RoleArn = roleArn,
                RoleSessionName = sessionName
            )
        except NoCredentialsError as e:
            raise Exception(f"{e}: Please make sure you have credentials to use STS")
        except ClientError as e1:
            raise Exception("{}\n\nEither the credentials used do not have permissions".format(e1) +
            "to access the role: {} OR\nthe role: {} does not exist.".format(roleArn,roleArn))
    else:
        try: 
            credentials = sts.assume_role(
                RoleArn = roleArn,
                RoleSessionName = sessionName,
                DurationSeconds = int(duration)
            )
        except NoCredentialsError as e:
            raise Exception(f"{e}: Please make sure you have credentials to use STS")
        except ClientError as e1:
            raise Exception("{}\n\nEither the credentials used do not have permissions".format(e1) +
            "to access the role: {} OR\nthe role: {} does not exist.".format(roleArn,roleArn))
    if credentials != None:
        try:
            writeCredentials(credentials['Credentials'],output)
        except ValueError as e:
            raise Exception(f"{type(e).__name__}: {e}")

def main(args):
    toolParser = createParser()
    arguments = vars(toolParser.parse_args(args))
    try:
        stsClient = createSTSClient()
    except ClientError:
        print('Could not create STS client')
        sys.exit(1)
    try:
        roleArn = createRoleARN(arguments['account_id'],arguments['roleName'])
    except Exception as e:
        print(f"{type(e).__name__}: {e}")
        sys.exit(1)
    try:
        fetchCredentials(roleArn,arguments['sessionName'],arguments['duration'],arguments['output'],stsClient)
        print("Successfully stored credentials for role: {} at {}".format(roleArn,getPath()))
    except Exception as e:
        print(e)
        sys.exit(1)

if __name__ == "__main__":
    main(sys.argv[1:])