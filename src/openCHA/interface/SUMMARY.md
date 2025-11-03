# Gradio UI Logic Summary - base.py

## Overview
The `Interface` class in `base.py` is a Pydantic-based wrapper around Gradio that creates a chatbot web interface. It handles UI component creation, event binding, and interface lifecycle management.

---

## Class Structure

### Interface Class (Pydantic BaseModel)
- **Attributes**:
  - `gr`: Gradio module (imported at initialization)
  - `interface`: Gradio Blocks instance (created after launch)

### Configuration
- Uses Pydantic `BaseModel` with `extra=Extra.forbid` and `arbitrary_types_allowed=True`

---

## Initialization Logic

### `validate_environment()` (model_validator)
**Purpose**: Validates Gradio installation and imports it

**Process**:
1. Attempts to `import gradio as gr`
2. Stores `gr` in `values["gr"]`
3. Raises `ValueError` if import fails with message: "Could not import gradio python package. Please install it with `pip install gradio`."

**Note**: This runs automatically when the class is instantiated (Pydantic model_validator).

---

## Interface Setup - `prepare_interface()`

### Method Signature
```python
def prepare_interface(
    self,
    respond,           # Callback function for processing user queries
    reset,             # Callback function for resetting state
    upload_meta,       # Callback function for handling file uploads
    available_tasks,   # List of available task names (strings)
    share=False,       # Whether to enable Gradio sharing (public link)
)
```

### UI Components Created

#### 1. Chatbot Display (Line 86)
```python
chatbot = self.gr.Chatbot(bubble_full_width=False)
```
- Displays conversation history
- **Warning**: Currently uses deprecated tuples format. Should use `type='messages'` for OpenAI-style dicts.

#### 2. Input Row (Lines 87-103)
Contains three components in a horizontal row:
- **Textbox** (`msg`): 
  - Scale: 9 (takes 9 parts of the row)
  - Label: "Question"
  - Info: "Put your query here and press enter."
  - Used for user query input
  
- **Upload Button** (`btn`):
  - Scale: 1 (takes 1 part of the row)
  - Icon: 📁
  - File types: ["image", "video", "audio", "text"]
  - Handles file uploads
  
- **Checkbox** (`check_box`):
  - Scale: 1
  - Default value: True
  - Label: "Use History"
  - Info: "If checked, the chat history will be sent over along with the next query."
  - Controls whether chat history is used in processing

#### 3. Tasks Selection Row (Lines 105-112)
- **Dropdown** (`tasks`):
  - Default value: [] (empty list)
  - Choices: `available_tasks` (list of task name strings)
  - Multiselect: True (users can select multiple tasks)
  - Label: "Tasks List"
  - Info: "The list of available tasks. Select the ones that you want to use."

#### 4. API Keys Row (Lines 114-122)
- **OpenAI API Key Textbox** (`openai_api_key_input`):
  - Label: "OpenAI API Key"
  - Info: "Enter your OpenAI API key here."
  
- **Serp API Key Textbox** (`serp_api_key_input`):
  - Label: "Serp API Key"
  - Info: "Enter your Serp API key here."

**Note**: There's a nested function `submit_api_keys()` defined (lines 77-83) but it's **NOT currently used** in the interface. API keys are handled directly in the `respond` callback.

---

## Event Handlers

### 1. Clear Button Handler (Lines 124-125)
```python
clear = self.gr.ClearButton([msg, chatbot])
clear.click(reset)
```
- **Action**: Clears both `msg` (textbox) and `chatbot` (chat history)
- **Callback**: Calls `reset()` function
- **When**: User clicks the clear button

### 2. Message Submit Handler (Lines 127-138)
```python
msg.submit(
    respond,
    [msg, openai_api_key_input, serp_api_key_input, chatbot, check_box, tasks],
    [msg, chatbot],
)
```
- **Trigger**: User presses Enter in the message textbox
- **Callback**: `respond()` function
- **Inputs** (in order):
  1. `msg` - User's query text
  2. `openai_api_key_input` - OpenAI API key string
  3. `serp_api_key_input` - Serp API key string
  4. `chatbot` - Current chat history (list of tuples)
  5. `check_box` - Boolean value for "Use History" checkbox
  6. `tasks` - List of selected task names (strings)
