# std
from typing import List, Optional as Opt, Union

# external
from jw_types import Data

# internal
from jw_datatools.internal.errors import expect


def normalize_keys(maybe_keys_or_path: Opt[Union[str, List[str]]] = None) -> List[str]:
    if maybe_keys_or_path is None:
        return []
    elif isinstance(maybe_keys_or_path, str):
        return maybe_keys_or_path.split('.')
    elif isinstance(maybe_keys_or_path, list):
        return maybe_keys_or_path
    else:
        expect(f'{maybe_keys_or_path} should be of type NoneType, str, or list')


def safeget(data: Data, keys: Opt[Union[str, List[str]]] = None, default: Data = None) -> Data:
    keys = normalize_keys(keys)
    tmp = data
    for key in keys:
        if isinstance(tmp, dict) and key in tmp:
            tmp = tmp[key]
        else:
            return default
    return tmp


def safeset(
        data: Data,
        keys: Union[str, List[str]],
        value: Data,
) -> Data:
    keys = normalize_keys(keys)
    expect('should provide at least 1 key for safeset', len(keys) > 0)
    tmp = data
    for key in keys[:-1]:
        if isinstance(tmp, dict):
            if not key in tmp:
                tmp[key] = {}
            tmp = tmp[key]
    expect('safeset expects nested dicts', isinstance(tmp, dict))
    tmp[keys[-1]] = value
    return data


def safepop(
        data: Data,
        keys: Union[str, List[str]],
        default: Data = None,
) -> Data:
    keys = normalize_keys(keys)
    expect('should provide at least 1 key for safepop', len(keys) > 0)
    tmp = data
    for key in keys[:-1]:
        if not isinstance(tmp, dict):
            return default
        if key not in tmp:
            return default
        tmp = tmp[key]
    if not isinstance(tmp, dict):
        return default
    return tmp.pop(keys[-1], default)
