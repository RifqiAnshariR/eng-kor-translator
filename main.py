import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from config import MODEL_NAME
from logger import get_logger

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
                device_map="auto"
            )
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name, trust_remote_code=True)
            self.logger.info(f"Model {self.model_name} and tokenizer loaded successfully.")
        except Exception as e:
            self.logger.error(f"Error loading model or tokenizer: {e}")
            raise
    
    # Generate response
    def generate_response(self, prompt):
        self.logger.info(f"Processing prompt: {prompt}")
        
        # Determine translation pipeline
        if "t-to-ko" in prompt:
            system_content = (
                "You are EXAONE model from LG AI Research."
                "A professional English to Korean translator."
            )
            prompt = prompt.replace("to-ko", "Translate this following text to natural, fluent Korean:", 1).strip()
        elif "t-to-en" in prompt:
            system_content = (
                "You are EXAONE model from LG AI Research."
                "A professional Korean to English translator."
            )
            prompt = prompt.replace("to-en", "Translate this following text to natural, fluent English:", 1).strip()
        elif "g-check" in prompt:
            system_content = (
                "You are EXAONE model from LG AI Research, "
                "a professional Korean and English grammar checker."
            )
            prompt = prompt.replace("g-check", 
                                    "Provide a grammar quality rating (1-10). Respond in strict format: rating, feedback", 1).strip()

        messages = [
            {"role": "system", "content": system_content},
            {"role": "user", "content": prompt}
        ]

        self.logger.info(f"Processing messages: {messages}")
        
        try:
            input_ids = self.tokenizer.apply_chat_template(
                messages,
                tokenize=True,
                add_generation_prompt=True,
                return_tensors="pt"
            )

            self.logger.info(f"Model ran on: {self.model.device}")

            output = self.model.generate(
                input_ids = input_ids.to(self.model.device),
                eos_token_id=self.tokenizer.eos_token_id,
                max_new_tokens=256,
                do_sample=True,
                top_p=0.95,
                temperature=0.7,
                repetition_penalty=1.2,
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

def main(prompt):
    handler = ModelHandler(MODEL_NAME)
    # prompt = "to-en스스로를 자랑해 봐"
    # prompt = "g-check I has a pencils"
    # response = handler.generate_response(prompt)
    # print(response)
    return handler.generate_response(prompt)

if __name__ == '__main__':
    main()
