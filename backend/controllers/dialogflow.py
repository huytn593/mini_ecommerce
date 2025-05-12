from fastapi import HTTPException, status
import os
import json
from google.cloud import dialogflow
from google.oauth2 import service_account

from ..utils.database import Database
from ..utils.logger import logger


async def detect_intent(text: str, session_id: str, language_code: str = "vi"):
    try:
        # Setup Dialogflow client
        dialogflow_token = os.getenv("ecommerce_project/backend/dialogflow-key.json")
        project_id = os.getenv("kowalski-cieb")

        if not dialogflow_token or not project_id:
            return {
                "fulfillment_text": "Cấu hình Dialogflow chưa được thiết lập",
                "all_required_params_present": True,
                "intent_detected": False
            }

        # Create Dialogflow session
        credentials = service_account.Credentials.from_service_account_file(dialogflow_token)
        session_client = dialogflow.SessionsClient(credentials=credentials)
        session = session_client.session_path(project_id, session_id)

        # Create text input
        # Use dictionary format for TextInput
        text_input = {
            "text": text,
            "language_code": language_code
        }
        query_input = {
            "text": text_input
        }

        # Detect intent
        response = session_client.detect_intent(
            request={"session": session, "query_input": query_input}
        )

        # Process response
        query_result = response.query_result

        # Check if we need to query product data
        if query_result.intent.display_name == "ProductRecommendation":
            # Get top 5 newest products
            cursor = Database.db.products.find({}).sort("created_at", -1).limit(5)
            products = await cursor.to_list(length=5)

            product_list = ""
            for i, product in enumerate(products, 1):
                product_list += f"{i}. {product['name']} - {product['price']} VND\n"

            fulfillment_text = f"Đây là những sản phẩm hot nhất hiện nay:\n{product_list}"
        else:
            fulfillment_text = query_result.fulfillment_text

        return {
            "fulfillment_text": fulfillment_text,
            "all_required_params_present": query_result.all_required_params_present,
            "intent_detected": query_result.intent.display_name != ""
        }
    except Exception as e:
        logger.error(f"Dialogflow error: {str(e)}")
        return {
            "fulfillment_text": f"Xin lỗi, tôi không thể xử lý yêu cầu của bạn lúc này.",
            "all_required_params_present": True,
            "intent_detected": False
        }