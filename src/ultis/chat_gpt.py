from openai import OpenAI

client = OpenAI(api_key="")

def openai_response(input_text):
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": input_text + "\n Hãy loại bỏ các ký tự đặc biệt, trả lời ngắn gọn và không cần đề mục."
            }
        ]
    )

    return completion.choices[0].message.content


if __name__ == "__main__":
    print(openai_response("Tôi muốn biết về bệnh mốc lá"))
