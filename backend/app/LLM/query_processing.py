import logging

from core.config import settings
from ai.gemini_client import get_gemini_client
from db.chat_queries import chatProgress, get_chat_history
from rag.retriever import retrieve_context
from ai.tools.handlers import handlers
from utils.time_utils import utc_now_iso
from LLM.prompt_renderer import render_gemini_prompt
from ai.tools.definitions import config
from LLM.llm_errors import handle_gemini_exception
from LLM.token_estimator import estimator, chunk_selection, history_selection
import json

logger = logging.getLogger(__name__)

def getResults(query:str, user_id: int, chat_id: int):
    final_text = ""
    try:
        # Chat history
        history = get_chat_history(chat_id=chat_id, user_id=user_id)
        print("Before modification: ", history, end="\n\n")
        modified_history = history_selection(history)
        print("After modification: ", modified_history, end="\n\n")

        # Context
        context = retrieve_context(query=query)
        print("Before modification: ", context, end="\n\n")
        modified_context = chunk_selection(context)
        print("After modification: ", modified_context, end="\n\n")

        prompt = render_gemini_prompt(
            query=query,
            context=modified_context,
            history=modified_history,
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
            final_text += handlers(
                function_call,
                modified_history,
                response,
                config,
                prompt,
                get_gemini_client(),
            )
        else:
            final_text += response.text

        return ({
            "data": final_text,
            "success": True,
            "message": "The solution to the query"
        })
    
    except Exception as e:
        return ({
            'error': handle_gemini_exception(e)
        })
    # Save and return final output
    finally:
        if final_text:
            chatProgress(
                id=user_id,
                chat_title = query,
                data={
                    "role": "model",
                    "parts": [{"text": final_text}],
                    "time_stamp": utc_now_iso(),
                    "token": estimator(final_text)
                }, 
                chat_id=chat_id
            )


def getResultsStream(query: str, user_id: int, chat_id: int):
    final_text = ""
    try:
        # Chat history
        history = get_chat_history(chat_id=chat_id, user_id=user_id)
        modified_history = history_selection(history)

        # Context
        context = retrieve_context(query=query)
        modified_context = chunk_selection(context)

        prompt = render_gemini_prompt(
            query=query,
            context=modified_context,
            history=modified_history,
        )

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
                    modified_history,
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

    except Exception as e:
        # Headers are already sent, so the error must be streamed as text.
        # (A `return` inside a generator just ends the stream silently.)
        logger.exception("Streaming query failed for chat_id=%s", chat_id)
        error = handle_gemini_exception(e)
        yield ("\n\n" if final_text else "") + error["message"]

    finally:
        # Save whatever the model produced; never save an empty answer
        if final_text:
            chatProgress(
                id=user_id,
                chat_title = query,
                data={
                    "role": "model",
                    "parts": [{"text": final_text}],
                    "time_stamp": utc_now_iso(),
                    "token": estimator(final_text)
                },
                chat_id=chat_id,
            )
