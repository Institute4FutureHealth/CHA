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

  def prepare_interface(self, respond, share=True):
    with self.gr.Blocks() as demo:
      chatbot = self.gr.Chatbot()
      msg = self.gr.Textbox()
      clear = self.gr.ClearButton([msg, chatbot])

      msg.submit(respond, [msg, chatbot], [msg, chatbot])

    demo.launch(share=share)
    self.interface = demo 

  def close(self):
    self.interface.close()