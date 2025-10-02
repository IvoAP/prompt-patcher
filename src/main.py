import time
from ask_LLM import generate_prompt, call_LLM
from utils import parse_arguments, save_results


def main():
    args = parse_arguments()

    match args.technique:
        case 'cognitive-verifier':
            print('Generating first prompt...')
            initial_prompt = generate_prompt(args.technique, args.vulnerability)

            timer_start = time.perf_counter()

            print('Fetching initial response...')
            initial_response = call_LLM(args.model, initial_prompt)

            if initial_response['status'] == 'OK':
                print('Generating second prompt...')
                second_prompt = generate_prompt('cognitive-verifier-follow-up', args.vulnerability, chat_context=initial_response['content'])
                
                print('Fetching verified response...')
                verified_response = call_LLM(args.model, second_prompt)

                if verified_response['status'] == 'OK':
                    timer_end = time.perf_counter()
                    elapsed_time = timer_end - timer_start

                    correction_patch = verified_response['content']
                    
                    save_results(args.model, args.technique, args.vulnerability, correction_patch, [initial_prompt, second_prompt], elapsed_time)
                else:
                    print(f'An error has occurred: {verified_response["details"]}')
            else:
                print(f'An error has occurred: {initial_response["details"]}')


        case _:
            print('Generating prompt...')
            prompt = generate_prompt(args.technique, args.vulnerability)

            print('Fetching LLM response')
            timer_start = time.perf_counter()

            response = call_LLM(args.model, prompt)

            timer_end = time.perf_counter()
            elapsed_time = timer_end - timer_start

            if response['status'] == 'OK':
                correction_patch = response['content']
                save_results(args.model, args.technique, args.vulnerability, correction_patch, [prompt], elapsed_time)
            else:
                print(f'An error has occurred: {response["details"]}')


if __name__ == "__main__":
    main()