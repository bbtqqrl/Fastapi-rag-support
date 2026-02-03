import json

from llm_client import llm_client
from .prompting.rewriting_prompt import REWRITING_QUERY_SYSTEM_PROMPT


async def rewrite_query(query: str, chat_history = None) -> str:
    prompt = REWRITING_QUERY_SYSTEM_PROMPT.format(query=query)
    
    if chat_history:
        prompt += f"\n\nConversation context: {chat_history[-3:]}"  
    
    response = await llm_client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=100
    )
    try:
        data = json.loads(response.choices[0].message.content.strip())
        if isinstance(data, list):
            print(data)
            return data

        if isinstance(data, dict):
            for key in data:
                if isinstance(data[key], list):
                    return data[key]
    except json.JSONDecodeError:
        pass

    return response                     

