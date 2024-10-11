from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    password: str
    email: str
    age: int

class SurveyCreate(BaseModel):
    user_id: int
    income: int
    needs: str
    learning_interests: str

class ContentCreate(BaseModel):
    title: str
    keyword: str
    description: str

class LearningPathCreate(BaseModel):
    user_id: int
    content_id: int
    progress: int
    needs_covered: str
    knowledge_covered: str

class DashboardCreate(BaseModel):
    user_id: int
    learning_path_id: int
    progress: int

class ChatMessage(BaseModel):
    sender_id: int
    content: str
    timestamp: str

class ProductCreate(BaseModel):
    name: str
    description: str