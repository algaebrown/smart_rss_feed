import streamlit.testing.v1 as st_test
from unittest.mock import patch


def test_app_runs():
    with (
        patch("ingest.ingest_newsletters_from_feed", return_value=[]),
        patch("visualization.compute_and_assign_embeddings_tsne", return_value=None),
    ):
        app = st_test.AppTest.from_file("src/app.py")
        app.run(timeout=20)
        # Example: check that the title is rendered (if present)
        # print(app.title)  # Uncomment to debug available titles
        # assert app.title[0].value == "Smart Newsletter Dashboard"
