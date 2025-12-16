from app.strategies.pm_role import PMToDevStrategy
from app.strategies.dev_role import DevToPMStrategy

class RoleFactory:
    _strategies = {
        "p2d": PMToDevStrategy(),
        "d2p": DevToPMStrategy()
    }

    @classmethod
    def get_strategy(cls, role_type: str):
        if role_type not in cls._strategies:
            raise ValueError(f"Unknown role type: {role_type}")
        return cls._strategies[role_type]
