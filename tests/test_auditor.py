from pydantic import BaseModel
from enum import Enum
import pytest

class RiskAssessment(str, Enum):
    Low = "Low"
    Medium = "Medium"
    High = "High"

class PURAudit(BaseModel):
    project_title: str
    trl_level: int
    methodology_summary: str
    risk_assessment: RiskAssessment
    compliance_score: int

def test_pur_audit_model():
    audit = PURAudit(
        project_title="Sample Project",
        trl_level=5,
        methodology_summary="This project uses advanced methodologies.",
        risk_assessment=RiskAssessment.Low,
        compliance_score=85
    )
    
    assert audit.project_title == "Sample Project"
    assert audit.trl_level == 5
    assert audit.methodology_summary == "This project uses advanced methodologies."
    assert audit.risk_assessment == RiskAssessment.Low
    assert audit.compliance_score == 85

def test_invalid_trl_level():
    with pytest.raises(ValueError):
        PURAudit(
            project_title="Invalid TRL Project",
            trl_level=10,  # Invalid TRL level
            methodology_summary="Invalid TRL level test.",
            risk_assessment=RiskAssessment.Medium,
            compliance_score=50
        )

def test_invalid_compliance_score():
    with pytest.raises(ValueError):
        PURAudit(
            project_title="Invalid Compliance Project",
            trl_level=3,
            methodology_summary="Invalid compliance score test.",
            risk_assessment=RiskAssessment.High,
            compliance_score=110  # Invalid compliance score
        )