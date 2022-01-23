import pod


class Variant(pod.Variant):
    def assign_value(self):
        # FIXME assign_value should use sha256 hash?!
        self.value = hash(self.name.lower())


class Discriminant(pod.Enum):
    @classmethod
    def get_tag_type(cls):
        return pod.U64
