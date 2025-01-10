from typing import Dict, List
import re

def extract_commands(message: str) -> List[Dict[str, str]]:
  command_pattern = r"\[COMANDO:(\w+):([^\]]+)\]"
  matches = re.findall(command_pattern, message)
  commands = [{"tipo": match[0], "acao": match[1]} for match in matches]
  return commands

def clean_message(message: str) -> str:
  command_pattern = r"\[COMANDO:\w+:[^\]]+\]"
  cleaned_message = re.sub(command_pattern, "", message).strip()
  return cleaned_message 