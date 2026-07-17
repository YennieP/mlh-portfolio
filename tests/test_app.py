# tests/test_app.py

import os
import unittest

# Set testing mode before importing the Flask app.
os.environ["TESTING"] = "true"

from app import app, mydb, TimelinePost


class YanxiPortfolioTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """
        Runs once before all tests.
        """
        app.config["TESTING"] = True

        if mydb.is_closed():
            mydb.connect()

        mydb.create_tables([TimelinePost], safe=True)

    def setUp(self):
        """
        Runs before each individual test.
        """
        self.client = app.test_client()

        # Start each test with an empty timeline table.
        TimelinePost.delete().execute()

    def tearDown(self):
        """
        Runs after each individual test.
        """
        TimelinePost.delete().execute()

    @classmethod
    def tearDownClass(cls):
        """
        Runs once after all tests finish.
        """
        mydb.drop_tables([TimelinePost], safe=True)

        if not mydb.is_closed():
            mydb.close()

    # Home page tests
    def test_home_page_returns_200(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)

    def test_home_page_contains_yanxi_profile(self):
        response = self.client.get("/")
        html = response.get_data(as_text=True)

        self.assertIn("Yanxi Pan", html)

    def test_home_page_links_to_yanxi_page(self):
        response = self.client.get("/")
        html = response.get_data(as_text=True)

        self.assertIn('href="/yanxi"', html)

    def test_home_page_contains_yanxi_profile_image(self):
        response = self.client.get("/")
        html = response.get_data(as_text=True)

        self.assertIn("Yanxi_profile.jpg", html)

    # Yennie main portfolio page tests
    def test_yanxi_page_returns_200(self):
        response = self.client.get("/yanxi")

        self.assertEqual(response.status_code, 200)

    def test_yanxi_page_contains_work_experience(self):
        response = self.client.get("/yanxi")
        html = response.get_data(as_text=True)

        self.assertIn("Fanfic Assistant", html)
        self.assertIn("Full-Stack Developer", html)

    def test_yanxi_page_contains_sql_buddy_experience(self):
        response = self.client.get("/yanxi")
        html = response.get_data(as_text=True)

        self.assertIn("SQL Buddy", html)
        self.assertIn("Backend Developer", html)

    def test_yanxi_page_contains_research_experience(self):
        response = self.client.get("/yanxi")
        html = response.get_data(as_text=True)

        self.assertIn(
            "NLP Semantic Understanding in M2M Communication",
            html
        )

        self.assertIn("Research Assistant", html)

    def test_yanxi_page_contains_medical_dialogue_project(self):
        response = self.client.get("/yanxi")
        html = response.get_data(as_text=True)

        self.assertIn("LLM Medical Dialogue Platform", html)
        self.assertIn("LLM Engineer", html)

    def test_yanxi_page_contains_education(self):
        response = self.client.get("/yanxi")
        html = response.get_data(as_text=True)

        self.assertIn(
            "Northeastern University - Silicon Valley",
            html
        )

        self.assertIn(
            "Master of Science in Computer Science",
            html
        )

        self.assertIn(
            "Beijing Normal University",
            html
        )

    def test_yanxi_page_contains_navigation_links(self):
        response = self.client.get("/yanxi")
        html = response.get_data(as_text=True)

        self.assertIn("About Me", html)
        self.assertIn("Hobbies", html)
        self.assertIn("Places", html)
        self.assertIn("Timeline", html)

    # Yennie hobbies page tests
    def test_yanxi_hobbies_page_returns_200(self):
        response = self.client.get("/yanxi/hobbies")

        self.assertEqual(response.status_code, 200)

    def test_yanxi_hobbies_page_contains_music(self):
        response = self.client.get("/yanxi/hobbies")
        html = response.get_data(as_text=True)

        self.assertIn("Listening to Music", html)

    def test_yanxi_hobbies_page_contains_singing(self):
        response = self.client.get("/yanxi/hobbies")
        html = response.get_data(as_text=True)

        self.assertIn("Singing", html)

    def test_yanxi_hobbies_page_contains_sims(self):
        response = self.client.get("/yanxi/hobbies")
        html = response.get_data(as_text=True)

        self.assertIn("Playing The Sims 4", html)

    def test_yanxi_hobbies_page_contains_writing(self):
        response = self.client.get("/yanxi/hobbies")
        html = response.get_data(as_text=True)

        self.assertIn("Writing", html)
        self.assertIn("fan fiction", html)

    def test_yanxi_hobbies_page_contains_drawing(self):
        response = self.client.get("/yanxi/hobbies")
        html = response.get_data(as_text=True)

        self.assertIn("Drawing", html)

    def test_yanxi_hobbies_page_contains_badminton(self):
        response = self.client.get("/yanxi/hobbies")
        html = response.get_data(as_text=True)

        self.assertIn("Badminton", html)

    def test_yanxi_hobbies_page_contains_hobby_images(self):
        response = self.client.get("/yanxi/hobbies")
        html = response.get_data(as_text=True)

        self.assertIn("Yanxi_listening_to_music.jpg", html)
        self.assertIn("Yanxi_singing.jpg", html)
        self.assertIn("Yanxi_Sims4.jpg", html)
        self.assertIn("Yanxi_writing.jpg", html)
        self.assertIn("Yanxi_drawing.jpg", html)
        self.assertIn("Yanxi_badminton.jpg", html)

    # Yanxi places page tests
    def test_yanxi_places_page_returns_200(self):
        response = self.client.get("/yanxi/places")

        self.assertEqual(response.status_code, 200)

    def test_yanxi_places_page_contains_russia(self):
        response = self.client.get("/yanxi/places")
        html = response.get_data(as_text=True)

        self.assertIn("Russia", html)

    def test_yanxi_places_page_contains_japan(self):
        response = self.client.get("/yanxi/places")
        html = response.get_data(as_text=True)

        self.assertIn("Japan", html)

    def test_yanxi_places_page_contains_thailand(self):
        response = self.client.get("/yanxi/places")
        html = response.get_data(as_text=True)

        self.assertIn("Thailand", html)

    def test_yanxi_places_page_contains_united_states(self):
        response = self.client.get("/yanxi/places")
        html = response.get_data(as_text=True)

        self.assertIn("United States", html)

    def test_yanxi_places_page_contains_china(self):
        response = self.client.get("/yanxi/places")
        html = response.get_data(as_text=True)

        self.assertIn("China", html)

    def test_yanxi_places_page_contains_european_locations(self):
        response = self.client.get("/yanxi/places")
        html = response.get_data(as_text=True)

        self.assertIn("Hungary", html)
        self.assertIn("Germany", html)

    def test_yanxi_places_page_contains_map_coordinates(self):
        response = self.client.get("/yanxi/places")
        html = response.get_data(as_text=True)

        # Test a few coordinates passed to the map template.
        self.assertIn("55.7558", html)
        self.assertIn("35.6762", html)
        self.assertIn("13.7563", html)

    # Timeline page tests
    def test_timeline_page_returns_200(self):
        response = self.client.get("/timeline")

        self.assertEqual(response.status_code, 200)

    def test_timeline_page_contains_timeline_title(self):
        response = self.client.get("/timeline")
        html = response.get_data(as_text=True)

        self.assertIn("Timeline", html)

    def test_timeline_page_contains_yanxi_navigation(self):
        response = self.client.get("/timeline")
        html = response.get_data(as_text=True)

        self.assertIn("About Me", html)
        self.assertIn("Hobbies", html)
        self.assertIn("Places", html)
        self.assertIn("Timeline", html)

    # Timeline GET API tests
    def test_get_timeline_returns_200(self):
        response = self.client.get("/api/timeline_post")

        self.assertEqual(response.status_code, 200)

    def test_get_timeline_returns_json(self):
        response = self.client.get("/api/timeline_post")

        self.assertTrue(response.is_json)

    def test_get_timeline_has_timeline_posts_key(self):
        response = self.client.get("/api/timeline_post")
        data = response.get_json()

        self.assertIn("timeline_posts", data)

    def test_get_timeline_is_empty_initially(self):
        response = self.client.get("/api/timeline_post")
        data = response.get_json()

        self.assertEqual(data["timeline_posts"], [])

    def test_get_timeline_returns_existing_post(self):
        TimelinePost.create(
            name="Yanxi Pan",
            email="yanxi@example.com",
            content="Welcome to my portfolio timeline!"
        )

        response = self.client.get("/api/timeline_post")
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data["timeline_posts"]), 1)

        post = data["timeline_posts"][0]

        self.assertEqual(post["name"], "Yanxi Pan")
        self.assertEqual(post["email"], "yanxi@example.com")
        self.assertEqual(
            post["content"],
            "Welcome to my portfolio timeline!"
        )

    def test_get_timeline_returns_multiple_posts(self):
        TimelinePost.create(
            name="First Visitor",
            email="first@example.com",
            content="First timeline post"
        )

        TimelinePost.create(
            name="Second Visitor",
            email="second@example.com",
            content="Second timeline post"
        )

        response = self.client.get("/api/timeline_post")
        data = response.get_json()

        self.assertEqual(len(data["timeline_posts"]), 2)

    def test_get_timeline_orders_newest_post_first(self):
        first_post = TimelinePost.create(
            name="First Visitor",
            email="first@example.com",
            content="Older post"
        )

        second_post = TimelinePost.create(
            name="Second Visitor",
            email="second@example.com",
            content="Newer post"
        )

        response = self.client.get("/api/timeline_post")
        data = response.get_json()
        posts = data["timeline_posts"]

        self.assertEqual(len(posts), 2)
        self.assertEqual(posts[0]["id"], second_post.id)
        self.assertEqual(posts[1]["id"], first_post.id)

    # Timeline POST API tests
    def test_create_timeline_post_returns_200(self):
        response = self.client.post(
            "/api/timeline_post",
            data={
                "name": "Portfolio Visitor",
                "email": "visitor@example.com",
                "content": "Yanxi has a great portfolio!"
            }
        )

        self.assertEqual(response.status_code, 200)

    def test_create_timeline_post_returns_json(self):
        response = self.client.post(
            "/api/timeline_post",
            data={
                "name": "Portfolio Visitor",
                "email": "visitor@example.com",
                "content": "Yanxi has a great portfolio!"
            }
        )

        self.assertTrue(response.is_json)

    def test_create_timeline_post_returns_correct_data(self):
        response = self.client.post(
            "/api/timeline_post",
            data={
                "name": "Portfolio Visitor",
                "email": "visitor@example.com",
                "content": "Great work on your projects!"
            }
        )

        data = response.get_json()

        self.assertEqual(data["name"], "Portfolio Visitor")
        self.assertEqual(data["email"], "visitor@example.com")
        self.assertEqual(
            data["content"],
            "Great work on your projects!"
        )

        self.assertIn("id", data)
        self.assertIn("created_at", data)

    def test_create_timeline_post_saves_to_database(self):
        self.client.post(
            "/api/timeline_post",
            data={
                "name": "Portfolio Visitor",
                "email": "visitor@example.com",
                "content": "Saved timeline post"
            }
        )

        self.assertEqual(TimelinePost.select().count(), 1)

        saved_post = TimelinePost.get()

        self.assertEqual(saved_post.name, "Portfolio Visitor")
        self.assertEqual(
            saved_post.email,
            "visitor@example.com"
        )
        self.assertEqual(
            saved_post.content,
            "Saved timeline post"
        )

    def test_created_post_appears_in_get_request(self):
        self.client.post(
            "/api/timeline_post",
            data={
                "name": "Portfolio Visitor",
                "email": "visitor@example.com",
                "content": "Created through the POST endpoint"
            }
        )

        response = self.client.get("/api/timeline_post")
        data = response.get_json()

        self.assertEqual(len(data["timeline_posts"]), 1)

        self.assertEqual(
            data["timeline_posts"][0]["content"],
            "Created through the POST endpoint"
        )

    def test_multiple_posts_have_different_ids(self):
        first_response = self.client.post(
            "/api/timeline_post",
            data={
                "name": "First Visitor",
                "email": "first@example.com",
                "content": "First post"
            }
        )

        second_response = self.client.post(
            "/api/timeline_post",
            data={
                "name": "Second Visitor",
                "email": "second@example.com",
                "content": "Second post"
            }
        )

        first_data = first_response.get_json()
        second_data = second_response.get_json()

        self.assertNotEqual(
            first_data["id"],
            second_data["id"]
        )

    # Invalid timeline request tests
    def test_post_without_name_returns_400(self):
        response = self.client.post(
            "/api/timeline_post",
            data={
                "email": "visitor@example.com",
                "content": "Missing name"
            }
        )

        self.assertEqual(response.status_code, 400)

    def test_post_without_email_returns_400(self):
        response = self.client.post(
            "/api/timeline_post",
            data={
                "name": "Portfolio Visitor",
                "content": "Missing email"
            }
        )

        self.assertEqual(response.status_code, 400)

    def test_post_without_content_returns_400(self):
        response = self.client.post(
            "/api/timeline_post",
            data={
                "name": "Portfolio Visitor",
                "email": "visitor@example.com"
            }
        )

        self.assertEqual(response.status_code, 400)

    # Invalid route and HTTP method tests
    def test_unknown_page_returns_404(self):
        response = self.client.get(
            "/yanxi/page-that-does-not-exist"
        )

        self.assertEqual(response.status_code, 404)

    def test_timeline_api_rejects_delete_request(self):
        response = self.client.delete(
            "/api/timeline_post"
        )

        self.assertEqual(response.status_code, 405)


if __name__ == "__main__":
    unittest.main()