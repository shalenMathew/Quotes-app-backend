class AIQuotePipelineError(Exception):
    """Base exception for AI quote generation failures."""


class GeminiGenerationError(AIQuotePipelineError):
    """Raised when Gemini fails to generate content."""


class InvalidAIResponseError(AIQuotePipelineError):
    """Raised when Gemini returns an invalid or empty parsed response."""


class NoValidQuotesError(AIQuotePipelineError):
    """Raised when no generated quotes pass validation."""


class DatabaseSaveError(AIQuotePipelineError):
    """Raised when saving a generated quote fails."""