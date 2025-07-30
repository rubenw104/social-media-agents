import ollama

def generate_post2(topic:str)-> str:
    response= ollama.generate(model='gemma3:1b', prompt=topic)
    return response.response

def generate_post(topic:str)-> str:

    content_types=['funfact', 'news', 'sarcastic', 'inspirational', 'educational', 'promotional', 'motivational', 'entertainment', 'review', 'personal']

    tones=['formal', 'informal', 'ironic', 'emotional', 'direct', 'professional', 'engaging', 'neutral']

    max_length=500
    language: str = 'english'
    include_emojis: bool = True
    include_hashtags: bool = True
    minimum_length=300

    content_type= 'educational'
    tone= 'neutral'

    system_prompt = f"""
    You are a professional copywriter specialized in creating engaging and effective Instagram post captions.

    Your task is to write a caption for an Instagram post, based on the user inputs.
    IMPORTANT: Do not include any commentary, explanation, or formatting—return only the final caption, ready to be published.
    """
    user_prompt=f"""Write an Instagram caption with the following details:

    - **Topic**: {topic}
    - **Content Type**: {content_type} (e.g., fun fact, news, sarcastic, promotional, inspirational, etc.)
    - **Tone of Voice**: {tone} (e.g., formal, informal, ironic, emotional, direct, professional, etc.)
    - **Maximum Length**: {max_length} characters
    - **Minimum Length**: {minimum_length} characters
    - **Include Emojis**: {include_emojis} 
    - **Include Hashtags**: {include_hashtags}
    - **Language**: {language}

    Guidelines:
    - Capture the reader’s attention from the very beginning.
    - Match the tone and content style appropriately.
    - If **Include Emojis** is true, insert relevant emojis naturally into the text.
    - If **Include Hashtags** is true, append creative and appropriate hashtags at the end (avoid clichés).
    - The caption must be written in {language}.
    - Keep the text between {minimum_length} and {max_length} characters.
    - Do not include any commentary, explanation, or formatting—return only the final caption, ready to be published.

    Output:
    - A single Instagram caption tailored to the inputs above.
    """

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]

    # First response from the bot
    response = ollama.chat(model='gemma3:1b', messages=messages)
    return response.message.content

# print(generate_post2('john cena'))
