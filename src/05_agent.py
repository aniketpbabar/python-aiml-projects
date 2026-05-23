"""A small agent: the model decides which tools to call to answer the question."""

import os
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()
client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])


# --- the tools the agent is allowed to use ---
def get_row_count(table_name):
    fake_db = {"customers": 1284, "orders": 9472, "products": 312}
    return fake_db.get(table_name, 0)


def add_numbers(a, b):
    return a + b


AVAILABLE = {"get_row_count": get_row_count, "add_numbers": add_numbers}

# the model needs a JSON description of each tool to know it exists
TOOLS = [
    {
        "name": "get_row_count",
        "description": "Get the number of rows in a database table.",
        "input_schema": {
            "type": "object",
            "properties": {"table_name": {"type": "string"}},
            "required": ["table_name"],
        },
    },
    {
        "name": "add_numbers",
        "description": "Add two numbers together.",
        "input_schema": {
            "type": "object",
            "properties": {"a": {"type": "number"}, "b": {"type": "number"}},
            "required": ["a", "b"],
        },
    },
]


def run_agent(question):
    messages = [{"role": "user", "content": question}]
    # keep looping until the model stops asking for tools
    while True:
        response = client.messages.create(
            model="claude-haiku-4-5",
            max_tokens=500,
            tools=TOOLS,
            messages=messages,
        )
        messages.append({"role": "assistant", "content": response.content})

        if response.stop_reason != "tool_use":
            # the final answer is in the text block(s)
            return "".join(b.text for b in response.content if b.type == "text")

        # run every tool the model asked for, send the results back
        tool_results = []
        for block in response.content:
            if block.type == "tool_use":
                result = AVAILABLE[block.name](**block.input)
                print(f"  [tool] {block.name}({block.input}) -> {result}")
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": str(result),
                })
        messages.append({"role": "user", "content": tool_results})


if __name__ == "__main__":
    print(run_agent("How many rows are in the customers and orders tables combined?"))
