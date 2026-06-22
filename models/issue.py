from pydantic import BaseModel, Field, HttpUrl

class IssueCreateResponse(BaseModel):
    """Модель для валидации ответа после создания задачи (POST)"""
    id: str
    key: str  # Например: "KAN-1"k
    self_url: HttpUrl = Field(..., alias="self")

class IssueStatus(BaseModel):
    name: str

class IssueFields(BaseModel):
    summary: str
    status: IssueStatus

class IssueGetResponse(BaseModel):
    """Модель для валидации полной информации о задаче (GET)"""
    id: str
    key: str
    fields: IssueFields