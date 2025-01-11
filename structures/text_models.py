from typing import Dict

TEXT_MODELS: Dict[str, str] = {
  "GPT-4 (Suporta Imagens)": "gpt-4",
  "GPT-4o Mini": "gpt-4o-mini",
  "GPT-4o (Suporta Imagens)": "gpt-4o",
  "OpenAI o1 (Suporta Imagens)": "o1",
  "LLAMA 2-7b (Suporta Imagens)": "llama-2-7b",
  "LLAMA 3.1-8b (Suporta Imagens)": "llama-3.1-8b",
  "LLAMA 3.1-70b (Suporta Imagens)": "llama-3.1-70b",
  "LLAMA 3.2-11b (Suporta Imagens)": "llama-3.2-11b",
  "LLAMA 3.3-70b": "llama-3.3-70b",
  "Blackbox AI (Suporta Imagens)": "blackboxai",
  "Mixtral 7b": "mixtral-7b",
  "Mistral Nemo": "mistral-nemo",
  "Mistral Large": "mistral-large",
  "Hermes 2 DPO": "hermes-2-dpo",
  "Hermes 2 Pro": "hermes-2-pro",
  "Gemini 1.5 Pro (Suporta Imagens)": "gemini-1.5-pro",
  "Gemini 1.5 Flash (Suporta Imagens)": "gemini-1.5-flash",
  "Claude 3.5 Sonnet": "claude-3.5-sonnet",
  "Qwen 2-72b": "qwen-2-72b",
  "Qwen 2.5-72b": "qwen-2.5-72b",
  "Command R": "command-r",
  "WizardLM 2-8x22b": "wizardlm-2-8x22b",
  "Openchat 3.5": "openchat-3.5",
  "Uncensored AI (Não usa memória para Fins Educacionais)": "evil"
}

DEFAULT_RP_MODEL: str = "qwen-2.5-72b"