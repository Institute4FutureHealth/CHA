from pydantic import BaseModel, model_validator, Extra
from typing import Any, Dict

class Interface(BaseModel):
  gr: Any = None
  interface: Any = None

  @model_validator(mode='before')
  def validate_environment(cls, values: Dict) -> Dict:
    """Validate that api key and python package exists in environment."""
    try:
      import gradio as gr
      values["gr"] = gr
    except ImportError:
      raise ValueError(
        "Could not import gradio python package. "
        "Please install it with `pip install gradio`."
      )
    return values
  
  class Config:
    """Configuration for this pydantic object."""

    extra = Extra.forbid
    arbitrary_types_allowed = True

  def prepare_interface(self, respond, reset, available_tasks=[], share=False):
    with self.gr.Blocks() as demo:
      chatbot = self.gr.Chatbot()
      with self.gr.Row():
        with self.gr.Column(scale=10):
          msg = self.gr.Textbox(label="Question", info="Put your query here and press enter.")
        with self.gr.Column(scale=1):
          check_box = self.gr.Checkbox(value=True, label="Use History", info="If checked, the chat history will be sent over along with the next query.")
      
      with self.gr.Row():
          tasks = self.gr.Dropdown(value=available_tasks, choices=available_tasks, multiselect=True, label="Tasks List", info="The list of available tasks. Select the ones that you want to use.")
      clear = self.gr.ClearButton([msg, chatbot])

      clear.click(reset)
      msg.submit(respond, [msg, chatbot, check_box, tasks], [msg, chatbot])

    demo.launch(share=share)
    self.interface = demo 

  def close(self):
    self.interface.close()