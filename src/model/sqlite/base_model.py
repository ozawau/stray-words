class BaseModel:
    """所有模型类的基类"""
    def __init__(self):
        self.id = None

    def to_dict(self):
        """将模型转换为字典"""
        return {k: v for k, v in self.__dict__.items() 
                if not k.startswith('_')}

    @classmethod
    def from_dict(cls, data: dict):
        """从字典创建模型实例"""
        instance = cls()
        for key, value in data.items():
            if hasattr(instance, key):
                setattr(instance, key, value)
        return instance