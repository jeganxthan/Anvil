from langchain_core.prompts import ChatPromptTemplate

from app.db.models.system_prompt import SystemPrompt


class PromptBuilder:


    def build(
        self,
        system_prompt: SystemPrompt,
    ) -> ChatPromptTemplate:


        return ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    system_prompt.content,
                ),
                (
                    "human",
                    "{question}",
                ),
            ]
        )