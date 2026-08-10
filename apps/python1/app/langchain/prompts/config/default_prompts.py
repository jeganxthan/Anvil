from app.db.models.system_prompt import SystemPrompt
from app.langchain.prompts.config.types import PromptType


DEFAULT_PROMPTS = {

    PromptType.SYSTEM: SystemPrompt.from_create(
        name="Default System",
        type=PromptType.SYSTEM.value,
        is_active=True,
        content="""
You are a helpful AI assistant.

Rules:
- Answer clearly.
- Do not invent information.
- Ask for clarification if needed.
""".strip(),
    ),


    PromptType.RAG: SystemPrompt.from_create(
        name="Default RAG",
        type=PromptType.RAG.value,
        is_active=True,
        content="""
Answer the question using only the provided context.

If the answer is not in the context, say you don't know.

Context:
{context}

Question:
{question}
""".strip(),
    ),


    PromptType.TOOL: SystemPrompt.from_create(
        name="Default Tool",
        type=PromptType.TOOL.value,
        is_active=True,
        content="""
You are an assistant with access to tools.

Use tools only when required.
Never create fake tool results.
""".strip(),
    ),


    PromptType.SUMMARY: SystemPrompt.from_create(
        name="Default Summary",
        type=PromptType.SUMMARY.value,
        is_active=True,
        content="""
Summarize the following content.

Content:
{text}
""".strip(),
    ),
}