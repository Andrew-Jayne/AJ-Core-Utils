from os import environ
from typing import TypeVar

INPUT_TYPE = TypeVar("INPUT_TYPE")


def _convert_value(
    value: str,
    var_name: str,
    return_type: type[INPUT_TYPE],
) -> INPUT_TYPE:
    """Convert an input string value to the specified type."""
    try:
        match return_type.__name__:
            case "str":
                return value  # type: ignore
            case "bool":
                if value == "True":
                    return True  # type: ignore
                elif value == "False":
                    return False  # type: ignore
                else:
                    raise ValueError(
                        f"Environment variable {var_name} with value {value} cannot be converted to bool. Only 'True' and 'False' are accepted."
                    )
            case "int":
                return int(value)  # type: ignore
            case "float":
                return float(value)  # type: ignore
            case "list":
                return [item.strip() for item in value.split(",")]  # type: ignore
            case "dict":
                result = {}
                pairs = [pair.strip() for pair in value.split(",")]
                for pair in pairs:
                    if "=" in pair:
                        k, v = pair.split("=", 1)
                        result[k.strip()] = v.strip()
                return result  # type: ignore
            case _:
                raise TypeError(f"Unsupported return_type: {return_type}")
    except Exception as e:
        raise ValueError(
            f"Failed to convert environment variable '{var_name}' to {return_type}: {e}"
        ) from e


def load_optional_var(
    var_name: str,
    default_value: INPUT_TYPE,
    *,
    return_type: type[INPUT_TYPE] = str,
) -> INPUT_TYPE:
    value = environ.get(var_name, None)
    if value is None:
        return default_value
    return _convert_value(value, var_name, return_type=return_type)


def load_mandatory_var(
    var_name: str,
    *,
    return_type: type[INPUT_TYPE] = str,
) -> INPUT_TYPE:
    try:
        value = environ[var_name]
        return _convert_value(value, var_name, return_type=return_type)
    except KeyError as exc:
        raise EnvironmentError(
            f"Environment variable '{var_name}' is required but not set."
        ) from exc
