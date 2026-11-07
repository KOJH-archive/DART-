"""Offline demo/report or explicitly requested DART acquisition from the CLI."""
import argparse
import json
import os
from pathlib import Path

from dotenv import load_dotenv

from .demo import build_demo
from .engine import analyze
from .exporters import make_excel, make_html, make_markdown
from .models import dataset_from_json, dataset_to_json


def main():
    load_dotenv()
    parser = argparse.ArgumentParser(description='DART 기업분석실: 로컬 분석 및 보고서 저장')
    source = parser.add_mutually_exclusive_group()
    source.add_argument('--input', type=Path, help='저장된 dataset JSON')
    source.add_argument('--corp-code', help='DART 회사 고유번호 8자리 (DART_API_KEY 필요)')
    parser.add_argument('--name', default='DART 조회 기업')
    parser.add_argument('--years', type=int, default=5)
    parser.add_argument('--scope', choices=['CFS', 'OFS'], default='CFS')
    parser.add_argument('--scenario', choices=['normal', 'restatement', 'missing', 'cash_mismatch'], default='normal')
    parser.add_argument('--output', type=Path, default=Path('reports'))
    args = parser.parse_args()
    if args.input:
        dataset = dataset_from_json(args.input.read_text(encoding='utf-8'))
        dataset.metadata['original_source_mode'] = dataset.source_mode
        dataset.source_mode = 'import'
        dataset.issues.append('저장 자료: 이 실행에서 DART 원본을 재조회하지 않았습니다.')
    elif args.corp_code:
        from .dart_client import DartClient, DartError
        try:
            with DartClient(os.getenv('DART_API_KEY', '')) as client:
                dataset = client.load_company(args.corp_code, args.name, years=args.years, scope=args.scope)
        except DartError as exc:
            parser.error(str(exc))
        if not dataset.periods:
            parser.error(' / '.join(dataset.issues) or '분석 가능한 공시가 없습니다.')
    else:
        dataset = build_demo(args.scenario)
    result = analyze(dataset)
    args.output.mkdir(parents=True, exist_ok=True)
    (args.output / 'report.html').write_text(make_html(dataset, result), encoding='utf-8')
    (args.output / 'report.md').write_text(make_markdown(dataset, result), encoding='utf-8')
    (args.output / 'analysis.xlsx').write_bytes(make_excel(dataset, result))
    (args.output / 'dataset.json').write_text(dataset_to_json(dataset), encoding='utf-8')
    (args.output / 'analysis.json').write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f'{dataset.company}: {len(dataset.periods)}개 기간 분석 → {args.output.resolve()}')
    print('검증용 가상 자료입니다.' if dataset.source_mode == 'demo' else '원천·보류사항은 보고서에 기록했습니다.')


if __name__ == '__main__':
    main()
