# SIMPLE GRADIO APP 

from vars import *
from openai import OpenAI
from dotenv import load_dotenv
import gradio as gr

load_dotenv()
client = OpenAI()

# Function to generate personalised email
def generate_email(name, role, company_name, company_news):

    email_prompt = f"""
    You are an expert outbound sales agent specialised in email marketing at {SENDER_COMPANY}.
    {SENDER_COMPANY_DESCRIPTION}
    The following information in triple ***'s is on {SENDER_COMPANY}'s website:
    ***{SENDER_COMPANY}: {COMPANY_WEBSITE_DESCRIPTION}***
    Write a personalised cold email with a subject line to the specified person, advertising {SENDER_COMPANY}'s offerings.
    Your subject line must be less than 5 words.
    Your email must be less than 75 words.
    You must always sign off as {SENDER_NAME}, {SENDER_ROLE}.
    Here are some example subject lines:
    Example Subject Line 1: {EXAMPLE_SL_1}
    Example Subject Line 2: {EXAMPLE_SL_2}
    Example Subject Line 3: {EXAMPLE_SL_3}
    Here are some example cold emails:
    Example Email 1: {EXAMPLE_EMAIL_1}
    Example Email 2: {EXAMPLE_EMAIL_2}
    Example Email 3: {EXAMPLE_EMAIL_3}
    """

    user_input = f"""
    Write an email to {name}, who is the {role} at {company_name}. Here is some recent news about {company_name}: {company_news}
    """

    chat_completion = client.chat.completions.create(
        model="gpt-4-turbo-2024-04-09",
        messages=[{"role":"system", "content": email_prompt}, {"role":"user", "content":user_input}]
    )
    cold_email = chat_completion.choices[0].message.content

    return cold_email

with gr.Blocks() as demo:
    
    gr.Markdown("""
    # Generate Cold Emails on Demand!
    """)

    with gr.Row():
        name = gr.Textbox(label="Recipient Name")
        role = gr.Textbox(label="Recipient Role")
        company = gr.Textbox(label="Recipient Company")
        company_news = gr.Textbox(label="Recipient Company News")

    button = gr.Button("GENERATE")

    email = gr.Textbox(label="Output")

    button.click(fn=generate_email, inputs=[name,role,company,company_news], outputs=email)

demo.launch()