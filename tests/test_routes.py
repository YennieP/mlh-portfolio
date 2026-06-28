"""Integration tests for the portfolio's Flask routes.

These hit the app through the test client and assert on the rendered HTML —
they cover that pages load, key content renders, the chat widget is scoped to
Yanxi's pages, and static assets resolve. Run with: pytest
"""
import pytest

YANXI_PAGES = ["/yanxi", "/yanxi/hobbies", "/yanxi/places"]
JANE_PAGES = ["/jane", "/jane/hobbies"]
ALL_ROUTES = ["/"] + JANE_PAGES + YANXI_PAGES


def html(client, path):
    return client.get(path).get_data(as_text=True)


# --- routes load ---------------------------------------------------------
@pytest.mark.parametrize("path", ALL_ROUTES)
def test_route_returns_200(client, path):
    assert client.get(path).status_code == 200


# --- content renders -----------------------------------------------------
def test_about_section(client):
    page = html(client, "/yanxi")
    assert "About Me" in page
    assert "Northeastern" in page


def test_projects_listed(client):
    page = html(client, "/yanxi")
    for name in ["Fanfic Assistant", "SQL Buddy"]:
        assert name in page


def test_hobbies_listed(client):
    page = html(client, "/yanxi/hobbies")
    for hobby in ["Listening to Music", "Singing", "Playing The Sims 4", "Badminton"]:
        assert hobby in page


def test_visited_countries(client):
    page = html(client, "/yanxi/places")
    for country in ["Russia", "Japan", "Thailand", "United States", "China", "Hungary", "Germany"]:
        assert country in page


def test_menu_has_three_tabs(client):
    page = html(client, "/yanxi")
    for label in ["About Me", "Hobbies", "Places"]:
        assert label in page


# --- chat widget is scoped to Yanxi's pages ------------------------------
@pytest.mark.parametrize("path", YANXI_PAGES)
def test_chatbot_on_yanxi_pages(client, path):
    assert "chatbot.js" in html(client, path)


@pytest.mark.parametrize("path", JANE_PAGES)
def test_chatbot_not_on_jane_pages(client, path):
    assert "chatbot.js" not in html(client, path)


# --- static assets resolve -----------------------------------------------
@pytest.mark.parametrize("asset", [
    "/static/js/chatbot.js",
    "/static/img/Yanxi_profile.jpg",
    "/static/styles/main.css",
])
def test_static_asset_served(client, asset):
    assert client.get(asset).status_code == 200
