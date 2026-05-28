from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Prompt")

@mcp.prompt()  
def get_prompt(topic: str) -> str:
    """
    Returns a prompt that will do a detailed analysis on a topic.
    Args:
        topic: the topic to do research on
    """
    return f"Do a detailed analysis on the following topic with proper research format and in the last make a summary of the topic: {topic}"

@mcp.prompt()  
def write_detailed_historical_report(topic: str, number_of_paragraphs: int) -> str:
    """
    Writes a detailed historical report.
    Args:
        topic: the topic to do research on
        number_of_paragraphs: number of paragraphs for the main body
    """
    prompt = """
    Create a concise research report on the history of {topic}. 
    The report should contain 3 sections: INTRODUCTION, MAIN, and CONCLUSION.
    The MAIN section should be {number_of_paragraphs} paragraphs long. 
    Include a timeline of key events.
    The conclusion should be in bullet points format. 
    """
    return prompt.format(topic=topic, number_of_paragraphs=number_of_paragraphs)

if __name__ == "__main__":
    mcp.run()