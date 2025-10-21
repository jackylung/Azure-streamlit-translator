import streamlit as st
import requests
import json
import logging
from dotenv import load_dotenv
import os

# 設置日誌記錄
logging.basicConfig(level=logging.DEBUG, format="[%(asctime)s] %(levelname)s: %(message)s", datefmt="%m/%d/%Y %I:%M:%S %p %Z")
logger = logging.getLogger(__name__)

# 載入環境變數
load_dotenv()
SUBSCRIPTION_KEY = os.getenv('SUBSCRIPTION_KEY')
SERVICE_REGION = os.getenv('SERVICE_REGION')

# 檢查環境變量是否正確加載
if not SUBSCRIPTION_KEY:
    logger.error("未設置 SUBSCRIPTION_KEY 環境變量")
if not SERVICE_REGION:
    logger.error("未設置 SERVICE_REGION 環境變量")

logger.info(f"加載環境變量 - SUBSCRIPTION_KEY: {'已設置' if SUBSCRIPTION_KEY else '未設置'}, SERVICE_REGION: {SERVICE_REGION or '未設置'}")

# 配置 Streamlit 頁面
st.set_page_config(page_title="Azure Translator 翻譯器", page_icon="🌐", initial_sidebar_state="auto", layout='centered')

# 應用標題和描述
NAME = "Azure Translator 翻譯器"
DESCRIPTION = "使用 Azure AI 翻譯服務"

# 支持的語言列表
supported_languages = {
    '自動檢測': 'auto',
    '中文(繁體)': 'zh-Hant',
    '中文(簡體)': 'zh-Hans',
    '英文': 'en',
    '日文': 'ja',
    '韓文': 'ko',
    '法文': 'fr',
    '德文': 'de',
    '西班牙文': 'es',
    '阿拉伯文': 'ar',
    '俄文': 'ru',
    '葡萄牙文': 'pt',
    '意大利文': 'it'
}

def translate_text(text, target_language, source_language='auto'):
    """
    使用 Azure Text Translation API 翻譯文本
    :param text: 要翻譯的文本
    :param target_language: 目標語言代碼
    :param source_language: 源語言代碼，默認為 'auto' 自動檢測
    :return: 翻譯後的文本
    """
    logger.debug(f"開始翻譯文本: {text[:50]}...")
    logger.debug(f"目標語言: {target_language}, 源語言: {source_language}")
    
    # 檢查憑據
    if not SUBSCRIPTION_KEY or not SERVICE_REGION:
        logger.error("缺少 Azure 認證信息")
        return None
    
    # Azure Text Translation API 端點
    endpoint = "https://api.cognitive.microsofttranslator.com"
    path = '/translate'
    constructed_url = endpoint + path
    
    logger.debug(f"API 端點: {constructed_url}")

    # 請求參數
    params = {
        'api-version': '3.0',
        'to': target_language
    }
    
    # 如果指定了源語言，則添加到參數中
    if source_language != 'auto':
        params['from'] = source_language
    
    logger.debug(f"請求參數: {params}")

    # 請求頭
    headers = {
        'Ocp-Apim-Subscription-Key': SUBSCRIPTION_KEY,
        'Ocp-Apim-Subscription-Region': SERVICE_REGION,
        'Content-Type': 'application/json',
    }
    
    logger.debug(f"請求頭: {headers}")

    # 請求體
    body = [{
        'Text': text
    }]
    
    logger.debug(f"請求體: {body}")

    # 發送請求
    try:
        logger.info("發送翻譯請求到 Azure Translator API")
        response = requests.post(constructed_url, params=params, headers=headers, json=body)
        logger.info(f"API 響應狀態碼: {response.status_code}")
        logger.debug(f"API 響應頭: {dict(response.headers)}")
        
        # 記錄響應內容（注意不要記錄敏感信息）
        if response.status_code < 400:
            logger.debug(f"API 響應內容: {response.text[:200]}...")
        else:
            logger.error(f"API 錯誤響應: {response.text}")
            
        response.raise_for_status()  # 如果請求失敗會拋出異常
        result = response.json()
        logger.debug(f"解析後的 JSON 結果: {result}")
        translated_text = result[0]['translations'][0]['text']
        logger.info(f"翻譯成功: {translated_text[:50]}...")
        return translated_text
    except requests.exceptions.RequestException as e:
        logger.error(f'翻譯請求失敗: {str(e)}')
        logger.error(f'請求URL: {constructed_url}')
        logger.error(f'請求參數: {params}')
        return None
    except (KeyError, IndexError) as e:
        logger.error(f'解析翻譯結果失敗: {str(e)}')
        logger.error(f'響應結果: {result if "result" in locals() else "無結果"}')
        return None
    except Exception as e:
        logger.error(f'翻譯過程發生未知錯誤: {str(e)}')
        return None

