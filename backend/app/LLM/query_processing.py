import logging

from core.config import settings
from ai.gemini_client import get_gemini_client
from db.chat_queries import chatProgress, get_chat_history
from rag.retriever import retrieve_context
from ai.tools.handlers import handlers
from utils.time_utils import utc_now_iso
from LLM.prompt_renderer import render_gemini_prompt
from ai.tools.definitions import config

logger = logging.getLogger(__name__)

def getResults(query:str, user_id: int, chat_id: int):
    # Chat history
    history = get_chat_history(chat_id=chat_id, user_id=user_id)

    # Context
    context = retrieve_context(query=query)

    prompt = render_gemini_prompt(
        query=query,
        context=context,
        history=history,
    )

    response = get_gemini_client().models.generate_content(
        model=settings.gemini_model,
        contents=prompt,
        config=config
    )

    part = response.candidates[0].content.parts[0]
    function_call = getattr(part, "function_call", None)
    logger.info("Gemini response received with %d content parts", len(response.candidates[0].content.parts))

    if function_call:
        final_text = handlers(
            function_call,
            history,
            response,
            config,
            prompt,
            get_gemini_client(),
        )
    else:
        final_text = response.text

    # Save and return final output
    chatProgress(
        id=user_id,
        chat_title = query,
        data={
            "role": "model",
            "parts": [{"text": final_text}],
            "time_stamp": utc_now_iso()
        }, 
        chat_id=chat_id
    )

    return ({
        "data": final_text,
        "success": True,
        "message": "The solution to the query"
    })

def getResultsStream(query: str, user_id: int, chat_id: int):
    # Chat history
    history = get_chat_history(chat_id=chat_id, user_id=user_id)

    # Context
    context = retrieve_context(query=query)

    prompt = render_gemini_prompt(
        query=query,
        context=context,
        history=history,
    )

    final_text = ""
    stream = get_gemini_client().models.generate_content_stream(
        model=settings.gemini_model,
        contents=prompt,
        config=config
    )

    for chunk in stream:
        function_calls = chunk.function_calls
        if function_calls:
            # Tool calls are resolved by the existing handler, which returns the full text
            tool_text = handlers(
                function_calls[0],
                history,
                chunk,
                config,
                prompt,
                get_gemini_client(),
            )
            final_text += tool_text
            yield tool_text
            break

        if chunk.text:
            final_text += chunk.text
            yield chunk.text

    logger.info("Gemini stream completed with %d characters", len(final_text))

    # Save final output once the stream is complete
    chatProgress(
        id=user_id,
        chat_title = query,
        data={
            "role": "model",
            "parts": [{"text": final_text}],
            "time_stamp": utc_now_iso()
        },
        chat_id=chat_id
    )
