# chains/llm_analysis.py
from langchain_community.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import os

def get_llm_analysis(resume_text: str, jd_text: str) -> dict:
    """Use LLM for persona and fit analysis"""
    try:
        # Initialize LLM - use your OpenAI API key
        llm = OpenAI(
            temperature=0.7, 
            openai_api_key=os.getenv("OPENAI_API_KEY"),
            max_tokens=500
        )
        
        # Persona analysis prompt
        persona_prompt = PromptTemplate(
            input_variables=["resume"],
            template="""Analyze this resume text and describe the candidate's professional persona in 2-3 phrases. 
            Focus on their strengths, technical abilities, and soft skills.
            
            Resume: {resume}
            
            Professional Persona:"""
        )
        
        # Fit analysis prompt  
        fit_prompt = PromptTemplate(
            input_variables=["resume", "jd"],
            template="""Analyze how well this candidate fits the job role. Consider:
            1. Technical skills match
            2. Experience relevance  
            3. Overall suitability
            4. Key strengths for this role
            5. Potential gaps
            
            Resume: {resume}
            
            Job Description: {jd}
            
            Fit Analysis:"""
        )
        
        persona_chain = LLMChain(llm=llm, prompt=persona_prompt)
        fit_chain = LLMChain(llm=llm, prompt=fit_prompt)
        
        # Run both analyses
        persona_analysis = persona_chain.run(resume=resume_text[:1500])  # Limit text length
        fit_analysis = fit_chain.run(
            resume=resume_text[:1500], 
            jd=jd_text[:1000]
        )
        
        return {
            "persona": persona_analysis,
            "fit_analysis": fit_analysis,
            "llm_used": "OpenAI GPT-3.5-turbo"
        }
        
    except Exception as e:
        # Fallback if LLM fails
        return {
            "persona": "LLM Analysis temporarily unavailable",
            "fit_analysis": f"Error in LLM analysis: {str(e)}",
            "llm_used": "Error"
        }