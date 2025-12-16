from app.strategies.base import BaseRoleStrategy

class DevToPMStrategy(BaseRoleStrategy):
    @property
    def system_prompt(self) -> str:
        return """
        你是一位懂技术的资深产品总监。
        你的任务是将枯燥的“技术方案”翻译成产品经理关注的“商业价值”。
        请务必包含以下四个维度的业务价值：
        1. 用户体验提升 (User Experience)
        2. 商业增长空间 (Business Growth)
        3. 成本与效率优化 (Cost & Efficiency)
        4. 迭代建议 (Next Steps)
        """

    def build_user_prompt(self, content: str) -> str:
        return f"【技术变更描述】：\n{content}\n\n请转化为业务价值说明："
