"""
税理士事務所の基本設定ファイル
各事務所の情報に合わせてカスタマイズしてください
"""

from dataclasses import dataclass
from typing import List, Dict

@dataclass
class OfficeInfo:
    """事務所基本情報"""
    name: str
    location: str
    prefecture: str
    city: str
    established: str
    website: str = ""
    phone: str = ""
    email: str = ""

@dataclass
class TargetCustomer:
    """ターゲット顧客情報"""
    type: str
    description: str
    keywords: List[str]

# 石井公認会計士・税理士事務所様の設定例
ISHII_OFFICE = OfficeInfo(
    name="石井公認会計士・税理士事務所",
    location="千葉県流山市",
    prefecture="千葉県",
    city="流山市",
    established="2022年",
    website="",
    phone="",
    email=""
)

# 主要サービス
MAIN_SERVICES = [
    "法人税務申告",
    "個人確定申告", 
    "会社設立支援",
    "経営コンサルティング",
    "相続税申告",
    "税務調査対応"
]

# ターゲット顧客
TARGET_CUSTOMERS = [
    TargetCustomer(
        type="地域の法人経営者",
        description="流山市およびその近隣地域の中小企業経営者",
        keywords=["法人税", "会社設立", "経営相談", "税務申告"]
    ),
    TargetCustomer(
        type="個人事業主",
        description="フリーランスや小規模事業者",
        keywords=["確定申告", "青色申告", "個人事業", "開業届"]
    ),
    TargetCustomer(
        type="新規開業予定者",
        description="起業を検討している個人・法人",
        keywords=["起業", "開業", "会社設立", "創業支援"]
    ),
    TargetCustomer(
        type="ITスタートアップ",
        description="IT・テック系のスタートアップ企業",
        keywords=["スタートアップ", "IT企業", "ベンチャー", "資金調達"]
    )
]

# 対象地域（優先順位順）
TARGET_AREAS = [
    "流山市",
    "柏市", 
    "松戸市",
    "野田市",
    "我孫子市",
    "鎌ケ谷市"
]

# SEO目標設定
SEO_GOALS = {
    "monthly_inquiries_current": 1,  # 現在の月間問い合わせ数
    "monthly_inquiries_target": 6,   # 目標月間問い合わせ数
    "target_keywords": [
        "流山市 税理士",
        "流山市 会計事務所",
        "流山市 確定申告",
        "流山市 会社設立",
        "千葉県 税理士",
        "柏市 税理士",
        "松戸市 税理士"
    ],
    "content_goals": {
        "weekly_articles": 1,      # 週間記事作成目標
        "monthly_articles": 5      # 月間記事作成目標
    }
}

# 事務所の強み・特徴
OFFICE_STRENGTHS = [
    "中小企業診断士も保有で戦略・新規事業のコンサル・伴走支援が可能",
    "IT企業の製品戦略・企画経験ありIT企業の会計処理・特殊事情に強い", 
    "スタートアップでのバックオフィス責任者経験で経理・労務・人事・ITサービス導入まで幅広く対応"
]

# 競合事務所情報
COMPETITORS = [
    {
        "name": "おりと税理士事務所",
        "url": "http://orito-cpta.com/",
        "location": "流山市"
    },
    {
        "name": "小林税務会計事務所", 
        "url": "https://zeimukaikei.info/",
        "location": "流山市"
    }
]

# 記事作成の設定
CONTENT_SETTINGS = {
    "preferred_themes": [
        "税務基礎知識の解説",
        "確定申告のノウハウ", 
        "会社設立手続きガイド",
        "経営・資金調達アドバイス"
    ],
    "article_types": [
        "季節・時期に応じた記事（確定申告時期等）",
        "専門性アピール記事",
        "地域密着型情報記事",
        "FAQ・よくある質問記事"
    ],
    "quality_policy": "完璧を求めず継続性重視",
    "collaboration": "税理士が方向性・プロットをまとめ、ライターが詳細作成"
}

# マーケティング予算
MARKETING_BUDGET = {
    "monthly_budget": 20000,  # 月間予算（円）
    "seo_tools_budget": 5000,  # SEOツール予算
    "content_creation_budget": 10000,  # コンテンツ作成予算
    "advertising_budget": 5000  # 広告予算
}