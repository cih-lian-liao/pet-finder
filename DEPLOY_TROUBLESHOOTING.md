# 🚨 部署故障排除指南

## 常見部署錯誤及解決方案

### 1. ModuleNotFoundError: No module named 'dj_database_url'

**錯誤原因**: 本地開發環境缺少生產依賴

**解決方案**:
```bash
# 安裝缺失的依賴
pip install dj-database-url

# 或者使用 requirements.txt
pip install -r requirements.txt
```

### 2. Build Command 失敗

**可能原因**:
- Python 版本不匹配
- 依賴衝突
- 網絡問題

**解決方案**:
1. 使用 `requirements-minimal.txt` 進行最小化部署
2. 檢查 Python 版本兼容性
3. 分步執行構建命令

### 3. 數據庫連接錯誤

**錯誤信息**: `django.db.utils.OperationalError`

**解決方案**:
1. 確認 `DATABASE_URL` 環境變量已設置
2. 檢查數據庫服務是否運行
3. 驗證連接字符串格式

### 4. 靜態文件加載失敗

**錯誤信息**: `404 Not Found` for CSS/JS files

**解決方案**:
1. 確認 `collectstatic` 命令成功執行
2. 檢查 `whitenoise` 配置
3. 驗證 `STATIC_ROOT` 設置

## 🔧 分步部署測試

### 步驟 1: 本地測試
```bash
# 激活虛擬環境
source venv/bin/activate

# 檢查 Django 配置
python manage.py check

# 測試靜態文件收集
python manage.py collectstatic --noinput

# 測試數據庫遷移
python manage.py migrate

# 啟動開發服務器
python manage.py runserver
```

### 步驟 2: 生產環境模擬
```bash
# 設置生產環境變量
export DEBUG=False
export SECRET_KEY="your-secret-key"
export ALLOWED_HOSTS="localhost"

# 測試 Gunicorn
gunicorn scraper.wsgi:application --bind 0.0.0.0:8000
```

### 步驟 3: 最小化部署
使用 `requirements-minimal.txt` 進行部署，只包含核心依賴：
- Django
- requests
- gunicorn
- whitenoise

## 🚀 替代部署方案

### 方案 1: Railway.app
1. 連接 GitHub 倉庫
2. 自動檢測 Django 項目
3. 免費 tier 可用

### 方案 2: Heroku
1. 創建 `Procfile`
2. 設置環境變量
3. 部署到 Heroku

### 方案 3: PythonAnywhere
1. 上傳代碼
2. 配置 WSGI
3. 設置靜態文件

## 📋 部署檢查清單

- [ ] 所有依賴已安裝
- [ ] 環境變量已設置
- [ ] 數據庫已配置
- [ ] 靜態文件已收集
- [ ] 遷移已執行
- [ ] Gunicorn 配置正確
- [ ] 健康檢查路徑設置
- [ ] 日誌配置正確

## 🔍 調試技巧

### 查看部署日誌
1. 在 Render 儀表板中查看 "Logs" 標籤
2. 檢查構建和運行時錯誤
3. 複製錯誤信息進行分析

### 本地調試
```bash
# 詳細輸出
python manage.py runserver --verbosity=2

# 檢查設置
python manage.py diffsettings

# 測試數據庫
python manage.py dbshell
```

### 生產環境調試
```bash
# 在 Render 控制台中執行
python manage.py shell
python manage.py check --deploy
```

## 📞 獲取幫助

如果問題持續存在，請提供以下信息：
1. 完整的錯誤日誌
2. 部署配置文件
3. 本地測試結果
4. 使用的 Python 版本
5. 依賴列表
