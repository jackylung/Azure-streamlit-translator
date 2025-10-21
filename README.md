# Azure Translator 翻譯器

這個 Streamlit 應用允許您使用 Azure 文本翻譯 API 翻譯多種語言的文本。它利用 Azure AI 服務創建一個簡單易用的翻譯工具。

## 用途
- 從下拉菜單中選擇源語言和目標語言
- 在文本區域中輸入要翻譯的文本
- 點擊「翻譯」按鈕開始翻譯過程
- 翻譯結果將顯示在下方的文本區域中

## 支持的語言
該應用支持超過 10 種語言，包括：
<div align='center'>
  <table>
  <thead>
    <tr>
      <th>語言</th>
      <th>代碼</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>中文(繁體)</td>
      <td>zh-Hant</td>
    </tr>
    <tr>
      <td>中文(簡體)</td>
      <td>zh-Hans</td>
    </tr>
    <tr>
      <td>英文</td>
      <td>en</td>
    </tr>
    <tr>
      <td>日文</td>
      <td>ja</td>
    </tr>
    <tr>
      <td>韓文</td>
      <td>ko</td>
    </tr>
    <tr>
      <td>法文</td>
      <td>fr</td>
    </tr>
    <tr>
      <td>德文</td>
      <td>de</td>
    </tr>
    <tr>
      <td>西班牙文</td>
      <td>es</td>
    </tr>
    <tr>
      <td>阿拉伯文</td>
      <td>ar</td>
    </tr>
    <tr>
      <td>俄文</td>
      <td>ru</td>
    </tr>
    <tr>
      <td>葡萄牙文</td>
      <td>pt</td>
    </tr>
    <tr>
      <td>意大利文</td>
      <td>it</td>
    </tr>
  </tbody>
</table>
</div>

## 設置

要運行該應用程序，您需要設置您的 Azure 文本翻譯訂閱密鑰和服務區域。

### 創建 Azure 資源

1. 登錄 [Azure 門戶](https://portal.azure.com/)
2. 搜索並創建「翻譯器」資源
3. 創建完成後，進入資源頁面
4. 在左側菜單中點擊「密鑰和終結點」
5. 複製其中一個密鑰和位置/區域信息

### 配置環境變量

應用程序需要以下環境變量：
- `SUBSCRIPTION_KEY`: 您的 Azure 翻譯服務訂閱密鑰
- `SERVICE_REGION`: 您的 Azure 翙譯服務區域（例如: eastasia, westus 等）

## 部署到 Streamlit Cloud

您可以將此應用程序部署到 Streamlit Community Cloud，讓其他人通過互聯網訪問：

1. 將此項目推送到 GitHub 倉庫
2. 訪問 [Streamlit Community Cloud](https://streamlit.io/cloud)
3. 登錄或創建一個帳戶
4. 點擊 "New app" 按鈕
5. 選擇您的 GitHub 倉庫
6. 配置應用程序設置：
   - 選擇正確的分支（通常是 main 或 master）
   - 設置主文件為 `app.py`
7. 在 "Advanced settings" 中添加應用程序所需的密鑰：
   - 添加 `SUBSCRIPTION_KEY` 變量及其值
   - 添加 `SERVICE_REGION` 變量及其值
8. 點擊 "Deploy!" 按鈕
9. 等待部署完成，然後訪問您的應用程序

## 本地運行

如果您想在本地運行應用程序：

1. 克隆項目到本地
2. 創建虛擬環境並激活它
3. 安裝依賴項：
   ```bash
   pip install -r requirements.txt
   ```
4. 創建 `.env` 文件並配置環境變量：
   ```
   SUBSCRIPTION_KEY=your_actual_subscription_key
   SERVICE_REGION=your_service_region
   ```
5. 運行應用：
   ```bash
   streamlit run app.py
   ```

## 引用
了解更多關於 Microsoft Azure 上的文本翻譯服務 [here](https://learn.microsoft.com/en-us/azure/ai-services/translator/text-translation/overview)