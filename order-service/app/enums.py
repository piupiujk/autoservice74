import enum

class OrderStatusEnum(enum.StrEnum):
    """Перечисление статусов заказов.

    Args:
        CREATED: Заказ создан
        IN_PROGRESS: Заказ в процессе
        COMPLETED: Заказ выполнен
        CANCELLED: Заказ отменен
    """
    CREATED = "created"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"