import pytest
from bs4 import BeautifulSoup
from parser import parse_one_card, base_url


@pytest.mark.parametrize(
    "html, expected",
    [
        (
            '<a class="card-news" href="/news/meme"><h3>Сегодня умер Дима Билан</h3></a>',
            {"title": "Заголовок", "link": base_url + "/news/123"},
        ),
        (
            '<a class="card-news" href="/news/meme"></a>',
            None,
        ),
        (
            '<a class="card-news"><h3>Сегодня умер Дима Билан</h3></a>',
            None,
        ),
    ]
)

def test_parse_one_card_parametrized(html, expected):
    card = BeautifulSoup(html, "lxml").a
    result = parse_one_card(card)

    if expected is None:
        assert result is None
    else:
        assert result["title"] == expected["title"]
        assert result["link"] == expected["link"]
