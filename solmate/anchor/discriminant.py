import pod

from .sighash import sighash


class Discriminant(pod.Variant):
    def assign_value(self, cls, prev_value):
        # TODO consider making "global" customizable
        self.value = sighash("global", self.name.lower())
