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