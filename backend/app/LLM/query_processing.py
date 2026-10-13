import google.genai as genai
import os
import json
from dotenv import load_dotenv
from db.chat_queries import chatProgress, get_chat_history
from rag.chromaDB import retrieve_context
from tool_calling.handlers import handlers
from datetime import datetime
from utils.history_dto import history_data_transform_object
from utils.tools.tools_definition import config

load_dotenv()

client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))

def getResults(query:str, user_id: int, chat_id: int):
    # Chat history
    history = get_chat_history(chat_id=chat_id)

    # Context
    context = retrieve_context(query=query)

    if (len(history) > 0):
        history_data_transform_object(history)
        
    print(history, context)

    if history: 
        current_question = query

        prompt = f"""
        You are a Days Gone game assistant.

        Use the provided game context to answer the user's question.
        Prefer the provided context over your general knowledge.
        If the context does not contain enough information, say that
        you don't have enough information rather than inventing details.

        Conversation history:
        {history[:-2] if len(history) > 2 else "There is no chat history"}

        Relevant context:
        {context}

        Current question:
        {current_question}

        Answer the current question using the relevant context.
        """

        response = client.models.generate_content(
            model="gemini-3.1-flash-lite",
            contents=prompt,
            config=config
        )
        
        part = response.candidates[0].content.parts[0]
        function_call = getattr(part, "function_call", None)
        print(response.candidates[0].content.parts)

        if function_call:
            final_text = handlers(function_call, history, response, config, prompt, client)    

        else:
            final_text = response.text
    else:
        interaction = client.interactions.create(
            model='gemini-3.1-flash-lite',
            input=query
        )
        final_text = interaction.output_text

    # Save and return final output
    now = datetime.now()
    chatProgress(
        id=user_id,
        chat_title = query,
        data={
            "role": "model",
            "parts": [{"text": final_text}],
            "time_stamp": now.strftime("%d-%m-%Y %H:%M %p")
        }, 
        chat_id=chat_id
    )

    return ({
        "data": final_text,
        "success": True,
        "message": "The solution to the query"
    })