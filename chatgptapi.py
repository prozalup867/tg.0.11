import openai
import time

# устанавливаем ключ API OpenAI из переменной окружения
openai.api_key = "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"

def rewrite_text(text):
    prompt = f"Given the following text, remove all hyperlinks (including 'Read More'), any references to competitors' websites, and any other mention of websites. Make the text more concise by removing any personal opinions and adding 3 emojis at the beginning of the text that describe its tone. Use Russian language\n\n{text}\n\nRewritten text:"
    while True:
        try:
            response = openai.Completion.create(
                model="text-davinci-003",
                prompt=prompt,
                temperature=0.3,
                max_tokens=1000,
                top_p=1.0,
                frequency_penalty=0.5,
                presence_penalty=0.0,
                stop=["/n"]
            )
            rewritten_text = response.choices[0].text
            break
        except openai.api_errors.RateLimitError as e:
            print(f"Rate limit reached. Retrying in {e.wait_seconds} seconds...")
            time.sleep(e.wait_seconds + 1) # Добавляем задержку на указанное время ожидания плюс 1 секунда
        except Exception as e:
            print(f"Unexpected error occurred: {e}")
            break

    return rewritten_text
