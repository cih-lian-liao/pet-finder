# 🚀 手動部署指南 - Render.com

如果自動部署失敗，請按照以下步驟手動部署：

## 步驟 1: 創建 Render.com 帳戶

1. 訪問 [render.com](https://render.com)
2. 使用 GitHub 帳戶登錄
3. 連接您的 GitHub 帳戶

## 步驟 2: 創建數據庫

1. 在 Render 儀表板中點擊 **"New +"** → **"PostgreSQL"**
2. 設置數據庫名稱：`pet-finder-db`
3. 選擇 **"Free"** plan
4. 點擊 **"Create Database"**
5. 等待數據庫創建完成
6. 記下數據庫連接信息

## 步驟 3: 創建 Web Service

1. 在 Render 儀表板中點擊 **"New +"** → **"Web Service"**
2. 選擇 **"Build and deploy from a Git repository"**
3. 選擇您的 `pet-finder` 倉庫
4. 點擊 **"Connect"**

## 步驟 4: 配置部署設置

### 基本設置：
- **Name**: `pet-finder`
- **Environment**: `Python 3`
- **Region**: 選擇離您最近的區域
- **Branch**: `main`
- **Root Directory**: 留空

### Build & Deploy 設置：
- **Build Command**: 
  ```bash
  pip install --upgrade pip && pip install -r requirements-prod.txt && python manage.py collectstatic --noinput && python manage.py migrate
  ```
- **Start Command**: 
  ```bash
  gunicorn scraper.wsgi:application --bind 0.0.0.0:$PORT
  ```

### 環境變量設置：
點擊 **"Advanced"** → **"Add Environment Variable"**，添加以下變量：

| Key | Value |
|-----|-------|
| `DEBUG` | `False` |
| `SECRET_KEY` | 點擊 "Generate" 生成新的密鑰 |
| `ALLOWED_HOSTS` | `pet-finder.onrender.com` |
| `DATABASE_URL` | 從步驟 2 創建的數據庫中複製連接字符串 |

## 步驟 5: 部署

1. 點擊 **"Create Web Service"**
2. 等待部署完成（大約 5-10 分鐘）
3. 查看部署日誌確認沒有錯誤

## 步驟 6: 測試部署

1. 部署完成後，您會獲得一個 URL（例如：`https://pet-finder.onrender.com`）
2. 訪問該 URL 測試網站是否正常工作
3. 測試搜索功能
4. 確認靜態文件（CSS、JS、圖片）正常加載

## 常見問題解決

### 問題 1: 部署失敗
- 檢查 Build Command 是否正確
- 確認所有環境變量已設置
- 查看部署日誌中的錯誤信息

### 問題 2: 網站無法訪問
- 檢查 `ALLOWED_HOSTS` 環境變量
- 確認 URL 是否正確

### 問題 3: 數據庫連接錯誤
- 檢查 `DATABASE_URL` 環境變量
- 確認數據庫已創建並運行

### 問題 4: 靜態文件不顯示
- 確認 `whitenoise` 已正確配置
- 檢查 `collectstatic` 命令是否成功執行

## 自動重新部署

部署成功後，每次您推送代碼到 GitHub 的 `main` 分支時，Render 會自動：
1. 檢測代碼變更
2. 重新構建應用
3. 重新部署

## 監控和維護

1. **查看日誌**: 在 Render 儀表板中查看實時日誌
2. **監控性能**: 檢查 CPU 和內存使用情況
3. **備份數據**: 定期備份 PostgreSQL 數據庫

## 免費 tier 限制

- 應用在 15 分鐘無活動後會休眠
- 重新啟動需要 30 秒
- 每月有使用限制
- 數據庫有存儲限制

## 升級選項

如果需要更好的性能，可以考慮升級到付費計劃：
- 更快的啟動時間
- 更多資源
- 更好的支持
