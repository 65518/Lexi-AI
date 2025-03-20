import requests
import json
import gradio as gr

# API configuration
url = "http://localhost:11434/api/generate"
headers = {
    'Content-Type': 'application/json',
}

conversation_history = []

def generate_response(prompt):
    conversation_history.append({"role": "user", "text": prompt})
    data = {
        "model": "lexi",
        "stream": False,
        "prompt": prompt,
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        data = json.loads(response.text)
        actual_response = data.get("response", "No response from model.")
        conversation_history.append({"role": "bot", "text": actual_response})
        return format_conversation()
    else:
        return "There was an error connecting to the model."

def format_conversation():
    formatted_conversation = ""
    for entry in conversation_history:
        if entry["role"] == "user":
            formatted_conversation += f"<div class='user-message'>{entry['text']}</div>"
        else:
            formatted_conversation += f"<div class='bot-message'>{entry['text']}</div>"
    return formatted_conversation

with gr.Blocks() as iface:
    # JavaScript to change tab title
    gr.Markdown(
        """
        <script>
            document.title = "LEXI - AI";
        </script>
        """,
        elem_id="js-inject",
    )
    
    gr.Markdown(
        """
        <div style="text-align: center; font-size: 24px; font-weight: bold; color: #6a5acd;">
            <h1>LEXI-AI</h1>
            <p style="font-size: 18px; color: #555;">I'm here to assist you with all your queries!</p>
        </div>
        """
    )
    
    # Vertical stacking
    with gr.Column():
        response_area = gr.HTML(label="Conversation", elem_id="response-area")

        input_box = gr.Textbox(lines=2, placeholder="Type your message here...", elem_id="input-box",label= "‎" )
        submit_button = gr.Button("Send")
        
        # Trigger response generation
        submit_button.click(generate_response, inputs=input_box, outputs=response_area)

    iface.css = """
    body {
        background: linear-gradient(135deg, #f4f4f9, #e4e0ff);
        font-family: 'Poppins', sans-serif;
        color: #333;
        margin: 0;
        padding: 0;
    }
    #response-area {
        background: #ffffff;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
        max-height: 70vh;
        overflow-y: auto;
        margin-bottom: 20px;
    }
    .user-message {
        background: linear-gradient(135deg, #ff7eb3, #ff758f);
        color: white;
        padding: 10px 15px;
        border-radius: 20px;
        margin: 10px 0;
        max-width: 80%;
        text-align: left;
        align-self: flex-end;
        box-shadow: 0px 4px 8px rgba(255, 120, 145, 0.5);
    }
    .bot-message {
        background: linear-gradient(135deg, #6a5acd, #836fff);
        color: white;
        padding: 10px 15px;
        border-radius: 20px;
        margin: 10px 0;
        max-width: 80%;
        text-align: left;
        align-self: flex-start;
        box-shadow: 0px 4px 8px rgba(106, 92, 208, 0.5);
    }
    #input-box {
        width: 100%;
        box-shadow: 0px 4px 8px rgba(106, 92, 208, 0.3);
        border-radius: 15px;
        padding: 10px;
        margin-bottom: 10px;
    }
    button {
        background: linear-gradient(135deg, #ff758f, #ff7eb3);
        color: white;
        border-radius: 20px;
        padding: 10px 20px;
        font-weight: bold;
        box-shadow: 0px 4px 8px rgba(255, 120, 145, 0.5);
        transition: background 0.3s, transform 0.3s;
    }
    button:hover {
        background: linear-gradient(135deg, #ff758f, #ff9ab3);
        transform: scale(1.05);
    }
    """
iface.launch()
