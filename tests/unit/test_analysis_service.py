from datetime import datetime, timezone

from app.models.heart_rate import HeartRate
from app.models.steps import Steps
from app.services.analysis_service import analyze_vitals


def test_analyze_vitals_generates_expected_alerts():
    now = datetime.now(timezone.utc)
    hr = [HeartRate(patient_id="p1", value=130, timestamp=now)]
    steps = [Steps(patient_id="p1", total=100, date=now)]

    alerts = analyze_vitals(hr, steps)
    codes = {a.code for a in alerts}
    assert "tachycardia" in codes
    assert "low_activity" in codes
