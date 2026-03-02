from typing import Annotated
from pydantic import AfterValidator, StringConstraints


def must_be_between_1_to_36_characters(v: str) -> str:
    if v.strip() == "":
        raise ValueError("input cannot be empty")

    if len(v) > 36:
        raise ValueError("input must be maximum 36 characters")

    return v.strip().lower().title()


Name = Annotated[str, AfterValidator(must_be_between_1_to_36_characters)]
NotEmptyString = Annotated[str, StringConstraints(min_length=1, strip_whitespace=True)]
