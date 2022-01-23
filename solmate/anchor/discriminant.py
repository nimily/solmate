import pod


class Variant(pod.Variant):
    def assign_value(self):
        self.value = hash(self.name.lower())


class Discriminant(pod.Enum):
    @classmethod
    def get_tag_type(cls):
        return pod.U64
