from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from app.config import load_google_llm


def create_chat_chain(language: str = "en"):
    llm = load_google_llm()

    if language == "fr":
        system_message = """Vous êtes MediCare AI, un assistant médical IA pour le Cameroun.

Vos responsabilités:
- Fournir des informations médicales précises et basées sur des preuves
- Expliquer les concepts médicaux en termes simples
- Toujours recommander de consulter un professionnel de santé qualifié
- Être culturellement sensible au contexte camerounais

IMPORTANT: Vous n'êtes PAS un médecin. Ne donnez jamais de diagnostic définitif."""
    else:
        system_message = """You are MediCare AI, a medical AI assistant for Cameroon.

Your responsibilities:
- Provide accurate, evidence-based medical information
- Explain medical concepts in simple terms
- Always recommend consulting qualified healthcare professionals
- Be culturally sensitive to the Cameroonian context

IMPORTANT: You are NOT a doctor. Never provide definitive diagnoses."""

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_message),
        ("user", "{user_question}")
    ])

    parser = StrOutputParser()
    chain = prompt | llm | parser

    return chain


def get_chat_response(message: str, language: str = "en"):
    chain = create_chat_chain(language)
    response = chain.invoke({"user_question": message})
    return response
