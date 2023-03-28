import pytest
from utils import extract_data


@pytest.fixture
def test_data():
    return [
        {
            "id": 0,
            "url": "https://www.theverge.com/2022/4/3/23008668/tesla-shanghai-factory-closed-lockdown-c hina",
            "headline": "Tesla’s Shanghai factory stays closed as COVID restrictions remain in place",
            "author": "Emma Roth",
            "date": "2022/4/3",
        },
        {
            "id": 1,
            "url": "https://www.theverge.com/2022/4/2/22999741/fortnite-chapter-3-season-2-building-returns-zer o-build-mode",
            "headline": "Fortnite brings back building",
            "author": "Andrew Webster",
            "date": "2022/4/3",
        },
        {
            "id": 37,
            "url": "https://www.theverge.com/2022/3/31/23004599/activision-blizzard-overwatch-anniversary-ev ent",
            "headline": "Overwatch sixth anniversary event offers ‘remixes’ of popular skins",
            "author": "Ash Parrish",
            "date": "2022/3/31",
        },
        # Add more test cases here
    ]


def test_extract_data(test_data):
    for data in test_data:
        results, error = extract_data(data["url"])
        assert error == ""  # Make sure no errors occurred during extraction
        assert results["title"] == data["headline"]
        assert results["author"] == data["author"]
        assert results["pub_date"] == data["date"]
        assert results["link"] == data["url"]
