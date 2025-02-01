import dspy

lm=dspy.LM('ollama_chat/deepseek-r1:14b', 
           api_base='https://8507-34-87-139-237.ngrok-free.app',
           api_key='')

response = lm(messages=[{"role": "user", "content": "Say this is a test!"}]) # => ['This is a test!']
print(response)