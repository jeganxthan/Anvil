from langchain_core.prompts import (
    ChatPromptTemplate,
    PromptTemplate,
)

from app.langchainDummy.prompts.model.system_prompt import (
    SystemPrompt,
)


class PromptBuilder:

    def build(
        self,
        system_prompt: SystemPrompt,
        variables: dict[str, str] | None = None,
    ) -> ChatPromptTemplate:

        variables = variables or {}

        rendered_system = (
            PromptTemplate
            .from_template(system_prompt.content)
            .format(**variables)
        )

        return ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    rendered_system,
                ),
                (
                    "human",
                    "{question}",
                ),
            ]
        )