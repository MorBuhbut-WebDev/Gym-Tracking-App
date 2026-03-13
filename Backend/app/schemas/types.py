from typing import Annotated

from pydantic import BeforeValidator, Field

Name = Annotated[
    str,
    BeforeValidator(lambda v: str(v).strip().lower().title()),
    Field(min_length=1, max_length=36),
]

NotEmptyString = Annotated[
    str, BeforeValidator(lambda v: str(v).strip()), Field(min_length=1)
]
