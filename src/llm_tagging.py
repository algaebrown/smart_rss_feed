import logging
import json
import streamlit as st
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
    output_prompt = ("Output ONLY valid JSON with the following fields:\n"
    "{ \"match\": true|false, \"confidence\": float (0-1), \"reason\": string }\n"
    "- 'match': true if the newsletter clearly fits the filter, else false.\n"
    "- 'confidence': your certainty as a float between 0 and 1.\n")
    full_prompt = (
        f"{system_prompt}\n\n"
        f"User Filter: {user_prompt}\n"
        f"Newsletter Content:\n{context}\n"
        f"{output_prompt}"
    )
    if ai_provider == "OpenAI" and api_keys.get("openai"):
        try:
            import openai
            openai.api_key = api_keys["openai"]
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "system", "content": system_prompt},
                          {"role": "user", "content": full_prompt}],
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
                messages=[{"role": "user", "content": full_prompt}]
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
    elif ai_provider == "Vertex AI" and api_keys.get("vertex_project") and api_keys.get("vertex_location"):
        try:
            from vertexai.language_models import ChatModel
            chat_model = ChatModel.from_pretrained("chat-bison")
            chat = chat_model.start_chat()
            response = chat.send_message(full_prompt)
            result = json.loads(response.text)
            if "confidence" in result:
                try:
                    result["confidence"] = float(result["confidence"])
                except Exception:
                    result["confidence"] = 0.0
            return result
        except Exception as e:
            logging.exception("Vertex AI error during newsletter filter:")
            return {"match": False, "confidence": 0.0, "reason": f"Vertex AI error: {e}"}
    elif ai_provider == "Ollama (local)" and ollama_url:
        try:
            from langchain_community.chat_models import ChatOllama
            json_llm = ChatOllama(model = 'gemma3:1b',format="json")
            response = json_llm.invoke(full_prompt)
            content = response.content if hasattr(response, 'content') else response

            logging.info(f"Ollama response: {content}, prompt: {full_prompt}")
            result = json.loads(content)
            if "confidence" in result:
                try:
                    result["confidence"] = float(result["confidence"])
                except Exception:
                    result["confidence"] = 0.0
            return result
        except Exception as e:
            logging.exception("Ollama error during newsletter filter:")
            return {"match": False, "confidence": 0.0, "reason": f"Ollama error: {e}"}
    return {"match": False, "confidence": 0.0, "reason": "No AI provider or key available."}
def filter_newsletters_with_ai(newsletters, user_prompt, ai_provider, api_keys, ollama_url=None, filter_key='AI_filter', pass_date = True):
    """
    Runs AI filtering on a list of newsletters, updates each newsletter's filters dict with the result under filter_key, and returns the filtered list.
    """
    progress_bar = st.progress(0, text="Filtering newsletters with AI...")
    total= len(newsletters)
    for idx, n in enumerate(newsletters[:30]):
        n.filters = n.filters or {}
        
        if pass_date and n.filters and n.filters.get('date_filter') is True:
            context = f"Title: {n.title}\nContent: {n.content}\n" 
            result = ai_newsletter_filter(context, user_prompt, ai_provider, api_keys, ollama_url)
            # transient output show result
            st.write(f"LLM result: {n.title}. {result}")
            # save result in newsletter filters
            n.filters[filter_key] = result
            
            if result.get("match"):
                st.write(f"LLM result {n.title}: {result}")
                st.write(f"Matched: {n.title} (Confidence: {result.get('confidence', 0.0):.2f}) - {result.get('reason', '')}")
            elif result.get("match") is None:
                st.write(f"LLM returns weird result for {n.title}: {result}")
            progress_bar.progress((idx + 1) / total, text=f"Filtering newsletters with AI... ({idx + 1}/{total})")
        else:
            n.filters[filter_key] = {"match": None, "confidence": None, "reason": "Filtered out by date."}

    progress_bar.empty()