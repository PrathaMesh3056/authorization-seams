from enum import StrEnum
from pydantic import BaseModel, ConfigDict, Field, JsonValue


class Model(BaseModel):
    model_config = ConfigDict(extra='forbid', validate_assignment=True)


class ValueType(StrEnum):
    STRING = 'string'
    INTEGER = 'integer'
    NUMBER = 'number'
    BOOLEAN = 'boolean'
    OBJECT = 'object'
    ARRAY = 'array'


class ArgSpec(Model):
    type: ValueType
    role: str = Field(pattern='^(authority|payload)$')
    required: bool = True


class ToolSchema(Model):
    kind: str = Field(pattern='^(query|effect)$')
    args: dict[str, ArgSpec]
    result_fields: dict[str, ValueType] = Field(default_factory=dict)
    # Structured fields exposed for elements of an array result.
    item_fields: dict[str, dict[str, ValueType]] = Field(default_factory=dict)


class Registry(Model):
    tools: dict[str, ToolSchema]


class Constraint(Model):
    type: ValueType
    equals: JsonValue = None
    has_equals: bool = False
    choices: list[JsonValue] | None = None
    minimum: float | None = None
    maximum: float | None = None


class Permission(Model):
    budget: int = Field(ge=0)
    allowed_args: list[str]
    constraints: dict[str, Constraint] = Field(default_factory=dict)
    # Exact payload values explicitly supported by the trusted request.
    trusted_payloads: dict[str, JsonValue] = Field(default_factory=dict)


class EvidenceRule(Model):
    query_args: dict[str, JsonValue]
    fields: dict[str, Constraint]
    integrity: dict[str, JsonValue] = Field(default_factory=dict)


class Obligation(Model):
    id: str = Field(min_length=1)
    kind: str = Field(pattern='^(evidence|effect|output)$')
    tool: str | None = None
    dependencies: list[str] = Field(default_factory=list)
    hard: bool = True
    enabled: bool = True
    evidence: EvidenceRule | None = None
    output_equals: JsonValue = None
    waiver_code: str | None = None


class Selector(Model):
    collection: str
    where: dict[str, JsonValue]
    allowed_fields: list[str]


class Binding(Model):
    source: str = Field(pattern='^(constant|evidence)$')
    constant: JsonValue = None
    evidence_obligation: str | None = None
    field: str | None = None
    derivation: str = Field(default='copy', pattern='^(copy|to_integer|affine)$')
    multiplier: int = 1
    offset: int = 0
    selector: Selector | None = None
    constraints: Constraint


class Verification(Model):
    # Native result fields must be observable in the frozen schema.
    postconditions: dict[str, JsonValue]


class Contract(Model):
    id: str
    trusted_request: str
    MAY: dict[str, Permission]
    MUST: list[Obligation]
    BIND: dict[str, dict[str, Binding]]
    VERIFY: dict[str, Verification]


class ObligationState(StrEnum):
    PENDING = 'PENDING'
    ACTIVE = 'ACTIVE'
    VERIFIED = 'VERIFIED'
    WAIVED = 'WAIVED'


class DecisionCode(StrEnum):
    STEP_UP_AUTH = 'STEP_UP_AUTH'
    ALLOW = 'ALLOW'
    PROOF_GAP = 'PROOF-GAP'
    DENY = 'DENY'


class CallRequest(Model):
    tool: str
    arguments: dict[str, JsonValue]
    obligation: str | None = None
    # Supplied by a protected provenance adapter, never by the untrusted planner.
    tainted_payloads: list[str] = Field(default_factory=list)


class EvidenceRecord(Model):
    id: str
    obligation: str
    tool: str
    query_args: dict[str, JsonValue]
    data: dict[str, JsonValue]


class ArgumentProof(Model):
    argument: str
    value: JsonValue
    binding_digest: str
    evidence_id: str | None = None
    evidence_digest: str | None = None
    candidate_set_digest: str | None = None
    selector_digest: str | None = None
    selected_record_digest: str | None = None


class EffectCertificate(Model):
    nonce: str
    contract_digest: str
    registry_digest: str
    session: str
    binding_mode: str
    obligation: str
    tool: str
    canonical_arguments: str
    proofs: dict[str, ArgumentProof]
    budget: int
    issued_at: int
    expires_at: int
    mac: str = ''


class CertificateEntry(Model):
    certificate: EffectCertificate
    lifecycle: str = Field(default='ISSUED', pattern='^(ISSUED|CONSUMED)$')
    dispatched_at: int | None = None
    receipt_processed: bool = False


class NativeResult(Model):
    certificate_nonce: str
    tool: str
    arguments: dict[str, JsonValue]
    success: bool
    result: dict[str, JsonValue]


class EffectReceipt(Model):
    certificate_nonce: str
    obligation: str
    native_result_digest: str


class Ledger(Model):
    E: dict[str, EvidenceRecord] = Field(default_factory=dict)
    S: dict[str, ObligationState]
    B: dict[str, int]
    K: dict[str, CertificateEntry] = Field(default_factory=dict)
    receipts: dict[str, EffectReceipt] = Field(default_factory=dict)
    waivers: dict[str, str] = Field(default_factory=dict)
    outputs: dict[str, JsonValue] = Field(default_factory=dict)


class RuntimeState(Model):
    contract: Contract
    registry: Registry
    contract_digest: str
    registry_digest: str
    session: str
    binding_mode: str = Field(default='complete', pattern='^(complete|diagnostic_coverage_gap)$')
    ledger: Ledger


class Decision(Model):
    code: DecisionCode
    checks: dict[str, bool]
    missing: list[str] = Field(default_factory=list)
    obligation: str | None = None
    proofs: dict[str, ArgumentProof] = Field(default_factory=dict)


class StaticResult(Model):
    accepted: bool
    failed_predicate: str | None = None
    reasons: list[str] = Field(default_factory=list)
    checks: dict[str, bool] = Field(default_factory=dict)
    normalized: Contract | None = None
