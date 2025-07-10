# 🌐 Multilingual Budget Chat Assistant

A comprehensive AI-powered financial advisor application that supports 50+ languages and advanced document analysis capabilities. Built with FastAPI backend and Next.js frontend, featuring ChatGPT-like interface and powered by Sutra LLM.

## ✨ Key Features

### 🤖 AI-Powered Financial Advice
- **Multilingual Support**: Automatically detects and responds in 50+ languages
- **Smart Language Detection**: Uses Sutra LLM to detect language from user input
- **Context-Aware Responses**: Provides personalized financial advice based on user queries

### 📄 Advanced Document Processing
- **Multiple File Types**: PDF, DOC, DOCX, XLSX, XLS, CSV, and Images
- **Intelligent Analysis**: Extracts and analyzes financial data from documents
- **OCR Technology**: Extracts text from images using Tesseract OCR
- **Data Insights**: Automatically identifies financial columns in spreadsheets
- **Statistical Analysis**: Provides summaries and statistics for numeric data

### 💬 ChatGPT-Like Interface
- **Modern Chat UI**: Clean, responsive design with message bubbles
- **File Upload**: Drag-and-drop support for document analysis
- **Real-time Processing**: Live typing indicators and instant responses
- **Mobile-Friendly**: Responsive design for all devices

### 🔐 Secure Authentication
- **JWT-based Authentication**: Secure user sessions
- **User Profiles**: Personalized financial recommendations
- **Data Privacy**: Secure file handling and processing

## 🛠️ Technology Stack

### Backend (FastAPI)
- **FastAPI**: Modern Python web framework
- **SQLAlchemy**: Async ORM with SQLite database
- **Sutra LLM**: Advanced multilingual AI model
- **Document Processing**: pandas, python-docx, PyPDF2, pytesseract
- **Authentication**: JWT tokens with bcrypt password hashing

### Frontend (Next.js)
- **Next.js 14**: React framework with App Router
- **TypeScript**: Type-safe development
- **Tailwind CSS**: Utility-first CSS framework
- **React Hooks**: Modern state management

## 📋 Supported File Types

| File Type | Extensions | Analysis Features |
|-----------|------------|------------------|
| **PDF Documents** | `.pdf` | Text extraction, page analysis, financial keyword detection |
| **Word Documents** | `.doc`, `.docx` | Text extraction, table analysis, paragraph counting |
| **Excel Spreadsheets** | `.xlsx`, `.xls` | Multi-sheet analysis, financial column detection, statistical summaries |
| **CSV Files** | `.csv` | Data analysis, numeric summaries, column type identification |
| **Images** | `.png`, `.jpg`, `.jpeg`, `.bmp`, `.tiff` | OCR text extraction, financial document recognition |

## 🚀 Getting Started

