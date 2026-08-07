import logging

from django.conf import settings
from groq import APIError, Groq, RateLimitError

logger = logging.getLogger(__name__)


def generate_insight_text(stock_symbol):
    client = Groq(api_key=settings.GROQ_API_KEY)
    prompt = (
        f"Give a brief stock insight for {stock_symbol} with three sections: "
        "Company Overview, Long-Term Relevance, Risks. "
        "Each section must be exactly 1-2 short sentences. Use markdown headers (# Header)."
    )

    try:
        response = client.chat.completions.create(
            model=settings.GROQ_MODEL,
            messages=[{"role": "user", "content": prompt}],
        )
        content = response.choices[0].message.content
        logger.info(f"AI_INSIGHT | symbol={stock_symbol} | status=success")
        logger.info(f"AI_INSIGHT_RAW | symbol={stock_symbol} | content={content!r}")
        return content
    except RateLimitError as e:
        logger.warning(f"AI_INSIGHT | symbol={stock_symbol} | status=failed | reason=rate limit | detail={e!s}")
        return None
    except APIError as e:
        logger.error(f"AI_INSIGHT | symbol={stock_symbol} | status=failed | reason=api error | detail={e!s}")
        return None
    except Exception as e:
        logger.error(f"AI_INSIGHT | symbol={stock_symbol} | status=failed | reason=unexpected | detail={e!s}")
    return None


def parse_insight_sections(content):
    sections = {"overview": "", "relevance": "", "risks": ""}
    current_key = None

    for line in content.splitlines():
        stripped = line.strip()
        is_header = stripped.startswith("#")
        lower_line = stripped.lower()

        if is_header and "overview" in lower_line:
            current_key = "overview"
            continue
        if is_header and "relevance" in lower_line:
            current_key = "relevance"
            continue
        if is_header and "risk" in lower_line:
            current_key = "risks"
            continue

        if current_key and stripped:
            sections[current_key] += stripped + " "

    return {k: v.strip() for k, v in sections.items()}
