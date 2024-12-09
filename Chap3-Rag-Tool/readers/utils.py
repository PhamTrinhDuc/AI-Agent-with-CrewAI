def split_text(text: str, max_tokens: int) -> list[str]:
    words = text.split() # Tokenize by spaces and newlines
    chunks = []
    curr_chunk = []
    curr_token_cnt = 0

    for word in words:
        token_count = len(word.split()) # Number of tokens in the word


        # If adding the current word exceeds max_tokens, finalize the current chunk
        if curr_token_cnt + token_count > max_tokens:
            chunks.append(" ".join(curr_chunk))
            curr_chunk = [word] # Start a new chunk with the current word
            curr_token_cnt = token_count
        else:
            curr_chunk.append(word)
            curr_token_cnt += token_count
    
    # Add the final chunk if any tokens are left
    if curr_chunk:
        chunks.append(" ".join(curr_chunk))
    return chunks