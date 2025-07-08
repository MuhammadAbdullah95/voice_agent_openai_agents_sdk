import random
from collections.abc import AsyncIterator
from typing import Callable
from agents import Agent, Runner, TResponseInputItem, function_tool, OpenAIChatCompletionsModel
from agents.run import RunConfig
from openai import AsyncOpenAI
from agents.extensions.handoff_prompt import prompt_with_handoff_instructions
from agents.voice import VoiceWorkflowBase, VoiceWorkflowHelper
from dotenv import load_dotenv
import os
load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")


client = AsyncOpenAI(api_key=GOOGLE_API_KEY, base_url="https://generativelanguage.googleapis.com/v1beta/openai/")

model = OpenAIChatCompletionsModel(model="gemini-2.5-flash", openai_client=client)

run_config = RunConfig(model=model, model_provider=client, tracing_disabled=True)

@function_tool
def get_weather(city: str) -> str:
    """Get the weather for a given city."""
    print(f"[debug] get_weather called with city: {city}")
    choices = ["sunny", "cloudy", "rainy", "snowy"]
    return f"The weather in {city} is {random.choice(choices)}."


english_agent = Agent(
    name="English",
    handoff_description="A english speaking agent.",
    instructions=prompt_with_handoff_instructions(
        "You're speaking to a human, so be polite and concise. Speak in English.",
    ),
    model=model,
)

agent = Agent(
    name="Assistant",
    instructions=prompt_with_handoff_instructions(
        "You're speaking to a human, so be polite and concise. If the user speaks in Urdu, handoff to the english agent.",
    ),
    handoffs=[english_agent],
    tools=[get_weather],
    model=model
)


class MyWorkflow(VoiceWorkflowBase):
    def __init__(self, secret_word: str, on_start: Callable[[str], None]):
        """
        Args:
            secret_word: The secret word to guess.
            on_start: A callback that is called when the workflow starts. The transcription
                is passed in as an argument.
        """
        self._input_history: list[TResponseInputItem] = []
        self._current_agent = agent
        self._secret_word = secret_word.lower()
        self._on_start = on_start

    async def run(self, transcription: str) -> AsyncIterator[str]:
        self._on_start(transcription)

        # Add the transcription to the input history
        self._input_history.append(
            {
                "role": "user",
                "content": transcription,
            }
        )

        # If the user guessed the secret word, do alternate logic
        if self._secret_word in transcription.lower():
            yield "You guessed the secret word!"
            self._input_history.append(
                {
                    "role": "assistant",
                    "content": "You guessed the secret word!",
                }
            )
            return

        # Otherwise, run the agent
        result = Runner.run_streamed(self._current_agent, self._input_history, run_config=run_config)

        try:
            async for chunk in VoiceWorkflowHelper.stream_text_from(result):
                yield chunk
        except Exception as e:
            print(f"[error] Failed to parse Gemini event stream: {e}")
            yield "⚠️ An error occurred while processing the response."


        # Update the input history and current agent
        self._input_history = result.to_input_list()
        self._current_agent = result.last_agent