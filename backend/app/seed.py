from sqlalchemy.orm import Session

from . import models
from .llm_orchestrator import generate_diagnostic_payload
from .schemas import IncidentCreate, SymptomFlags


def seed_data(db: Session):
    if db.query(models.Equipment).count() > 0:
        return

    equipment_items = [
        models.Equipment(
            name="Bomba P-101",
            type="Bomba centrífuga",
            sector="Utilidades",
            manufacturer="WEG",
            model="CPX-400",
            criticality="alta",
            status="operando com restrição",
        ),
        models.Equipment(
            name="Motor M-204",
            type="Motor elétrico",
            sector="Mistura",
            manufacturer="Siemens",
            model="HT-315",
            criticality="média",
            status="operacional",
        ),
        models.Equipment(
            name="Compressor C-88",
            type="Compressor rotativo",
            sector="Ar comprimido",
            manufacturer="Atlas Copco",
            model="GA-75",
            criticality="alta",
            status="em observação",
        ),
    ]
    db.add_all(equipment_items)
    db.flush()

    incident_payload = IncidentCreate(
        equipment_id=equipment_items[0].id,
        main_symptom="Vibração crescente com aquecimento",
        description="Operador relatou aumento de vibração nas últimas 6 horas e temperatura acima do padrão.",
        shift="manhã",
        perceived_urgency="alta",
        symptoms=SymptomFlags(vibration=True, overheating=True, performance_loss=True),
    )
    incident = models.Incident(
        equipment_id=incident_payload.equipment_id,
        main_symptom=incident_payload.main_symptom,
        description=incident_payload.description,
        shift=incident_payload.shift,
        perceived_urgency=incident_payload.perceived_urgency,
        status="open",
        abnormal_noise=0,
        vibration=1,
        overheating=1,
        leakage=0,
        electrical_failure=0,
        total_stop=0,
        performance_loss=1,
    )
    db.add(incident)
    db.flush()

    diagnostic = models.Diagnostic(
        incident_id=incident.id,
        **generate_diagnostic_payload(equipment_items[0], incident_payload),
    )
    db.add(diagnostic)
    db.commit()
