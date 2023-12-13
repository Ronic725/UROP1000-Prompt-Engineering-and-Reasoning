from langchain import PromptTemplate #用于 PromptTemplate 为字符串提示创建模板
from langchain.prompts.pipeline import PipelinePromptTemplate #for multiple prompt merging

#base class of all prompt generators, provide single prompt given arguments
class PromptGenerator:
    def __init__(self, promptFString):
        self.prompt_template = PromptTemplate.from_template(
            promptFString
            #Sample: "Tell me a {adjective} joke about {content}."
        )
    
    def generatePrompt(self,**kwargs):
        formatted_prompt = self.prompt_template.format(**kwargs)
        return formatted_prompt


#prompt generator for MAD situation:
class MADPromptGenerator:
    def __init__(self, prePromptGuide, postPromptGuide, numOfAgents):
        self.prePromptGuide = PromptTemplate.from_template( prePromptGuide)
        self.postPromptGuide = PromptTemplate.from_template(postPromptGuide)
        self.numOfAgents = numOfAgents
        self.angentsAnsGuide = PromptTemplate.from_template("\n\n".join( [f" One agent response:{{example{index}}}" for index in range(numOfAgents)]))

    def generatePrompt(self, prevAgentsInputs, currentAgentIndex,currentRound, preInputs=None,postInputs=None):
        if preInputs !=None:
            prePrompt = self.prePromptGuide.format(preInputs)
        else:
            prePrompt =  self.prePromptGuide.format()
        
        if postInputs != None:
            postPrompt = self.postPromptGuide.format(postInputs)
        else:
            postPrompt = self.postPromptGuide.format()
        
        
        fullPrompt = prePrompt + "\n \n"
        for i in range(currentRound):
            currentAgentInput = prevAgentsInputs[i][currentAgentIndex]
            fullPrompt = fullPrompt +  f"Your Answer: {currentAgentInput}" + "\n\n"
            prevAgentsInputs[i][currentAgentIndex] = " "
            print(i,prevAgentsInputs[i])
            currentRoundAgentsContext = self.angentsAnsGuide.format(*(prevAgentsInputs[i]))
            fullPrompt = fullPrompt + "These are the recent/updated opinions from other agents:"+ currentRoundAgentsContext + "\n \n"
            prevAgentsInputs[i][currentAgentIndex] = currentAgentInput
        
        fullPrompt += postPrompt

        return fullPrompt

        

        
