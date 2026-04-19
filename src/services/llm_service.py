from groq import Groq

from config.settings import settings


class LLMService:
    def __init__(self) -> None:
        if not settings.GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY is missing. Please set it in your .env file.")

        self.client = Groq(api_key=settings.GROQ_API_KEY)
        self.model_name = settings.MODEL_NAME

    def generate_response(self, prompt: str) -> str:
        """
        Sends a prompt to Groq and returns the generated text response.
        """
        try:
            completion = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a professional technical hiring assistant.",
                    },
                    {
                        "role": "user",
                        "content": prompt,
                    },
                ],
                temperature=0.4,
                max_tokens=500,
            )

            content = completion.choices[0].message.content
            if not content:
                raise RuntimeError("Empty response received from Groq.")

            return content.strip()

        except Exception as exc:
            raise RuntimeError(f"Groq API error: {exc}") from exc