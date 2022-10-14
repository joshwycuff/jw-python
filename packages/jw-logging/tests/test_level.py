# internal
from jw_logging.level import Level, Verbosity


def test_level_try_from_string_Critical():
    assert Level.try_from_string('critical') == Level.Critical


def test_level_try_from_string_Error():
    assert Level.try_from_string('error') == Level.Error


def test_level_try_from_string_Warning():
    assert Level.try_from_string('warning') == Level.Warning


def test_level_try_from_string_Info():
    assert Level.try_from_string('info') == Level.Info


def test_level_try_from_string_Debug():
    assert Level.try_from_string('debug') == Level.Debug


def test_level_try_from_string_Trace():
    assert Level.try_from_string('trace') == Level.Trace


def test_level_try_from_string_Unknown():
    assert Level.try_from_string('unknown') == Level.Warning


def test_level_try_from_verbosity_Error():
    assert Level.try_from_verbosity(Verbosity.Error) == Level.Error


def test_level_try_from_verbosity_Warning():
    assert Level.try_from_verbosity(Verbosity.Warning) == Level.Warning


def test_level_try_from_verbosity_Info():
    assert Level.try_from_verbosity(Verbosity.Info) == Level.Info


def test_level_try_from_verbosity_Debug():
    assert Level.try_from_verbosity(Verbosity.Debug) == Level.Debug


def test_level_try_from_verbosity_Trace():
    assert Level.try_from_verbosity(Verbosity.Trace) == Level.Trace


def test_level_try_from_verbosity_Unknown():
    assert Level.try_from_verbosity(None) == Level.Warning


def test_verbosity_from_int_0():
    assert Verbosity.from_int(0) == Verbosity.Error


def test_verbosity_from_int_1():
    assert Verbosity.from_int(1) == Verbosity.Warning


def test_verbosity_from_int_2():
    assert Verbosity.from_int(2) == Verbosity.Info


def test_verbosity_from_int_3():
    assert Verbosity.from_int(3) == Verbosity.Debug


def test_verbosity_from_int_4():
    assert Verbosity.from_int(4) == Verbosity.Trace
