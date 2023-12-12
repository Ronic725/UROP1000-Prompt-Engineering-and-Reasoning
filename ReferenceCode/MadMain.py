import ReferenceCode.ProcessHandler as ProcessHandler
import ReferenceCode.PromptGenerators as PromptGenerators
import numpy as np

if __name__ == "__main__":
    agents = 2
    rounds = 3
    ph = ProcessHandler.MADProcessHandler(rounds,agents,
         "Make sure to state your answer at the end of the response."
         ,"Use these opinions carefully as additional advice, can you provide an updated answer? Make sure to state your answer at the end of the response.")
    
    a, b, c, d, e, f = np.random.randint(0, 30, size=6)

    answer = a + b * c + d - e * f
    question_prompt = "What is the result of {}+{}*{}+{}-{}*{}?".format(a, b, c, d, e, f)
    print(ph.generateAnswer(question_prompt))