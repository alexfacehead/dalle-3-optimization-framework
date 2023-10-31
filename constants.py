SYSTEM_MESSAGE_ANALYZER = """Given a textual prompt, such as "Can you create an image of a pendulum board with crystal pendulum swinging over with a witch with long blonde hair using it," analyze the provided Python code for evaluating the improvement of an image based on various metrics. The code takes a dictionary of metrics as input and calculates a weighted score to determine the degree of improvement. Consider the following aspects while analyzing the code:

1. Are the chosen metrics appropriate for evaluating image improvement, considering the varying nature of the textual prompts?
2. Are the weights assigned to each metric reasonable in the context of different prompts?
3. Can the normalization techniques used for each metric be improved to better handle varying prompts?
4. Are there any additional metrics that could be included to enhance the evaluation function, considering the potential variability in the prompts?
5. Can the code be refactored or optimized for better readability or performance, given the varying nature of the prompts?

Additionally, provide suggestions for modifying the code, such as altering the weights, normalization techniques, or incorporating new metrics, to improve the evaluation of image improvement in the context of varying prompts. Keep in mind the following feedback when providing suggestions:


1. Try your best not to omit metrics. Retain the integrity of the original structure.
2. For the MSE, Edge MSE, and FFT MSE, you may want to experiment with different scaling factors to better balance their contributions to the overall score.
3. The PSNR normalization assumes a maximum value of 50. You may want to make this value adjustable or use a more adaptive normalization technique.
4. The BRISQUE difference normalization assumes a range up to 100. You may want to verify if this range is appropriate for your dataset or adjust it accordingly.
5. The entropy difference normalization assumes a range up to 10. You may want to verify if this range is appropriate for your dataset or adjust it accordingly.
6. Consider adding comments to explain the choice of weights and normalization techniques for each metric.

Ensure that your suggestions can be easily integrated with the existing code without requiring a complete overhaul of the code structure and can adapt to the varying nature of textual prompts.\n\n
This includes avoiding adding contrived or unnecessary functions, unless you deem it absolutely necessary. Focus on tweaking the metrics as they are in relation to the prompt used, using your semantic analysis skills."""

STATIC_CODE = """```py
def evaluate_image_improvement_v1(metrics):
    \"\"\"
    Evaluate the improvement of an image based on various metrics.
    
    Args:
    - metrics (dict): Dictionary containing values for various metrics.
    
    Returns:
    - score (float): A score indicating the degree of improvement. Higher values indicate more significant improvement.
    - summary (str): A textual summary of the evaluation.
    \"\"\"
    # Initialize the score
    score = 0
    
    # Handle MSE, Edge MSE, FFT MSE: Lower is better
    # Normalize by inverting the values and scaling down to a reasonable range
    score += 3 * (1 / (1 + metrics['mse'] / 20000))
    score += 3 * (1 / (1 + metrics['edge_mse'] / 20000))
    score += 3 * (1 / (1 + metrics['fft_mse'] / 1e9))
    
    # Handle SSIM: Higher is better
    score += 4 * metrics['ssim']
    
    # Handle PSNR: Higher is better
    # Normalize PSNR to a 0-1 scale (assuming max possible PSNR is 50)
    score += 3 * (metrics['psnr'] / 50)
    
    # Handle BRISQUE Difference: More negative is better for improvement
    # Normalize assuming BRISQUE difference ranges up to 100
    score += 4 * max(0, -metrics['brisque_diff'] / 100)
    
    # Handle Histogram Correlation: Closer to 1 is better
    # Normalize to 0-1 scale
    score += 2 * ((metrics['hist_corr'] + 1) / 2)
    
    # Handle Entropy: Higher is better
    score += metrics['entropy_diff'] / 10  # Normalize assuming entropy difference is up to 10
    
    # Handle MS-SSIM: Higher is better
    score += 4 * metrics['ms_ssim']
    
    # Handle GSIM: Higher is better
    score += 4 * metrics['gsim']
    
    # Handle VMAF: Higher is better
    score += 2.5 * (metrics['vmaf'] / 100)  # Assuming VMAF ranges from 0 to 100
    
    # Calculate average score
    total_weights = 3 + 3 + 3 + 4 + 3 + 4 + 2 + 2 + 4 + 4 + 5
    score /= total_weights  # Dividing by the sum of weights
    
    # Create a summary
    if score > 0.8:
        summary = "The improved image is significantly better than the base image."
    elif score > 0.5:
        summary = "The improved image shows notable enhancement compared to the base image."
    elif score > 0.2:
        summary = "The improved image has slight improvements over the base image."
    else:
        summary = "The improved image does not show clear improvements over the base image."
    
    return score, summary
    ```"""

DEFAULT_PLACEHOLDER_PROMPT = "Make an image."
AI_FILE_IMPORTS = """
from typing import Optional\n"""

STATIC_QUERY_FOR_CODE = "Great. Now, please return nothing but the code, without any backticks or anything. Just the code, no imports, with all the implementations you've made:"