from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from app.config import load_google_llm
from app.models.schemas import MedicalAnalysis


def create_analysis_chain(language: str = "en"):
    llm = load_google_llm()
    parser = PydanticOutputParser(pydantic_object=MedicalAnalysis)
    format_instructions = parser.get_format_instructions()

    if language == "fr":
        system_message = """Vous êtes un assistant médical IA analysant des dossiers médicaux.
Fournissez des informations claires, précises et actionnables.
Restez objectif et recommandez toujours une consultation médicale professionnelle."""

        user_template = """Analysez ce dossier médical et fournissez une analyse structurée:

Dossier Médical:
{medical_text}

Contexte Additionnel:
{context}

{format_instructions}

Répondez UNIQUEMENT en JSON valide."""
    else:
        system_message = """You are a medical AI assistant analyzing medical records.
Provide clear, accurate, and actionable insights.
Stay objective and always recommend professional medical consultation."""

        user_template = """Analyze this medical record and provide a structured analysis:

Medical Record:
{medical_text}

Additional Context:
{context}

{format_instructions}

Respond ONLY with valid JSON."""

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_message),
        ("user", user_template)
    ])

    prompt = prompt.partial(format_instructions=format_instructions)
    chain = prompt | llm | parser

    return chain


def analyze_medical_record(text: str, context: str = "", language: str = "en"):
    chain = create_analysis_chain(language)

    try:
        result = chain.invoke({
            "medical_text": text,
            "context": context if context else "No additional context provided"
        })
        return result
    except Exception as e:
        print(f"Analysis error: {e}")
        # Return a fallback object if parsing fails
        return MedicalAnalysis(
            summary=f"Analysis completed but encountered formatting issues: {str(e)[:200]}",
            key_findings=["Analysis was performed but results need manual review"],
            recommendations=["Consult with a healthcare professional for detailed interpretation"],
            next_steps=["Schedule appointment with your doctor", "Keep this record for your medical history"]
        )