### Prerequisites
- Python 3.9+
- Node.js 18+
- Sutra API Key from [two.ai](https://two.ai)

### Backend Setup

1. **Clone the repository**
```bash
git clone <repository-url>
cd sutra_multilingual_chat
```

2. **Install Python dependencies**
```bash
cd fastapi_backend
pip install -r requirements.txt
```

3. **Set up environment variables**
```bash
cp .env.example .env
# Edit .env with your configuration
```

Required environment variables:
```env
SUTRA_API_KEY=your_sutra_api_key_here
JWT_SECRET_KEY=your_jwt_secret_key_here
ACCESS_TOKEN_EXPIRE_MINUTES=30
DATABASE_URL=sqlite:///./multilingual_budget.db
```

4. **Run the backend**
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Setup

1. **Install Node.js dependencies**
```bash
cd frontend
npm install
```

2. **Run the frontend**
```bash
npm run dev
```

3. **Access the application**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## 📊 Document Analysis Features

### Excel/CSV Analysis
- **Data Overview**: Row and column counts, data types
- **Financial Column Detection**: Automatically identifies amount, price, balance columns
- **Statistical Summaries**: Mean, median, standard deviation for numeric data
- **Missing Data Analysis**: Identifies null values and data quality issues

### PDF/Word Analysis
- **Text Extraction**: Full text content extraction
- **Structure Analysis**: Page/paragraph counting, table detection
- **Financial Keyword Detection**: Identifies budget, expense, income mentions
- **Content Summarization**: Key insights and recommendations

### Image Analysis
- **OCR Processing**: Extracts text from financial documents
- **Receipt Processing**: Identifies amounts, dates, vendor information
- **Bank Statement Analysis**: Extracts transaction details
- **Invoice Processing**: Identifies totals, line items, payment terms

## 🌍 Language Support

The application automatically detects and responds in 50+ languages including:

- **English** (en)
- **Spanish** (es)
- **French** (fr)
- **German** (de)
- **Hindi** (hi)
- **Tamil** (ta)
- **Telugu** (te)
- **Malayalam** (ml)
- **Kannada** (kn)
- **Chinese** (zh)
- **Japanese** (ja)
- **Korean** (ko)
- **Arabic** (ar)
- **Portuguese** (pt)
- **Italian** (it)
- **Russian** (ru)
- And many more...

## 🔧 API Endpoints

### Authentication
- `POST /auth/register` - User registration
- `POST /auth/login` - User login
- `GET /auth/me` - Get current user

### AI Advisor
- `POST /ai/get-advice` - Get financial advice
- `POST /ai/upload-document` - Upload and analyze documents
- `GET /ai/document-info` - Get supported file types and features

### Transactions
- `GET /transactions/` - List user transactions
- `POST /transactions/` - Create new transaction

## 📈 Usage Examples

### Text-based Financial Advice
```json
{
  "message": "பணத்தை மிச்சப்படுத்த 10 வழிகள் சொல்லுங்கள்",
  "language": null
}
```

Response: AI automatically detects Tamil and responds in Tamil with 10 money-saving tips.

### Document Analysis
Upload a CSV file with financial data:
- Automatically detects financial columns
- Provides statistical analysis
- Generates budget recommendations
- Identifies spending patterns

### Excel Spreadsheet Analysis
Upload an Excel budget file:
- Analyzes multiple sheets
- Identifies income/expense categories
- Provides financial health insights
- Suggests optimization strategies

## 🛡️ Security Features

- **JWT Authentication**: Secure token-based authentication
- **File Validation**: Strict file type and size validation (50MB limit)
- **Input Sanitization**: Prevents malicious input injection
- **CORS Protection**: Configurable cross-origin resource sharing
- **Password Hashing**: bcrypt encryption for user passwords

## 🔧 Development

### Project Structure
```
sutra_multilingual_chat/
├── fastapi_backend/
│   ├── main.py                 # FastAPI application
│   ├── database.py             # Database configuration
│   ├── models.py               # Database models
│   ├── schemas.py              # Pydantic schemas
│   ├── auth.py                 # Authentication utilities
│   ├── routers/
│   │   ├── auth.py            # Authentication routes
│   │   ├── transactions.py    # Transaction routes
│   │   └── ai_advisor.py      # AI advisor routes
│   ├── services/
│   │   ├── ai_service.py      # Sutra LLM integration
│   │   └── document_processor.py # Document analysis
│   └── utils/
│       └── file_handler.py    # File upload utilities
├── frontend/
│   ├── app/
│   │   ├── page.tsx           # Main application page
│   │   └── layout.tsx         # Root layout
│   ├── components/
│   │   ├── ChatInterface.tsx  # Chat interface
│   │   └── AuthModal.tsx      # Authentication modal
│   └── hooks/
│       └── useAuth.ts         # Authentication hook
└── README.md
```

### Adding New Document Types

1. **Update document_processor.py**
```python
async def _analyze_new_format(self, file_path: Path) -> Dict[str, Any]:
    # Your analysis logic here
    pass
```

2. **Update supported file types**
```python
self.supported_types['.new_ext'] = 'New Document Type'
```

3. **Add to frontend file input**
```typescript
accept=".pdf,.doc,.docx,.xlsx,.xls,.csv,.png,.jpg,.jpeg,.bmp,.tiff,.new_ext"
```

## 🐛 Troubleshooting

### Common Issues

1. **Sutra API Key Error**
   - Verify your API key is correct
   - Check if your account has sufficient credits

2. **File Upload Fails**
   - Ensure file size is under 50MB
   - Check file type is supported
   - Verify backend upload directory permissions

3. **Language Detection Issues**
   - Ensure text contains enough content for detection
   - Check Sutra API connectivity

4. **Dependencies Not Installing**
   - Use Python 3.9+ for backend
   - Use Node.js 18+ for frontend
   - Check system requirements for pytesseract

## 📄 License

This project is licensed under the MIT License. See the LICENSE file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📞 Support

For support and questions, please open an issue in the GitHub repository.

---

**Built with ❤️ using Sutra LLM for multilingual financial intelligence**
