"""Domain service for health anomaly analysis."""

from app.models.heart_rate import HeartRate
from app.models.steps import Steps
from app.schemas.analysis import AlertItem


def analyze_vitals(heart_rates: list[HeartRate], steps: list[Steps]) -> list[AlertItem]:
    """Generate patient alerts from heart rate and steps signals."""
    alerts: list[AlertItem] = []
    emitted_codes: set[str] = set()

    def add_alert(code: str, severity: str, message: str, evidence: dict) -> None:
        if code in emitted_codes:
            return
        emitted_codes.add(code)
        alerts.append(
            AlertItem(code=code, severity=severity, message=message, evidence=evidence)
        )

    if heart_rates:
        max_hr = max(hr.value for hr in heart_rates)
        min_hr = min(hr.value for hr in heart_rates)
        if max_hr > 120:
            add_alert(
                code="tachycardia",
                severity="high",
                message="Heart rate is above 120 bpm.",
                evidence={"max_heart_rate": max_hr},
            )
        if min_hr < 45:
            add_alert(
                code="bradycardia",
                severity="high",
                message="Heart rate is below 45 bpm.",
                evidence={"min_heart_rate": min_hr},
            )

    if steps:
        total_steps = sum(item.total for item in steps)
        if total_steps < 500:
            add_alert(
                code="low_activity",
                severity="medium",
                message="Low activity detected in the selected time window.",
                evidence={"total_steps": total_steps},
            )

    return alerts
