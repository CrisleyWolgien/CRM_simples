from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

class service(SQLModel, table=True):
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True) # identificador único do serviço (auto-gerado)
    name: str  # nome do serviço
    description: Optional[str] = None  # descrição do serviço
    price: float  # preço do serviço
    duration: int  # duração do serviço em minutos
    created_at: datetime = Field(default_factory=datetime.now)  # data de criação do serviço (auto-gerada)
    payment_status: Optional[str] = None  # status do pagamento (pago, pendente, cancelado)

    def __repr__(self):
        return f"Service(id={self.id}, name={self.name}, description={self.description}, price={self.price}, duration={self.duration}, created_at={self.created_at}, payment_status={self.payment_status})"