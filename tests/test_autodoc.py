import pytest


@pytest.mark.sphinx('html', testroot='ext-autodoc_pydantic')
def test_model_plain(app, autodocument):
    options_app = dict(autodoc_pydantic_model_show_schema=False)
    actual = autodocument(app=app,
                          documenter='pydantic_model',
                          object_path='target.model.PlainModel',
                          options_app=options_app)

    assert list(actual) == [
        '',
        '.. py:pydantic_model:: PlainModel',
        '   :module: target.model',
        '',
        '   Model Plain.',
        ''
    ]

@pytest.mark.sphinx('html', testroot='ext-autodoc_pydantic')
def test_model_with_field(app, autodocument):
    options_app = dict(autodoc_pydantic_model_show_schema=False)
    options_doc = dict(members=None)
    actual = autodocument(app=app,
                          documenter='pydantic_model',
                          object_path='target.model.ModelWithField',
                          options_doc=options_doc,
                          options_app=options_app)

    assert list(actual) == [
        '',
        '.. py:pydantic_model:: ModelWithField',
        '   :module: target.model',
        '',
        '   Model With Field.',
        '',
        '',
        '   .. py:pydantic_field:: ModelWithField.field',
        '      :module: target.model',
        '      :type: int',
        '      :value: 1',
        '',
        '      Doc field',
        ''
    ]

@pytest.mark.sphinx('html', testroot='ext-autodoc_pydantic')
def test_model_with_field_validator(app, autodocument):
    options_app = dict(autodoc_pydantic_model_show_schema=False)
    options_doc = dict(members=None)
    actual = autodocument(app=app,
                          documenter='pydantic_model',
                          object_path='target.model.ModelWithFieldValidator',
                          options_doc=options_doc,
                          options_app=options_app)

    assert list(actual) == [
        '',
        '.. py:pydantic_model:: ModelWithFieldValidator',
        '   :module: target.model',
        '',
        '   Model With Field Validator.',
        '',
        '   :Validators:',
        '      - :py:obj:`is_integer <target.model.ModelWithFieldValidator.is_integer>` » :py:obj:`field <target.model.ModelWithFieldValidator.field>`',
        '',
        '   .. py:pydantic_field:: ModelWithFieldValidator.field',
        '      :module: target.model',
        '      :type: int',
        '      :value: 1',
        '',
        '      Doc field',
        '',
        '      :Validated by:',
        '         - :py:obj:`is_integer <target.model.ModelWithFieldValidator.is_integer>`',
        '',
        '   .. py:pydantic_validator:: ModelWithFieldValidator.is_integer',
        '      :module: target.model',
        '      :classmethod:',
        '',
        '      Doc validator.',
        '',
        '      :Validates:',
        '         - :py:obj:`field <target.model.ModelWithFieldValidator.field>`',
        ''
    ]