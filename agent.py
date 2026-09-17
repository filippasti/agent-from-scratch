from dotenv import load_dotenv
import os
import anthropic
from datetime import datetime

load_dotenv()
api_key = os.environ["ANTHROPIC_API_KEY"]
client = anthropic.Anthropic(api_key=api_key)

def get_current_time():
    jetzt = datetime.now()
    return jetzt.strftime("%d.%m.%Y, %H:%M Uhr")

tools = [
    {
        "name": "get_current_time",
        "description": "Gibt die aktuelle Uhrzeit und das aktuelle Datum auf dem System des Nutzers zurück. Nutze dieses Werkzeug immer, wenn nach der aktuellen Zeit, dem heutigen Datum oder dem Wochentag gefragt wird.",
        "input_schema": {"type": "object", "properties": {}, "required": []}
    }
]

messages = [{"role": "user", "content": "Wie spät ist es, und wie viele Minuten sind es noch bis 18 Uhr?"}]


while True:
    print("--- Runde, Historie hat", len(messages), "Einträge")
    response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=1024,
        messages=messages,
        tools=tools
    )

    if response.stop_reason != "tool_use":
        print(response.content[0].text)
        break

    for block in response.content:
        if block.type == "tool_use":
            tool_block = block
    if tool_block.name == "get_current_time":
        ergebnis = get_current_time()
    messages.append({"role": "assistant", "content": response.content})
    messages.append({
        "role": "user",
        "content": [{
            "type": "tool_result",
            "tool_use_id": tool_block.id,
            "content": ergebnis
        }]
        })


