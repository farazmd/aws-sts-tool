import pytest
import sys
import os
import importlib  
sys.path.append(os.path.pathsep.join(__file__.split()[:-1]))
aws_sts_tool = importlib.import_module('aws-sts-tool')

''' Test for parser '''

def test_no_arguments_passed(capsys):
    ''' Test for no arguments passed '''
    parser = aws_sts_tool.createParser()
    with pytest.raises(SystemExit):
        parser.parse_args([])
    captured = capsys.readouterr()
    assert 'error: the following arguments are required: account_id, sessionName, roleName, output' in captured.err