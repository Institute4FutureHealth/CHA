import os
import shutil
import uuid
from typing import Any
from typing import Dict

import numpy as np
from gradio.data_classes import FileData
from gradio_multimodalchatbot import MultimodalChatbot
from pydantic import BaseModel
from pydantic import Extra
from pydantic import model_validator

from default_prompts import DefaultPrompts
from utils import parse_addresses


class Interface(BaseModel):
    gr: Any = None
    interface: Any = None
    run_query: Any = None
    meta_data: Any = None

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


        Example:
            .. code-block:: python

                from langchain import ReActChain, OpenAI
                react = ReAct(llm=OpenAI())

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

    def copy_file(self, file_path):
        os.makedirs("./data", exist_ok=True)
        dest_path = (
            f"./data/{str(uuid.uuid4())}.{file_path.split('.')[-1]}"
        )
        shutil.copy(file_path, dest_path)
        return dest_path

    def add_meta(
        self,
        meta_message,
        metabot_history,
        mic,
    ):
        if self.meta_data is None:
            self.meta_data = []

        new_metas = []
        print(meta_message)
        for file in meta_message["files"]:
            dest_path = self.copy_file(file["path"])
            new_metas.append({"file": FileData(path=dest_path)})

        mic_dest_path = ""
        if mic is not None:
            dest_path = self.copy_file(mic)
            new_metas.append({"file": FileData(path=dest_path)})
            mic_dest_path = dest_path
            meta_message[
                "text"
            ] = "This file is the user audio that contains user question or important information."

        self.meta_data += [
            {
                "description": meta_message["text"],
                "path": meta["file"].path,
                "tag": "user_audio"
                if meta["file"].path == mic_dest_path
                else "other",
            }
            for meta in new_metas
        ]

        metabot_history.append(
            [
                {"text": meta_message["text"], "files": new_metas},
                {"text": "", "files": []},
            ]
        )
        return metabot_history, {"text": "", "files": []}, None

    def prepare_chat_history(self, chat_history):
        chat = []
        for c in chat_history:
            chat.append([c[0].text, c[1].text])
        return chat

    def respond_audio(
        self,
        message,
        chat_history,
        check_box,
        response_generator_main_prompt,
        tasks_list,
        meta_message,
        metabot_history,
        mic,
    ):
        metabot_history, meta_message, mic = self.add_meta(
            meta_message, metabot_history, mic
        )
        message, chat_history = self.respond(
            message,
            chat_history,
            check_box,
            response_generator_main_prompt,
            tasks_list,
        )

        return (
            metabot_history,
            chat_history,
            message,
            meta_message,
            mic,
        )

    def respond(
        self,
        message,
        chat_history,
        check_box,
        response_generator_main_prompt,
        tasks_list,
    ):
        kwargs = {
            "response_generator_main_prompt": response_generator_main_prompt
        }

        query, response, meta_data = self.run_query(
            query=message,
            meta=self.meta_data,
            chat_history=self.prepare_chat_history(chat_history),
            available_tasks=tasks_list,
            use_history=check_box,
            **kwargs,
        )

        files = [
            {"file": FileData(path=meta.path)} for meta in meta_data
        ]
        chat_history.append(
            [
                {"text": query, "files": []},
                {
                    "text": response,
                    "files": files,
                },
            ]
        )

        self.meta_data = []
        return "", chat_history

    def prepare_interface(
        self,
        reset,
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



        Example:
            .. code-block:: python

                from langchain import ReActChain, OpenAI
                react = ReAct(llm=OpenAI())

        """

        with self.gr.Blocks() as demo:
            with self.gr.Row():
                with self.gr.Column(scale=9):
                    chatbot = MultimodalChatbot()
                    with self.gr.Row():
                        msg = self.gr.Textbox(
                            scale=9,
                            label="Question",
                            info="Put your query here and press enter.",
                        )
                        check_box = self.gr.Checkbox(
                            scale=1,
                            value=True,
                            label="Use History",
                            info="If checked, the chat history will be used for answering.",
                        )
                    with self.gr.Row():
                        tasks = self.gr.Dropdown(
                            scale=9,
                            value=[],
                            choices=available_tasks,
                            multiselect=True,
                            label="Tasks List",
                            info="The list of available tasks. Select the ones that you want to use.",
                        )

                with self.gr.Column(scale=4):
                    with self.gr.Row():
                        metabot = MultimodalChatbot(label="Meta Data")
                    with self.gr.Row():
                        meta_msg = self.gr.MultimodalTextbox(
                            scale=9,
                            interactive=True,
                            file_types=[
                                "file"
                            ],  # all files should be supported
                            label="Question",
                            info="Put your query here and press enter.",
                            placeholder="Enter message or upload file...",
                        )
                    with self.gr.Row():
                        mic = self.gr.Audio(
                            scale=4,
                            sources=["microphone"],
                            type="filepath",
                        )

            with self.gr.Row():
                response_generator_main_prompt = self.gr.Textbox(
                    scale=9,
                    label="Respnose Generator Prompt",
                    info="Put your prompt for the response generator here.",
                    value=DefaultPrompts.RESPONSE_GENERATOR_MAIN_PROMPT,
                )

            clear = self.gr.ClearButton([msg, chatbot, mic, meta_msg])

            clear.click(reset)
            msg.submit(
                self.respond,
                [
                    msg,
                    chatbot,
                    check_box,
                    response_generator_main_prompt,
                    tasks,
                ],
                [msg, chatbot],
            )
            meta_msg.submit(
                self.add_meta,
                [
                    meta_msg,
                    metabot,
                    mic,
                ],
                [metabot, meta_msg, mic],
            )

            mic.stop_recording(
                self.respond_audio,
                [
                    msg,
                    chatbot,
                    check_box,
                    response_generator_main_prompt,
                    tasks,
                    meta_msg,
                    metabot,
                    mic,
                ],
                [metabot, chatbot, msg, meta_msg, mic],
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



        Example:
            .. code-block:: python

                from langchain import ReActChain, OpenAI
                react = ReAct(llm=OpenAI())

        """

        self.interface.close()
