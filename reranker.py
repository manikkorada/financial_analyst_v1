#Note - Build the reranker for ordering the retrieved documents. 
#Due to token limit and somer other issues unable to use it.

prompt_rerank = """
You are a helpful assistant that ranks paragraphs based on how well they answer the question.

Question: {question}

Paragraphs:
{paragraphs}

Rank the paragraphs from most to least relevant (1 being most relevant). Return the ordered paragraphs.

Output :
Must be the order of numbers don't include like "Answer" or any sentences like "Here are the ordered paragraphs" etc..
Don't include other things like paragraphs just order of the sequence as mentioned below examples.
Example1: [5, 2, 3, 1, 4]
Example2: [3, 5, 1, 2, 4]
"""

docs = retriever.invoke(query)
paragraphs = "\n\n".join([f"{i+1}. {doc.page_content}" for i, doc in enumerate(docs)])
prompt_rerank_v2 = [SystemMessage(content=prompt_rerank.format(question =query, paragraphs = paragraphs))]
rerank_order = llm.invoke(prompt_rerank_v2)
lst = ast.literal_eval(aa)
ordered_paragraphs = [f"{i+1}. {doc.page_content}" for i, doc in enumerate(docs)]
reranked_paragraphs = [ordered_paragraphs[i-1] for i in reranked_indices][:3]
for i in range(len(reranked_paragraphs)):
    retrieve_text += reranked_paragraphs[i][4:]