import logging
import json
import streamlit as st
from google import genai
from pydantic import BaseModel, ValidationError, Field
import re
from time import sleep


def clean_json_response(text: str) -> str:
    """cleans markdown encasing around json"""
    # Remove code fences like ```json ... ```
    cleaned = re.sub(r"^```(?:json)?\n?", "", text.strip())
    cleaned = re.sub(r"```$", "", cleaned.strip())
    return cleaned.strip()


class NewsletterResult(BaseModel):
    match: bool
    confidence: float = Field(ge=0.0, le=1.0)  # confidence between 0 and 1
    reason: str | None = None  # optional


def get_google_genai_client(api_key):
    """
    Initialize and return a Google Gemini API client.
    api_key: str, your Google Gemini API key
    Returns: genai.Client instance
    """
    client = genai.Client(
        api_key=api_key,
    )
    return client


def ai_newsletter_filter(context, user_prompt, ai_provider, api_keys, ollama_url=None):
    """
    Returns a dict: {"match": bool, "confidence": float, "reason": str}
    context: str, all newsletter info (title, content)
    user_prompt: str, the user's filter prompt
    ai_provider: str, one of 'OpenAI', 'Claude', 'Vertex AI', 'Ollama (local)'
    api_keys: dict, e.g. {"openai": ..., "claude": ..., "vertex_project": ..., "vertex_location": ...}
    ollama_url: str, if using Ollama
    """
    system_prompt = (
        "You are an assistant that decides if a newsletter matches a user's filter. "
        "Base your decision ONLY on the provided User Filter and Newsletter Content. "
        "Do not speculate or use outside knowledge. "
        "Always justify using specific phrases or facts from the newsletter."
    )
    output_prompt = (
        "Output ONLY valid JSON with the following fields:\n"
        '{ "match": true|false, "confidence": float (0-1), "reason": string }\n'
        "- 'match': true if the newsletter clearly fits the filter, else false.\n"
        "- 'confidence': your certainty as a float between 0 and 1.\n"
    )
    full_prompt = (
        f"{system_prompt}\n\n"
        f"User Filter: {user_prompt}\n"
        f"Newsletter Content:\n{context}\n"
        f"{output_prompt}"
    )
    logging.info(f"AI Provider: {ai_provider}, Prompt: {full_prompt}")
    if ai_provider == "OpenAI" and api_keys.get("openai"):
        try:
            import openai

            openai.api_key = api_keys["openai"]
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": full_prompt},
                ],
                max_tokens=128,
                temperature=0.2,
            )
            result = json.loads(response.choices[0].message.content)
            if "confidence" in result:
                try:
                    result["confidence"] = float(result["confidence"])
                except Exception:
                    result["confidence"] = 0.0
            return result
        except Exception as e:
            logging.exception("OpenAI error during newsletter filter:")
            return {"match": False, "confidence": 0.0, "reason": f"OpenAI error: {e}"}
    elif ai_provider == "Claude" and api_keys.get("claude"):
        try:
            import anthropic

            client = anthropic.Anthropic(api_key=api_keys["claude"])
            response = client.messages.create(
                model="claude-3-opus-20240229",
                max_tokens=128,
                temperature=0.2,
                messages=[{"role": "user", "content": full_prompt}],
            )
            result = json.loads(response.content[0].text)
            if "confidence" in result:
                try:
                    result["confidence"] = float(result["confidence"])
                except Exception:
                    result["confidence"] = 0.0
            return result
        except Exception as e:
            logging.exception("Claude error during newsletter filter:")
            return {"match": False, "confidence": 0.0, "reason": f"Claude error: {e}"}
    elif ai_provider == "Google" and api_keys.get("gemini"):
        try:
            # Gemma does not have a json output mode, so we need to clean the response
            client = get_google_genai_client(api_keys.get("gemini"))
            response = client.models.generate_content(
                model="gemma-3-12b-it", contents=full_prompt
            )
            logging.info(f"Google response: {response.text}, prompt: {full_prompt}")
            raw_result = json.loads(clean_json_response(response.text))
            result = NewsletterResult(**raw_result)
            # sleep 2s because of rate limits
            sleep(2)
            return dict(result)
        except Exception as e:
            logging.exception("Google gemma-3-12b-it error during newsletter filter:")
            logging.info(f"Response text: {response.text}")
            return {
                "match": False,
                "confidence": 0.0,
                "reason": f"Google gemma-3-12b-it error: {e}",
                "response": response.text,
            }
    elif ai_provider == "Ollama (local)" and ollama_url:
        try:
            from langchain_community.chat_models import ChatOllama

            json_llm = ChatOllama(model="gemma3:1b", format="json")
            response = json_llm.invoke(full_prompt)
            content = response.content if hasattr(response, "content") else response

            logging.info(f"Ollama response: {content}, prompt: {full_prompt}")
            raw_result = json.loads(content)
            result = NewsletterResult(**raw_result)
            return dict(result)
        except Exception as e:
            logging.exception("Ollama error during newsletter filter:")
            return {"match": False, "confidence": 0.0, "reason": f"Ollama error: {e}"}
    return {
        "match": False,
        "confidence": 0.0,
        "reason": "No AI provider or key available.",
    }


def filter_newsletters_with_ai(
    newsletters,
    user_prompt,
    ai_provider,
    api_keys,
    ollama_url=None,
    filter_key="AI_filter",
    pass_date=True,
):
    """
    Runs AI filtering on a list of newsletters, updates each newsletter's filters dict with the result under filter_key, and returns the filtered list.
    """
    progress_bar = st.progress(
        0,
        text="Filtering newsletters with AI within date range. Please be patient, limited by API rate limits.",
    )

    # only process newsletters that pass the date filter if pass_date is True
    to_process = [
        n
        for n in newsletters
        if not pass_date or (n.filters and n.filters.get("date_filter") is True)
    ]
    total = len(to_process)
    # estimate 2 seconds per request for rate limiting, so show progress accordingly
    estimated_time = total * 2  # seconds
    # tell the user estimated time
    st.info(
        f"Estimated time for AI filtering: {estimated_time} seconds for {total} newsletters."
    )
    for idx, n in enumerate(to_process):
        n.filters = n.filters or {}

        if pass_date and n.filters and n.filters.get("date_filter") is True:
            context = f"Title: {n.title}\nContent: {n.content}\n"
            result = ai_newsletter_filter(
                context, user_prompt, ai_provider, api_keys, ollama_url
            )
            # save result in newsletter filters
            n.filters[filter_key] = result

            if result.get("match"):
                st.write(
                    f"Matched: {n.title} (Confidence: {result.get('confidence', 0.0):.2f}) - {result.get('reason', '')}"
                )
            elif result.get("match") is None:
                logging.warning(
                    f"AI filter returned None match for newsletter '{n.title}': {result}"
                )
            progress_bar.progress(
                (idx + 1) / total,
                text=f"Filtering newsletters with AI... ({idx + 1}/{total})",
            )
        else:
            n.filters[filter_key] = {
                "match": None,
                "confidence": None,
                "reason": "Filtered out by date.",
            }

    progress_bar.empty()
