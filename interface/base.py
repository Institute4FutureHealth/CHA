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

  def prepare_interface(self, respond, reset, upload_meta, available_tasks=[], share=False):
    with self.gr.Blocks() as demo:
      chatbot = self.gr.Chatbot(bubble_full_width=False)
      with self.gr.Row():
        msg = self.gr.Textbox(scale=9, label="Question", info="Put your query here and press enter.")
        btn = self.gr.UploadButton("📁", scale=1, file_types=["image", "video", "audio", "text"])
        check_box = self.gr.Checkbox(scale=1, value=True, label="Use History", info="If checked, the chat history will be sent over along with the next query.")
      
      with self.gr.Row():
        tasks = self.gr.Dropdown(value=available_tasks, choices=available_tasks, multiselect=True, label="Tasks List", info="The list of available tasks. Select the ones that you want to use.")
      clear = self.gr.ClearButton([msg, chatbot])

      clear.click(reset)
      msg.submit(respond, [msg, chatbot, check_box, tasks], [msg, chatbot])
      file_msg = btn.upload(upload_meta, [chatbot, btn], [chatbot], queue=False)

    demo.launch(share=share)
    self.interface = demo 

  def close(self):
    self.interface.close()