def detect_language(text):
    """
    檢測文本的語言
    :param text: 要檢測的文本
    :return: 檢測到的語言代碼
    """
    logger.debug(f"開始檢測語言，文本: {text[:50]}...")
    
    # 檢查憑據
    if not SUBSCRIPTION_KEY or not SERVICE_REGION:
        logger.error("缺少 Azure 認證信息")
        return None
    
    # Azure Text Translation API 端點
    endpoint = "https://api.cognitive.microsofttranslator.com"
    path = '/detect'
    constructed_url = endpoint + path
    
    logger.debug(f"API 端點: {constructed_url}")

    # 請求參數
    params = {
        'api-version': '3.0'
    }
    
    logger.debug(f"請求參數: {params}")

    # 請求頭
    headers = {
        'Ocp-Apim-Subscription-Key': SUBSCRIPTION_KEY,
        'Ocp-Apim-Subscription-Region': SERVICE_REGION,
        'Content-Type': 'application/json',
    }
    
    logger.debug(f"請求頭: {headers}")

    # 請求體
    body = [{
        'Text': text
    }]
    
    logger.debug(f"請求體: {body}")

    # 發送請求
    try:
        logger.info("發送語言檢測請求到 Azure Translator API")
        response = requests.post(constructed_url, params=params, headers=headers, json=body)
        logger.info(f"API 響應狀態碼: {response.status_code}")
        logger.debug(f"API 響應頭: {dict(response.headers)}")
        
        # 記錄響應內容（注意不要記錄敏感信息）
        if response.status_code < 400:
            logger.debug(f"API 響應內容: {response.text[:200]}...")
        else:
            logger.error(f"API 錯誤響應: {response.text}")
            
        response.raise_for_status()  # 如果請求失敗會拋出異常
        result = response.json()
        logger.debug(f"解析後的 JSON 結果: {result}")
        detected_lang = result[0]['language']
        logger.info(f"語言檢測成功: {detected_lang}")
        return detected_lang
    except requests.exceptions.RequestException as e:
        logger.error(f'語言檢測請求失敗: {str(e)}')
        logger.error(f'請求URL: {constructed_url}')
        logger.error(f'請求參數: {params}')
        return None
    except (KeyError, IndexError) as e:
        logger.error(f'解析語言檢測結果失敗: {str(e)}')
        logger.error(f'響應結果: {result if "result" in locals() else "無結果"}')
        return None
    except Exception as e:
        logger.error(f'語言檢測過程發生未知錯誤: {str(e)}')
        return None

def get_supported_languages():
    """
    獲取支持的語言列表
    :return: 支持的語言列表
    """
    logger.debug("開始獲取支持的語言列表")
    
    # Azure Text Translation API 端點
    endpoint = "https://api.cognitive.microsofttranslator.com"
    path = '/languages'
    constructed_url = endpoint + path
    
    logger.debug(f"API 端點: {constructed_url}")

    # 請求參數
    params = {
        'api-version': '3.0',
        'scope': 'translation'
    }
    
    logger.debug(f"請求參數: {params}")

    # 發送請求
    try:
        logger.info("發送語言列表請求到 Azure Translator API")
        response = requests.get(constructed_url, params=params)
        logger.info(f"API 響應狀態碼: {response.status_code}")
        logger.debug(f"API 響應頭: {dict(response.headers)}")
        
        # 記錄響應內容（注意不要記錄敏感信息）
        if response.status_code < 400:
            logger.debug(f"API 響應內容大小: {len(response.text)} 字符")
        else:
            logger.error(f"API 錯誤響應: {response.text}")
            
        response.raise_for_status()  # 如果請求失敗會拋出異常
        result = response.json()
        logger.debug(f"解析後的 JSON 結果包含 {len(result)} 個鍵")
        language_list = result['translation']
        logger.info(f"成功獲取語言列表，共 {len(language_list)} 種語言")
        return language_list
    except requests.exceptions.RequestException as e:
        logger.error(f'獲取語言列表請求失敗: {str(e)}')
        logger.error(f'請求URL: {constructed_url}')
        logger.error(f'請求參數: {params}')
        return None
    except (KeyError, IndexError) as e:
        logger.error(f'解析語言列表結果失敗: {str(e)}')
        logger.error(f'響應結果: {result if "result" in locals() else "無結果"}')
        return None
    except Exception as e:
        logger.error(f'獲取語言列表過程發生未知錯誤: {str(e)}')
        return None

