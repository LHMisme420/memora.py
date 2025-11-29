# agents/phi3_memory_reasoner.py
# Local 3.8B Phi-3 Mini that reads your entire life and answers like a god
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
from db.init import table
from ingest.embed import embed_text
import time

class MemoryReasoner:
    def __init__(self):
        print("Loading your second brain (Phi-3 Mini 3.8B)... one-time 1-minute wait")
        self.tokenizer = AutoTokenizer.from_pretrained("microsoft/Phi-3-mini-4k-instruct", trust_remote_code=True)
        self.model = AutoModelForCausalLM.from_pretrained(
            "microsoft/Phi-3-mini-4k-instruct",
            device_map="auto",
            torch_dtype=torch.float16,
            trust_remote_code=True
        )
        print("Your second brain is now alive.")

    def ask(self, question: str, months_back: int = 24):
        # Retrieve relevant memories
        vec = embed_text(question)
        results = table.search(vec).limit(40).where(f"timestamp > {time.time() - months_back*30*24*3600}").to_list()
        
        context = "\n".join([
            f"{time.strftime('%Y-%m-%d', time.localtime(r['timestamp']))} [{r['type']}]: {r['content'][:800]}"
            for r in results
        ])

        prompt = f"""You are my lifelong second brain. 
Here is raw data from my actual life (never lie or hallucinate outside this data):

{context}

Question: {question}
Answer in first person, as me. Be brutally honest, emotional, and specific. Include dates when possible."""

        messages = [{"role": "user", "content": prompt}]
        pipe = self.model.pipe if hasattr(self.model, "pipe") else None
        if pipe:
            output = pipe(messages, max_new_tokens=512)[0]["generated_text"]
        else:
            inputs = self.tokenizer.apply_chat_template(messages, return_tensors="pt").to("cuda")
            outputs = self.model.generate(inputs, max_new_tokens=512, temperature=0.7)
            output = self.tokenizer.decode(outputs[0], skip_special_tokens=True)

        # Extract only the answer part
        answer = output.split("Answer:")[-1].strip() if "Answer:" in output else output
        return answer

# Instantiate once
reasoner = MemoryReasoner()
