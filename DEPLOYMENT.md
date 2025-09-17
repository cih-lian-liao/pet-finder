# 🚀 Pet Finder 部署指南

## 免費部署選項

### 1. Render.com (推薦) ⭐⭐⭐⭐⭐

**優點**：
- 完全免費
- 自動從 GitHub 部署
- 支持 PostgreSQL 數據庫
- 自動 SSL 證書
- 簡單易用

**限制**：
- 免費 tier 在 15 分鐘無活動後會休眠
- 醒來需要 30 秒

#### 部署步驟：

1. **註冊 Render.com 帳戶**
   - 訪問 [render.com](https://render.com)
   - 使用 GitHub 帳戶登錄

2. **連接 GitHub 倉庫**
   - 點擊 "New +" → "Web Service"
   - 選擇您的 `pet-finder` 倉庫
   - 選擇 "Build and deploy from a Git repository"

3. **配置部署設置**
   - **Name**: `pet-finder`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate`
   - **Start Command**: `gunicorn scraper.wsgi:application`

4. **設置環境變量**
   - `DEBUG`: `False`
   - `SECRET_KEY`: 點擊 "Generate" 生成新的密鑰
   - `ALLOWED_HOSTS`: `pet-finder.onrender.com`

5. **添加數據庫**
   - 在 Render 儀表板中點擊 "New +" → "PostgreSQL"
   - 選擇 "Free" plan
   - 記下數據庫連接字符串

6. **部署**
   - 點擊 "Create Web Service"
   - 等待部署完成

### 2. Railway.app ⭐⭐⭐⭐

**優點**：
- 現代化的部署平台
- 優秀的 GitHub 集成
- 免費 tier 包含數據庫

#### 部署步驟：

1. **註冊 Railway 帳戶**
   - 訪問 [railway.app](https://railway.app)
   - 使用 GitHub 帳戶登錄

2. **部署項目**
   - 點擊 "New Project"
   - 選擇 "Deploy from GitHub repo"
   - 選擇您的 `pet-finder` 倉庫

3. **添加數據庫**
   - 在項目中添加 PostgreSQL 服務
   - Railway 會自動設置 `DATABASE_URL` 環境變量

4. **設置環境變量**
   - `DEBUG`: `False`
   - `SECRET_KEY`: 生成新的密鑰
   - `ALLOWED_HOSTS`: `your-app.railway.app`

### 3. Vercel (適用於靜態網站) ⭐⭐⭐

**注意**: Vercel 主要用於靜態網站，對於 Django 應用需要額外配置。

## 部署前準備

### 1. 確保所有文件都已提交到 GitHub

```bash
git add .
git commit -m "Prepare for deployment"
git push origin main
```

### 2. 檢查必要的文件

確保以下文件存在：
- `requirements.txt`
- `render.yaml` (用於 Render.com)
- `Procfile` (用於 Heroku/Railway)
- `static/` 目錄包含 favicon 文件

### 3. 環境變量設置

在部署平台上設置以下環境變量：
- `DEBUG`: `False`
- `SECRET_KEY`: 生成的安全密鑰
- `ALLOWED_HOSTS`: 您的域名
- `DATABASE_URL`: 數據庫連接字符串 (由平台自動提供)

## 部署後檢查

1. **網站可訪問性**: 確認網站可以正常訪問
2. **靜態文件**: 確認 CSS、JS、圖片正常加載
3. **數據庫功能**: 測試搜索功能
4. **Favicon**: 確認網站圖標正常顯示

## 自動部署

一旦設置完成，每次您推送代碼到 GitHub 的 `main` 分支時，平台會自動：
1. 檢測代碼變更
2. 安裝依賴
3. 運行數據庫遷移
4. 收集靜態文件
5. 重新部署應用

## 故障排除

### 常見問題：

1. **部署失敗**
   - 檢查 `requirements.txt` 是否包含所有依賴
   - 確認 Python 版本兼容性

2. **靜態文件不顯示**
   - 確認 `whitenoise` 已正確配置
   - 檢查 `STATIC_ROOT` 設置

3. **數據庫錯誤**
   - 確認 `DATABASE_URL` 環境變量已設置
   - 檢查數據庫遷移是否成功運行

4. **網站無法訪問**
   - 檢查 `ALLOWED_HOSTS` 設置
   - 確認域名配置正確

## 性能優化

1. **啟用緩存**: 在生產環境中啟用 Django 緩存
2. **CDN**: 考慮使用 CDN 加速靜態文件
3. **數據庫優化**: 添加必要的數據庫索引

## 監控和維護

1. **日誌監控**: 定期檢查應用日誌
2. **備份**: 定期備份數據庫
3. **更新**: 定期更新依賴包以修復安全漏洞
