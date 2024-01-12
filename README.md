## ポイントカード照会システム

とあるスーパーのポイントカード残高ポイントを照会するサービス(以下、本システム)です。<br>
本システムでは、**ポイント残高照会**の他、ポイントカード会員様の買い物履歴、スーパーの商品検索、スーパーへのお問い合わせメッセージの送信を行うことができます。<br>
また、管理者ページでは、お問い合わせメッセージを一覧で確認することが出来ます。<br>
なお、本システムは、XAMPPの起動、phpMyAdminによるデータベースへの接続が必須となっております。<br><br>
一般会員様ページへのログイン方法：<br>
ID(メールアドレス):2@gmail.com<br>
パスワード:0000<br>
※新規会員登録は可能ですが、こちらの会員様には買い物履歴存在しますため、機能の確認にはこちらのご利用を推奨いたします。<br><br>
管理者ページへのログイン方法：<br>
ID(メールアドレス):1@gmail.com<br>
パスワード:0000<br>
※管理者権限の付与は、本システム上では行うことが出来かねますため、機能の確認にはこちらのご利用を推奨いたします。
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

### ① GET /search_result
・・・商品検索結果の概要を返す。
<br><br>
内容：<br>
{<br>
　search_result: [<br>
　　{<br>
　　　p_name: ???<br>
　　　price_no_tax: ???,<br>
　　　price: ???,<br>
　　　stock_number: ???,<br>
　　　bar_code: ???<br>
　　}<br>
　]<br>
}<br>
<br>
説明：<br>
p_name: 商品名<br>
price_no_tax: 税抜価格(本体価格),<br>
price: 税込み価格,<br>
stock_number: 在庫数,<br>
bar_code: バーコード<br>
