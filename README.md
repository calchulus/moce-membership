# MOCE 会员卡 — Alipay Mini-App Membership Demo (PWA)

A **functional, installable Progressive Web App** that simulates the Alipay mini-program
「申请会员卡」(join-membership) flow for **MOCE 五金**, a physical hardware store.
Not a static mockup: the phone-auth sheet gates entry, the form validates, and a member
record is issued and persisted in `localStorage`.

## Live
GitHub Pages: <https://calchulus.github.io/moce-membership/>

## The flow
1. **会员卡 landing** — brand header, tier hero (银/金/黑/工程采购), 开卡礼 banner, 权益 grid, store list.
2. **一键授权手机号** — Alipay-style bottom sheet (masked bound number, 拒绝 / 允许).
3. **会员资料 form** — name + CN-mobile validation, 个人/企业 segmented type, birthday, store, required 协议 checkbox.
4. **开卡中 → 会员卡** — member number, mock QR + barcode, 500 积分, ¥50 开卡礼券, tier progress, 添加到卡包.

## Run locally
```bash
python3 -m http.server 8099      # then open http://localhost:8099
```
`localhost` is a secure context, so the service worker registers and the install prompt appears.
There is also a fully self-contained **`moce-membership-single.html`** (no external refs) that can be
opened directly via `file://` or shared as one file; it omits only the install/offline-cache layer.

## Files
| File | Purpose |
|---|---|
| `index.html` | Source of truth — all CSS/JS inline; the PWA app |
| `manifest.json` | Web-app manifest (install) |
| `sw.js` | Cache-first service worker (offline shell) |
| `icons/` | Generated PNG icons (see `make_icons.py`) |
| `make_icons.py` | Pillow icon generator |
| `build_single.py` | Regenerates `moce-membership-single.html` from `index.html` |
| `moce-membership-single.html` | Self-contained single-file build |

After editing `index.html`, run `python3 build_single.py` to refresh the single-file build.

## Mapping to real Alipay APIs
| Simulated here | Real mini-program API |
|---|---|
| Phone-auth sheet | `my.getAuthCode` + 手机号快速验证 (`getPhoneNumber`) |
| 添加到卡包 | `my.addCardAuth` / `my.openCardList` |
| Nav capsule (••• ◎) | native mini-program chrome |

## Notes
- The QR / barcode are **decorative deterministic canvases** (seeded by member number) — they look
  right but are not scannable. Swap in a real QR library when scannability is required.
- All data stays on-device in `localStorage`; nothing is uploaded.
- Demo only — no real membership is created.
