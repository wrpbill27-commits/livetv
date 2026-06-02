# 🌍 Custom Domain Setup for Live TV

## Step 1: ซื้อ Domain
- แนะนำ: Namecheap (~$5-10/ปี) หรือ Cloudflare Registrar (~$8/ปี)
- ตัวเลือก:
  - `lovelive.tv` — จดจำง่าย สั้น
  - `dookeraa.com` — ตามแบรนด์ Telegram
  - `dooball.live` — SEO keyword ตรง
  - `livetv247.com` — มืออาชีพ

## Step 2: ตั้งค่า DNS
เพิ่ม CNAME record:
```
Type:  CNAME
Name:  www (หรือ @ สำหรับ root domain)
Value: wrpbill27-commits.github.io
TTL:   Auto
```

## Step 3: GitHub Pages
1. เอา domain ใส่ใน CNAME file → git push
2. ไป repo Settings → Pages → Custom domain → ใส่ domain → Save
3. รอ HTTPS auto-issue (~5 นาที)

## Step 4: Cloudflare (Optional — ฟรี CDN + DDoS protection)
1. เปลี่ยน nameserver ไป Cloudflare
2. เปิด proxy (orange cloud) → ซ่อน IP จริง
3. SSL: Full (strict)
