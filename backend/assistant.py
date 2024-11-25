import vehicles
import os
from enum import Enum
from langchain_community.vectorstores import Chroma
from langchain_nomic.embeddings import NomicEmbeddings
from langchain.prompts import PromptTemplate
from langchain_ollama import OllamaEmbeddings
from langchain_community.chat_models import ChatOllama
from langchain_core.output_parsers import JsonOutputParser
from abc import ABC, abstractmethod


class ChatBot(ABC):

    class Interaction:

        class Source:
            AI = 0
            HUMAN = 1

        def __init__(self, source: Source, message: str):
            self.src = source
            self.message = message

        def __str__(self):
            source = "AI: " if self.src == self.Source.AI \
                else "HUMAN: "
            return source + self.message

    def stringify_interaction_history(self, interactions: list[Interaction]):
        return "\n".join([str(interaction) for interaction in interactions])

    @abstractmethod
    def prompt_bot(self, past_interactions: list[Interaction],
                   latest_message: str) -> str:
        pass


class ChillGuyChatbot(ChatBot):
    def __init__(self, llama_name: str = "llama3"):
        template = PromptTemplate(
            template="""Prompt:\nYou are an AI chat assistant designed to have casual and friendly conversations with users. Your persona is based on the "Chill Guy" meme, also known as "My New Character." Your responses should be relaxed, easygoing, and concise, helping users feel at ease during their interaction. You have access to the past conversation history to maintain context and continuity.\nKey Characteristics of the "Chill Guy" Tone:\n - Relaxed and easygoing\n - Friendly and approachable\n - Calm and unbothered\n - Casual and conversational\n - Short and concise\n - Light-hearted and humorous\n - Patient and supportive\n - Responses to questions about your identity: 'My whole deal is that I'm a chill guy that lowkey dgaf but I'm here to talk.'\n\nConversation History:\n\n{history}\n\nUser's Latest Input:\n\n{user_input}\n\nYour Response as the AI:""",
            input_variables=["history", "user_input"])
        llama = ChatOllama(model=llama_name, temperature=1.)
        self.model = template | llama

    def prompt_bot(self, past_interaction: list[ChatBot.Interaction], latest_message: str) -> str:
        chat_history = self.stringify_interaction_history(past_interaction)
        return self.model.invoke({"history": chat_history, "user_input": latest_message}).content


class ChillGuyCarDealershipAssistant(ChatBot):

    def __init__(self,
                 vehicles_list: list[vehicles.Vehicle],
                 embedding_llama: str = "llama3.2:1b",
                 llama_name: str = "llama3"):
        span = slice(1, len(vehicles_list))
        vehicles_str = [str(vehicle) for vehicle in vehicles_list]
        texts = vehicles_str[span]
        save_directory = "./vectorstore1"

        embedding = OllamaEmbeddings(model=embedding_llama)

        if os.path.exists(save_directory):
            self.retriever = Chroma(
                persist_directory=save_directory,
                embedding_function=embedding).as_retriever()
        else:
            self.retriever = Chroma.from_texts(
                texts=texts,
                collection_name="rag-chroma",
                persist_directory=save_directory,
                embedding=embedding).as_retriever()
        template = PromptTemplate(template="""Prompt:\nYou are an AI chat assistant designed to assist customers with their inquiries about the cars available at a specific dealership. You have access to the conversation history and a subset of the vehicles that another AI has identified as relevant for this prompt, but there may be more vehicles that you are not aware of until more context is given. Your responses should be concise, providing just enough information to answer the customer's question without being too long. Additionally, adopt a relaxed and laid-back tone, similar to the "Chill Guy" meme, also known as "My New Character." This means your responses should be calm, friendly, and unbothered, helping customers feel at ease. Unlike the real "Chill Guy," your main challenge is finding the best car for the customer, but you're here to help with that.\n\nKey Characteristics of the "Chill Guy" Tone:\n - Relaxed and easygoing\n - Friendly and approachable\n - Calm and unbothered\n - Casual and conversational\n - Patient and supportive\n - Enthusiastic about finding the best car\n - Short and concise\n - Light-hearted and humorous\n - Enthusiastic about finding the best car\n - \nConversation History: \n\n{history}\n\nAvailable vehicles: \n\n{vehicles}\n\nCustomer's Latest Query:\n\n{question}\n\nYour Response as the AI:""",
                                  input_variables=["history", "vehicles", "question"])
        llm_model = ChatOllama(
            model=llama_name,
            temparature=0.25,
        )
        self.model = template | llm_model

    def prompt_bot(self, past_interactions: list[ChatBot.Interaction],
                   latest_message: str) -> str:
        """
            Generates response for latest message, given history of interactions and the latest message.
        """
        relevant_documents = []
        for interaction in past_interactions:
            if (interaction.src ==
                    ChillGuyCarDealershipAssistant.Interaction.Source.AI):
                continue
            docs = self.retriever.get_relevant_documents(interaction.message)
            relevant_documents.extend(docs)

        docs = self.retriever.get_relevant_documents(latest_message)
        relevant_documents.extend(docs)

        relevant_documents = [
            relevant_document.page_content
            for relevant_document in relevant_documents
        ]
        chat_history = self.stringify_interaction_history(past_interactions)
        relevant_vehicles = "\n".join(relevant_documents)
        return self.model.invoke({
            "history": chat_history,
            "vehicles": relevant_vehicles,
            "question": latest_message
        }).content


def main():
    print("RETRIEVING VEHICLES")
    vehicles_list = vehicles.Vehicle.get_objects("../vehicles.json")
    print("INNITIATING ASSISTANT")
    assistant = ChillGuyCarDealershipAssistant(vehicles_list)
    interaction_history = [
        ChillGuyCarDealershipAssistant.Interaction(
            ChillGuyCarDealershipAssistant.Interaction.Source.AI,
            "They make it look so easy, connecting with another human. It's like no one ever told them, it's the hardest thing in the world. How can I help you today ?"
        )
    ]
    while True:
        user_prompt = input("> ")
        if user_prompt == "q":
            break
        print("INITIATION ANSWER")
        res = assistant.prompt_bot(interaction_history, user_prompt)
        interaction_history.append(
            ChillGuyCarDealershipAssistant.Interaction(
                ChillGuyCarDealershipAssistant.Interaction.Source.HUMAN,
                user_prompt))
        interaction_history.append(
            ChillGuyCarDealershipAssistant.Interaction(
                ChillGuyCarDealershipAssistant.Interaction.Source.AI, res))
        print(res)


if __name__ == "__main__":
    main()
