import podite

from .sighash import sighash
from ..utils import snake_to_pascal


class AccountDiscriminant(podite.Variant):
    def assign_value(self, cls, prev_value):
        self.value = sighash("account", snake_to_pascal(self.name.lower()))


class InstructionDiscriminant(podite.Variant):
    def assign_value(self, cls, prev_value):
        self.value = sighash("global", self.name.lower())
