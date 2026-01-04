import language_tool_python
from fastapi.concurrency import run_in_threadpool

class LanguageToolService:
    def __init__(self):
        self.tool = language_tool_python.LanguageTool("en-US")

    async def check_text(self, text: str) -> tuple[str, str]:
        matches = await run_in_threadpool(self.tool.check, text)
        if not matches:
            return text, "Your sentence is correct!"
        corrected = language_tool_python.utils.correct(text, matches)
        return corrected, "We corrected your sentence"
