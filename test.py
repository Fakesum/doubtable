from doubtable.scraper.gpt import ChatgptMainThread

print(ChatgptMainThread._gpt_request({
    "messages": [
        {
            "role": "user",
            "content": "hello"
        }
    ]
}))