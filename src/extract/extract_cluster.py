import nltk
from sentence_transformers import SentenceTransformer
from sklearn.cluster import AgglomerativeClustering
import json

# Download the NLTK tokenizer if not already downloaded
nltk.download('punkt_tab')

def read_text_file(file_path):
    """
    Reads the content of a .txt file.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def chunk_by_topic(text,  num_topics):
    model = SentenceTransformer('all-MiniLM-L6-v2')  # A lightweight transformer model
    sentences = nltk.sent_tokenize(text)

    # Compute embeddings for all sentences
    indexed_sentences = [(i, s) for i, s in enumerate(sentences)]
    embeddings = model.encode([s for _, s in indexed_sentences])

    # Perform clustering
    clustering_model = AgglomerativeClustering(n_clusters=num_topics, metric='euclidean', linkage='ward')
    clustering_labels = clustering_model.fit_predict(embeddings)


    # Group sentences by semantic similarity
    topic_chunks = {}
    for (index, sentence), label in zip(indexed_sentences, clustering_labels):
        if label not in topic_chunks:
            topic_chunks[label] = []
        topic_chunks[label].append((index, sentence))

    # Convert clusters to a structured list
    chunks = []
    for label, sentences_with_indices in topic_chunks.items():
        sentences_with_indices.sort()
        sentences = [s for _, s in sentences_with_indices]
        print(label)
        print(sentences)
        chunks.append({
            "topic": f"Storage",
            "subtopic": f"Topic {label+1}",  # Placeholder topic names
            "text": " ".join(sentences)
        })

    return chunks


text_file_path = "src/documentation/Storage.txt"

# Example usage
if __name__ == "__main__":
    # Replace with your .txt file path
    output_file = 'src/cluster_chunks.json'
    text_file_path = "src/documentation/Storage.txt"

    try:
        text = read_text_file(text_file_path)
        chunks = chunk_by_topic(text, 7)
        print(f"Extracted {len(chunks)} chunks from the text file.")

        # Write chunks to a new JSON file
        with open(output_file, 'w', encoding='utf-8') as file:
            json.dump(chunks, file, indent=4)
    except FileNotFoundError:
        print(f"Text file not found: {text_file_path}")
