### main.py

from scraping_model import initialize_driver, open_tabs, real_time_scraping
from nlp_model import refine_query

def main():
    """Main function to handle user input, process it, and scrape data."""
    user_input = input("Enter your course search query: ")

    # Process the query through the NLP model
    refined_query = refine_query(user_input)
    print(f"Refined Query: {refined_query}")

    # Initialize the web driver
    driver = initialize_driver()

    # Open websites with refined query
    tabs = open_tabs(driver, refined_query)

    print("All tabs are open. You can interact with the browser.")
    print("Close individual tabs manually or close the browser to exit.")

    try:
        while True:
            command = input("Enter 'scrape' to scrape data or 'exit' to close: ").strip().lower()
            if command == 'scrape':
                real_time_scraping(driver, tabs)
            elif command == 'exit':
                break
    except KeyboardInterrupt:
        print("\nExiting...")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
