from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.llms import HuggingFaceEndpoint
from langgraph.graph import END, MessageGraph

def get_retriever():
    return vector_store.as_retriever(search_kwargs={"k": 3})

class RAGOrchestrator:
    def __init__(self):
        self.retriever = get_retriever()
        self.models = {
            "openai": ChatOpenAI(model="gpt-3.5-turbo"),
            "huggingface": HuggingFaceEndpoint(
                repo_id="google/flan-t5-xxl",
                temperature=0.5
            )
        }
        
    def build_graph(self):
        workflow = MessageGraph()
        
        workflow.add_node("retrieve", self.retrieve_context)
        workflow.add_node("generate", self.generate_response)
        
        workflow.add_edge("retrieve", "generate")
        workflow.add_edge("generate", END)
        
        workflow.set_entry_point("retrieve")
        return workflow.compile()
    
    def retrieve_context(self, state):
        return {"context": self.retriever.get_relevant_documents(state["question"])}
    
    def generate_response(self, state):
        selected_model = self.models[state["model"]]
        qa = RetrievalQA.from_chain_type(
            selected_model,
            retriever=self.retriever
        )
        return {"answer": qa.run(state["question"])}