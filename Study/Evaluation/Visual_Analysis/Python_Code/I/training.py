from transformers import GPT2Tokenizer, GPT2LMHeadModel

# Deutsches GPT-2 Modell und Tokenizer laden
tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
model = GPT2LMHeadModel.from_pretrained('dbmdz/german-gpt2')
