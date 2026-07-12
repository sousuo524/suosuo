# suosuo 写真引流（GitHub Pages + 自动发 X）

## 你现在在哪一步？

GitHub 空仓库页面 **不用点任何按钮**，按下面顺序做。

---

## 第一步：开启 GitHub Pages

1. 打开 https://github.com/sousuo524/suosuo/settings/pages
2. **Source** 选 `Deploy from a branch`
3. **Branch** 选 `main`，目录选 `/ (root)`
4. 点 **Save**

> 需要先有代码在 `main` 分支上，下面第二步 push 完成后 Pages 才会生效。

---

## 第二步：把本地项目推到 GitHub

在项目目录 `suosuo/` 打开终端，执行：

```bash
cd suosuo
git init
git add .
git commit -m "init promo project"
git branch -M main
git remote add origin https://github.com/sousuo524/suosuo.git
git push -u origin main
```

推送时 GitHub 会要求登录，按提示在浏览器授权即可。

---

## 第三步：上传写真原图

把图片放进 `images/`，命名例如：

```
images/001.jpg
images/002.jpg
...
images/020.jpg   （至少 4 张，建议 20 张以上）
```

然后：

```bash
git add images/
git commit -m "add images"
git push
```

也可以在 GitHub 网页点 **Add file → Upload files**，上传到 `images/` 文件夹。

---

## 第四步：配置环境变量

```bash
cp .env.example .env
```

编辑 `.env`，填写：

| 变量 | 说明 |
|------|------|
| `GITHUB_TOKEN` | GitHub → Settings → Developer settings → Token，勾选 `repo` |
| `X_USERNAME` | X 小号用户名 |
| `X_EMAIL` | X 注册邮箱 |
| `X_PASSWORD` | X 密码 |

---

## 第五步：安装依赖并登录 X

```bash
pip install -r requirements.txt
cd scripts
python post_to_x.py --login
```

按提示完成 X 登录，会生成 `cookies.json`。

---

## 第六步：测试发 1 条（不真发 X）

```bash
python post_to_x.py --dry-run
```

会生成拼图、落地页并 push 到 GitHub，但不发 X。

检查：

1. https://sousuo524.github.io/suosuo/pages/001.html 能否跳转 TG
2. [X Card 预览工具](https://opentweet.io/tools/x-card-validator) 能否看到大图

---

## 第七步：真发 1 条

```bash
python post_to_x.py
```

---

## 第八步：VPS 定时自动发（每天 10 条）

```bash
crontab -e
```

加入：

```cron
0 8,10,12,14,16,18,19,20,21,22 * * * cd /opt/suosuo/scripts && /opt/suosuo/venv/bin/python post_to_x.py >> /var/log/suosuo.log 2>&1
```

---

## 目录说明

| 目录/文件 | 作用 |
|-----------|------|
| `images/` | 原始写真图（你上传） |
| `covers/` | 脚本自动生成的 4 宫格拼图 |
| `pages/` | 脚本自动生成的落地页 |
| `copy/templates.txt` | 话术池，随机抽取 |
| `scripts/post_to_x.py` | 主脚本：拼图 + 落地页 + 发 X |
| `state.json` | 发帖进度记录 |

---

## 常见问题

**Q：GitHub 页面点哪个？**  
A：空仓库页面不用点。用上面的 `git push` 把本地代码推上去。

**Q：至少要几张图？**  
A：至少 4 张，建议 50～200 张。

**Q：每天发几条？**  
A：`.env` 里 `DAILY_LIMIT=10`，配合 cron 10 个时间点。
