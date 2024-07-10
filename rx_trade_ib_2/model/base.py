from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel, to_snake


class BasePydanticModel(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
    )


class IgnoreExtraPydanticModel(BasePydanticModel):
    model_config = ConfigDict(alias_generator=to_snake, extra="ignore")
