from .schemas import StructuredDiagnosticDraft


def validate_structured_diagnostic(draft: StructuredDiagnosticDraft) -> StructuredDiagnosticDraft:
    if not draft.probable_cause.strip():
        raise ValueError("Structured diagnostic requires a probable cause.")
    if not draft.recommended_actions:
        raise ValueError("Structured diagnostic requires at least one recommended action.")
    if not draft.evidence_summary:
        raise ValueError("Structured diagnostic requires at least one evidence item.")
    return draft
