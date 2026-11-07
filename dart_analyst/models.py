from __future__ import annotations

from dataclasses import asdict, dataclass, field
from decimal import Decimal
from datetime import date
import json


@dataclass
class Fact:
    key: str
    name: str
    amount: Decimal | None
    statement: str
    start: str
    end: str
    scope: str = "CFS"
    currency: str = "KRW"
    unit: Decimal = Decimal("1")
    source_id: str = ""
    source_url: str = ""
    account_id: str = ""
    source_field: str = "thstrm_amount"
    attribution: str = "total"
    period_kind: str = "FY"
    reason: str = ""
    source_details: dict = field(default_factory=dict)


@dataclass
class Period:
    label: str
    year: int
    start: str
    end: str
    scope: str = "CFS"
    kind: str = "FY"
    filing_id: str = ""
    facts: dict[str, Fact] = field(default_factory=dict)
    comparatives: dict[str, Fact] = field(default_factory=dict)
    raw_accounts: list[dict] = field(default_factory=list)
    issues: list[str] = field(default_factory=list)


@dataclass
class Dataset:
    company: str
    corp_code: str = ""
    stock_code: str = ""
    scope: str = "CFS"
    source_mode: str = "demo"
    periods: list[Period] = field(default_factory=list)
    notes: list[dict] = field(default_factory=list)
    issues: list[str] = field(default_factory=list)
    metadata: dict = field(default_factory=dict)

    @property
    def has_financial_industry_code(self) -> bool:
        return str(self.metadata.get("industry_code") or "").strip().startswith(("64", "65", "66"))


def dataset_to_json(dataset: Dataset) -> str:
    return json.dumps(asdict(dataset), ensure_ascii=False, indent=2, default=str)


def dataset_from_json(text: str) -> Dataset:
    if len(text.encode('utf-8')) > 10 * 1024 * 1024:
        raise ValueError("자료는 10MB 이하여야 합니다.")
    obj = json.loads(text)
    if not isinstance(obj, dict) or not isinstance(obj.get('company'), str):
        raise ValueError("회사 정보가 올바르지 않습니다.")
    if obj.get('scope', 'CFS') not in {'CFS', 'OFS'}:
        raise ValueError("재무제표 기준이 올바르지 않습니다.")
    periods = []
    for raw in obj.pop("periods", []):
        if not isinstance(raw, dict) or raw.get('scope', 'CFS') not in {'CFS', 'OFS'}:
            raise ValueError("기간 정보가 올바르지 않습니다.")
        if date.fromisoformat(raw['start']) > date.fromisoformat(raw['end']):
            raise ValueError("기간의 시작과 종료가 역전되었습니다.")
        if raw.get('kind', 'FY') not in {'FY', 'YTD'}:
            raise ValueError("연간 또는 누적 자료만 지원합니다.")
        if not isinstance(raw.get('label'), str) or any(p.label == raw['label'] for p in periods):
            raise ValueError("기간 이름은 중복될 수 없습니다.")
        for collection in ("facts", "comparatives"):
            converted = {}
            for key, value in raw.get(collection, {}).items():
                if not isinstance(value.get("source_details", {}), dict):
                    raise ValueError("계정 원천 상세는 객체여야 합니다.")
                if key != value.get('key'):
                    raise ValueError("계정 키가 일치하지 않습니다.")
                if date.fromisoformat(value['start']) > date.fromisoformat(value['end']):
                    raise ValueError("계정 기간이 올바르지 않습니다.")
                value["amount"] = Decimal(str(value["amount"])) if value.get("amount") is not None else None
                if value["amount"] is not None and not value["amount"].is_finite():
                    raise ValueError("금액은 유한한 숫자여야 합니다.")
                value["unit"] = Decimal(str(value.get("unit", "1")))
                if not value["unit"].is_finite() or value["unit"] <= 0:
                    raise ValueError("단위는 양의 유한한 숫자여야 합니다.")
                if any(n is not None and (len(n.as_tuple().digits) > 50 or abs(n.as_tuple().exponent) > 20) for n in (value['amount'], value['unit'])):
                    raise ValueError("지원하는 금액 정밀도 범위를 초과했습니다.")
                converted[key] = Fact(**value)
            raw[collection] = converted
        periods.append(Period(**raw))
    return Dataset(periods=periods, **obj)
