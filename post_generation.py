import ollama

def generate_post(topic:str)-> str:
    response= ollama.generate(model='curiosity', prompt=topic)
    return response.response
