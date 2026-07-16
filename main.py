import sys
from ingest import run_ingestion
from rag import ask_with_rag

def main():
    print("--- GovSchemesHub RAG System ---")
    if len(sys.argv) > 1 and sys.argv[1] == "ingest":
        print("Starting ingestion...")
        run_ingestion()
    else:
        # Default query for testing
        query = "What is the eligibility criteria for the PM-KISAN scheme?"
        
        # If user provides a query in quotes as an argument, use that
        if len(sys.argv) > 1 and sys.argv[1] != "ingest":
            query = sys.argv[1]

        print(f"\nUser Query: {query}")
        print("Generating response...")
        response = ask_with_rag(query)
        print("\n--- LLM Response ---")
        print(response)
        print("--------------------")

if __name__ == "__main__":
    main()