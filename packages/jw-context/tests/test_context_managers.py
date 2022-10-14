# std
import os

# internal
from jw_context.context_managers import EnvironmentVariables


def test_environment_variable():
    os.environ['test_environment_variable'] = '1'
    assert os.environ['test_environment_variable'] == '1'
    with EnvironmentVariables(test_environment_variable='2'):
        assert os.environ['test_environment_variable'] == '2'
    assert os.environ['test_environment_variable'] == '1'


def test_environment_variables():
    os.environ['test_environment_variables_1'] = '1'
    os.environ['test_environment_variables_2'] = '2'
    env = EnvironmentVariables(
        test_environment_variables_1='3',
        test_environment_variables_2='4',
    )
    assert os.environ['test_environment_variables_1'] == '1'
    assert os.environ['test_environment_variables_2'] == '2'
    with env:
        assert os.environ['test_environment_variables_1'] == '3'
        assert os.environ['test_environment_variables_2'] == '4'
    assert os.environ['test_environment_variables_1'] == '1'
    assert os.environ['test_environment_variables_2'] == '2'
