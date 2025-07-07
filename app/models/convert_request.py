from pydantic import BaseModel

class ConvertRequest(BaseModel):
    output_format: str
    model_name: str

    @classmethod
    def as_form(cls, output_format: str, model_name: str):
        return cls(output_format=output_format, model_name=model_name)
