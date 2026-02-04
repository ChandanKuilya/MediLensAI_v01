from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from app.models.schemas import (
    ChatRequest, ChatResponse,
    AnalysisRequest, AnalysisResponse,
    ImageAnalysisResponse
)
from app.chains.chat_chain import get_chat_response
from app.chains.analysis_chain import analyze_medical_record
from app.services.gemini_service import gemini_service
from datetime import datetime

router = APIRouter(prefix="/api", tags=["Analysis"])


@router.post("/chat", response_model=ChatResponse)
async def chat_with_ai(request: ChatRequest):
    try:
        response_text = get_chat_response(
            message=request.message,
            language=request.language
        )
        return ChatResponse(
            response=response_text,
            language=request.language,
            timestamp=datetime.now()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chat error: {str(e)}")


@router.post("/analyze-text", response_model=AnalysisResponse)
async def analyze_medical_text(request: AnalysisRequest):
    try:
        analysis = analyze_medical_record(
            text=request.text,
            context=request.context,
            language=request.language
        )

        disclaimer = (
            "This analysis is for informational purposes only. "
            "Always consult qualified healthcare professionals for medical advice."
        )

        return AnalysisResponse(
            summary=analysis.summary,
            key_findings=analysis.key_findings,
            recommendations=analysis.recommendations,
            next_steps=analysis.next_steps,
            disclaimer=disclaimer,
            language=request.language,
            timestamp=datetime.now()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis error: {str(e)}")


@router.post("/analyze-image", response_model=ImageAnalysisResponse)
async def analyze_medical_image(
    file: UploadFile = File(...),
    language: str = Form(default="en"),
    extract_text_only: bool = Form(default=False)
):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")

    try:
        image_bytes = await file.read()
        
        # If the user just wants text extraction (OCR)
        if extract_text_only:
            extracted_text = gemini_service.extract_text_from_image(image_bytes)
            return ImageAnalysisResponse(
                extracted_text=extracted_text,
                analysis=AnalysisResponse(
                    summary="Text extraction completed",
                    key_findings=[],
                    recommendations=[],
                    next_steps=["Review the extracted text", "Analyze if needed"],
                    disclaimer="Text extraction only - no analysis performed",
                    language=language,
                    timestamp=datetime.now()
                )
            )

        # Full analysis (Vision -> Analysis)
        # Note: We can either extract text first then analyze text, OR use vision model directly.
        # The prompt suggests a 2-step approach for reliability or direct vision.
        # Let's use the direct vision analysis method we implemented in gemini_service
        # effectively doing both in one pass or as configured.
        
        # Actually, looking at the tutorial logic, it suggests:
        # "We first extract text using Gemini Vision (OCR), then analyze that text using our LangChain analysis chain."
        # OK, I will follow that.
        
        extracted_text = gemini_service.extract_text_from_image(image_bytes)
        analysis = analyze_medical_record(text=extracted_text, language=language)
        
        disclaimer = (
            "This analysis is for informational purposes only. "
            "Always consult qualified healthcare professionals for medical advice."
        )

        return ImageAnalysisResponse(
            extracted_text=extracted_text,
            analysis=AnalysisResponse(
                summary=analysis.summary,
                key_findings=analysis.key_findings,
                recommendations=analysis.recommendations,
                next_steps=analysis.next_steps,
                disclaimer=disclaimer,
                language=language,
                timestamp=datetime.now()
            )
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Image analysis error: {str(e)}")


@router.post("/extract-text")
async def extract_text_from_image(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")

    try:
        image_bytes = await file.read()
        extracted_text = gemini_service.extract_text_from_image(image_bytes)
        return {
            "extracted_text": extracted_text,
            "timestamp": datetime.now()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Text extraction error: {str(e)}")
