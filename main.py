import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

from logger import get_logger

class ModelHandler:
    def __init__(self, model_name):
        self.logger = get_logger()
        self.model_name = model_name
        self.model = None
        self.tokenizer = None
        self.load_model()   # Load model immediately

    # Load Model and Tokenizer
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
    
    # Generate Response
    def generate_response(self, prompt):
        self.logger.info("=" * 68)
        self.logger.info(f"Processing prompt: {prompt}")

        # Determine translation pipeline
        task_config = {
            "t-to-ko": {
                "system_content": "You are EXAONE model from LG AI Research. A professional English to Korean translator.",
                "new_tokens": 128,
                "command": "Translate this following text to natural, fluent Korean:"
            },
            "t-to-en": {
                "system_content": "You are EXAONE model from LG AI Research. A professional Korean to English translator.",
                "new_tokens": 128,
                "command": "Translate this following text to natural, fluent English:"
            },
            "g-check": {
                "system_content": "You are EXAONE model from LG AI Research, a professional Korean and English grammar checker.",
                "new_tokens": 256,
                "command": "Provide a grammar quality rating (1-10). Respond in strict format: rating, feedback"
            }
        }

        task_name = next((key for key in task_config if key in prompt), None)
        if task_name:
            task = task_config[task_name]
            system_content = task["system_content"]
            new_tokens = task["new_tokens"]
            prompt = prompt.replace(task_name, task["command"], 1).strip()
        else:
            self.logger.error(f"Unknown task in prompt: {prompt}")
        
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
                max_new_tokens=new_tokens,
                do_sample=True,
                top_p=0.95,
                temperature=0.7,
                repetition_penalty=1.2,
            )
            
            input_length = input_ids.shape[1]
            generated_ids = output[:, input_length:]
            result = self.tokenizer.decode(generated_ids[0], skip_special_tokens=True)
            
            self.logger.info(f"Generated output: {result}")
            return result

        except Exception as e:
            self.logger.error(f"Error during model inference: {e}")
            raise
