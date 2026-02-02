REWRITING_QUERY_SYSTEM_PROMPT = """
Create a search query for document retrieval.

USER QUERY: {query}

RULES:
1. **FOCUS**: Use keywords from the user's query
2. **LANGUAGE**: Same as input language
3. **LENGTH**: 3-6 words
4. **FORMAT**: Only the search query, no additional text

EXAMPLES:
- "дати контакти" → "контактна інформація телефон email адреса"
- "вартість столу" → "ціна обіднього стола дерево"
- "як налаштувати роутер" → "налаштування домашнього роутера інструкція"

Return only the search query:
"""

