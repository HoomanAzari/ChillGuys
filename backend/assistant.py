import vehicles
from enum import Enum
from langchain_community.vectorstores import Chroma
from langchain_nomic.embeddings import NomicEmbeddings
from langchain.prompts import PromptTemplate
from langchain_community.chat_models import ChatOllama
from langchain_core.output_parsers import JsonOutputParser


class Assistant:

    class Interaction:

        class Source:
            AI = 0
            HUMAN = 1

        def __init__(self, source: Source, message: str):
            self.src = source
            self.message = message

        def __str__(self):
            source = "AI: " if self.src == Assistant.Interaction.Source.AI \
                    else "HUMAN: "
            return source + self.message

    def __init__(self,
                 vehicles_list: list[vehicles.Vehicle],
                 llama_name: str = "llama3.2:1b"):
        span = slice(1, 10)
        vehicles_str = [str(vehicle) for vehicle in vehicles_list]
        for vehicle in vehicles_list[span]:
            print(f"{vehicle.Make} {vehicle.Model} {vehicle.Body}")
        texts = vehicles_str[span]
        self.retriever = Chroma.from_texts(
            # texts=vehicles_str,
            texts=texts,
            collection_name="rag-chroma",
            embedding=NomicEmbeddings(
                model="nomic-embed-text-v1.5",
                # device="cpu",
                inference_mode="local",
            )).as_retriever()
        # print(f"GOT RETRIEVER {self.retriever}")
        # template = PromptTemplate(template=\
        #                           """You are a helpful AI assistant tasked with assisting humans with their inquiries about the cars available at a given dealership. You are given the past history of the conversation You are also given a list of all the available vehicles at that dealship. \nHere is a history: \n\n {history} \n\nHere are the possibly relevant vehicles: \n\n {vehicles} \n\n The human's latest response is : \n\n {question} \n\nYour response as the AI:
        #                 """,
        #                                input_variables=["history", "vehicles", "question"])
        template = PromptTemplate(template=\
                                  """You are a helpful AI assistant designed to assist customers with their inquiries about the cars available at a specific dealership. You have access to the conversation history and a list of all the vehicles available at the dealership.\nConversation History: \n\n{history}\n\nAvailable vehicles: \n\n{vehicles}\n\nCustomer's Latest Query:\n\n{question}\n\nYour Response as the AI:""",
                                       input_variables=["history", "vehicles", "question"])
        # print(f"GOT TEMPLATE {template}")
        llm_model = ChatOllama(
            model=llama_name,
            temparature=0,
            #num_predict=40
        )
        # print(f"GOT LLAMA {llm_model}")
        self.model = template | llm_model

    def stringify_interaction_history(self, interactions: list[Interaction]):
        return "\n".join([str(interaction) for interaction in interactions])

    def prompt_bot(self, past_interactions: list[Interaction],
                   latest_message: str) -> str:
        """
            Generates response for latest message, given history of interactions and the latest message.
        """
        relevant_documents = []
        for interaction in past_interactions:
            if (interaction.src == Assistant.Interaction.Source.AI):
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
    assistant = Assistant(vehicles_list)
    interaction_history = [
        Assistant.Interaction(
            Assistant.Interaction.Source.AI,
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
            Assistant.Interaction(Assistant.Interaction.Source.HUMAN,
                                  user_prompt))
        interaction_history.append(
            Assistant.Interaction(Assistant.Interaction.Source.AI, res))
        print(res)


if __name__ == "__main__":
    main()
