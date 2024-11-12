import unittest
from SearchEngine import SearchEngine

class TestSearchEngine(unittest.TestCase):

    def setUp(self):
        # Initialize SearchEngine with a test directory
        self.search_engine = SearchEngine(directory="Docs")
        self.search_engine.load_documents()

    def test_preprocess_text(self):
        self.assertEqual(
            self.search_engine.preprocess_text("This is a test sentence!"),
            ["test", "sentence"]
        )

    def test_indexing(self):
        self.search_engine.index("doc1.txt", "Artificial Intelligence AI machine learning", self.search_engine.content_index)
        self.assertIn("artificial", self.search_engine.content_index)
        self.assertIn("intelligence", self.search_engine.content_index)

    def test_search_single_word(self):
        results = self.search_engine.search("machine", search_type="content")
        self.assertTrue(any("machine" in doc[1].lower() for doc in results))

    def test_empty_query(self):
        results = self.search_engine.search("", search_type="content")
        self.assertEqual(results, [])

    def test_nonexistent_query(self):
        results = self.search_engine.search("nonexistentword", search_type="content")
        self.assertEqual(results, [])

    def test_search_relevance_order(self):
        results = self.search_engine.search("AI machine learning", search_type="content")
        self.assertTrue(results[0][3] >= results[1][3] if len(results) > 1 else True)

if __name__ == '__main__':
    unittest.main()
