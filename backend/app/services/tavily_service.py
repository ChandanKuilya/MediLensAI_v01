from tavily import TavilyClient
from app.config import settings


class TavilyService:
    def __init__(self):
        # Initialize client lazily or directly; settings are already loaded
        pass

    @property
    def client(self):
        return TavilyClient(api_key=settings.tavily_api_key)

    def search_medical_research(self, query: str, max_results: int = 5):
        try:
            response = self.client.search(
                query=f"medical research {query}",
                search_depth="advanced",
                max_results=max_results,
                include_domains=[
                    "pubmed.ncbi.nlm.nih.gov",
                    "nih.gov",
                    "who.int",
                    "cdc.gov",
                    "mayoclinic.org",
                    "webmd.com",
                    "healthline.com",
                    "medicalnewstoday.com"
                ]
            )
            return response
        except Exception as e:
            raise Exception(f"Research search error: {str(e)}")

    def format_results(self, raw_results):
        formatted = []
        for result in raw_results.get("results", []):
            formatted.append({
                "title": result.get("title", "Untitled"),
                "url": result.get("url", ""),
                "content": result.get("content", "")[:500],
                "score": result.get("score", 0.0)
            })
        return formatted


tavily_service = TavilyService()
