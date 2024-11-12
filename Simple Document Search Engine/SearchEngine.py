import os
import string

class SearchEngine:
    def __init__(self, directory):
        self.directory = directory
        self.documents = {}  # Stores document title and content
        self.content_index = {}    # Index for content words
        self.title_index = {}      # Index for title words
        self.stop_words = set([
            "a", "an", "and", "are", "as", "at", "be", "but", "by", "for", "if", 
            "in", "into", "is", "it", "no", "not", "of", "on", "or", "such", 
            "that", "the", "their", "then", "there", "these", "they", "this", 
            "to", "was", "will", "with"
        ])

    def load_documents(self):
        for filename in os.listdir(self.directory):
            if filename.endswith(".txt"):
                with open(os.path.join(self.directory, filename), 'r', encoding='utf-8') as file:
                    doc = file.read().split("\n", 1)
                    title = doc[0].replace("Title: ", "")
                    content = doc[1].replace("Content: ", "")
                    self.documents[filename] = {
                        "title": title,
                        "content": content
                    }
                    # Index both title and content
                    self.index(filename, title, self.title_index)
                    self.index(filename, content, self.content_index)

    def preprocess_text(self, text):
        text = text.lower().translate(str.maketrans('', '', string.punctuation))
        words = [word for word in text.split() if word not in self.stop_words]
        return words

    def index(self, filename, content, index):
        words = self.preprocess_text(content)
        for word in words:
            if word not in index:
                index[word] = set()
            index[word].add(filename)

    def search(self, query, search_type="content"):
        words = self.preprocess_text(query)
        matching_documents = set()

        index = self.title_index if search_type == "title" else self.content_index
        for word in words:
            if word in index:
                matching_documents.update(index[word])

        results = []
        for filename in matching_documents:
            title = self.documents[filename]["title"]
            snippet = ' '.join(self.documents[filename]["content"].split()[:20])  # First 20 words as snippet
            snippet+="........."
            results.append((filename, title, snippet))
        return results

    def display_results(self, results):
        if not results:
            print("\nNo matching documents found. Try different keywords.")
        else:
            print("\nSearch Results:")
            for filename, title, snippet in results:
                print(f"\nDocument: {filename}\nTitle: {title}\nSnippet: {snippet}\n")

    def interactive_search(self):
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
search_engine = SearchEngine(directory="Docs")
search_engine.load_documents()
search_engine.interactive_search()
