
from typing import Optional
def evaluate_image_improvement_v2(metrics):
    """
    Evaluate the improvement of an image based on various metrics.
    
    Args:
    - metrics (dict): Dictionary containing values for various metrics.
    
    Returns:
    - score (float): A score indicating the degree of improvement. Higher values indicate more significant improvement.
    - summary (str): A textual summary of the evaluation.
    """
    # Initialize the score
    score = 0
    
    # Handle MSE, Edge MSE, FFT MSE: Lower is better
    # Normalize by inverting the values and scaling down to a reasonable range
    score += 2 * (1 / (1 + metrics['mse'] / 20000))
    score += 2 * (1 / (1 + metrics['edge_mse'] / 20000))
    score += 2 * (1 / (1 + metrics['fft_mse'] / 1e9))
    
    # Handle SSIM: Higher is better
    score += 5 * metrics['ssim']
    
    # Handle PSNR: Higher is better
    # Normalize PSNR to a 0-1 scale (assuming max possible PSNR is 50)
    score += 2 * (metrics['psnr'] / 50)
    
    # Handle BRISQUE Difference: More negative is better for improvement
    # Normalize assuming BRISQUE difference ranges up to 100
    score += 3 * max(0, -metrics['brisque_diff'] / 100)
    
    # Handle Histogram Correlation: Closer to 1 is better
    # Normalize to 0-1 scale
    score += 1 * ((metrics['hist_corr'] + 1) / 2)
    
    # Handle Entropy: Higher is better
    score += metrics['entropy_diff'] / 10  # Normalize assuming entropy difference is up to 10
    
    # Handle MS-SSIM: Higher is better
    score += 5 * metrics['ms_ssim']
    
    # Handle GSIM: Higher is better
    score += 5 * metrics['gsim']
    
    # Handle VMAF: Higher is better
    score += 3.5 * (metrics['vmaf'] / 100)  # Assuming VMAF ranges from 0 to 100

    # Handle Feature Presence: Higher is better
    score += 4 * metrics['feature_presence']  # Assuming feature_presence ranges from 0 to 1
    
    # Calculate average score
    total_weights = 2 + 2 + 2 + 5 + 2 + 3 + 1 + 1 + 5 + 5 + 7 + 4
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