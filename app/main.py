from abc import ABC, abstractmethod


class IntegerRange:
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __set_name__(self, owner: type, name: int | str) -> None:
        self.private_name = "_" + name

    def __get__(self, instance: object, owner: type) -> None:
        return getattr(instance, self.private_name)

    def __set__(self, instance: object, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError(f"{self.private_name} must be an integer")
        if not (self.min_amount <= value <= self.max_amount):
            raise (ValueError
                   (f"{self.private_name} "
                    f"must be between "
                    f"{self.min_amount} and {self.max_amount}"))
        setattr(instance, self.private_name, value)


class Visitor:
    def __init__(self, name: str, age: int,
                 weight: int, height: int) -> None:
        self.name = name
        self.age = age
        self.weight = weight
        self.height = height


class SlideLimitationValidator(ABC):
    def __init__(self, age: int,
                 weight: int, height: int) -> None:
        self.age = age
        self.weight = weight
        self.height = height

    @abstractmethod
    def validate(self, visitor: object) -> None:
        pass


class ChildrenSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRange(4, 14)
    height = IntegerRange(80, 120)
    weight = IntegerRange(20, 50)

    def validate(self, visitor: int) -> None:
        self.age = visitor.age
        self.height = visitor.height
        self.weight = visitor.weight


class AdultSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRange(14, 60)
    height = IntegerRange(120, 220)
    weight = IntegerRange(50, 120)

    def validate(self, visitor: int) -> None:
        self.age = visitor.age
        self.height = visitor.height
        self.weight = visitor.weight


class Slide:
    def __init__(self, name: str, limitation_class: type) -> None:
        self.name = name
        self.limitation_class = limitation_class

    def can_access(self, visitor: Visitor) -> bool:
        try:
            limitations = (self.limitation_class
                           (visitor.age, visitor.weight, visitor.height))
            limitations.validate(visitor)
            return True
        except (TypeError, ValueError):
            return False
