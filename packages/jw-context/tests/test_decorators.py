# std
import os

# internal
from jw_context.decorators import environment_variables


def test_environment_variable():
    os.environ['test_environment_variable'] = '1'

    @environment_variables(test_environment_variable='2')
    def func():
        assert os.environ['test_environment_variable'] == '2'

    assert os.environ['test_environment_variable'] == '1'
    func()
    assert os.environ['test_environment_variable'] == '1'


def test_environment_variables():
    os.environ['test_environment_variables_1'] = '1'
    os.environ['test_environment_variables_2'] = '2'

    @environment_variables(
        test_environment_variables_1='3',
        test_environment_variables_2='4',
    )
    def func():
        assert os.environ['test_environment_variables_1'] == '3'
        assert os.environ['test_environment_variables_2'] == '4'

    assert os.environ['test_environment_variables_1'] == '1'
    assert os.environ['test_environment_variables_2'] == '2'
    func()
    assert os.environ['test_environment_variables_1'] == '1'
    assert os.environ['test_environment_variables_2'] == '2'
