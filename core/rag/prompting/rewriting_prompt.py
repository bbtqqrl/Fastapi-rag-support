REWRITING_QUERY_SYSTEM_PROMPT = """
Generate 3 distinct search query variations for document retrieval.
Each query should approach the user's request from a different angle.

USER QUERY: {query}

RULES:
1. **VARIATION 1**: Main focus - use core keywords
2. **VARIATION 2**: Broader focus - include related terms  
3. **VARIATION 3**: Specific focus - add details from similar queries
4. **LANGUAGE**: Same as input (Ukrainian)
5. **FORMAT**: JSON array of exactly 3 strings
6. **LENGTH**: 3-6 words per query

EXAMPLES FOR "дати контакти":
[
    "контактна інформація компанії телефон email",
    "адреса сайт соціальні мережі контакти",
    "як зв'язатися з майстернею контакти"
]

EXAMPLES FOR "вартість столу":
[
    "ціна деревяного обіднього стола",
    "скільки коштує меблевий стіл",
    "розцінки виготовлення столу з масиву"
]

Return ONLY JSON array:
"""

