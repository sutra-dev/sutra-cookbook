import os
import logging
from pathlib import Path
from typing import Optional, List
from datetime import datetime

from fastapi import APIRouter, Depends, File, UploadFile, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from ..auth import get_current_user
from .. import models, schemas
from ..database import get_db
from ..utils.file_handler import save_upload_file
from ..services.document_processor import DocumentAnalyzer
from ..services.ai_service import AIFinancialAdvisor

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

UPLOAD_DIR = Path("uploads")
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB

router = APIRouter(prefix="/ai", tags=["ai"])


async def get_or_create_conversation(db: AsyncSession, user_id: str, conversation_id: Optional[str] = None) -> models.Conversation:
    """Get existing conversation or create a new one."""
    if conversation_id:
        # Try to get existing conversation
        stmt = select(models.Conversation).where(
            models.Conversation.id == conversation_id,
            models.Conversation.user_id == user_id
        ).options(
            selectinload(models.Conversation.messages),
            selectinload(models.Conversation.documents)
        )
        result = await db.execute(stmt)
        conversation = result.scalar_one_or_none()
        
        if conversation:
            return conversation
        else:
            raise HTTPException(status_code=404, detail="Conversation not found")
    else:
        # Create new conversation
        conversation = models.Conversation(
            user_id=user_id,
            language="en"  # Will be updated when first message is processed
        )
        db.add(conversation)
        await db.commit()
        await db.refresh(conversation)
        return conversation


async def get_conversation_context(db: AsyncSession, conversation: models.Conversation) -> tuple[List[dict], List[dict]]:
    """Get conversation history and document context."""
    # Get conversation messages
    messages_stmt = select(models.ConversationMessage).where(
        models.ConversationMessage.conversation_id == conversation.id
    ).order_by(models.ConversationMessage.timestamp.asc())
    
    messages_result = await db.execute(messages_stmt)
    messages = messages_result.scalars().all()
    
    conversation_context = []
    for msg in messages:
        conversation_context.append({
            'role': msg.role,
            'content': msg.content,
            'timestamp': msg.timestamp
        })
    
    # Get document context
    docs_stmt = select(models.ConversationDocument).where(
        models.ConversationDocument.conversation_id == conversation.id
    ).order_by(models.ConversationDocument.uploaded_at.asc())
    
    docs_result = await db.execute(docs_stmt)
    documents = docs_result.scalars().all()
    
    document_context = []
    for doc in documents:
        document_context.append({
            'file_name': doc.file_name,
            'file_type': doc.file_type,
            'analysis_result': doc.analysis_result
        })
    
    return conversation_context, document_context


@router.get("/document-info", response_model=schemas.DocumentSummaryResponse)
async def get_document_info():
    """Get information about supported document types and features."""
    return schemas.DocumentSummaryResponse(
        supported_file_types=[
            "PDF (.pdf)",
            "Word Documents (.doc, .docx)",
            "Excel Spreadsheets (.xlsx, .xls)",
            "CSV Files (.csv)",
            "Images (.png, .jpg, .jpeg, .bmp, .tiff)"
        ],
        max_file_size="50MB",
        features=[
            "Text extraction from PDFs and Word documents",
            "OCR text extraction from images",
            "Data analysis for Excel and CSV files",
            "Financial column detection in spreadsheets",
            "Statistical analysis of numeric data",
            "Multilingual AI analysis and advice",
            "Structured data insights",
            "Conversation context preservation"
        ]
    )


