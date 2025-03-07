import datetime
import logging
import os
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import re

class LanguageModel():
    instance = None

    def __new__(cls,model_name):
        if cls.instance is None:
            # The Singleton class extends the object class, so super() refers to object
            cls.instance = super().__new__(cls)
            if not re.search("^.+/.+$",model_name): raise NameError("Does not match model_name pattern.")
            cls.tokenizer = AutoTokenizer.from_pretrained(model_name)
            cls.model = AutoModelForCausalLM.from_pretrained(model_name,torch_dtype=torch.float16)
            # cls.model.eval()
            if torch.cuda.is_available():
                cls.model = cls.model.to("cuda")
            print("Create Language model instance.")
        return cls.instance
    
    def build_prompt(self, user_query, inputs=""):
        with open(".prompt", mode = "r") as fp:
            PROMPT = fp.read()
        if os.path.isfile(".document"):
            with open(".document", mode = "r") as fp:
                DOCUMENT = fp.read()
            prompt = [
                {"role": "system", "content": PROMPT},
                {"role": "document", "content": DOCUMENT},
                {"role": "user", "content": user_query},
            ]
        else:
            prompt = [
                {"role": "system", "content": PROMPT},
                {"role": "user", "content": user_query},
            ]
        return prompt
    
    def generator(self,text:str) -> str:
        start_time = datetime.datetime.now()
        logging.info("Generate Start!\t{}".format(start_time))
        prompt = self.build_prompt(text)
        input_ids = self.tokenizer.apply_chat_template(prompt, tokenize=True, add_generation_prompt=True, return_tensors="pt").to(device=self.model.device)
        attention_mask = input_ids.ne(self.tokenizer.pad_token_id).long()
        tokens = self.model.generate(
            input_ids,
            max_length=2048,
            do_sample=False,
            num_beams=1,
            pad_token_id=self.tokenizer.eos_token_id,
            attention_mask=attention_mask,
        )
        out = self.tokenizer.decode(tokens[0][len(input_ids[0]):], skip_special_tokens=True)
        end_time = datetime.datetime.now()
        logging.info("Generate finish!\t{}".format(end_time))
        logging.info("Total: {}".format(end_time - start_time))
        return out.encode("utf8")