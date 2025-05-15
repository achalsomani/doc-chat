import tiktoken

tokenizer = tiktoken.encoding_for_model("text-embedding-3-small")

def split_text_into_chunks(text: str, max_tokens: int = 200, overlap_tokens: int = 50) -> list[str]:
    sentences = text.split(". ")
    chunks, current_chunk, current_tokens = [], [], 0

    for idx, sentence in enumerate(sentences):
        tokens = tokenizer.encode(sentence)
        token_count = len(tokens)

        if current_tokens + token_count <= max_tokens:
            current_chunk.append(sentence)
            current_tokens += token_count
        else:
            chunks.append(". ".join(current_chunk) + ".")
            if overlap_tokens > 0:
                overlap_sentences = sentences[max(0, idx - 1):idx]
                current_chunk = overlap_sentences + [sentence]
                current_tokens = sum(len(tokenizer.encode(s)) for s in current_chunk)
            else:
                current_chunk = [sentence]
                current_tokens = token_count

    if current_chunk:
        chunks.append(". ".join(current_chunk) + ".")

    return chunks
