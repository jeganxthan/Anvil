from langchain_core.prompts import PromptTemplate


class PromptRenderer:

    def render(
        self,
        template: str,
        variables: dict[str, str],
    ) -> str:

        prompt = PromptTemplate.from_template(
            template
        )

        return prompt.format(
            **variables
        )