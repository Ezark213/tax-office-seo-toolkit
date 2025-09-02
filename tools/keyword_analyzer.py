#!/usr/bin/env python3
"""
キーワード分析ツール
地域×税理士業界のキーワード分析を実行
"""

import click
import pandas as pd
from typing import List, Dict, Optional
import requests
import time
import json
from pathlib import Path
import sys
import os

# プロジェクトのルートディレクトリをパスに追加
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.keyword_database import (
    LOCATION_KEYWORDS, SERVICE_KEYWORDS, SEASONAL_KEYWORDS,
    get_location_service_combinations, get_target_keywords_for_office
)
from config.office_settings import TARGET_AREAS, MAIN_SERVICES

class KeywordAnalyzer:
    """キーワード分析クラス"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        初期化
        
        Args:
            api_key: Google Keyword Planner API key (オプション)
        """
        self.api_key = api_key
        self.results = {}
    
    def analyze_location_keywords(self, location: str, services: List[str] = None) -> Dict:
        """
        地域キーワードの分析
        
        Args:
            location: 対象地域
            services: 対象サービス一覧
            
        Returns:
            分析結果辞書
        """
        if services is None:
            services = MAIN_SERVICES
        
        print(f"🔍 {location}の税理士業界キーワード分析を開始...")
        
        # 基本キーワード生成
        primary_keywords = [
            f"{location} 税理士",
            f"{location} 会計事務所", 
            f"{location} 公認会計士",
            f"税理士 {location}",
            f"会計士 {location}"
        ]
        
        # サービス別キーワード
        service_keywords = []
        for service in services:
            service_keywords.extend([
                f"{location} {service}",
                f"{service} {location}",
                f"{location} {service} 相談",
                f"{location} {service} 料金"
            ])
        
        # ロングテールキーワード
        long_tail_keywords = []
        for service in services:
            long_tail_keywords.extend([
                f"{location} {service} おすすめ",
                f"{location} {service} 安い",
                f"{location} {service} 評判",
                f"{location} {service} 比較"
            ])
        
        results = {
            "location": location,
            "primary_keywords": primary_keywords,
            "service_keywords": service_keywords,
            "long_tail_keywords": long_tail_keywords,
            "total_keywords": len(primary_keywords) + len(service_keywords) + len(long_tail_keywords)
        }
        
        # 検索ボリューム推定（モックデータ）
        results["volume_estimates"] = self._estimate_search_volumes(
            primary_keywords + service_keywords[:10]
        )
        
        self.results[location] = results
        return results
    
    def _estimate_search_volumes(self, keywords: List[str]) -> Dict[str, int]:
        """
        検索ボリューム推定（モックデータ）
        実際の実装では Google Ads API や他のツールを使用
        """
        volumes = {}
        
        for keyword in keywords:
            # 地域規模による基本ボリューム設定
            base_volume = 100
            
            # キーワードタイプによる調整
            if "税理士" in keyword and any(area in keyword for area in ["流山", "柏", "松戸"]):
                base_volume = 200
            elif "確定申告" in keyword:
                base_volume = 300
            elif "会社設立" in keyword:
                base_volume = 150
            elif "相談" in keyword:
                base_volume = 80
            elif "料金" in keyword or "費用" in keyword:
                base_volume = 120
            
            # ランダムな変動を追加（実際のデータのバラつきを模擬）
            import random
            variation = random.randint(-30, 50)
            volumes[keyword] = max(10, base_volume + variation)
        
        return volumes
    
    def analyze_competitor_keywords(self, competitor_urls: List[str]) -> Dict:
        """
        競合サイトのキーワード分析
        
        Args:
            competitor_urls: 競合サイトのURL一覧
            
        Returns:
            競合分析結果
        """
        print("🔍 競合サイトのキーワード分析...")
        
        competitor_data = {}
        
        for url in competitor_urls:
            print(f"  📊 分析中: {url}")
            
            # 実際の実装では、SEOツールのAPIやスクレイピングを使用
            # ここではモックデータを返す
            competitor_data[url] = {
                "estimated_keywords": random.randint(50, 200),
                "estimated_traffic": random.randint(500, 2000),
                "top_keywords": [
                    f"流山市 税理士",
                    f"千葉県 確定申告", 
                    f"会社設立 流山",
                    f"税務相談 柏市"
                ],
                "content_gaps": [
                    "IT企業向け税務",
                    "スタートアップ支援",
                    "相続税専門"
                ]
            }
            
            time.sleep(1)  # API制限対策
        
        return competitor_data
    
    def generate_content_keywords(self, month: int = None) -> List[str]:
        """
        コンテンツ作成用キーワード生成
        
        Args:
            month: 対象月（1-12）
            
        Returns:
            コンテンツ向けキーワード一覧
        """
        print("📝 コンテンツ作成用キーワード生成...")
        
        content_keywords = []
        
        # 基本的な解説コンテンツキーワード
        basic_content = [
            "確定申告 やり方",
            "青色申告 白色申告 違い", 
            "会社設立 手順",
            "個人事業主 税金",
            "法人税 計算方法",
            "経費 範囲",
            "控除 種類",
            "税務調査 対策"
        ]
        content_keywords.extend(basic_content)
        
        # 月別・季節コンテンツ
        if month:
            seasonal = SEASONAL_KEYWORDS.get(f"{month}月", [])
            for item in seasonal:
                content_keywords.extend([
                    f"{item} とは",
                    f"{item} 手続き",
                    f"{item} 注意点",
                    f"{item} 期限"
                ])
        
        # 地域密着コンテンツ
        for area in TARGET_AREAS[:3]:  # 上位3地域
            content_keywords.extend([
                f"{area} 税理士 選び方",
                f"{area} 開業 手続き",
                f"{area} 会計事務所 比較"
            ])
        
        return content_keywords
    
    def export_results(self, output_file: str = None) -> str:
        """
        分析結果をエクスポート
        
        Args:
            output_file: 出力ファイルパス
            
        Returns:
            出力ファイルパス
        """
        if not output_file:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            output_file = f"keyword_analysis_{timestamp}.json"
        
        output_path = Path("data/keywords") / output_file
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, ensure_ascii=False, indent=2)
        
        print(f"✅ 分析結果を保存: {output_path}")
        return str(output_path)

