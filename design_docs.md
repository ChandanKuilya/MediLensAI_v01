# MediCare AI Architecture & Design

## High-Level Design (HLD)

This diagram represents the high-level architecture of the **MediCare AI Backend**, illustrating how requests flow from the client through the FastAPI layer to the application services and external AI providers.

```mermaid
graph TD
    %% Clients
    Client[Web/Mobile Client]
    
    %% API Layer
    subgraph Backend [FastAPI Backend]
        API[API Router]
        
        %% Routes
        subgraph Routes
            Health[Health Route]
            Chat[Chat Route]
            Analysis[Analysis Route]
            Research[Research Route]
        end
        
        %% Business Logic
        subgraph Logic [Application Logic]
            ChatChain[Chat Chain via LCEL]
            AnalysisChain[Analysis Chain via LCEL]
            GeminiSVc[Gemini Service]
            TavilySvc[Tavily Service]
        end
        
        %% Data Models
        Schemas[Pydantic Schemas]
    end
    
    %% External Services
    subgraph External [External APIs]
        Gemini[Google Gemini 2.0 API]
        Tavily[Tavily Search API]
    end

    %% Connections
    Client -->|HTTP/JSON| API
    API --> Health
    API --> Chat
    API --> Analysis
    API --> Research
    
    Chat -->|Invoke| ChatChain
    Analysis -->|Extract Text| GeminiSVc
    Analysis -->|Process Text| AnalysisChain
    Research -->|Search| TavilySvc
    Research -->|Summarize| ChatChain
    
    ChatChain -->|Generate Content| Gemini
    AnalysisChain -->|Structured Output| Gemini
    GeminiSVc -->|Vision/OCR| Gemini
    TavilySvc -->|Medical Search| Tavily
    
    Schemas -.->|Validate| Routes
    Schemas -.->|Format| AnalysisChain
```

---

## End-to-End Program Flows

### 1. Medical Image Analysis Flow
This sequence demonstrates the complex flow of uploading a medical record image, extracting text using Gemini Vision, and then analyzing that text for medical insights using LangChain.

```mermaid
sequenceDiagram
    autonumber
    participant User
    participant API as FastAPI Router
    participant GemSvc as GeminiService (Vision)
    participant AC as AnalysisChain (LangChain)
    participant LLM as Google Gemini 2.0
    
    note over User, LLM: **Medical Image Analysis Process**
    
    User->>API: POST /api/analyze-image (Image + Language)
    activate API
    
    %% Step 1: Text Extraction (OCR)
    API->>GemSvc: extract_text_from_image(bytes)
    activate GemSvc
    GemSvc->>LLM: Invoke Vision Model (Prompt + Image)
    activate LLM
    LLM-->>GemSvc: Return Extracted Text
    deactivate LLM
    GemSvc-->>API: Return text
    deactivate GemSvc
    
    %% Step 2: Medical Analysis
    API->>AC: analyze_medical_record(text, language)
    activate AC
    AC->>AC: Format Prompt (System + User + JSON Instructions)
    AC->>LLM: Invoke Chat Model (Analysis Request)
    activate LLM
    LLM-->>AC: Return JSON String
    deactivate LLM
    AC->>AC: PydanticParse (Validate Data)
    AC-->>API: Return MedicalAnalysis Object
    deactivate AC
    
    %% Step 3: Response
    API->>API: Construct Response (Info + Disclaimer)
    API-->>User: JSON Response (Summary, Findings, Recs)
    deactivate API
```

### 2. Medical Research Flow
This sequence shows how the system performs an external search for medical information and summarizes the results.

```mermaid
sequenceDiagram
    autonumber
    participant User
    participant API as FastAPI Router
    participant TavSvc as TavilyService
    participant TavExt as Tavily API
    participant CC as ChatChain (Summarizer)
    participant LLM as Google Gemini 2.0
    
    note over User, LLM: **Medical Research Process**
    
    User->>API: POST /api/research (Query)
    activate API
    
    %% Step 1: Search
    API->>TavSvc: search_medical_research(query)
    activate TavSvc
    TavSvc->>TavExt: Search (Advanced, Medical Domains)
    activate TavExt
    TavExt-->>TavSvc: Return Search Results
    deactivate TavExt
    TavSvc->>TavSvc: Format Results
    TavSvc-->>API: Return Formatted List
    deactivate TavSvc
    
    %% Step 2: Summarization
    API->>CC: get_chat_response(Prompt + Context)
    activate CC
    CC->>LLM: Invoke Chat Model
    activate LLM
    LLM-->>CC: Return Summary Text
    deactivate LLM
    CC-->>API: Return Summary
    deactivate CC
    
    %% Step 3: Response
    API-->>User: JSON Response (Summary + Citations)
    deactivate API
```
