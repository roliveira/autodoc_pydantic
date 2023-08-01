"""This module contains compatibility functions to abstract away implementation
differences between different sphinx versions.

"""
import importlib
from typing import Tuple, List
import re

import pydantic
import sphinx
from sphinx.addnodes import desc_sig_punctuation, desc_annotation, pending_xref


def package_is_missing(package_name):
    """Check if a Python package is not available"""
    try:
        importlib.import_module(package_name)
        return False
    except ImportError:
        return True


def desc_annotation_default_value(value: str):
    """Provides compatibility abstraction for `desc_annotation` for default
    values for sphinx version smaller and greater equal sphinx 4.3.

    """

    if sphinx.version_info < (4, 3):
        return [desc_annotation, f" = {value}"]
    from sphinx.addnodes import desc_sig_space
    return (desc_sig_space,
            [desc_sig_punctuation, "="],
            desc_sig_space,
            value)


def desc_annotation_type_annotation(type_str: str) -> Tuple:
    """Provides compatibility abstraction for `desc_annotation` for type
    annotation for sphinx version smaller and greater equal sphinx 4.3.

    """

    if sphinx.version_info < (4, 3):
        return (": ", [pending_xref, type_str])
    from sphinx.addnodes import desc_sig_space
    return ([desc_sig_punctuation, ":"],
            desc_sig_space,
            [pending_xref, type_str])


def desc_annotation_directive_prefix(prefix: str):
    """Provides compatibility abstraction for `desc_annotation` for directive
    prefix for sphinx version smaller and greater equal sphinx 4.3.

    """

    if sphinx.version_info >= (4, 3):
        from sphinx.addnodes import desc_sig_space
        return (prefix, desc_sig_space)
    return f'{prefix} '


def rst_alias_class_directive() -> str:
    """Provides compatibility abstraction for `class` directive when used with
    sphinx 4.3 or newer.

    """

    return ":py:class:" if sphinx.version_info >= (4, 3) else ":class:"


def convert_ellipsis_to_none(result: List[str]) -> List[str]:
    """Eliminate subtle differences in default values of required pydantic
    fields between various pydantic versions.

    """

    return [x.replace("Ellipsis", "None") for x in result]


def typing_module_prefix() -> str:
    """Provides compatibility abstraction to account for changed behaviour of
    `autodoc_typehints_format` in sphinx 5.0 from fully qualified to short
    which requires types of typing module to prefixed with `~typing.`.

    """

    if (5,) <= sphinx.version_info < (6, 1):
        return "~typing."

    return ""

def typing_module_prefix() -> str:
    """Provides compatibility abstraction to account for changed behaviour of
    `autodoc_typehints_format` in sphinx 5.0 from fully qualified to short
    which requires types of typing module to prefixed with `~typing.`.

    """

    if sphinx.version_info >= (5,):
        return "~typing."

    return ""


def typehints_prefix() -> str:
    """Provides compatibility abstraction to account for changed behaviour of
    `autodoc_typehints_format` in sphinx 5.0 from fully qualified to short
    which requires `~`.

    """

    if sphinx.version_info >= (5,):
        return "~"

    return ""


def module_doc_string_tab() -> str:
    """Provides compatibility abstraction to account for changed behaviour of
    python module doc string in sphinx 5.2 that gains an additional whitespace
    tab at the start.

    """

    if sphinx.version_info >= (5, 2):
        return "   "

    return ""


def get_optional_type_expected(field_type: str):
    """Provide compatibility to account for changed behaviour of
    autodoc_typehints_format with optional field which return either
    `Optional[<type>]` or `<type> | None` depending on the version.

    Here is an example output with sphinx 5.3:

    .. code-block: pycon
        >>> import sphinx
        >>> print(sphinx.version_info[:2])
        (5, 3)
        >>> get_optional_type_expected('int')
        int | None

    Here is an example output with sphinx 6.1:
    .. code-block: pycon
        >>> import sphinx
        >>> print(sphinx.version_info[:2])
        (6, 1)
        >>> get_optional_type_expected('int')
        Optional[int]
    """
    if sphinx.version_info >= (6, 1):
        optional_match = re.findall(r'Optional\[(\w*)\]', field_type)
        if optional_match is not None and len(optional_match) > 0:
            return optional_match[0] + ' | None'  # int | None
    return field_type  # 'Optional[int]'


TYPING_MODULE_PREFIX = typing_module_prefix()
TYPEHINTS_PREFIX = typehints_prefix()
OPTIONAL_INT = TYPING_MODULE_PREFIX + get_optional_type_expected(
    'Optional[int]')
