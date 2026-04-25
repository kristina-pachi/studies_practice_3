import pytest
from bs4 import BeautifulSoup
from parser import parse_one_card, parse_all_cards, base_url


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

@pytest.mark.parametrize(
    "html_list, expected_count",
    [
        (
            [
                '<a class="card-news" href="/n1"><h3>Новость 1</h3></a>',
                '<a class="card-news" href="/n2"><h3>Новость 2</h3></a>',
            ],
            2,
        ),
        (
            [
                '<a class="card-news" href="/n1"><h3>Новость 1</h3></a>',
                '<a class="card-news"><h3>Без ссылки</h3></a>',
            ],
            1,
        ),
        (
            [
                '<a class="card-news"></a>',
                '<a class="card-news"><h3></h3></a>',
            ],
            0,
        ),
    ]
)

def test_parse_all_cards_parametrized(html_list, expected_count):
    cards = [BeautifulSoup(html, "lxml").a for html in html_list]

    result = parse_all_cards(cards)

    assert len(result) == expected_count

    # проверка нумерации
    for i, item in enumerate(result, start=1):
        assert item["№"] == i
        assert item["link"].startswith(base_url)
