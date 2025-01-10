from nlp_model import refine_query
from scraping_model import scrape_all_websites

def main():
    print("Welcome to the AI-Powered Search Engine!")
    user_input = input("Enter your course search query: ")

    # Step 1: NLP Processing
    refined = refine_query(user_input)
    print("\n--- NLP Output ---")
    print(f"Original Query: {refined['original_query']}")
    print(f"Preprocessed Query: {refined['preprocessed_query']}")
    print(f"Intent: {refined['intent']}")

    # Step 2: Web Scraping
    print("\n--- Scraping Results ---")
    results = scrape_all_websites(refined['preprocessed_query'])
    for site, data in results.items():
        print(f"\nResults from {site}:")
        if isinstance(data, list):
            for idx, item in enumerate(data, start=1):
                print(f"{idx}. {item}")
        else:
            print(data)

if __name__ == "__main__":
    main()
