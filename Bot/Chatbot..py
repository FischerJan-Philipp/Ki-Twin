from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

def chat_with_bot(time_delay=1):
    chatbot = ChatBot("Narcissist",
        storage_adapter="chatterbot.storage.SQLStorageAdapter",
        logic_adapters=[
            "chatterbot.logic.BestMatch",
            "chatterbot.logic.SpecificResponseAdapter"
        ],
        input_adapter="chatterbot.input.TerminalAdapter",
        output_adapter="chatterbot.output.TerminalAdapter",
        database_uri="sqlite:///database.sqlite3"
    )

    trainer = ChatterBotCorpusTrainer(chatbot)
    trainer.train("chatterbot.corpus.english.greetings")
    trainer.train("chatterbot.corpus.english.conversations")

    print("Bot: ", chatbot.get_response("Hello"))
    print("Bot: ", chatbot.get_response("What's your name?"))

    while True:
        try:
            user_input = input("User: ")
            if user_input.lower() == "exit":
                break

            response = chatbot.get_response(user_input)
            print("Bot: ", response)
            time.sleep(time_delay)

        except(KeyboardInterrupt, EOFError, SystemExit):
            break

chat_with_bot(time_delay=3)