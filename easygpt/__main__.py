import argparse
import os

from easygpt.main import main  # This should correctly import the main function

def parse_arguments():
    parser = argparse.ArgumentParser(description="Run the EasyGPT program with specific parameters")

    parser.add_argument("--model", type=str, default="gpt-3.5-turbo-16k", help="Specify the model to be used")
    parser.add_argument("--temperature", type=float, default=0.33, help="Set the model temperature")
    parser.add_argument("--query-mode", action="store_true", help="Enable query mode")  # This uses store_true so if --query-mode is given, the variable is set to True
    parser.add_argument("--openai-api-key", type=str, default=None, help="Provide OpenAI API key")
    parser.add_argument("--super-charged", action="store_true", help="Enable super charged mode")
    parser.add_argument("--prompt-dir", type=str, default=os.path.join(os.getcwd(), "resources", "prompts"), help="Directory path for prompts")

    return parser.parse_args()

if __name__ == '__main__':
    args = parse_arguments()
    
    main(model=args.model,
         temperature=args.temperature,
         query_mode=args.query_mode,
         openai_api_key=args.openai_api_key,
         super_charged=args.super_charged,
         prompt_dir=args.prompt_dir)
