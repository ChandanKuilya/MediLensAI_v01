from langchain_core.messages import HumanMessage
from app.config import load_google_vision_llm
import base64
import json


class GeminiService:
    def __init__(self):
        # We load the model lazily or via the cached loader
        self.vision_llm_loader = load_google_vision_llm

    @property
    def vision_llm(self):
        return self.vision_llm_loader()

    def extract_text_from_image(self, image_bytes: bytes):
        try:
            image_b64 = base64.b64encode(image_bytes).decode('utf-8')

            extraction_prompt = """You are a medical text extractor. Extract ALL text from this medical document/record.

Include:
- Patient information
- Test results
- Doctor's notes
- Prescriptions
- Dates and measurements
- Any handwritten text

Format the output clearly and preserve the structure. If text is unclear, indicate with [unclear].

Extract all text now:"""

            message = HumanMessage(
                content=[
                    {"type": "text", "text": extraction_prompt},
                    {"type": "image_url", "image_url": f"data:image/jpeg;base64,{image_b64}"}
                ]
            )

            response = self.vision_llm.invoke([message])
            return response.content

        except Exception as e:
            raise Exception(f"Image text extraction error: {str(e)}")

    def analyze_image_directly(self, image_bytes: bytes, language: str = "en"):
        try:
            image_b64 = base64.b64encode(image_bytes).decode('utf-8')

            if language == "fr":
                prompt = """Analysez cette image de dossier médical et fournissez une analyse au format JSON avec ces clés:
- summary: Aperçu bref de ce que vous voyez
- key_findings: Liste des résultats importants
- recommendations: Recommandations de santé
- next_steps: Actions suggérées

- extracted_text: Le texte complet extrait de l'image.

Répondez UNIQUEMENT en JSON valide."""
            else:
                prompt = """Analyze this medical record image and provide analysis in JSON format with these keys:
- summary: Brief overview of what you see
- key_findings: List of important findings
- recommendations: Health recommendations
- next_steps: Suggested actions
- extracted_text: The complete text extracted from the image.

Respond ONLY with valid JSON."""

            message = HumanMessage(
                content=[
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": f"data:image/jpeg;base64,{image_b64}"}
                ]
            )

            response = self.vision_llm.invoke([message])
            content = response.content.replace("```json", "").replace("```", "").strip()
            result = json.loads(content)
            return result

        except json.JSONDecodeError:
            return {
                "summary": response.content[:500],
                "key_findings": ["Analysis completed - see summary"],
                "recommendations": ["Consult with a healthcare professional"],
                "next_steps": ["Schedule appointment with your doctor"],
                "extracted_text": "Could not extract structured text."
            }
        except Exception as e:
            raise Exception(f"Image analysis error: {str(e)}")


gemini_service = GeminiService()
