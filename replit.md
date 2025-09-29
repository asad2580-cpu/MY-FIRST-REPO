# Tally ERP Automation Suite

## Overview

This is a comprehensive Streamlit-based web application that automates the import of financial data into Tally ERP. The application processes bank statements, invoices, and GST returns using Google's Gemini AI, with specialized functionality for converting official GSTR2B JSON data into separate Masters and Transactions XML files for seamless Tally import.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Framework**: Streamlit web framework for rapid prototyping and deployment
- **User Interface**: Simple form-based interface with file upload capabilities
- **Layout**: Wide layout configuration with columnar organization for configuration inputs
- **Caching**: Streamlit's `@st.cache_resource` decorator for efficient resource management

### Backend Architecture
- **Core Components**:
  - `TransactionExtractor`: Handles AI-powered data extraction from bank statement images
  - `TallyXMLGenerator`: Converts extracted data to Tally-compatible XML format
  - `InvoiceProcessor`: AI-powered invoice data extraction and processing
  - `GSTProcessor`: GST return file processing and validation
  - `GSTR2BDedicatedProcessor`: Specialized processor for official GSTR2B JSON files
  - `GSTR2BMastersXMLGenerator`: Creates Masters XML for vendor and tax ledgers
  - `GSTR2BTransactionsXMLGenerator`: Creates Transactions XML for purchase vouchers
- **Data Processing Pipelines**:
  1. **Bank Statements**: Image upload → AI extraction → XML generation
  2. **Invoices**: Image/PDF upload → AI processing → JSON/XML output
  3. **GST Returns**: JSON upload → validation → XML conversion
  4. **GSTR2B Dedicated**: Official JSON → separate Masters + Transactions XML
- **Error Handling**: Comprehensive validation with user-friendly error messages

### Data Models
- **Transaction Schema**: Bank statement transactions with date, narration, amounts, and balance
- **Invoice Schema**: Sales/purchase invoices with GST details and line items
- **GSTR2B Models**: Vendor and invoice models for GST purchase data
- **XML Structures**: Multiple Tally-compatible formats for different data types

### AI Integration
- **Provider**: Google Gemini AI for optical character recognition and data extraction
- **Input Processing**: Accepts PNG image format for bank statements
- **Output Formatting**: Structured JSON extraction with specific field mapping
- **Prompt Engineering**: Specialized prompts for financial document processing

## External Dependencies

### AI Services
- **Google Gemini API**: Primary AI service for image analysis and text extraction
  - Requires `GEMINI_API_KEY` environment variable
  - Used for OCR and structured data extraction from bank statement images

### Python Libraries
- **Streamlit**: Web application framework for user interface
- **Pydantic**: Data validation and modeling for transaction structures
- **PIL (Pillow)**: Image processing and manipulation
- **xml.etree.ElementTree**: XML generation for Tally import format

### Accounting Software Integration
- **Tally**: Target accounting software for XML import
  - Requires company name configuration
  - Requires bank ledger name mapping
  - Uses suspense ledger for unmatched transactions