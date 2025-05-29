from openai import OpenAI

client = OpenAI(api_key="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")

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
