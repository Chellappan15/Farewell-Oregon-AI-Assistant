class ChatNotFoundError(Exception):
    """Raised when a chat does not exist or does not belong to the user."""

    def __init__(self, chat_id: int):
        super().__init__(f"Chat {chat_id} not found")
        self.chat_id = chat_id
