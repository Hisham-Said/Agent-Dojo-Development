class BaseAttack:
    name = "base_attack"

    def apply(self, content):
        """Modify untrusted content for an attack scenario."""
        raise NotImplementedError