- **Outputs**:
  1. `msg` - Cleared (empty string returned)
  2. `chatbot` - Updated chat history

### 3. File Upload Handler (Lines 140-142)
```python
btn.upload(
    upload_meta, [chatbot, btn], [chatbot], queue=False
)
```
- **Trigger**: User uploads a file via the upload button
- **Callback**: `upload_meta()` function
- **Inputs**:
  1. `chatbot` - Current chat history
  2. `btn` - Uploaded file object (Gradio file handle)
- **Output**: Updated `chatbot` with file reference
- **Queue**: False (runs immediately, not queued)

### 4. Launch (Line 144)
```python
demo.launch(share=share)
self.interface = demo
```
- Launches the Gradio web server
- If `share=True`, creates a public shareable link
- Stores the demo instance in `self.interface`

---

## Required Callback Functions

The `prepare_interface()` method expects three callback functions. These are typically methods from the `openCHA` class:

### 1. `respond()` Function

**Expected Signature**:
```python
def respond(
    message,                    # str: User's query text
    openai_api_key_input,       # str: OpenAI API key
    serp_api_key_input,         # str: Serp API key  
    chat_history,               # List[Tuple[str, str]]: Current chat history
    check_box,                  # bool: Whether to use history
    tasks_list,                 # List[str]: Selected task names
    **kwargs                    # Additional keyword arguments
) -> Tuple[str, List[Tuple[str, str]]]
```

**Expected Behavior**:
1. Set environment variables from API keys:
   - `os.environ["OPENAI_API_KEY"] = openai_api_key_input`
   - `os.environ["SEPR_API_KEY"] = serp_api_key_input`
2. Process the query using internal `_run()` method with:
   - `query=message`
   - `chat_history=chat_history`
   - `tasks_list=tasks_list`
   - `use_history=check_box`
3. Parse file addresses from response using `parse_addresses()` utility
4. Update chat history:
   - If no files found: append `(message, response)` to history
   - If files found: split response around file addresses and append segments with file references
5. Return: `("", chat_history)` - empty string for cleared input, updated history

**Implementation Example** (from `openCHA.py`):
```python
def respond(self, message, openai_api_key_input, serp_api_key_input, 
            chat_history, check_box, tasks_list, **kwargs):
    os.environ["OPENAI_API_KEY"] = openai_api_key_input
    os.environ["SEPR_API_KEY"] = serp_api_key_input
    response = self._run(
        query=message,
        chat_history=chat_history,
        tasks_list=tasks_list,
        use_history=check_box,
        **kwargs
    )
    files = parse_addresses(response)
    if len(files) == 0:
        chat_history.append((message, response))
    else:
        # Handle file addresses in response...
        for i in range(len(files)):
            chat_history.append((message if i == 0 else None, 
                                response[: files[i][1]]))
            chat_history.append((None, (files[i][0],)))
            response = response[files[i][2]:]
    return "", chat_history
```

### 2. `reset()` Function

**Expected Signature**:
```python
def reset() -> None
```

**Expected Behavior**:
- Reset internal state (e.g., clear previous actions, reset orchestrator)
- No return value needed

**Implementation Example** (from `openCHA.py`):
```python
def reset(self):
    self.previous_actions = []
```

### 3. `upload_meta()` Function

**Expected Signature**:
```python
def upload_meta(
    history,    # List[Tuple[str, str]]: Current chat history
    file        # Gradio file object: Uploaded file handle
) -> List[Tuple[str, str]]
```

**Expected Behavior**:
1. Add file reference to chat history: `history + [((file.name,), None)]`
2. Store file name in metadata list: `self.meta.append(file.name)`
3. Return updated history

