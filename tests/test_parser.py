import pytest
import sys
import os
# print(os.path.sep.join(__file__.split(os.path.sep)[:-3]))
# sys.path.append(os.path.sep.join(__file__.split(os.path.sep)[:-3]))
from aws_sts_tool import cli

''' Test for parser '''

def test_no_arguments_passed(capsys):
    ''' Test for no arguments passed '''
    # print(aws_sts_tool)
    parser = cli.createParser()
    with pytest.raises(SystemExit):
        parser.parse_args([])
    captured = capsys.readouterr()
    assert 'error: the following arguments are required: account_id, sessionName, roleName, output' in captured.err