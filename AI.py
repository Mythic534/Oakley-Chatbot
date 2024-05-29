from openai import OpenAI # type: ignore
import tiktoken # type: ignore
from dotenv import load_dotenv # type: ignore
import os

def get_messages(question):

    # Read website text
    with open("website.txt", "r", encoding="utf-8") as f:
        website = f.read()

    # Read context text
    with open("context.txt", "r", encoding="utf-8") as f:
        context = f.read()

    message = f"Use the following information to aid in answering the subsequent question:\n\n{context}\n\nAs well as information from our website if provided:{website}\n\nQuestion: {question}" # Pass question in as a cmd line argument with quotation marks

    messages=[
            {
                "role": "system",
                "content": "You are Oakley, a friendly AI assistant representing Oak Tree Animals' Charity on their website. Politely avoid answering questions irrelevant to the Charity, its website or animal welfare. If you don't know the answer to a question, answer 'I don't know'."
            },
            {
                "role": "user",
                "content": message
            }
        ]
    
    return messages

def get_response(_messages):

    load_dotenv()
    APIkey = os.getenv("API_KEY")
        
    client = OpenAI(api_key=APIkey)
    
    # Submit to OpenAI
    chat_completion = client.chat.completions.create(
        messages=_messages,
        model="gpt-3.5-turbo",
    )

    return chat_completion.choices[0].message.content

# Return the number of tokens used by a list of messages. 
def cost_of_message(_messages, token_price=0.0005/1000):
    
    encoding = tiktoken.get_encoding("cl100k_base")
    tokens_per_message = 3
    tokens_per_name = 1
    num_tokens = 0
    for message in _messages:
        num_tokens += tokens_per_message
        for key, value in message.items():
            num_tokens += len(encoding.encode(value))
            if key == "name":
                num_tokens += tokens_per_name
    num_tokens += 3
    print(f"No. of Tokens: {num_tokens}")
    print(f"Cost of message: ${round(num_tokens*token_price, 5)}")