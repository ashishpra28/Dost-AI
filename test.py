# from langchain_groq import ChatGroq
# from dotenv import load_dotenv
# load_dotenv()


# res = ChatGroq(model="openai/gpt-oss-20b")

# print(res.invoke("hi bro").content)

from tools import search_youtube_video

result = search_youtube_video.invoke({
    "youtube_url": "https://youtu.be/QDLlQ5IL2Bk?si=_8ePbRQbNOv2SwUz",
    "question": "What is this video about?"
})

print(result)