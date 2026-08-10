from langchain_core.output_parsers import (
    StrOutputParser,
    JsonOutputParser,
    PydanticOutputParser,
)

from pydantic import BaseModel


class OutputParserFactory:


    @staticmethod
    def create(
        parser_type: str,
        schema: type[BaseModel] | None = None,
    ):


        match parser_type:


            case "string":

                return StrOutputParser()


            case "json":

                return JsonOutputParser()


            case "pydantic":

                if schema is None:
                    raise ValueError(
                        "Schema required for pydantic parser"
                    )

                return PydanticOutputParser(
                    pydantic_object=schema
                )


            case _:

                raise ValueError(
                    f"Unknown parser {parser_type}"
                )