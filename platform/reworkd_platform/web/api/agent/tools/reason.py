from fastapi.responses import StreamingResponse as FastAPIStreamingResponse
from lanarky.responses import StreamingResponse
from langchain import LLMChain

from reworkd_platform.web.api.agent.model_settings import create_model
from reworkd_platform.web.api.agent.tools.tool import Tool


class Reason(Tool):
    description = (
        "Reason about task via existing information or understanding. "
        "Make decisions / selections from options."
    )

    async def call(
        self, goal: str, task: str, input_str: str
    ) -> FastAPIStreamingResponse:
        from reworkd_platform.web.api.agent.prompts import execute_task_prompt

        llm = create_model(self.model_settings, streaming=True)
        chain = LLMChain(llm=llm, prompt=execute_task_prompt)

        return StreamingResponse.from_chain(
            chain,
            {"goal": goal, "language": self.model_settings.language, "task": task},
            media_type="text/event-stream",
        )
