import pod

from .sighash import sighash
from ..utils import snake_to_pascal


class AccountDiscriminant(pod.Variant):
    def assign_value(self, cls, prev_value):
        self.value = sighash("account", snake_to_pascal(self.name.lower()))


class InstructionDiscriminant(pod.Variant):
    def assign_value(self, cls, prev_value):
        self.value = sighash("global", self.name.lower())
