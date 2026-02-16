from collections import defaultdict
from qdrant_client import QdrantClient

from .config import COLLECTION_NAME, DB_PATH
from .embed import embed_text

THRESHOLD = 0.0

def run_search():
    client = QdrantClient(path=DB_PATH)

    user_query = input("\nEnter required skills: ")

    if not user_query.strip():
        print("No query entered.")
        return

    query_vector = embed_text([user_query])[0]

    hits = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,
        limit=100,
        with_payload=True
    ).points

    scores = defaultdict(float)

    for hit in hits:
        cv_id = hit.payload["cv_id"]
        if hit.score > scores[cv_id]:
            scores[cv_id] = hit.score

    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)

    final = ranked


    matching_ids = [cv_id for cv_id, _ in final]

    if matching_ids:
        reasoning = "; ".join(
            [f"{cv_id} score {round(score, 3)}" for cv_id, score in final]
        )
    else:
        reasoning = "No strong matches found."

    result = {
        "matching_cv_ids": matching_ids,
        "reasoning": reasoning
    }

    print("\nRESULT:")
    print(result)
