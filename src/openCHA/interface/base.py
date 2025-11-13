import os
from pathlib import Path
from typing import Any
from typing import Dict

from pydantic import BaseModel
from pydantic import Extra
from pydantic import model_validator


class Interface(BaseModel):
    gr: Any = None
    interface: Any = None

    @model_validator(mode="before")
    def validate_environment(cls, values: Dict) -> Dict:
        """
        Validate that api key and python package exists in environment.

        This function checks if the `gradio` Python package is installed in the environment. If the package is not found, it raises a `ValueError`
        with an appropriate error message.

        Args:
            cls (object): The class to which this method belongs.
            values (Dict): A dictionary containing the environment values.
        Return:
            Dict: The updated `values` dictionary with the `gradio` package imported.
        Raise:
            ValueError: If the `gradio` package is not found in the environment.

        """

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

    def _load_custom_css(self) -> str:
        """
        Load custom CSS file for styling the interface.

        Returns:
            str: The CSS content as a string, or empty string if file not found.
        """
        css_path = Path(__file__).parent / "styles.css"
        try:
            with open(css_path, "r", encoding="utf-8") as f:
                return f.read()
        except FileNotFoundError:
            return ""
        except Exception as e:
            print(f"Warning: Could not load custom CSS: {e}")
            return ""

    def prepare_interface(
        self,
        respond,
        reset,
        upload_meta,
        available_tasks,
        share=False,
    ):
        """
        Prepare the Gradio interface for the chatbot.

        This method sets up the Gradio interface for the chatbot.
        It creates various UI components such as a textbox for user input, a checkbox for enabling/disabling chat history,
        a dropdown for selecting tasks, and a clear button to reset the interface. The interface is then launched and stored
        in the `self.interface` attribute.

        Args:
            self (object): The instance of the class.
            respond (function): The function to handle user input and generate responses.
            reset (function): The function to reset the chatbot state.
            upload_meta (Any): meta data.
            available_tasks (list, optional): A list of available tasks. Defaults to an empty list.
            share (bool, optional): Flag indicating whether to enable sharing the interface. Defaults to False.
        Return:
            None

        """

        def submit_api_keys(openai_api_key, serp_api_key):
            # Set environment variables
            os.environ["OPENAI_API_KEY"] = openai_api_key
            os.environ["SEPR_API_KEY"] = serp_api_key

            print("keys submitted")
            print(openai_api_key)

        # Load custom CSS
        custom_css = self._load_custom_css()
        
        # Define welcome message (used for initialization and reset)
        welcome_message = [(None, "Welcome to OpenCHA! 👋\n\nI'm your AI-powered health and wellness assistant. How can I help you today?")]

        with self.gr.Blocks(css=custom_css, title="OpenCHA Assistant") as demo:
            # Main layout: Left sidebar for tasks, Right side for main content
            with self.gr.Row():
                # Left Sidebar: Tasks List
                with self.gr.Column(scale=1, min_width=250):
                    with self.gr.Column(elem_classes=["tasks-sidebar"]):
                        with self.gr.Column(elem_classes=["tasks-header"]):
                            self.gr.Markdown("## 📋 Available Tasks")
                        
                        # Create checkboxes for each task
                        task_checkboxes = []
                        
                        with self.gr.Column(elem_classes=["tasks-container"]):
                            for task in available_tasks:
                                checkbox = self.gr.Checkbox(
                                    label=task,
                                    value=False,
                                    elem_classes=["task-checkbox-item"]
                                )
                                task_checkboxes.append(checkbox)
                        
                        # Store selected tasks - will be updated by checkboxes
                        tasks = self.gr.State(value=[])
                        
                        # Function to collect selected tasks from all checkboxes
                        def collect_selected_tasks(*checkbox_values):
                            selected = [available_tasks[i] for i, checked in enumerate(checkbox_values) if checked]
                            return selected
                        
                        # Update tasks state whenever any checkbox changes
                        if task_checkboxes:
                            def update_tasks(*vals):
                                return [available_tasks[i] for i, checked in enumerate(vals) if checked]
                            
                            for checkbox in task_checkboxes:
                                checkbox.change(
                                    fn=update_tasks,
                                    inputs=task_checkboxes,
                                    outputs=[tasks],
                                    queue=False
                                )
                
                # Right Side: Main content
                with self.gr.Column(scale=4):
                    # Chatbot section - full width
                    chatbot = self.gr.Chatbot(
                        bubble_full_width=False,
                        value=welcome_message,
                        height=600,
                        show_label=False,
                        container=True
                    )
                    
                    # Input row - compact
                    with self.gr.Row():
                        msg = self.gr.Textbox(
                            scale=8,
                            label="Question",
                            info="Type your question and press Enter",
                            placeholder="Ask me anything...",
                        )
                        with self.gr.Column(scale=1):
                            btn = self.gr.UploadButton(
                                "+",
                                file_types=["image", "video", "audio", "text"],
                                elem_classes=["circular-upload-button"]
                            )
                            check_box = self.gr.Checkbox(
                                value=True,
                                label=" ",
                                elem_classes=["toggle-switch"]
                            )

                    # Settings in accordion - collapsible (API keys only now)
                    with self.gr.Accordion("⚙️ Settings", open=False):
                        with self.gr.Row():
                            openai_api_key_input = self.gr.Textbox(
                                label="OpenAI API Key",
                                info="Enter your OpenAI API key",
                                type="password",
                                scale=1,
                            )
                            serp_api_key_input = self.gr.Textbox(
                                label="Serp API Key",
                                info="Enter your Serp API key",
                                type="password",
                                scale=1,
                            )

            def reset_with_welcome():
                reset()
                return "", welcome_message
            
            clear = self.gr.ClearButton([msg, chatbot])
            clear.click(
                reset_with_welcome,
                outputs=[msg, chatbot]
            )

            # Wrapper function to collect current checkbox values and call respond
            def respond_with_current_tasks(message, openai_key, serp_key, history, use_hist, tasks_state, *checkbox_values):
                # Collect selected tasks from checkbox values
                current_tasks = [available_tasks[i] for i, checked in enumerate(checkbox_values) if checked]
                return respond(message, openai_key, serp_key, history, use_hist, current_tasks)
            
            # Include all task checkboxes as inputs
            all_inputs = [
                msg,
                openai_api_key_input,
                serp_api_key_input,
                chatbot,
                check_box,
                tasks,
            ] + task_checkboxes
            
            msg.submit(
                respond_with_current_tasks,
                all_inputs,
                [msg, chatbot],
            )

            btn.upload(
                upload_meta, [chatbot, btn], [chatbot], queue=False
            )

        demo.launch(share=share)
        self.interface = demo

    def close(self):
        """
        Close the Gradio interface.

        This method closes the Gradio interface associated with the chatbot.
        It calls the `close` method of the interface object stored in the `self.interface` attribute.

        Args:
            self (object): The instance of the class.
        Return:
            None
        """

        self.interface.close()
