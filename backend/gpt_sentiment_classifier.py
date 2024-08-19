import openai
import ast

class GptSentimentClassifier:
    """
    A class to classify sentiment of sentences using the GPT model.

    Attributes:
    -----------
    message_history : list
        A list of messages representing the conversation history.
    """

    def __init__(self, message_history: list) -> None:
        """
        Initializes the GptSentimentClassifier with a conversation history.

        Parameters:
        -----------
        message_history : list
            A list of dictionaries representing the message history for the chat.
        """
        with open("key.txt", "r") as file:
            openai.api_key = file.read().strip()
        self.message_history = message_history

    def get_message_history(self) -> list:
        """
        Returns the current message history.

        Returns:
        --------
        list
            The message history of the chat.
        """
        return self.message_history

    def chat(self) -> list:
        """
        Starts an interactive chat session with the GPT model.

        Returns:
        --------
        list
            The updated message history after the chat session.
        """
        is_continue = True
        while is_continue:
            input_s = input(">")
            self.message_history.append({"role": "user", "content": input_s})

            try:
                completion = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=self.message_history
                )
                reply_content = completion.choices[0].message.content
                print(reply_content)
                self.message_history.append({"role": "assistant", "content": reply_content})
            except openai.error.OpenAIError as e:
                print(f"An error occurred: {e}")
                break

            yes_or_no = input("Would you like to continue to chat? (Yes:y, No:n) ")
            if yes_or_no.lower() == "n":
                is_continue = False

        return self.message_history

    def classify_sentence(self, sentence: str) -> str:
        """
        Classifies the sentiment of a given sentence using the GPT model.

        Parameters:
        -----------
        sentence : str
            The sentence to be classified.

        Returns:
        --------
        str
            The sentiment result returned by the GPT model.
        """
        self.message_history.append({"role": "user", "content": sentence})

        try:
            completion = openai.ChatCompletion.create(
                model="gpt-4",
                messages=self.message_history
            )
            sentiment_result = completion.choices[0].message.content
            self.message_history.append({"role": "assistant", "content": sentiment_result})
            return sentiment_result
        except openai.error.OpenAIError as e:
            print(f"An error occurred while classifying the sentence: {e}")
            return "Error in sentiment classification."

if __name__ == '__main__':
    with open('message_history.txt', "r", encoding="utf-8") as file:
        message_history = ast.literal_eval(file.read())
    
    gpt_classifier = GptSentimentClassifier(message_history)
    sentiment = gpt_classifier.classify_sentence("Küresel piyasalarda ABD'den gelen veriler geçen haftanın öne çıkan gündem maddeleri olurken, Türkiye'de TCMB'nin attığı adımlar ve açıklanan veriler izlendi.")
    print(f"Sentiment: {sentiment}")
