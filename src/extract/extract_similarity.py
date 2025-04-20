import nltk
from sentence_transformers import SentenceTransformer, util
import json

# Download the NLTK tokenizer if not already downloaded
nltk.download('punkt_tab')

def read_text_file(file_path):
    """
    Reads the content of a .txt file.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def chunk_by_topic(text,  similarity_threshold=0.3):
    model = SentenceTransformer('all-MiniLM-L6-v2')  # A lightweight transformer model
    sentences = nltk.sent_tokenize(text)
    print(sentences)

    # Compute embeddings for all sentences
    # embeddings = model.encode(sentences, convert_to_tensor=True)
    clusters = []
    current_cluster = [sentences[0]]
    print(current_cluster)
    for i in range(1, len(sentences)):
        similarity = util.pytorch_cos_sim(
            model.encode(current_cluster[-1], convert_to_tensor=True),
            model.encode(sentences[i], convert_to_tensor=True)
        ).item()
        print("similarity", similarity)
        if similarity >= similarity_threshold:
            current_cluster.append(sentences[i])
        else:
            clusters.append(" ".join(current_cluster))
            current_cluster = [sentences[i]]
        print("crret cluster", current_cluster)
    if current_cluster:
        clusters.append(" ".join(current_cluster))

    print("clusters ", clusters)
    chunks = []
    for idx, cluster in enumerate(clusters):
        print(f"sentence_{idx+1}: {cluster}")
        chunks.append({
            "name": f"sentence_{idx+1}",
            "topic": f"Storage",  # Replace this with actual topic detection if available
            "text": cluster
        })

    return chunks

# def chunk_text(text, max_chunk_size=512):
#     """
#     Splits text into chunks of a specified maximum size.
#     Each chunk will be approximately `max_chunk_size` words.
#     """
#     sentences = sent_tokenize(text)
#     chunks = []
#     current_chunk = []
#
#     current_length = 0
#     for sentence in sentences:
#         sentence_length = len(sentence.split())
#         if current_length + sentence_length > max_chunk_size:
#             # If adding the current sentence exceeds max size, save the current chunk
#             chunks.append(" ".join(current_chunk))
#             current_chunk = [sentence]  # Start a new chunk
#             current_length = sentence_length
#         else:
#             current_chunk.append(sentence)
#             current_length += sentence_length
#
#     # Add the last chunk if it contains any text
#     if current_chunk:
#         chunks.append(" ".join(current_chunk))
#
#     return chunks
#
# def process_text_file_to_chunks(file_path, max_chunk_size=512):
#     """
#     Processes a .txt file and returns chunks of text.
#     """
#     text = read_text_file(file_path)
#     chunks = chunk_by_topic(text, max_chunk_size)
#     return chunks

# Example usage
if __name__ == "__main__":
    # Replace with your .txt file path
    text_file_path = "src/documentation/extracted_md.md"

    try:
        output_file = 'src/similarity_chunks.json'
        text = read_text_file(text_file_path)
        chunks = chunk_by_topic(text)
        print(f"Extracted {len(chunks)} chunks from the text file.")

        # Write chunks to a new JSON file
        with open(output_file, 'w', encoding='utf-8') as file:
            json.dump(chunks, file, indent=4)
    except FileNotFoundError:
        print(f"Text file not found: {text_file_path}")
