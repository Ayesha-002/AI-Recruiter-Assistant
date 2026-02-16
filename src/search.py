from collections import defaultdict
from qdrant_client import QdrantClient

from .config import COLLECTION_NAME, DB_PATH
from .embed import embed_text

TOP_K = 5
MIN_SCORE = 0.10

def extract_keywords(query):
    return [word.lower() for word in query.split() if len(word) > 3]

def run_search():
    client = QdrantClient(path=DB_PATH)

    user_query = input("\nEnter required skills: ").strip()

    if not user_query:
        print("No query entered.")
        return

    query_vector = embed_text([user_query])[0]
    keywords = extract_keywords(user_query)

    hits = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,
        limit=100,
        with_payload=True
    ).points

    scores = defaultdict(float)
    text_map = {}

    for hit in hits:
        cv_id = hit.payload["cv_id"]
        score = hit.score
        full_text = hit.payload.get("full_text", "")

        # Keep highest score
        if score > scores[cv_id]:
            scores[cv_id] = score
            text_map[cv_id] = full_text

    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)

    filtered = []

    for cv_id, score in ranked:
        full_text = text_map.get(cv_id, "")

        if not full_text:
            continue

        match_count = sum(keyword in full_text for keyword in keywords)

        if match_count >= 1 and score >= MIN_SCORE:
            filtered.append((cv_id, score))


    final = [
        (cv_id, round(score * 100, 2))
        for cv_id, score in filtered[:TOP_K]
    ]

    matching_ids = [cv_id for cv_id, _ in final]

    if matching_ids:
        reasoning = "; ".join(
            [f"{cv_id} match {score}%" for cv_id, score in final]
        )
    else:
        reasoning = "No strong matches found."

    result = {
        "matching_cv_ids": matching_ids,
        "reasoning": reasoning
    }

    print("\nRESULT:")
    print(result)
