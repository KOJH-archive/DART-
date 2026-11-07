import json
import pytest
from dart_analyst.demo import build_demo
from dart_analyst.models import dataset_from_json, dataset_to_json
from dart_analyst.engine import analyze


def test_roundtrip_preserves_decimal_results():
    data = build_demo('restatement')
    restored = dataset_from_json(dataset_to_json(data))
    assert analyze(data) == analyze(restored)


@pytest.mark.parametrize('amount', ['NaN', 'Infinity', '1e999999'])
def test_nonfinite_or_excessive_amounts_rejected(amount):
    obj = json.loads(dataset_to_json(build_demo()))
    obj['periods'][0]['facts']['revenue']['amount'] = amount
    with pytest.raises(ValueError):
        dataset_from_json(json.dumps(obj))


def test_duplicate_period_labels_rejected():
    obj = json.loads(dataset_to_json(build_demo()))
    obj['periods'][1]['label'] = obj['periods'][0]['label']
    with pytest.raises(ValueError):
        dataset_from_json(json.dumps(obj))


@pytest.mark.parametrize('scenario,status', [('normal', 'pass'), ('missing', 'incomplete'), ('cash_mismatch', 'fail')])
def test_accounting_scenarios_are_distinguished(scenario, status):
    analysis = analyze(build_demo(scenario))
    check = next(c for c in analysis['checks'] if c['key'] == 'cash_flow' and c['period'] == '2026 H1')
    assert check['status'] == status
