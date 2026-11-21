import logging

from core.config import settings
from ai.gemini_client import get_gemini_client
from db.chat_queries import chatProgress, get_chat_history
from rag.context_builder import RetrievalMode, build_context
from ai.tools.handlers import run_tools
from utils.time_utils import utc_now_iso
from LLM.prompt_renderer import render_gemini_prompt
from ai.tools.definitions import get_tool_config
from core.games import DEFAULT_GAME, GameKey, get_game
from LLM.llm_errors import handle_gemini_exception
from LLM.token_estimator import estimator, chunk_selection, history_selection
import json

from utils.request_timing import RequestTimer

from google.genai import types

logger = logging.getLogger(__name__)

def getResults(
    query: str,
    user_id: int,
    chat_id: int,
    retrieval_mode: RetrievalMode = "hybrid",
    game: GameKey = DEFAULT_GAME,
):
    final_text = ""
    timer = RequestTimer(game=game, mode=retrieval_mode, stream=False)
    try:
        # Chat history
        history = get_chat_history(chat_id=chat_id, user_id=user_id)
        timer.lap("history")
        print("Before modification: ", history, end="\n\n")
        modified_history = history_selection(history)
        print("After modification: ", modified_history, end="\n\n")

        # Context
        context = build_context(query=query, mode=retrieval_mode, game=game)
        timer.lap("retrieval")
        print("Before modification: ", context, end="\n\n")
        modified_context = chunk_selection(context)
        print("After modification: ", modified_context, end="\n\n")

        prompt = render_gemini_prompt(
            query=query,
            context=modified_context,
            history=modified_history,
            game_name=get_game(game).name,
        )
        tool_config = get_tool_config(game)

        response = get_gemini_client().models.generate_content(
            model=settings.gemini_model,
            contents=prompt,
            config=tool_config
        )

        if response.function_calls:
            final_text += run_tools(
                response.candidates[0].content,
                modified_history,
                prompt,
                get_gemini_client(),
                tool_config,
                stats=timer.fields,
            )
        else:
            final_text += response.text or ""
        timer.lap("llm")

        return ({
            "data": final_text,
            "success": True,
            "message": "The solution to the query"
        })
    
    except Exception as e:
        timer.fields["status"] = "error"
        return ({
            'error': handle_gemini_exception(e)
        })
    # Save and return final output
    finally:
        timer.log()
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


def getResultsStream(
    query: str,
    user_id: int,
    chat_id: int,
    retrieval_mode: RetrievalMode = "hybrid",
    game: GameKey = DEFAULT_GAME,
):
    final_text = ""
    timer = RequestTimer(game=game, mode=retrieval_mode, stream=True)
    try:
        # Chat history
        history = get_chat_history(chat_id=chat_id, user_id=user_id)
        modified_history = history_selection(history)
        timer.lap("history")

        # Context
        context = build_context(query=query, mode=retrieval_mode, game=game)
        modified_context = chunk_selection(context)
        timer.lap("retrieval")

        prompt = render_gemini_prompt(
            query=query,
            context=modified_context,
            history=modified_history,
            game_name=get_game(game).name,
        )
        tool_config = get_tool_config(game)

        stream = get_gemini_client().models.generate_content_stream(
            model=settings.gemini_model,
            contents=prompt,
            config=tool_config
        )

        # Collect every part of the model's turn: a tool request can be split across
        # chunks, and several tools can be requested at once.
        turn_parts = []
        wants_tools = False

        for chunk in stream:
            content = chunk.candidates[0].content if chunk.candidates else None
            if content and content.parts:
                turn_parts.extend(content.parts)

            if chunk.function_calls:
                wants_tools = True

            # Stream text live until the model asks for a tool
            if not wants_tools and chunk.text:
                timer.since_start("first_token")
                final_text += chunk.text
                yield chunk.text

        if wants_tools:
            # Tool rounds run non-streamed; the final answer is sent in one piece
            tool_text = run_tools(
                types.Content(role="model", parts=turn_parts),
                modified_history,
                prompt,
                get_gemini_client(),
                tool_config,
                stats=timer.fields,
            )
            if tool_text:
                timer.since_start("first_token")
                final_text += tool_text
                yield tool_text
        timer.lap("llm")

        logger.info("Gemini stream completed with %d characters", len(final_text))

    except Exception as e:
        # Headers are already sent, so the error must be streamed as text.
        # (A `return` inside a generator just ends the stream silently.)
        logger.exception("Streaming query failed for chat_id=%s", chat_id)
        timer.fields["status"] = "error"
        error = handle_gemini_exception(e)
        yield ("\n\n" if final_text else "") + error["message"]

    finally:
        timer.log()
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
