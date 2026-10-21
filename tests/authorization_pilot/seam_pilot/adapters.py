from .model import ARMS, Decision, MockWorld
from .native import APC, Progent


class Adapter:
    """One serialized root task. Authorize is immediately followed by mock execution.

    APC authorizes and commits state in one operation. Progent therefore runs first
    in the retained pipeline; its denial must not consume APC's budget/history.
    """

    def __init__(self, arm: str):
        if arm not in ARMS:
            raise ValueError(arm)
        self.arm = arm
        self.downstream = False

    def initialize(self, case):
        self.case = case
        self.world = MockWorld(case)
        self.apc = None if self.arm == "progent_alone" else APC(case, self.world)
        self.progent = Progent(case, case.resources) if self.arm == "progent_alone" else None
        return self.world

    def handoff(self):
        self.downstream = True
        if self.apc:
            self.apc.handoff(reset=self.arm == "apc_apc_reset",
                             fresh_pdp=self.arm in ("apc_apc_preserved", "apc_apc_reset"))
        if self.arm == "progent_alone":
            self.progent = Progent(self.case, set(self.case.resources) & set(self.case.role_resources))
        elif self.arm.startswith("apc_progent"):
            self.progent = Progent(self.case, self.apc.envelope.effective_scope.resources)

    def authorize(self, call, args):
        if not self.downstream:
            return (self.apc or self.progent).authorize(call, args)
        if self.arm == "apc_progent_fail_closed":
            # All v1 roots require identity/context/freshness/budget/composition.
            # This static JSON-schema profile cannot express those obligations.
            return Decision(False, ["bridge rejects unsupported dynamic root obligations"], checked_by=["bridge"])
        if self.arm == "apc_progent_retained":
            result = self.progent.authorize(call, args)
            if not result.allowed:
                return result
            result = self.apc.authorize(call, args)
            result.checked_by.insert(0, "Progent")
            return result
        if self.arm in ("progent_alone", "apc_progent_scope_only"):
            return self.progent.authorize(call, args)
        return self.apc.authorize(call, args)

    def execute(self, call, args, decision):
        if not decision.allowed:
            return []
        return self.world.execute(call, args)

    def state(self):
        if not self.apc:
            return None
        return {"budget": self.apc.budget.snapshot(), "history": list(self.apc.composition.action_history),
                "envelope_id": self.apc.envelope.envelope_id,
                "evidence_integrity": self.apc.sink.verify_integrity().valid}
