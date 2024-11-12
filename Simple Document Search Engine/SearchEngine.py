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
        current_directory = os.path.dirname(__file__)
        file_path = os.path.join(current_directory, self.directory)
        for filename in os.listdir(file_path):
            if filename.endswith(".txt"):
                with open(os.path.join(file_path, filename), 'r', encoding='utf-8') as file:
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
        word_counts = {}
        
        for word in words:
            word_counts[word] = word_counts.get(word, 0) + 1

        for word, count in word_counts.items():
            if word not in index:
                index[word] = {}
            index[word][filename] = count

    def search(self, query, search_type="content"):
        words = self.preprocess_text(query)
        matching_documents = {}  # Dictionary to store document scores

        index = self.title_index if search_type == "title" else self.content_index
        for word in words:
            if word in index:
                for filename, freq in index[word].items():
                    if filename not in matching_documents:
                        matching_documents[filename] = 0
                    matching_documents[filename] += freq

        # Sort documents by the relevance score (higher score first)
        sorted_results = sorted(matching_documents.items(), key=lambda item: item[1], reverse=True)
        
        results = []
        for filename, score in sorted_results:
            title = self.documents[filename]["title"]
            snippet = ' '.join(self.documents[filename]["content"].split()[:20])  # First 20 words as snippet
            snippet+="........."
            results.append((filename, title, snippet, score))
        return results

    def display_results(self, results):
        if not results:
            print("\nNo matching documents found. Try different keywords.")
        else:
            print("\nSearch Results:")
            for filename, title, snippet, score in results:
                print(f"\nDocument: {filename}\nTitle: {title}\nSnippet: {snippet}\nRelevance Score: {score}\n")

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
if __name__ == '__main__':
    search_engine = SearchEngine(directory="Docs")
    search_engine.load_documents()
    search_engine.interactive_search()
