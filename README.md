## ポイントカード照会

**ポイント残高**を照会できます。

## ER図

```mermaid
erDiagram
    users{
        int user_id PK
        string user_pcard_number "ポイントカード番号"
        string user_email "メールアドレス"
        string user_name "氏名"
        string user_phone_number "携帯電話番号"
        string user_password "ログイン用パスワード"      
        int user_point "保有ポイント"
        int user_point_ticket_all "累計ポイント券枚数"
        string user_admin "ユーザor管理者"
    }

    buy_receipts{
        int receipt_id PK
        int user_id FK
        date buy_date "購入日"
        time buy_time "購入時"
        int register_number "レジ番号"
        int receipt_number "レシート番号"
        int total_price_no_tax "小計"
        int total_price "合計"
        int buy_count "購入商品点数"
        string payment_method "支払方法"
        int input_money "投入金額"
        int output_money "お釣り金額"
        int point_new "発生ポイント"
        int point_now "残高ポイント"
        int point_ticket "発生ポイント券枚数"
    }

    buy_details{
        int detail_id PK
        int receipt_id FK
        int item_id FK
        int detail_number "個数"
    }

    items{
        int item_id PK
        string barcode "バーコード"
        int category_number "部門番号"
        string Product_name "商品名"
        int price_no_tax "単価"
        int price "税込価格"
        int tax_rate "税率"
        int stock_number "在庫数"
    }

    customerforms{
        int cf_id PK
        int user_id FK
        text form
    }

users ||--o{ buy_receipts : ""
users ||--o{ customerforms : ""
buy_receipts ||--o{ buy_details : ""
items ||--o{ buy_details : ""

```

**各テーブルの扱う情報について**

user : ユーザの個人情報等<br>
buy_receipt : 買い物の基本情報等<br>
buy_detail : 買い物で購入した商品情報等<br>
item : 商品情報等<br>
matmome : まとめ売り情報等<br>


## API仕様書

### ① GET /api/result
・・・レシート検索結果の概要を返す。
<br><br>
例<br>
{<br>
　receipt: [<br>
　　{<br>
　　　receipt_id: 1,<br>
　　　buy_date: "2023/11/01",<br>
　　　buy_time: "12:34",<br>
　　　receipt_number: 1234,<br>
　　　total_price: 2023,<br>
　　　payment_method: "クレジットカード決済",<br>
　　　point_new: 8,<br>
　　　point_now: 8,<br>
　　　point_ticket: 0<br>
　　}<br>
　]<br>
}<br>
<br>
説明：<br>
receipt_id: レシートID<br>
buy_date: 購入日<br>
buy_time: 購入時間<br>
receipt_number: レシート番号<br>
total_price: 合計金額<br>
payment_method: 支払方法<br>
point_new: 発生ポイント<br>
point_now: 残留ポイント<br>
point_ticket: 発生ポイント券枚数<br>
