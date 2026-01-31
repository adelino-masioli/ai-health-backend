"""Validation rules for health data (aligned with frontend)."""

HEART_RATE_MIN = 30
HEART_RATE_MAX = 220
STEPS_MIN = 0
STEPS_MAX = 100_000


def is_valid_heart_rate(value: int) -> bool:
    """Check if heart rate is within physiological range (30-220 bpm)."""
    return HEART_RATE_MIN <= value <= HEART_RATE_MAX


def is_valid_steps(total: int) -> bool:
    """Check if steps count is within reasonable range (0-100000)."""
    return STEPS_MIN <= total <= STEPS_MAX


def validate_heart_rate(value: int) -> str | None:
    """
    Validate heart rate. Returns None if valid, otherwise error message.
    """
    if not isinstance(value, int):
        return "Heart rate must be an integer."
    if value < HEART_RATE_MIN:
        return f"Heart rate must be at least {HEART_RATE_MIN} bpm."
    if value > HEART_RATE_MAX:
        return f"Heart rate must be at most {HEART_RATE_MAX} bpm."
    return None


def validate_steps(total: int) -> str | None:
    """
    Validate steps. Returns None if valid, otherwise error message.
    """
    if not isinstance(total, int):
        return "Steps must be an integer."
    if total < STEPS_MIN:
        return f"Steps must be at least {STEPS_MIN}."
    if total > STEPS_MAX:
        return f"Steps must be at most {STEPS_MAX}."
    return None
