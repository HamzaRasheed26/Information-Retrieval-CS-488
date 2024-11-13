import os
import string
from Dictionary import CustomDictionary

class SearchEngine:
    """
    A simple document search engine that indexes and searches text files in a specified directory.

    Attributes:
        directory (str): Directory containing the text documents.
        documents (dict): Stores document title and content.
        content_index (dict): Index for content-based word search.
        title_index (dict): Index for title-based word search.
        stop_words (set): Common stop words to exclude from indexing.
    """
    def __init__(self, directory):
        """
        Initializes the search engine with the directory to load documents from.

        Args:
            directory (str): Directory path containing text files to be indexed.
        """
        self.directory = directory
        self.documents = CustomDictionary()  # Stores document title and content
        self.content_index = CustomDictionary()    # Index for content words
        self.title_index = CustomDictionary()      # Index for title words
        self.stop_words = set([
            "a", "an", "and", "are", "as", "at", "be", "but", "by", "for", "if", 
            "in", "into", "is", "it", "no", "not", "of", "on", "or", "such", 
            "that", "the", "their", "then", "there", "these", "they", "this", 
            "to", "was", "will", "with", "from"
        ]) # Stop words to reomve

    def load_documents(self):
        """
        Loads documents from the directory, reading titles and contents, and indexes them by title and content.
        """
        file_path = os.path.join(os.path.dirname(__file__), self.directory)
        for filename in os.listdir(file_path):
            if filename.endswith(".txt"): # Reading .txt files
                with open(os.path.join(file_path, filename), 'r', encoding='utf-8') as file:
                    # Arranging the text in the file
                    doc = file.read().split("\n", 1)
                    title = doc[0].replace("Title: ", "")
                    content = doc[1].replace("Content: ", "")
                    self.documents.insert(filename, {"title": title, "content": content})
                    # Index both title and content
                    self.index(filename, title, self.title_index)
                    self.index(filename, content, self.content_index)

    def preprocess_text(self, text):
        """
        Converts text to lowercase, removes punctuation, and excludes stop words.

        Args:
            text (str): The text to be processed.
        
        Returns:
            list: List of processed words.
        """
        text = text.lower().translate(str.maketrans('', '', string.punctuation))
        words = [word for word in text.split() if word not in self.stop_words]
        return words

    def index(self, filename, content, index):
        """
        Indexes words from the content, storing their frequencies.

        Args:
            filename (str): The document filename.
            content (str): The document content.
            index (dict): The index to update (title or content index).
        """
        words = self.preprocess_text(content)
        word_counts = {}
        
        # Count how many times each word occur in one file
        for word in words:
            word_counts[word] = word_counts.get(word, 0) + 1

        # Creating the index word by word with thier filename and count
        for word, count in word_counts.items():
            try:
                existing = index.get(word)
            except KeyError:
                existing = CustomDictionary()
                index.insert(word, existing)
            existing.insert(filename, count)

    def search(self, query, search_type="content"):
        """
        Searches for the query in the specified index and ranks results by relevance score.

        Args:
            query (str): The search query.
            search_type (str): Either 'content' or 'title', determining the search index.

        Returns:
            list: Sorted list of matching documents with filenames, titles, snippets, and scores.
        """
        words = self.preprocess_text(query)
        matching_documents = CustomDictionary() # Dictionary to store document scores

        # Selecting the index base on search type
        index = self.title_index if search_type == "title" else self.content_index
        # for word in words:
        #     if word in index:
        #         # Finding the word in index and getting the filenames and counts in which it exist
        #         for filename, freq in index[word].items(): 
        #             if filename not in matching_documents:
        #                 matching_documents[filename] = 0
        #             matching_documents[filename] += freq # Caculating the relevance score

        for word in words:
            try:
                docs_with_word = index.get(word)
                for filename, freq in docs_with_word.items():  # Use items() to get key-value pairs
                    try:
                        score = matching_documents.get(filename) + freq
                        matching_documents.insert(filename, score)
                    except KeyError:
                        matching_documents.insert(filename, freq)
            except KeyError:
                continue

        # Sort documents by the relevance score (higher score first)
        sorted_results = sorted(
            [(filename, score) for filename, score in matching_documents.items() if filename],
            key=lambda item: item[1], reverse=True
        )
        
        results = []
        for filename, score in sorted_results:
            doc = self.documents.get(filename)
            title = doc["title"]
            snippet = ' '.join(doc["content"].split()[:15]) + "........."  # First 15 words as snippet
            results.append((filename, title, snippet, score))
        return results

    def display_results(self, results):
        """
        Displays search results in a user-friendly format with relevance scores.

        Args:
            results (list): List of tuples with filename, title, snippet, and score.
        """
        if not results:
            print("\nNo matching documents found. Try different keywords.")
        else:
            print("\nSearch Results:")
            print(f"Total Documents found: {len(results)}")
            print("=======================================================================")
            for filename, title, snippet, score in results:
                print(f"\nDocument: {filename}\nTitle: {title}\nSnippet: {snippet}\nRelevance Score: {score}\n")
                print("=======================================================================")
    

    def searchUI(self):
        """
        Provides an interactive command-line menu for searching by content or title.
        """
        while True:
            # Clearing the Screen
            os.system('cls')
            print("\n--- Document Search Engine ---")
            print("1. Search by Content")
            print("2. Search by Title")
            print("3. Exit")
            choice = input("Enter your choice (1/2/3): ")

            if choice == "3":
                print("Exiting the search engine. Goodbye!")
                break
            elif choice in ["1", "2"]:
                search_type = "content" if choice == "1" else "title"
                query = input("Enter your search query: ").strip()
                if query:
                    results = self.search(query, search_type=search_type)
                    self.display_results(results)
                else:
                    print("Query cannot be empty. Please enter a valid search term.")
                input("Press any key to continue.......")
            else:
                print("Invalid choice. Please enter 1, 2, or 3.")

# Example usage
if __name__ == '__main__':
    search_engine = SearchEngine(directory="Docs")
    search_engine.load_documents()
    search_engine.searchUI()
