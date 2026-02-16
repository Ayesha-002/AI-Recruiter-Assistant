import os
import uuid
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct

from .config import DATA_FOLDER, COLLECTION_NAME, VECTOR_SIZE, DB_PATH
from .extract import extract_text
from .embed import embed_text

def chunk_text(text, chunk_size=1000, overlap=200):
    chunks = []
    i = 0
    while i < len(text):
        chunks.append(text[i:i+chunk_size])
        i += chunk_size - overlap
    return chunks

def run_indexing():
    client = QdrantClient(path=DB_PATH)

    if COLLECTION_NAME not in [c.name for c in client.get_collections().collections]:
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=VECTOR_SIZE, distance=Distance.COSINE),
        )

    print("Indexing CVs...")

    for file in os.listdir(DATA_FOLDER):
        if file.endswith(".pdf"):
            cv_id = file.replace(".pdf", "")
            text = extract_text(os.path.join(DATA_FOLDER, file))
            chunks = chunk_text(text)
            vectors = embed_text(chunks)

            points = []
            for chunk, vector in zip(chunks, vectors):
                points.append(
                    PointStruct(
                        id=str(uuid.uuid4()),
                        vector=vector,
                        payload={"cv_id": cv_id},
                    )
                )

            client.upsert(collection_name=COLLECTION_NAME, points=points)

    print("Indexing complete.")
