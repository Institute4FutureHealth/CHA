import json
import os


class TaskCreator:
    def __init__(self):
        self.class_name = None
        self.description = None
        self.dependencies = []
        self.inputs = []
        self.outputs = []
        self.output_type = False
        self.return_direct = False

    def get_user_input(self, prompt, input_type=str):
        while True:
            user_input = input(f"{prompt}: ")
            try:
                user_input = input_type(user_input)
                break
            except ValueError:
                print("Invalid input. Please enter a valid value.")
        return user_input

    def generate_task(self):
        self.class_name = self.get_user_input("Enter the name of the sub-class")
        self.description = self.get_user_input("Enter the description of the sub-class")

        while True:
            dependency = self.get_user_input("Enter a dependency for the sub-class (press Enter to finish)",
                                             input_type=str)
            if not dependency:
                break
            self.dependencies.append(dependency)

        while True:
            input_description = self.get_user_input("Enter an input for the sub-class (press Enter to finish)",
                                                    input_type=str)
            if not input_description:
                break
            self.inputs.append(input_description)

        while True:
            output_description = self.get_user_input("Enter an output for the sub-class (press Enter to finish)",
                                                     input_type=str)
            if not output_description:
                break
            self.outputs.append(output_description)

        self.output_type = self.get_user_input("Does the sub-class have an output type? (True/False)", input_type=bool)
        self.return_direct = self.get_user_input("Should the sub-class return the result directly? (True/False)",
                                                 input_type=bool)

        class_template = f"""from typing import Any
from typing import List
from tasks.task import BaseTask
from datapipes.datapipe import DataPipe


class {self.class_name}(BaseTask):
    \"\"\"
    {self.description}
    \"\"\"

    name: str = "{self.class_name.lower()}"
    chat_name: str = "{self.class_name}Chat"
    description: str = {json.dumps(self.description)}
    dependencies: List[str] = {self.dependencies}
    inputs: List[str] = {self.inputs}
    outputs: List[str] = {self.outputs}
    datapipe: DataPipe = None
    output_type: bool = {str(self.output_type)}
    return_direct: bool = {str(self.return_direct)}

    def _execute(self, inputs: List[Any]) -> str:
        return inputs[0]
    
"""

        file_name = f"{self.class_name.lower()}.py"
        file_path = os.path.join("tasks", file_name)

        with open(file_path, "w") as class_file:
            class_file.write(class_template)
            print(f"Task '{self.class_name}' created successfully in '{file_name}'.")

    def generate_test(self):

        class_template = f"""from src.tasks.{self.class_name.lower()} import {self.class_name}


def test_{self.class_name.lower()}_execute():
    user_input = "User input text."
    obj = {self.class_name}()

    result = obj._execute([user_input])

    assert result == user_input


"""

        file_name = f"test_{self.class_name.lower()}.py"
        file_path = os.path.join("../tests/unit_tests/tasks", file_name)

        with open(file_path, "w") as class_file:
            class_file.write(class_template)
            print(f"Test 'test_{self.class_name}' created successfully in '{file_name}'.")


def main():
    task_creator = TaskCreator()
    task_creator.generate_task()
    task_creator.generate_test()


if __name__ == "__main__":
    main()
