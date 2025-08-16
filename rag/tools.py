print("tools: > thu vien")
print("-------------")
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from langchain.tools import tool
from pydantic import BaseModel, Field
import requests
from langchain.prompts import ChatPromptTemplate
# from langchain_community.vectorstores import Chroma
# from langchain.embeddings import SentenceTransformerEmbeddings
# from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_core.output_parsers import StrOutputParser
from operator import itemgetter


print("tools: > api key")
print("-------------")
# Load environment variables from .env file
load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")
weather_api = os.getenv("WEATHER_API_KEY")
model_gemini = ChatGoogleGenerativeAI(
    api_key = gemini_api_key,
    model="gemini-2.5-flash",
    temperature=0.1,
)

print("tools: > toeic_qs")
print("-------------")
#==========================================================={TOOL: toeic_question}
"""Trả lời các câu hỏi về kì thi TOEIC dựa vào thông tin tổ chức IIG VIỆT NAM"""
def format_qa_pair(question, answer):
    """Format Q and A pair"""
    formatted_string = ""
    formatted_string += f"Question: {question}\nAnswer: {answer}\n\n"
    return formatted_string.strip()

current_dir = os.getcwd()
persistent_directory = os.path.abspath(os.path.join(current_dir,".." ,"db"))
# sentence_tranformer_ef = SentenceTransformerEmbeddings(model_name="AITeamVN/Vietnamese_Embedding") 
embedding_model = HuggingFaceEmbeddings(model_name="AITeamVN/Vietnamese_Embedding")
vectorBD = Chroma(embedding_function=embedding_model,
                  persist_directory=persistent_directory)
retriever = vectorBD.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 4},
)


#--------------------------------------------------------------
'''Tách thành các câu hỏi đa dạng nhưng cùng ý nghĩa'''
# Decomposition
template = """
Bạn là một trợ lý AI liên quan đến kì thi TOEIC ở Việt Nam. Nhiệm vụ của bạn là tạo ra 2 phiên bản diễn đạt khác nhau của câu đầu vào sau bằng tiếng Việt, 
nhằm tìm kiếm được nhiều tài liệu liên quan nhất từ cơ sở dữ liệu vector. 
Các phiên bản mới cần giữ nguyên ý nghĩa gốc nhưng sử dụng cách diễn đạt hoặc từ khóa khác, 
có thể mở rộng phạm vi truy vấn nếu hợp lý. 
Xuất ra 2 câu hỏi thay thế, mỗi câu trên một dòng.
Câu hỏi gốc: {question}
Kết quả:
"""
prompt_decomposition = ChatPromptTemplate.from_template(template)
# Chain
generate_queries_decomposition = ( 
                                  prompt_decomposition 
                                  | model_gemini 
                                  | StrOutputParser()
                                  | (lambda x: x.split("\n")))


#--------------------------------------------------------------
'''Đưa ra câu trả lời hoàn chỉnh dựa vào các thông tin đã có'''
template = """Bạn là một trợ lý AI thông minh, nhiệm vụ của bạn là trả lời câu hỏi của người dùng dựa trên thông tin được cung cấp.
Câu hỏi của người dùng: {question}.\n
Dữ liệu nền (cặp câu hỏi + câu trả lời trước đây, nếu có):
{q_a_pairs}\n
Ngữ cảnh bổ sung (trích xuất từ cơ sở dữ liệu liên quan đến câu hỏi):
{context}\n
YÊU CẦU:
- Chỉ sử dụng thông tin trong phần ngữ cảnh và dữ liệu nền để trả lời.
- Nếu không tìm thấy thông tin liên quan, hãy trả lời: "Xin lỗi, tôi không tìm thấy thông tin để trả lời câu hỏi này."
- Giữ câu trả lời ngắn gọn, rõ ràng, và đúng trọng tâm.
- Nếu có thể, hãy trích dẫn nguồn từ metadata (ví dụ: tên tài liệu hoặc số trang).

Câu trả lời:
"""
decomposition_prompt = ChatPromptTemplate.from_template(template)
rag_chain = (
            {"context": itemgetter("question") | retriever, 
            "question": itemgetter("question"),
            "q_a_pairs": itemgetter("q_a_pairs")} 
            | decomposition_prompt
            | model_gemini
            | StrOutputParser())


#--------------------------------------------------------------
'''Set up hàm toeic_question thành tool của agent''' 
class ToeicQueryInput(BaseModel):
    question: str = Field(description="The question about TOEIC test")


@tool(args_schema=ToeicQueryInput)
def toeic_question(question: str):
    """Hàm trả lời các câu hỏi về kì thi TOEIC ở Việt Nam. Nhận tất cả câu hỏi liên quan đến TOEIC.
    Giải đáp về: 
    - Dịch vụ sau thi.
    - Hỗ trợ khách hàng.
    - Hướng dẫn dự thi.
    - Mọi quy dịnh liên quan đến kì thi TOEIC
    
    """
    questions = generate_queries_decomposition.invoke({"question":question})
    q_a_pairs = ""
    list_answers = []
    for q in questions:
        
        rag_chain = (
                    {"context": itemgetter("question") | retriever, 
                    "question": itemgetter("question"),
                    "q_a_pairs": itemgetter("q_a_pairs")} 
                    | decomposition_prompt
                    | model_gemini
                    | StrOutputParser())

        answer = rag_chain.invoke({"question":q,"q_a_pairs":q_a_pairs})
        list_answers.append(answer)
        q_a_pair = format_qa_pair(q,answer)
        q_a_pairs = q_a_pairs + "\n---\n"+  q_a_pair
    return answer



print("tools: > weather")
print("-------------")
#==========================================================={TOOL: get_weather}
'''Set up hàm get_weather thành tool của agent'''
class WeatherInput(BaseModel):
    city: str = Field(description="Name of the city to get the weather and time for")

@tool(name_or_callable="TIMEandWEATHER",
      args_schema=WeatherInput)
def get_weather(city:str):
    """
      Đây là hàm cá thể trả lời về Thời gian (giờ, time) và thời tiết (weather) hiện tại của city được gọi.
      Đầu vào là tên thành phố viết theo chuẩn Tiếng Anh. Ví dụ: Hà Nội -> Ha Noi.
      Trả lời đầy đủ tất cả các thông tin có được. 
    """
    url = f"http://api.weatherapi.com/v1/current.json?key={weather_api}&q={city}&aqi=no"
    response = requests.get(url)
    information = response.json()
    '''
    # result_dict = {
    #   'city': information["location"]["name"],
    #   'country': information["location"]["country"],
    #   'localtime': information["location"]["localtime"],
    #   'temp_c': information["current"]["temp_c"],
    #   'temp_f': information["current"]["temp_f"],
    #   'condition': information["current"]["condition"]["text"],
    #   'wind_kph': information["current"]["wind_kph"],        
    #   'humidity': information["current"]["humidity"],           
    #   }
    '''
    result = (
    f"Thành phố: {information['location']['name']}, {information['location']['country']}\n"
    f"Giờ địa phương: {information['location']['localtime']}\n"
    f"Nhiệt độ: {information['current']['temp_c']}°C / {information['current']['temp_f']}°F\n"
    f"Tình trạng: {information['current']['condition']['text']}\n"
    f"Tốc độ gió: {information['current']['wind_kph']} km/h\n"
    f"Độ ẩm: {information['current']['humidity']}%"
    )
    return result


print("tools: DONE")
print("-------------")


