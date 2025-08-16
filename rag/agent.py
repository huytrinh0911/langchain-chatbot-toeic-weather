print("agent: > thu vien")
print("-------------")
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain.memory import ConversationBufferMemory
from langchain.prompts import MessagesPlaceholder
from langchain.prompts import ChatPromptTemplate
from tools import (model_gemini,
                   get_weather,
                   toeic_question)
                

tools = [get_weather, toeic_question]

# Pull the prompt template from the hub
# prompt = hub.pull("hwchase17/openai-tools-agent")

system = """Bạn là một AI có thể sử dụng các công cụ (tool) sau [get_weather, toeic_question]:
1. toeic_question tool: Trả lời các câu hỏi liên quan đến bài thi TOEIC (không hỏi thêm thông tin ngoài lề).
2. get_weather tool: Trả lời câu hỏi về thời tiết hiện tại hoặc thời gian của một thành phố.
3. Nếu câu hỏi không thuộc 2 nhóm trên và bạn biết câu trả lời, hãy trả lời trực tiếp mà không dùng tool.

Quy tắc:
- Luôn xác định loại câu hỏi trước khi trả lời.
- Nếu câu hỏi yêu cầu thông tin về TOEIC → dùng tool toeic_question. 
- Các câu hỏi về TOEIC thì nên giữ nguyên hoặc viết lại rõ hơn trước khi đưa vào tool.
- Nếu câu hỏi yêu cầu thời tiết hoặc thời gian ở một địa điểm cụ thể → dùng tool get_weather.
- Nếu có thể trả lời ngay mà không cần tool → trả lời trực tiếp.
- Không đoán thông tin nếu không chắc, hãy nói rõ nếu bạn không biết.
- Khi dùng tool, chỉ chọn đúng 1 tool phù hợp nhất với câu hỏi.
"""
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system),    
        MessagesPlaceholder("chat_history"),  # thêm lịch sử trò chuyện      
        ("human", "{input}"),
        MessagesPlaceholder("agent_scratchpad")
    ]
)
memory = ConversationBufferMemory(
    memory_key="chat_history", return_messages=True)    #Tạo memory cho đoạn chat

# Create the ReAct agent using the create_tool_calling_agent function
# This function sets up an agent capable of calling tools based on the provided prompt.
agent = create_tool_calling_agent(
    llm=model_gemini,  # Language model to use
    tools=tools,  # List of tools available to the agent
    prompt=prompt,  # Prompt template to guide the agent's responses
)

# Create the agent executor
agent_executor = AgentExecutor.from_agent_and_tools(
    agent=agent,  # The agent to execute
    tools=tools,  # List of tools available to the agent
    memory= memory,
    verbose=True,  # Enable verbose logging
    handle_parsing_errors=True,  # Handle parsing errors gracefully
)


def chat_with_agent(user_input: str):
    response = agent_executor.invoke({"input": user_input})
    return response["output"]
print("agent: DONE")
print("-------------")