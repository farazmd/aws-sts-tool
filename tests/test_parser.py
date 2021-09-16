import pytest
import sys
import os
# print(os.path.sep.join(__file__.split(os.path.sep)[:-3]))
# sys.path.append(os.path.sep.join(__file__.split(os.path.sep)[:-3]))
from aws_sts_tool import cli

''' Test for parser '''

def test_no_arguments_passed(capsys):
    ''' Test for no arguments passed '''
    parser = cli.createParser()
    with pytest.raises(SystemExit):
        parser.parse_args([])
    captured = capsys.readouterr()
    assert 'error: the following arguments are required: account_id, sessionName, roleName, output' in captured.err

def test_all_required_arguments_passed(capsys):
    ''' Test for all required arguments passed '''
    parser = cli.createParser()
    args = vars(parser.parse_args(['123456789012','test','test-role','json']))
    assert 'account_id' in args
    assert 'sessionName' in args
    assert 'roleName' in args
    assert 'output' in args

def test_all_required_and_optional_arguments_passed(capsys):
    ''' Test for all required arguments passed '''
    parser = cli.createParser()
    args = vars(parser.parse_args(['123456789012','test','test-role','json','--duration','7200']))
    assert 'account_id' in args
    assert 'sessionName' in args
    assert 'roleName' in args
    assert 'output' in args
    assert 'duration' in args