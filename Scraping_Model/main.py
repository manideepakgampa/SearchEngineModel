from nlp_model import refine_query
from scraping_model import initialize_driver, open_tabs, real_time_scraping
import time
def main():
    """Main function for managing the scraping process."""
    user_input = input("Enter your course search query: ")
    refined_query = refine_query(user_input)  # Process input using NLP
    query = refined_query["preprocessed_query"]
    print(f"\nRefined Query: {query}\n")
    
    driver = initialize_driver()
    try:
        tabs = open_tabs(driver, query)  # Open tabs for websites
        real_time_scraping(driver, tabs)  # Scrape data from each tab
    except Exception as e:
        print(f"Error during scraping: {e}")
    finally:
        print("Tabs are open. You can interact with the browser.")
        print("Close the browser when done.")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nClosing browser...")
            driver.quit()

if __name__ == "__main__":
    main()
