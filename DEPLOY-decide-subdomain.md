# decide.motinextai.com 上线步骤（走你现有的 Cloudflare Tunnel）

背景：免费 .tech 域名卡在 MLH 的手机验证 + GitHub 绑定两道坎；但你的 Cloudflare Tunnel（tunnel 名 `app`）本来就通着，`app.motinextai.com` 就是它带的。给同一条隧道再加一个 hostname，5 分钟就有 live demo 链接：`https://decide.motinextai.com`。

前提：决定外包机在你本机跑起来（mock 模式，不用 key）。

## 步骤（都在你 Windows 本机做）

### 1. 本机启动决定外包机（端口 5001）

```powershell
cd <你解压 decideforme 的目录>
pip install -r requirements.txt
python app.py
```

浏览器开 http://localhost:5001，能玩就说明起来了（默认 FLASK_PORT=5001）。

### 2. 给隧道加一条 ingress 规则

打开你当初配 tunnel 用的那个 `config.yml`（Windows 服务跑的是 SYSTEM 账户，注意别找成你用户目录下的那个——以你当时实际生效的为准），在 `ingress:` 下面加一行：

```yaml
ingress:
  - hostname: decide.motinextai.com
    service: http://127.0.0.1:5001
  - hostname: app.motinextai.com
    service: http://127.0.0.1:8080
  - service: http_status:404
```

注意：`decide` 这条必须放在 catch-all（`http_status:404`）之前；`app.motinextai.com` 那条原样保留。

### 3. 建 DNS 记录（一条命令）

```powershell
cloudflared tunnel route dns app decide.motinextai.com
```

这会在 Cloudflare 自动建好 `decide.motinextai.com` 的 CNAME，不用手动去面板加。

### 4. 重启 cloudflared 让新规则生效

- 如果装成了 Windows 服务：services.msc 里重启 cloudflared 服务。
- 如果是前台窗口跑的：关掉重开（带上 `--config` 指向同一个 config.yml）。

### 5. 验证

浏览器开 https://decide.motinextai.com，能打开决定外包机页面即成功。
`app.motinextai.com` 不受影响，照常用。

## 上线后回填投稿文

`DEV-POST-v2.md` 里两处 [待填]：
- Demo 节：填 `https://decide.motinextai.com`
- Prize Categories：只有真领到 .tech 域名才写 Best Use of a .tech Domain；没领整节删掉（规则：一个挑战一个奖项，不影响总冠军）

## 说明

- 这条路线**不替代** .tech：Best Use of a .tech Domain 那个 $100 奖必须真有个 .tech 域名；但投稿要的 live demo 和接单资料包要的作品集链接，用自己的子域名完全够。
- 全程 0 费用、无续费、无需 MLH 验证；反悔就把 ingress 那两行删掉重启即可。
