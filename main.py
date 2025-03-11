import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from model_config import MODEL_NAME
from logger import get_logger
from interface import 

class ModelHandler:
    def __init__(self, model_name):
        self.logger = get_logger()
        self.model_name = model_name
        self.model = None
        self.tokenizer = None
        self.load_model()   # Load model immediately

    # Load model and tokenizer
    def load_model(self):
        self.logger.info(f"Loading model: {self.model_name}")
        try:
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_name,
                torch_dtype=torch.float32,
                trust_remote_code=True,
                device_map="cpu"
            )
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name, trust_remote_code=True)
            self.logger.info(f"Model {self.model_name} and tokenizer loaded successfully.")
        except Exception as e:
            self.logger.error(f"Error loading model or tokenizer: {e}")
            raise
    
    # Generate response
    def generate_response(self, prompt):
        self.logger.info(f"Processing prompt: {prompt}")
        
        # Determine translation direction and create appropriate system message
        if "to-ko" in prompt:
            system_content = (
                "You are EXAONE model from LG AI Research. "
                "You are a professional English to Korean translator. "
                "Translate the following English text to natural, fluent Korean. "
                "Maintain the original meaning and nuance."
            )
            prompt = prompt.replace("to-ko", "", 1).strip()
        elif "to-en" in prompt:
            system_content = (
                "You are EXAONE model from LG AI Research. "
                "You are a professional Korean to English translator. "
                "Translate the following Korean text to natural, fluent English. "
                "Maintain the original meaning and nuance."
            )
            prompt = prompt.replace("to-en", "", 1).strip()
        else:
            system_content = (
                "You are EXAONE model from LG AI Research. "
                "Translate the following text appropriately while maintaining "
                "the original meaning and nuance."
            )
        
        messages = [
            {"role": "system", "content": system_content},
            {"role": "user", "content": prompt}
        ]

        try:
            input_ids = self.tokenizer.apply_chat_template(
                messages,
                tokenize=True,
                add_generation_prompt=True,
                return_tensors="pt"
            )

            output = self.model.generate(
                input_ids.to("cpu"),
                eos_token_id=self.tokenizer.eos_token_id,
                max_new_tokens=128,
                do_sample=True,
            )

            # Potong input dan ambil hanya respons baru
            input_length = input_ids.shape[1]
            generated_ids = output[:, input_length:]
            result = self.tokenizer.decode(generated_ids[0], skip_special_tokens=True)
            
            self.logger.info(f"Generated output: {result}")
            return result

        except Exception as e:
            self.logger.error(f"Error during model inference: {e}")
            raise

def main():
    handler = ModelHandler(MODEL_NAME)
    # prompt = "to-en스스로를 자랑해 봐"
    prompt = "to-korHello, how are you?"
    response = handler.generate_response(prompt)
    print(response)

if __name__ == '__main__':
    main()
