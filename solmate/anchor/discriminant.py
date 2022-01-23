import pod

from .sighash import sighash


class Variant(pod.Variant):
    def assign_value(self, cls, prev_value):
        # TODO consider making global customizable
        self.value = sighash("global", self.name.lower())


class Discriminant(pod.Enum):
    @classmethod
    def get_tag_type(cls):
        return pod.U64
