import os
from dotenv import load_dotenv
from anthropic import Anthropic

# load the API key
load_dotenv()
client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

prompt = "Explain what a data pipeline is in one simple sentence."

# Get the response from the model
response = client.messages.create(
    model="claude-haiku-4-5",
    max_tokens=200,
    messages=[
        {"role": "user", "content": prompt},
    ],
)

print(response.content[0].text)
