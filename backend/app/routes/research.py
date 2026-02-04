from fastapi import APIRouter, HTTPException
from app.models.schemas import ResearchRequest, ResearchResponse, ResearchResult
from app.services.tavily_service import tavily_service
from app.chains.chat_chain import get_chat_response
from datetime import datetime

router = APIRouter(prefix="/api", tags=["Research"])


@router.post("/research", response_model=ResearchResponse)
async def search_medical_research(request: ResearchRequest):
    try:
        raw_results = tavily_service.search_medical_research(
            query=request.query,
            max_results=request.max_results
        )

        formatted_results = tavily_service.format_results(raw_results)

        results_text = "\n\n".join([
            f"Source: {r['title']}\n{r['content']}"
            for r in formatted_results[:3]
        ])

        summary_prompt = f"""Based on these medical research results, provide a brief summary in 2-3 sentences:

{results_text}

Focus on the key takeaways and most important information."""

        summary = get_chat_response(summary_prompt, request.language)

        research_results = [
            ResearchResult(
                title=r["title"],
                url=r["url"],
                content=r["content"],
                score=r["score"]
            )
            for r in formatted_results
        ]

        return ResearchResponse(
            query=request.query,
            results=research_results,
            summary=summary,
            timestamp=datetime.now()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Research error: {str(e)}")
