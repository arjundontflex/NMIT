from gpt_index import SimpleDirectoryReader, GPTListIndex,GPTSimpleVectorIndex,LLMPredictor, PromptHelper,ServiceContext 
from langchain import OpenAI
import sys
import os

os.environ["OPENAI_API_KEY"] = "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"

def createVectorIndex(path):
    max_input = 4096
    tokens = 256
    chunk_size = 600
    max_chunk_overlap = 20

    prompt_helper = PromptHelper(max_input,tokens,max_chunk_overlap,chunk_size_limit=chunk_size)


    #LLM(Large Lng Models)
    llmPredictor = LLMPredictor(llm=OpenAI(temperature=0,model_name="text-ada-001",max_tokens=tokens))

    #loading the data
    docs = SimpleDirectoryReader(path).load_data()

    service_context = ServiceContext.from_defaults(llm_predictor=llmPredictor,prompt_helper=prompt_helper)
    vectorIndex = GPTSimpleVectorIndex.from_documents(documents=docs,service_context=service_context)
    #create vecotr index(which is like an array)
    #vectorIndex = GPTSimpleVectorIndex(documents=docs,llm_predictor=llmPredictor,prompt_helper=prompt_helper)
    vectorIndex.save_to_disk('vectorIndex.json')
    return vectorIndex

vectorIndex = createVectorIndex("D:\BOOKS")

def answerMe(vectorIndex):
    vIndex = GPTSimpleVectorIndex.load_from_disk(vectorIndex)
    while True:
        prompt = input("Please ask me anything: ")
        response = vIndex.query(prompt,response_mode="compact")
        print(f"Response: {response} \n")
        
answerMe('vectorIndex.json')