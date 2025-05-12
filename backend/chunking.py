from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")  # You can change the model if needed

def split_text_into_chunks(text: str, max_tokens: int = 200, overlap_tokens: int = 50) -> list[str]:
    sentences = text.split('. ') 
    chunks = []
    current_chunk = []
    current_tokens = 0

    for sentence in sentences:
        token_count = len(tokenizer.encode(sentence, add_special_tokens=False))

        if current_tokens + token_count <= max_tokens:
            current_chunk.append(sentence)
            current_tokens += token_count
        else:
            chunks.append(". ".join(current_chunk) + ".")
            if overlap_tokens > 0:
                overlap_content = tokenizer.encode(". ".join(current_chunk), add_special_tokens=False)[-overlap_tokens:]
                current_chunk = [tokenizer.decode(overlap_content), sentence]
                current_tokens = len(tokenizer.encode(" ".join(current_chunk), add_special_tokens=False))
            else:
                current_chunk = [sentence]
                current_tokens = token_count

    if current_chunk:
        chunks.append(". ".join(current_chunk) + ".")

    return chunks
