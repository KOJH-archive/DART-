from datetime import datetime, timezone
import json

import httpx
import pytest

from dart_analyst.models import Dataset
from dart_analyst.news import NewsError, fetch_news, parse_feed, select_news, summarize_news


NOW = datetime(2026, 11, 7, 12, tzinfo=timezone.utc)
URL = "https://news.einfomax.co.kr/news/articleView.html?idxno=12345"


def feed(url=URL, published="Sat, 07 Nov 2026 10:00:00 +0000"):
    return f"""<rss><channel><item><title>은행 대출 금리 변동</title><link>{url}</link>
    <pubDate>{published}</pubDate><description>&lt;p&gt;은행권 대출 금리가 지난달보다 상승했다고 보도했습니다.&lt;/p&gt;</description>
    </item></channel></rss>""".encode()


def test_rss_filters_stale_future_and_unsafe_links_and_strips_markup():
    article, = parse_feed(feed(), "정책/금융", NOW)
    assert article["summary"] == "은행권 대출 금리가 지난달보다 상승했다고 보도했습니다."
    assert article["url"] == URL
    korean, = parse_feed(feed(published="2026-11-07 19:00:00"), "경제", NOW)
    assert korean["published_at"] == "2026-11-07T10:00:00+00:00"
    assert not parse_feed(feed("https://example.com/news/articleView.html?idxno=1"), "경제", NOW)
    assert not parse_feed(feed(published="Sat, 24 Oct 2026 10:00:00 +0000"), "경제", NOW)
    assert not parse_feed(feed(published="Sun, 08 Nov 2026 10:00:00 +0000"), "경제", NOW)
    with pytest.raises(NewsError):
        parse_feed(b'<!DOCTYPE rss [<!ENTITY x SYSTEM "file:///secret">]><rss>&x;</rss>', "경제", NOW)


def test_rss_deduplicates_and_keeps_successful_feed_when_other_feeds_fail():
    def handler(request):
        return httpx.Response(503) if "S1N16" in request.url.path else httpx.Response(200, content=feed())
    with httpx.Client(transport=httpx.MockTransport(handler)) as client:
        result = fetch_news(client=client, now=NOW)
    assert len(result["articles"]) == 1
    assert len(result["errors"]) == 1
    assert select_news(result["articles"], Dataset("가상", metadata={"industry_code": "64121"}))[0]["relevance"] == "업종 관련"


@pytest.mark.parametrize("index", [0, 4])
def test_ollama_can_only_select_supplied_article_sentences(index):
    articles = select_news(parse_feed(feed(), "정책/금융", NOW), Dataset("가상"))

    def handler(request):
        body = json.loads(request.content)
        assert body["model"] == "test-model"
        assert request.url.host == "127.0.0.1"
        options = body["format"]["properties"]["items"]["items"]["anyOf"]
        assert options[0]["properties"]["ref"]["enum"] == ["n0"]
        assert options[0]["properties"]["sentence"]["enum"] == [-1, 0]
        return httpx.Response(200, json={"done": True, "done_reason": "stop",
            "message": {"content": json.dumps({"items": [{"ref": "n0", "sentence": index}]})}})
    with httpx.Client(transport=httpx.MockTransport(handler)) as client:
        if index == 0:
            selected = summarize_news(articles, "http://127.0.0.1:11434", "test-model", client=client)
            assert selected[0]["summary"] == articles[0]["summary"]
            assert selected[0]["url"] == URL
        else:
            with pytest.raises(NewsError):
                summarize_news(articles, "http://127.0.0.1:11434", "test-model", client=client)
