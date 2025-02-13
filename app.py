from fastapi import FastAPI
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

# Initialize FastAPI app
app = FastAPI()

# Load model and tokenizer
tokenizer = AutoTokenizer.from_pretrained("cognitivecomputations/Dolphin3.0-Mistral-24B")
model = AutoModelForCausalLM.from_pretrained("cognitivecomputations/Dolphin3.0-Mistral-24B", torch_dtype=torch.float16).cuda()

# Define input data model
class InputText(BaseModel):
    prompt: str
    max_length: int = 100

@app.post("/generate")
async def generate_text(input_data: InputText):
    inputs = tokenizer(input_data.prompt, return_tensors="pt").to("cuda")
    output = model.generate(**inputs, max_length=input_data.max_length)
    generated_text = tokenizer.decode(output[0], skip_special_tokens=True)
    return {"response": generated_text}

# Make sure Render finds the app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
