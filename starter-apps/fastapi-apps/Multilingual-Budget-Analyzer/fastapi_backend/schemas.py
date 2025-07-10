from datetime import datetime
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Dict, List, Any


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    preferred_language: Optional[str] = "en"
    currency: Optional[str] = "USD"


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: str
    email: EmailStr
    preferred_language: str
    currency: str
    created_at: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str = Field(default="bearer")


class TransactionCreate(BaseModel):
    amount: float
    currency: str = "USD"
    description: Optional[str] = None
    category: Optional[str] = None
    date: Optional[datetime] = None


class TransactionOut(BaseModel):
    id: str
    amount: float
    currency: str
    description: Optional[str]
    category: Optional[str]
    date: datetime
    created_at: datetime

    class Config:
        from_attributes = True


# --------- Conversation Models ---------


class ConversationMessage(BaseModel):
    id: str
    role: str  # 'user' or 'assistant'
    content: str
    timestamp: datetime
    message_metadata: Optional[Dict[str, Any]] = None

    class Config:
        from_attributes = True


class ConversationDocument(BaseModel):
    id: str
    file_name: str
    file_type: str
    file_size: float
    analysis_result: Optional[Dict[str, Any]] = None
    uploaded_at: datetime

    class Config:
        from_attributes = True


class ConversationOut(BaseModel):
    id: str
    title: Optional[str] = None
    language: str
    created_at: datetime
    updated_at: datetime
    messages: List[ConversationMessage] = []
    documents: List[ConversationDocument] = []

    class Config:
        from_attributes = True


# --------- AI Advice ---------


class AdviceRequest(BaseModel):
    message: str
    language: Optional[str] = None  # Auto-detect language if None
    conversation_id: Optional[str] = None  # For context continuity


class AdviceResponse(BaseModel):
    answer: str
    conversation_id: str  # Return conversation ID for context


# --------- Enhanced Document Upload ---------


class DocumentUploadRequest(BaseModel):
    conversation_id: Optional[str] = None  # For context continuity


class DocumentAnalysis(BaseModel):
    file_type: str
    analysis_type: str
    summary: str
    text_content: str
    # Optional fields that may be present depending on file type
    page_count: Optional[int] = None
    word_count: Optional[int] = None
    char_count: Optional[int] = None
    sheet_count: Optional[int] = None
    total_rows: Optional[int] = None
    total_columns: Optional[int] = None
    rows: Optional[int] = None
    columns: Optional[int] = None
    column_names: Optional[List[str]] = None
    data_types: Optional[Dict[str, str]] = None
    numeric_columns: Optional[List[str]] = None
    text_columns: Optional[List[str]] = None
    potential_financial_columns: Optional[List[str]] = None
    image_size: Optional[List[int]] = None
    sheets: Optional[Dict[str, Any]] = None
    tables: Optional[List[List[str]]] = None


class DocumentUploadResponse(BaseModel):
    file_path: str
    file_type: str
    file_size: int
    analysis: DocumentAnalysis
    ai_advice: str
    insights: List[str]
    conversation_id: str  # Return conversation ID for context


class DocumentSummaryResponse(BaseModel):
    supported_file_types: List[str]
    max_file_size: str
    features: List[str] 