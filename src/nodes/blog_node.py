from src.states.blogstate import BlogState
from langchain_core.messages import SystemMessage, HumanMessage
from src.states.blogstate import Blog

class BlogNode:
    """A class to represent a blog node in the application."""

    def __init__(self, llm):
        self.llm = llm

    def title_creation(self, state: BlogState):
        """Generate a title for the blog post based on the given topic."""

        if "topic" in state and state["topic"]:
            prompt = """ 
                      you are a professional blog writer. Write a catchy and engaging title for a blog post about the following topic: {topic}. The title should be seo-friendly, attention-grabbing, and relevant to the topic. Please provide only the title without any additional text or explanation.
                       
                      """
            system_message = prompt.format(topic=state["topic"])
            response = self.llm.invoke(system_message)
            return {"blog": {"title": response.content}}


    def content_generation(self, state: BlogState):
        """Generate content for the blog post based on the given title and topic."""

        if "blog" in state and "title" in state["blog"] and "topic" in state:
            prompt = """
                      you are a professional blog writer. Write a detailed and informative blog post based on the following title: {title} and topic: {topic}. The blog post should be well-structured, engaging, and provide valuable information to the readers. Please provide only the content of the blog post without any additional text or explanation.
                      """
            system_message = prompt.format(title=state["blog"]["title"], topic=state["topic"])
            response = self.llm.invoke(system_message)
            return {"blog": {"title": state["blog"]["title"], "content": response.content}} 


    def translation(self, state: BlogState):
        """Translate the blog post content into the specified language."""
        translation_prompt = """
        you are a professional translator. Translate the following blog post content into {current_language}. The translation should be accurate, fluent, and maintain the original meaning and tone of the content. Please provide only the translated content without any additional text or explanation.
        Original Content: 
        {blog_content}
        """
        blog_content = state["blog"]["content"]
        messages=[ 
            HumanMessage(translation_prompt.format(current_language=state["current_language"],blog_content=blog_content))
        ]
        translation_content=self.llm.invoke(messages)
        return {"blog":{"content":translation_content}}

    def route(self, state:BlogState ):
        return {"current_language": state['current_language']}


    def route_decision(self, state:BlogState):
        if state["current_language"]=="hindi":
           return "hindi"
        elif state["current_language"]=="french":
           return "french"
        else:
           return state["current_language"]