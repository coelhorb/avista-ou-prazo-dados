#!/usr/bin/env python3
"""Gera docs/rates.json a partir de params.json e da cotação do AUPO11."""
import datetime as dt
import json
import os
import pathlib
import urllib.error
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "docs" / "rates.json"
QUOTE_URL = "https://brapi.dev/api/quote/AUPO11"


def previous_quote():
    try:
        return json.loads(OUTPUT.read_text(encoding="utf-8")).get("aupo11")
    except (FileNotFoundError, json.JSONDecodeError):
        return None


def fetch_quote(token):
    request = urllib.request.Request(
        QUOTE_URL,
        headers={"Authorization": f"Bearer {token}", "User-Agent": "avista-ou-prazo-dados"},
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        result = json.load(response)["results"][0]
    return {
        "price": f"{float(result['regularMarketPrice']):.2f}",
        "as_of": str(result["regularMarketTime"])[:10],
    }


def main():
    quote = previous_quote()
    token = os.environ.get("BRAPI_TOKEN", "")
    if not token:
        print("::warning::BRAPI_TOKEN ausente; mantendo a cotação anterior")
    else:
        try:
            quote = fetch_quote(token)
        except (urllib.error.URLError, TimeoutError, KeyError, IndexError, TypeError, ValueError) as error:
            print(f"::warning::Falha ao buscar AUPO11 ({type(error).__name__}); mantendo a cotação anterior")

    params = json.loads((ROOT / "params.json").read_text(encoding="utf-8"))
    rates = {
        "generated_at": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "mercado_pago": params["mercado_pago"],
        "aupo11": quote,
    }
    OUTPUT.write_text(json.dumps(rates, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
