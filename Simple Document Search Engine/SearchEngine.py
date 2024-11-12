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
        # Convert text to lowercase and remove punctuation
        text = text.lower().translate(str.maketrans('', '', string.punctuation))
        # Split text into words and remove stop words
        words = [word for word in text.split() if word not in self.stop_words]
        return words

    def index(self, filename, content, index):
        # Preprocess title
        words = self.preprocess_text(content)
        for word in words:
            if word not in index:
                index[word] = set()
            index[word].add(filename)

    def display_index(self):
        # Display the index for debugging purposes
        for word, filenames in self.index.items():
            print(f"{word}: {filenames}")

    def search(self, query, search_type="content"):
        # Preprocess the search query
        words = self.preprocess_text(query)
        # Find matching documents
        matching_documents = set()

        if search_type == "title":
            index = self.title_index
        else:
            index = self.content_index

        for word in words:
            if word in index:
                matching_documents.update(index[word])
        
        # Display results
        results = []
        for filename in matching_documents:
            title = self.documents[filename]["title"]
            # snippet = ' '.join(self.documents[filename]["content"].split()[:30])  # First 30 words as snippet
            results.append((filename, title))
        return results

    def display_results(self, results):
        # Display search results in a readable format
        if not results:
            print("No matching documents found.")
        else:
            for filename, title in results:
                print(f"Document: {filename} - Title: {title}\n")

# Example usage:
search_engine = SearchEngine(directory="Docs")
search_engine.load_documents()
# search_engine.display_index()


# Run a search query
query = "artificial intelligence"
results = search_engine.search(query, search_type="content")
search_engine.display_results(results)

print("------------------")
# search by title
query = "Basics of"
results = search_engine.search(query, search_type="title")
search_engine.display_results(results)