@router.post(
    "/upload-document",
    response_model=schemas.DocumentUploadResponse,
    status_code=status.HTTP_201_CREATED,
)
async def upload_document(
    file: UploadFile = File(...),
    conversation_id: Optional[str] = None,
    current_user: models.User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Upload and analyze a financial document."""
    logger.info(f"Starting document upload for file: {file.filename}")
    
    # Check if SUTRA_API_KEY is set
    if not os.getenv("SUTRA_API_KEY"):
        logger.error("SUTRA_API_KEY environment variable not set")
        raise HTTPException(
            status_code=500,
            detail="API configuration error. Please set SUTRA_API_KEY environment variable."
        )
    
    # Check file size
    if file.size and file.size > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail=f"File size exceeds maximum limit of {MAX_FILE_SIZE // (1024*1024)}MB"
        )
    
    # Check file type
    if not file.filename:
        raise HTTPException(status_code=400, detail="No filename provided")
    
    file_extension = Path(file.filename).suffix.lower()
    supported_extensions = {'.pdf', '.doc', '.docx', '.xlsx', '.xls', '.csv', '.png', '.jpg', '.jpeg', '.bmp', '.tiff'}
    
    if file_extension not in supported_extensions:
        raise HTTPException(
            status_code=400, 
            detail=f"Unsupported file type: {file_extension}. Supported types: {', '.join(supported_extensions)}"
        )
    
    try:
        # Get or create conversation
        conversation = await get_or_create_conversation(db, current_user.id, conversation_id)
        
        # Get conversation context
        conversation_context, document_context = await get_conversation_context(db, conversation)
        
        # Save the uploaded file
        logger.info(f"Saving file to: {UPLOAD_DIR}")
        saved_path = await save_upload_file(file, UPLOAD_DIR)
        logger.info(f"File saved to: {saved_path}")
        
        # Analyze the document
        logger.info("Starting document analysis")
        analyzer = DocumentAnalyzer()
        analysis_result = await analyzer.analyze_document(saved_path)
        logger.info(f"Document analysis completed: {analysis_result.get('file_type', 'Unknown')}")
        
        # Generate AI advice based on document type and content with conversation context
        logger.info("Generating AI advice")
        advisor = AIFinancialAdvisor()
        ai_advice = await advisor.get_financial_document_advice(
            analysis_result, 
            file_type=analysis_result.get('file_type', 'Unknown'),
            conversation_context=conversation_context
        )
        logger.info("AI advice generated successfully")
        
        # Generate insights based on the analysis
        logger.info("Generating document insights")
        insights = await advisor.generate_document_insights(analysis_result)
        logger.info(f"Generated {len(insights)} insights")
        
        # Get file size
        file_size = os.path.getsize(saved_path)
        
        # Store document in conversation
        conversation_doc = models.ConversationDocument(
            conversation_id=conversation.id,
            file_name=file.filename,
            file_path=str(saved_path),
            file_type=analysis_result.get('file_type', 'Unknown'),
            file_size=file_size,
            analysis_result=analysis_result
        )
        db.add(conversation_doc)
        
        # Store user message (file upload)
        user_message = models.ConversationMessage(
            conversation_id=conversation.id,
            role="user",
            content=f"Uploaded document: {file.filename}",
            message_metadata={"file_id": conversation_doc.id, "file_type": analysis_result.get('file_type', 'Unknown')}
        )
        db.add(user_message)
        
        # Store assistant response
        assistant_message = models.ConversationMessage(
            conversation_id=conversation.id,
            role="assistant",
            content=ai_advice,
            message_metadata={"insights": insights}
        )
        db.add(assistant_message)
        
        # Update conversation language if detected
        if analysis_result.get('text_content'):
            detected_language = await advisor.detect_language(analysis_result.get('text_content', ''))
            conversation.language = detected_language
        
        conversation.updated_at = datetime.utcnow()
        
        await db.commit()
        
        # Create DocumentAnalysis object
        document_analysis = schemas.DocumentAnalysis(
            file_type=analysis_result.get('file_type', 'Unknown'),
            analysis_type=analysis_result.get('analysis_type', 'general'),
            summary=analysis_result.get('summary', ''),
            text_content=analysis_result.get('text_content', ''),
            page_count=analysis_result.get('page_count'),
            word_count=analysis_result.get('word_count'),
            char_count=analysis_result.get('char_count'),
            sheet_count=analysis_result.get('sheet_count'),
            total_rows=analysis_result.get('total_rows'),
            total_columns=analysis_result.get('total_columns'),
            rows=analysis_result.get('rows'),
            columns=analysis_result.get('columns'),
            column_names=analysis_result.get('column_names'),
            data_types=analysis_result.get('data_types'),
            numeric_columns=analysis_result.get('numeric_columns'),
            text_columns=analysis_result.get('text_columns'),
            potential_financial_columns=analysis_result.get('potential_financial_columns'),
            image_size=analysis_result.get('image_size'),
            sheets=analysis_result.get('sheets'),
            tables=analysis_result.get('tables')
        )
        
        logger.info("Document upload and analysis completed successfully")
        
        return schemas.DocumentUploadResponse(
            file_path=str(saved_path),
            file_type=analysis_result.get('file_type', 'Unknown'),
            file_size=file_size,
            analysis=document_analysis,
            ai_advice=ai_advice,
            insights=insights,
            conversation_id=conversation.id
        )
        
    except Exception as exc:
        logger.error(f"Document analysis failed: {str(exc)}", exc_info=True)
        # Clean up file if analysis failed
        if 'saved_path' in locals() and saved_path.exists():
            saved_path.unlink()
        raise HTTPException(status_code=400, detail=f"Document analysis failed: {str(exc)}")


@router.post("/get-advice", response_model=schemas.AdviceResponse)
async def get_advice(
    payload: schemas.AdviceRequest,
    current_user: models.User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get financial advice from AI with conversation context."""
    # Check if SUTRA_API_KEY is set
    if not os.getenv("SUTRA_API_KEY"):
        raise HTTPException(
            status_code=500,
            detail="API configuration error. Please set SUTRA_API_KEY environment variable."
        )
    
    try:
        # Get or create conversation
        conversation = await get_or_create_conversation(db, current_user.id, payload.conversation_id)
        
        # Get conversation context
        conversation_context, document_context = await get_conversation_context(db, conversation)
        
        # Get AI advice with context
        advisor = AIFinancialAdvisor()
        answer = await advisor.get_advice(
            payload.message, 
            language=payload.language,
            conversation_context=conversation_context,
            document_context=document_context
        )
        
        # Store user message
        user_message = models.ConversationMessage(
            conversation_id=conversation.id,
            role="user",
            content=payload.message
        )
        db.add(user_message)
        
        # Store assistant response
        assistant_message = models.ConversationMessage(
            conversation_id=conversation.id,
            role="assistant",
            content=answer
        )
        db.add(assistant_message)
        
        # Update conversation language if detected
        if not payload.language:
            detected_language = await advisor.detect_language(payload.message)
            conversation.language = detected_language
        else:
            conversation.language = payload.language
        
        conversation.updated_at = datetime.utcnow()
        
        await db.commit()
        
        return schemas.AdviceResponse(answer=answer, conversation_id=conversation.id)
        
    except Exception as exc:
        logger.error(f"Get advice failed: {str(exc)}", exc_info=True)
        raise HTTPException(status_code=400, detail=f"Failed to get advice: {str(exc)}")


@router.get("/conversations", response_model=List[schemas.ConversationOut])
async def get_conversations(
    current_user: models.User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get all conversations for the current user."""
    stmt = select(models.Conversation).where(
        models.Conversation.user_id == current_user.id
    ).options(
        selectinload(models.Conversation.messages),
        selectinload(models.Conversation.documents)
    ).order_by(models.Conversation.updated_at.desc())
    
    result = await db.execute(stmt)
    conversations = result.scalars().all()
    
    return conversations


@router.get("/conversations/{conversation_id}", response_model=schemas.ConversationOut)
async def get_conversation(
    conversation_id: str,
    current_user: models.User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get a specific conversation by ID."""
    stmt = select(models.Conversation).where(
        models.Conversation.id == conversation_id,
        models.Conversation.user_id == current_user.id
    ).options(
        selectinload(models.Conversation.messages),
        selectinload(models.Conversation.documents)
    )
    
    result = await db.execute(stmt)
    conversation = result.scalar_one_or_none()
    
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    return conversation 