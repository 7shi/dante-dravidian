from xml.dom.minidom import Document, parseString
from llm7shi.compat import generate_with_schema

class LLMClient:
    def __init__(self, model, think):
        self.model = model
        self.think = think
        self.history = []

    def call(self, prompt, system_prompt=None):
        """Call LLM and automatically add query/response to history.

        Args:
            prompt: User prompt text
            system_prompt: Optional system prompt (used only for first call)

        Returns:
            Response text from LLM
        """
        messages = []
        if system_prompt:
            messages.append({'role': 'system', 'content': system_prompt})
        messages.extend(self.history)
        messages.append({'role': 'user', 'content': prompt})

        response = generate_with_schema(messages, model=self.model, include_thoughts=self.think, show_params=False)
        response_text = response.text.strip()

        # Automatically add to history
        if system_prompt:
            self.history.append({'role': 'system', 'content': system_prompt})
        self.history.append({'role': 'user', 'content': prompt})
        self.history.append({'role': 'assistant', 'content': response_text})

        return response_text

def history_to_xml(history):
    """Convert LLM interaction history to XML format.

    Args:
        history: List of message dictionaries with 'role' and 'content'

    Returns:
        XML string representing the history
    """
    doc = Document()
    messages = doc.createElement("messages")
    doc.appendChild(messages)
    for msg in history:
        message = doc.createElement("message")
        message.setAttribute("role", msg["role"])
        content = msg["content"].rstrip()
        if content:
            message.appendChild(doc.createCDATASection(f"\n{content}\n"))
        messages.appendChild(message)
    return doc.toprettyxml(encoding='utf-8', indent='').decode('utf-8')

def xml_to_history(xml_string):
    """Convert XML format back to LLM interaction history.

    Args:
        xml_string: XML string representing the history

    Returns:
        List of message dictionaries with 'role' and 'content'
    """
    doc = parseString(xml_string)
    history = []
    for message in doc.getElementsByTagName("message"):
        role = message.getAttribute("role")
        content = ""
        for child in message.childNodes:
            if child.nodeType == child.CDATA_SECTION_NODE:
                content = child.data
                if content.startswith('\n'):
                    content = content[1:]
                break
        history.append({"role": role, "content": content})
    return history
