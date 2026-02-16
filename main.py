import sys
from src.indexer import run_indexing
from src.search import run_search

if "--index" in sys.argv:
    run_indexing()

elif "--search" in sys.argv:
    run_search()

else:
    print("Use:")
    print("python main.py --index")
    print("python main.py --search")
