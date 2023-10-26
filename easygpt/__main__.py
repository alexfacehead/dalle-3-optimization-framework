import argparse
import os

from easygpt.main import main 

from easygpt.main import main  # This should correctly import the main function

def parse_arguments():
    parser = argparse.ArgumentParser(description="Run the EasyGPT program with specific parameters")

    parser.add_argument("--model", type=str, default="gpt-3.5-turbo-16k", help="Specify the model to be used")
    parser.add_argument("--temperature", type=float, default=0.33, help="Set the model temperature")
    parser.add_argument("--query_mode", action="store_true", help="Enable query mode")  # This uses store_true so if --query-mode is given, the variable is set to True
    parser.add_argument("--openai_api_key", type=str, default="", help="Provide OpenAI API key")
    parser.add_argument("--super_charged", action="store_true", help="Enable super charged mode")
    parser.add_argument("--prompt_dir", type=str, default=os.path.join(os.getcwd(), "resources", "prompts"), help="Directory path for prompts")

    return parser.parse_args()

if __name__ == '__main__':
    args = parse_arguments()

    # Check for None or invalid values and reset to defaults
    model = args.model or "gpt-3.5-turbo-16k"
    temperature = args.temperature or 0.33
    openai_api_key = ""
    if args.openai_api_key != None:
        openai_api_key = args.openai_api_key
    prompt_dir = args.prompt_dir or os.path.join(os.getcwd(), "resources", "prompts")

    main(model=model,
         temperature=temperature,
         query_mode=args.query_mode,
         openai_api_key=openai_api_key,
         super_charged=args.super_charged,
         prompt_dir=prompt_dir)