def main():
    """
    主應用函數
    """
    logger.debug("開始執行主函數")
    
    # 應用標題
    st.title("Azure Translator 翻譯器")
    
    # 檢查環境變量配置
    if not SUBSCRIPTION_KEY or not SERVICE_REGION:
        st.error("❌ 缺少 Azure 認證信息")
        st.info("請在項目根目錄創建 `.env` 文件，並配置 `SUBSCRIPTION_KEY` 和 `SERVICE_REGION` 環境變量。")
        st.info("請參考 `.env.example` 文件的格式進行配置。")
        return
    
    # 用戶界面
    st.subheader("文本翻譯")
    
    # 創建兩列佈局
    col1, col2 = st.columns(2)
    
    # 源語言選擇
    with col1:
        source_lang_name = st.selectbox('選擇源語言', list(supported_languages.keys()), index=0)
        source_lang_code = supported_languages[source_lang_name]
        logger.debug(f"用戶選擇的源語言: {source_lang_name} ({source_lang_code})")
    
    # 目標語言選擇
    with col2:
        target_lang_name = st.selectbox('選擇目標語言', list(supported_languages.keys()), index=2)  # 默認選中英文
        target_lang_code = supported_languages[target_lang_name]
        logger.debug(f"用戶選擇的目標語言: {target_lang_name} ({target_lang_code})")
    
    # 文本輸入區域
    text_input = st.text_area(f'輸入文本', height=150)
    logger.debug(f"用戶輸入的文本長度: {len(text_input)} 字符")
    
    # 翻譯按鈕
    translate_button = st.button("翻譯")
    logger.debug(f"用戶點擊翻譯按鈕: {translate_button}")
    
    # 當用戶點擊翻譯按鈕時執行翻譯
    if translate_button:
        logger.info("用戶點擊翻譯按鈕，開始處理翻譯請求")
        if text_input.strip() != '':
            logger.debug("文本輸入有效，開始翻譯流程")
            with st.spinner("正在翻譯..."):
                # 如果選擇了自動檢測，則先檢測語言
                if source_lang_code == 'auto':
                    logger.info("用戶選擇自動檢測語言")
                    detected_lang = detect_language(text_input)
                    if detected_lang:
                        logger.info(f"檢測到語言: {detected_lang}")
                        st.info(f"檢測到的語言: {detected_lang}")
                        # 調用翻譯函數，使用檢測到的語言作為源語言
                        logger.debug(f"開始翻譯，源語言: {detected_lang}，目標語言: {target_lang_code}")
                        translated_text = translate_text(text_input, target_lang_code, detected_lang)
                    else:
                        logger.error("語言檢測失敗")
                        st.error("無法檢測語言，請手動選擇源語言")
                        translated_text = None
                else:
                    # 調用翻譯函數
                    logger.debug(f"開始翻譯，源語言: {source_lang_code}，目標語言: {target_lang_code}")
                    translated_text = translate_text(text_input, target_lang_code, source_lang_code)
                
                if translated_text:
                    logger.info("翻譯成功")
                    st.success('翻譯成功 ✅')
                    # 顯示翻譯結果
                    st.text_area(f'翻譯結果 ({target_lang_name})', translated_text, height=150)
                else:
                    logger.error("翻譯失敗")
                    st.error("翻譯失敗，請檢查您的 Azure 認證信息是否正確配置 ❌")
        else:
            logger.info("用戶未輸入文本")
            st.info("請輸入要翻譯的文本 😄")

# 程序入口點
if __name__ == '__main__':
    logger.debug("應用開始運行")
    main()
    logger.debug("應用運行結束")