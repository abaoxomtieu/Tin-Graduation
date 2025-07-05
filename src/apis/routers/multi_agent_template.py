from fastapi import APIRouter, status, Depends, UploadFile, Form
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel, Field
from typing import Optional, List
import json
from langchain_core.messages.ai import AIMessageChunk
from src.agents.multi_agent.flow import app
from src.utils.logger import logger
from src.utils.helper import preprocess_messages
from src.apis.middlewares.auth_middleware import get_current_user
from typing import Annotated
from pydantic import BaseModel, Field, EmailStr

router = APIRouter(prefix="/ai", tags=["AI"])


class User(BaseModel):
    id: str = Field("", description="User's id")
    email: EmailStr = Field("", description="User's email")
    role: str = Field("", description="User's role")

    class Config:
        json_schema_extra = {
            "example": {
                "id": "123",
                "email": "johnUS192@gmail.com",
                "role": "user",
            }
        }


user_dependency = Annotated[User, Depends(get_current_user)]


async def message_generator(input_graph: dict, config: dict):
    last_output_state = None
    temp = ""
    async for event in app.astream(
        input=input_graph,
        stream_mode=["messages", "values"],
        config=config,
    ):
        # try:
        event_type, event_message = event
        if event_type == "messages":
            message, metadata = event_message
            if isinstance(message, AIMessageChunk):
                temp += message.content
                yield json.dumps(
                    {
                        "type": "message",
                        "content": temp,
                    },
                    ensure_ascii=False,
                ) + "\n\n"
                logger.info(f"Message: {message.content}")
        if event_type == "values":
            last_output_state = event_message

    if last_output_state is None:
        raise ValueError("No output state received from workflow")

    if "messages" not in last_output_state:
        raise ValueError("No LLM response in output")

    # try:
    final_response = json.dumps(
        {
            "type": "final",
            "content": {
                "final_response": last_output_state["messages"][-1].content,
                "selected_ids": last_output_state.get("selected_ids", []),
                "selected_documents": last_output_state.get("selected_documents", []),
            },
        },
        ensure_ascii=False,
    )
    yield final_response + "\n\n"


@router.post("/multi_agent_template/stream")
async def multi_agent_template_stream(
    user: user_dependency,
    query: str = Form(...),
    conversation_id: Optional[str] = Form(None),
    attachs: List[UploadFile] = [],
):
    try:
        logger.info(f"User: {user}")
        email = "admin@gmail.com"
        messages = await preprocess_messages(query, attachs)

        config = {
            "configurable": {
                "thread_id": conversation_id,
                "email": email,
            }
        }
        input_graph = {
            "messages": messages,
        }

        return StreamingResponse(
            message_generator(
                input_graph=input_graph,
                config=config,
            ),
            media_type="text/event-stream",
        )
    except Exception as e:
        logger.error(f"Error in streaming endpoint: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error": f"Streaming error: {str(e)}"},
        )
