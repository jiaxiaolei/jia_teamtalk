
from app.strategies.base import BaseRoleStrategy

class PMToDevStrategy(BaseRoleStrategy):
    @property
    def system_prompt(self) -> str:
        return """
        你是一位拥有15年经验的技术架构师。
        你的任务是将产品经理的“业务需求”翻译成开发工程师能理解的“技术规范”。
        请务必包含以下四个维度的技术细节：
        1. 核心技术拆解 (Architecture)
        2. 算法与数据流 (Algorithms & Data)
        3. 性能与工作量预估 (Performance & Effort)
        4. 潜在技术风险 (Risks)
        """

    def build_user_prompt(self, content: str) -> str:
        return f"【产品需求描述】：\n{content}\n\n请转化为技术规范文档："


