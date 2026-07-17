# test_db.py

import unittest
from peewee import *

from app import TimelinePost


MODELS = [TimelinePost]

# Use an in-memory SQLite database for tests.
test_db = SqliteDatabase(":memory:")


class TestTimelinePost(unittest.TestCase):

    def setUp(self):
        # Bind model classes to the test database.
        test_db.bind(
            MODELS,
            bind_refs=False,
            bind_backrefs=False
        )

        test_db.connect()
        test_db.create_tables(MODELS)

    def tearDown(self):
        # Delete the test tables and close the database connection.
        test_db.drop_tables(MODELS)
        test_db.close()

    def test_timeline_post(self):
        # Create two timeline posts.
        first_post = TimelinePost.create(
            name="John Doe",
            email="john@example.com",
            content="Hello world, I'm John!"
        )

        assert first_post.id == 1

        second_post = TimelinePost.create(
            name="Jane Doe",
            email="jame@example.com",
            content="Hello world, I'm Jane!"
        )

        assert second_post.id == 2

        # Get timeline posts and verify that they are correct.
        posts = list(TimelinePost.select().order_by(TimelinePost.id))

        self.assertEqual(len(posts), 2)

        self.assertEqual(posts[0].name, "John Doe")
        self.assertEqual(posts[0].email, "john@example.com")
        self.assertEqual(posts[0].content, "Hello world, I'm John!")

        self.assertEqual(posts[1].name, "Jane Doe")
        self.assertEqual(posts[1].email, "jame@example.com")
        self.assertEqual(posts[1].content, "Hello world, I'm Jane!")


if __name__ == "__main__":
    unittest.main()