**Implementation Example** (from `openCHA.py`):
```python
def upload_meta(self, history, file):
    history = history + [((file.name,), None)]
    self.meta.append(file.name)
    return history
```

---

## Utility Functions Used

### `parse_addresses()` (from `openCHA.utils`)
**Purpose**: Extracts file addresses from response strings

**Signature**:
```python
def parse_addresses(input_string: str) -> List[Tuple[str, int, int]]
```

**Behavior**:
- Searches for pattern: `"address:filename.ext"` where ext is png, csv, or json
- Returns list of tuples: `(filename, start_index, end_index)`
- Used to split responses that contain file references

**Example**:
```python
parse_addresses("Here is your result address:chart.png and more text")
# Returns: [("chart.png", start_index, end_index)]
```

---

## Cleanup - `close()`

**Purpose**: Shuts down the Gradio interface

**Method**:
```python
def close(self):
    self.interface.close()
```

**Usage**: Call this when the interface should be terminated.

---

## Integration Example

From `openCHA.py`, the interface is set up like this:

```python
def run_with_interface(self, **kwargs):
    available_tasks = [key.value for key in TASK_TO_CLASS.keys()]
    interface = Interface()
    interface.prepare_interface(
        respond=lambda *args, **inner_kwargs: self.respond(*args, **kwargs, **inner_kwargs),
        reset=self.reset,
        upload_meta=self.upload_meta,
        available_tasks=available_tasks,
    )
```

**Flow**:
1. Get list of available tasks from `TASK_TO_CLASS` dictionary
2. Create `Interface()` instance (validates Gradio installation)
3. Call `prepare_interface()` with callbacks bound to `openCHA` instance methods
4. Interface launches and runs until closed

---

## Data Formats

### Chat History Format
- **Type**: `List[Tuple[str, str]]`
- **Format**: `[(user_message, bot_response), ...]`
- **File References**: `(None, (filename,))` - First element None, second is tuple with filename
- **Example**: 
  ```python
  [
      ("What is the weather?", "It's sunny today."),
      ("Show me a chart", "Here it is address:chart.png"),
      (None, ("chart.png",)),
      ("Thanks", "You're welcome!")
  ]
  ```

### Task List Format
- **Type**: `List[str]`
- **Values**: Task name strings (e.g., `["serpapi", "extract_text", "ask_user"]`)
- **Source**: Keys from `TASK_TO_CLASS` dictionary converted to string values

---

## Important Notes

1. **Deprecation Warning**: The Chatbot component should use `type='messages'` instead of default tuples format. Current code shows a warning.

2. **API Key Handling**: API keys are passed directly to `respond()` callback, not through the unused `submit_api_keys()` function.

3. **File Upload Format**: Files are referenced in chat history as `(None, (filename,))` tuples.

4. **Environment Variables**: API keys are set in `os.environ` within the `respond()` callback before processing.

5. **Async Behavior**: File uploads use `queue=False` for immediate processing, while message submits are queued by default.

---

## Complete Event Flow

### User Query Flow:
1. User enters message in `msg` textbox
2. User selects tasks from dropdown (optional)
3. User checks/unchecks "Use History" (optional)
4. User enters API keys (if not already set)
5. User presses Enter
6. `msg.submit` triggers → calls `respond()` callback
7. `respond()` processes query, updates `chat_history`
8. Returns `("", updated_chat_history)`
9. UI updates: message box cleared, chatbot displays new exchange

### File Upload Flow:
1. User clicks upload button (📁)
2. User selects file
3. `btn.upload` triggers → calls `upload_meta()` callback
4. `upload_meta()` adds file reference to history and metadata
5. Returns updated `chat_history`
6. UI updates: chatbot displays file reference

### Reset Flow:
1. User clicks clear button
2. `clear.click` triggers → calls `reset()` callback
3. `reset()` clears internal state
4. UI clears: message box and chatbot history reset

