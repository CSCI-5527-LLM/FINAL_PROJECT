import json
import os
import platform

# Function to clear the console
def clear_console():
    if platform.system() == "Windows":
        os.system('cls')
    else:
        os.system('clear')

# Load the JSON file with models and outputs
with open('processed_model_outputs.json', 'r') as file:
    models_data = json.load(file)

# Load the targets JSON file
with open('targets.json', 'r') as file:
    targets_data = json.load(file)

# Function to iterate over models and outputs
def iterate_and_compare(models_data, targets_data):
    for model in models_data:
        for output, target in zip(model['output'], targets_data):
            # Check if 'name' key exists in the output
            name = output.get('name', 'Unknown Name')
            print(f"Model: {model['model']}, Name: {name}")
            for key in target.keys():
                target_value = target[key]
                output_value = output.get(key, "missing")

                # Special case for mean length and width
                if key in ['mean length (microns)', 'mean width (microns)']:
                    output_value = output.get('cell_size', "missing")

                print(f"\nAttribute: {key}")
                print(f"Output value: {output_value}")
                print(f"Target value: {target_value}")

                # Handling correctness
                correctness = input("Is this correct? Enter 1 for yes, 0 for no: ")

                # Update the original dictionary based on user input
                output[key] = {
                    "value": output_value,
                    "correctness": int(correctness)
                }

                clear_console()

        # Save the progress after each model
        with open('updated_models_output.json', 'w') as file:
            json.dump(models_data, file, indent=4)

# Run the function
iterate_and_compare(models_data, targets_data)
