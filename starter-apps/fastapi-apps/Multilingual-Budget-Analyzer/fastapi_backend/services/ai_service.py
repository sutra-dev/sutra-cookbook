import os
from typing import cast, Optional, List, Dict, Any

from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, AIMessage, SystemMessage
from pydantic import SecretStr


class AIFinancialAdvisor:
    """Service wrapper around Sutra LLM for financial advice."""

    def __init__(self):
        key_str = os.getenv("SUTRA_API_KEY")
        if not key_str:
            raise ValueError("SUTRA_API_KEY environment variable not set")

        # Pass key via 'openai_api_key' accepted by langchain_openai ChatOpenAI
        self.llm = ChatOpenAI(
            openai_api_key=key_str,  # type: ignore[arg-type]
            base_url="https://api.two.ai/v2",
            model="sutra-v2",
            temperature=0.7,
        )

    async def detect_language(self, text: str) -> str:
        """Detect the language of the input text using Sutra LLM."""
        detection_prompt = f"""
        Detect the language of the following text and respond with only the language code (e.g., 'en' for English, 'es' for Spanish, 'fr' for French, 'de' for German, 'hi' for Hindi, 'ta' for Tamil, 'te' for Telugu, 'ml' for Malayalam, 'kn' for Kannada, etc.).
        
        Text: {text}
        
        Language code:
        """
        
        messages = [HumanMessage(content=detection_prompt)]
        response = await self.llm.ainvoke(messages)
        detected_language = cast(str, response.content).strip().lower()
        
        # Return the detected language code or default to 'en' if detection fails
        return detected_language if detected_language else "en"

    async def get_advice(self, prompt: str, language: Optional[str] = None, conversation_context: Optional[List[Dict[str, Any]]] = None, document_context: Optional[List[Dict[str, Any]]] = None) -> str:
        """Get financial advice with conversation context and document context."""
        
        # If no language is provided, detect it automatically
        if language is None:
            language = await self.detect_language(prompt)
        
        # Build the conversation messages
        messages = []
        
        # Add system message with language and context instructions
        system_content = f"""
        You are a helpful multilingual financial advisor. The user has asked a question in {language}.
        IMPORTANT: You must respond in the exact same language as the user's question.
        
        Language guidelines:
        - If the user writes in English, respond in English
        - If the user writes in Tamil, respond in Tamil
        - If the user writes in Hindi, respond in Hindi
        - If the user writes in Spanish, respond in Spanish
        - If the user writes in French, respond in French
        - If the user writes in German, respond in German
        - If the user writes in any other language, respond in that same language
        
        Always match the user's language exactly and provide helpful financial advice.
        
        """
        
        # Add document context if available
        if document_context:
            system_content += "\n\nIMPORTANT DOCUMENT CONTEXT:\n"
            for doc in document_context:
                system_content += f"\n📄 Document: {doc.get('file_name', 'Unknown')}\n"
                system_content += f"Type: {doc.get('file_type', 'Unknown')}\n"
                if doc.get('analysis_result'):
                    analysis = doc['analysis_result']
                    system_content += f"Summary: {analysis.get('summary', 'No summary available')}\n"
                    if analysis.get('text_content'):
                        # Include first 500 characters of text content
                        text_preview = analysis.get('text_content', '')[:500]
                        system_content += f"Content Preview: {text_preview}...\n"
            system_content += "\nUse this document context to provide more relevant and specific advice.\n"
        
        messages.append(SystemMessage(content=system_content))
        
        # Add conversation history if available
        if conversation_context:
            for msg in conversation_context:
                if msg.get('role') == 'user':
                    messages.append(HumanMessage(content=msg.get('content', '')))
                elif msg.get('role') == 'assistant':
                    messages.append(AIMessage(content=msg.get('content', '')))
        
        # Add current user message
        messages.append(HumanMessage(content=prompt))
        
        response = await self.llm.ainvoke(messages)
        return cast(str, response.content)

    async def get_financial_document_advice(self, analysis_result: Dict[str, Any], file_type: str, conversation_context: Optional[List[Dict[str, Any]]] = None) -> str:
        """Generate financial advice based on document analysis with conversation context."""
        
        # Detect language from the document content
        text_content = analysis_result.get('text_content', '')
        language = await self.detect_language(text_content) if text_content else "en"
        
        # Build conversation messages
        messages = []
        
        # Create context-specific system message
        system_content = f"""
        You are an expert financial advisor analyzing documents. Provide practical, actionable financial advice based on the document analysis.
        
        IMPORTANT: You must respond in {language} language to match the document content.
        
        Focus on:
        - Key financial insights from the document
        - Actionable recommendations
        - Budgeting and expense management advice
        - Investment or savings opportunities
        - Risk assessment if applicable
        
        Provide clear, specific, and practical advice.
        """
        
        # Add conversation context if available
        if conversation_context:
            system_content += "\n\nCONVERSATION CONTEXT:\n"
            system_content += "Consider the previous conversation when providing advice.\n"
        
        messages.append(SystemMessage(content=system_content))
        
        # Add conversation history if available
        if conversation_context:
            for msg in conversation_context:
                if msg.get('role') == 'user':
                    messages.append(HumanMessage(content=msg.get('content', '')))
                elif msg.get('role') == 'assistant':
                    messages.append(AIMessage(content=msg.get('content', '')))
        
        # Create document analysis prompt
        if file_type == "Excel Spreadsheet" or file_type == "CSV File":
            prompt = f"""
            I have analyzed a {file_type} with the following characteristics:
            
            File Summary: {analysis_result.get('summary', '')}
            
            Data Details:
            - Rows: {analysis_result.get('rows', 'N/A')}
            - Columns: {analysis_result.get('columns', 'N/A')}
            - Column Names: {', '.join(analysis_result.get('column_names', []))}
            - Numeric Columns: {', '.join(analysis_result.get('numeric_columns', []))}
            - Potential Financial Columns: {', '.join(analysis_result.get('potential_financial_columns', []))}
            
            Based on this financial data, provide specific insights and recommendations for better financial management.
            Focus on actionable advice related to budgeting, expense tracking, and financial planning.
            """
        
        elif file_type == "PDF Document" or file_type == "Word Document":
            prompt = f"""
            I have analyzed a {file_type} with the following content:
            
            Document Summary: {analysis_result.get('summary', '')}
            
            Content Preview:
            {text_content[:1000]}...
            
            Based on this financial document, provide specific insights and recommendations.
            Focus on key financial information, potential action items, and advice for better financial management.
            """
        
        elif file_type == "Image":
            prompt = f"""
            I have analyzed an image document with OCR text extraction:
            
            Image Summary: {analysis_result.get('summary', '')}
            
            Extracted Text:
            {text_content}
            
            Based on this financial document image, provide insights and recommendations.
            Focus on any financial information that can be extracted and provide relevant advice.
            """
        
        else:
            prompt = f"""
            I have analyzed a financial document with the following content:
            
            Summary: {analysis_result.get('summary', '')}
            Content: {text_content[:1000]}...
            
            Please provide financial insights and recommendations based on this document.
            """
        
        messages.append(HumanMessage(content=prompt))
        
        response = await self.llm.ainvoke(messages)
        return cast(str, response.content)

    async def generate_document_insights(self, analysis_result: Dict[str, Any]) -> List[str]:
        """Generate key insights from document analysis."""
        
        insights = []
        
        # File type specific insights
        file_type = analysis_result.get('file_type', 'Unknown')
        
        if file_type == "Excel Spreadsheet":
            insights.append(f"📊 Excel file contains {analysis_result.get('sheet_count', 0)} sheets with {analysis_result.get('total_rows', 0)} total rows")
            
            if analysis_result.get('potential_financial_columns'):
                insights.append(f"💰 Detected financial columns: {', '.join(analysis_result.get('potential_financial_columns', []))}")
            
            if analysis_result.get('numeric_columns'):
                insights.append(f"📈 Contains {len(analysis_result.get('numeric_columns', []))} numeric columns for analysis")
        
        elif file_type == "CSV File":
            insights.append(f"📋 CSV file with {analysis_result.get('rows', 0)} rows and {analysis_result.get('columns', 0)} columns")
            
            if analysis_result.get('potential_financial_columns'):
                insights.append(f"💰 Financial data columns identified: {', '.join(analysis_result.get('potential_financial_columns', []))}")
        
        elif file_type == "PDF Document":
            insights.append(f"📄 PDF document with {analysis_result.get('page_count', 0)} pages")
            insights.append(f"📝 Contains {analysis_result.get('word_count', 0)} words of text content")
        
        elif file_type == "Word Document":
            insights.append(f"📝 Word document with {analysis_result.get('paragraph_count', 0)} paragraphs")
            
            if analysis_result.get('table_count', 0) > 0:
                insights.append(f"📊 Contains {analysis_result.get('table_count', 0)} tables with structured data")
        
        elif file_type == "Image":
            insights.append(f"🖼️ Image document ({analysis_result.get('image_size', [0, 0])[0]}x{analysis_result.get('image_size', [0, 0])[1]})")
            insights.append(f"🔍 OCR extracted {analysis_result.get('word_count', 0)} words")
        
        # General insights
        if analysis_result.get('text_content'):
            # Check for financial keywords
            text_lower = analysis_result.get('text_content', '').lower()
            financial_keywords = ['expense', 'income', 'budget', 'investment', 'profit', 'loss', 'revenue', 'cost', 'salary', 'payment', 'transaction', 'account', 'balance', 'credit', 'debit', 'loan', 'mortgage', 'insurance', 'tax', 'savings']
            found_keywords = [keyword for keyword in financial_keywords if keyword in text_lower]
            if found_keywords:
                insights.append(f"💼 Financial keywords found: {', '.join(found_keywords[:5])}")
        
        # Check for specific financial data patterns
        if analysis_result.get('potential_financial_columns'):
            insights.append(f"💰 Expense data found")
        
        if any(col in str(analysis_result.get('column_names', [])).lower() for col in ['credit', 'debit', 'balance']):
            insights.append(f"🏦 Credit information found")
        
        return insights 