@click.command()
@click.option('--location', '-l', default='流山市', help='対象地域')
@click.option('--services', '-s', multiple=True, help='対象サービス')
@click.option('--competitors', '-c', help='競合URLリストファイル')
@click.option('--month', '-m', type=int, help='対象月（1-12）')
@click.option('--output', '-o', help='出力ファイル名')
@click.option('--api-key', help='Google Ads API Key')
def main(location, services, competitors, month, output, api_key):
    """税理士事務所向けキーワード分析ツール"""
    
    print("🚀 税理士事務所向けキーワード分析ツール")
    print("=" * 50)
    
    analyzer = KeywordAnalyzer(api_key)
    
    # サービス一覧の設定
    if not services:
        services = MAIN_SERVICES
    else:
        services = list(services)
    
    print(f"📍 対象地域: {location}")
    print(f"🛠️ 対象サービス: {', '.join(services)}")
    
    # 地域キーワード分析
    location_results = analyzer.analyze_location_keywords(location, services)
    
    print(f"\n📊 分析結果:")
    print(f"  - プライマリキーワード: {len(location_results['primary_keywords'])}個")
    print(f"  - サービス関連: {len(location_results['service_keywords'])}個")
    print(f"  - ロングテール: {len(location_results['long_tail_keywords'])}個")
    print(f"  - 合計: {location_results['total_keywords']}個")
    
    # 検索ボリューム上位5位を表示
    volumes = location_results['volume_estimates']
    top_keywords = sorted(volumes.items(), key=lambda x: x[1], reverse=True)[:5]
    
    print(f"\n🔝 検索ボリューム上位:")
    for keyword, volume in top_keywords:
        print(f"  - {keyword}: {volume:,}/月")
    
    # 競合分析（オプション）
    if competitors:
        competitor_urls = []
        if Path(competitors).exists():
            with open(competitors, 'r') as f:
                competitor_urls = [line.strip() for line in f if line.strip()]
        
        if competitor_urls:
            competitor_results = analyzer.analyze_competitor_keywords(competitor_urls)
            analyzer.results['competitors'] = competitor_results
            
            print(f"\n🏢 競合分析完了: {len(competitor_urls)}サイト")
    
    # コンテンツキーワード生成
    content_keywords = analyzer.generate_content_keywords(month)
    analyzer.results['content_keywords'] = content_keywords
    
    print(f"\n📝 コンテンツ向けキーワード: {len(content_keywords)}個生成")
    
    # 結果をエクスポート
    output_file = analyzer.export_results(output)
    
    print(f"\n✅ 分析完了！")
    print(f"📄 詳細結果: {output_file}")
    
    # 次のアクション提案
    print(f"\n💡 次のステップ:")
    print(f"  1. 競合分析: python tools/competitor_analysis.py")
    print(f"  2. コンテンツ作成: python tools/content_generator.py") 
    print(f"  3. 順位追跡開始: python tools/rank_tracker.py --setup")

if __name__ == '__main__':
    import random
    main()