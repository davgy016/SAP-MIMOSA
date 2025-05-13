# Use a pipeline as a high-level helper
from transformers import pipeline

# Load the model (replace 'gpt2' with your desired model name)
pipe = pipeline("text-generation", model="gpt2")

# Generate text
input_text = "Once upon a time"  # Replace with your input text
output = pipe(input_text, max_length=50, num_return_sequences=1)  # Adjust parameters as needed

# Print the output
print(output)