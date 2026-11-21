from google.genai.errors import ClientError

def handle_gemini_exception(exc):
    message = str(exc).lower()

    if isinstance(exc, ClientError) and (
        "unauthenticated" in message
        or "api key" in message
        or "permission denied" in message
    ):
        return {
            "code": "SERVICE_CONFIGURATION_ERROR",
            "message": "Our AI service is temporarily unavailable. Please try again in a few minutes."
        }

    if isinstance(exc, ClientError) and "quota" in message:
        return {
            "code": "SERVICE_CAPACITY_EXCEEDED",
            "message": "The service is currently experiencing high demand. Please try again shortly."
        }

    if isinstance(exc, ClientError) and (
        "resource_exhausted" in message
        or "rate limit" in message
    ):
        return {
            "code": "RATE_LIMITED",
            "message": "Too many requests are being processed at the moment. Please wait a moment and try again."
        }

    if isinstance(exc, ClientError) and "model not found" in message:
        return {
            "code": "MODEL_UNAVAILABLE",
            "message": "The AI service is temporarily unavailable. Please try again later."
        }

    if isinstance(exc, ConnectionError):
        return {
            "code": "NETWORK_ERROR",
            "message": "We couldn't reach the AI service. Please try again."
        }

    if isinstance(exc, TimeoutError):
        return {
            "code": "REQUEST_TIMEOUT",
            "message": "The request is taking longer than expected. Please try again."
        }

    if isinstance(exc, (ValueError, TypeError)):
        return {
            "code": "INVALID_REQUEST",
            "message": "We couldn't process the request. Please rephrase your question and try again."
        }

    return {
        "code": "UNEXPECTED_ERROR",
        "message": "Something went wrong while processing your request. Please try again."
    }