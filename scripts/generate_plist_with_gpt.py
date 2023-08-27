import openai
import argparse
import os
import getpass
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Read the API key from the environment
api_key = os.environ.get("OPENAI_API_KEY")

def generate_plist_from_description(description, filename):
    # Prepare the API call
    openai.api_key = api_key

    PROMPT_PLIST_GENERATION = """Generate a .plist file content for a task that: {description}. Return only plist content. As label use com.{username}.{file} """
    print(PROMPT_PLIST_GENERATION.format(description=description, username=getpass.getuser(), file=filename.replace('.plist', '')))
    # Make an API call to GPT-3.5 to generate .plist content based on the description
    response = openai.Completion.create(
        engine="gpt-3.5-turbo",
        prompt=PROMPT_PLIST_GENERATION.format(description=description, username=getpass.getuser(), file=filename.replace('.plist', '')),
        max_tokens=300
    )
    print(response)
    # Extract and return the generated text
    generated_text = response.choices[0].text.strip()
    return generated_text

def save_to_file(content, filename):
    # Write the generated .plist content to a file
    with open(filename, 'w') as f:
        f.write(content)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate a .plist task file using natural language description.')
    parser.add_argument('description', help='Natural language description of the task.')
    parser.add_argument('filename', help='Filename to save the generated .plist content.')
    args = parser.parse_args()

    # Generate .plist content
    plist_content = generate_plist_from_description(args.description, args.filename)

    # Save to file
    save_to_file(plist_content, args.filename)

    print(f"Generated .plist content saved to {args.filename}")
