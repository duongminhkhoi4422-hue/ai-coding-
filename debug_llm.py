from llm_clients import call_llm

system_prompt = "You are helpful."
user_prompt = "Say hello in one sentence."

response = call_llm(system_prompt, user_prompt)

print("=== LLM RESPONSE ===")
print(response)