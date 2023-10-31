
from typing import Optional
def evaluate_image_improvement_v2(metrics):
    score = 0
    score += 3 * (1 / (1 + metrics['mse'] / 20000))
    score += 3 * (1 / (1 + metrics['edge_mse'] / 20000))
    score += 3 * (1 / (1 + metrics['fft_mse'] / 1e9))
    score += 4 * metrics['ssim']
    score += 3 * (metrics['psnr'] / 50)
    score += 4 * max(0, -metrics['brisque_diff'] / 100)
    score += 2 * ((metrics['hist_corr'] + 1) / 2)
    score += metrics['entropy_diff'] / 10
    score += 4 * metrics['ms_ssim']
    score += 4 * metrics['gsim']
    score += 2.5 * (metrics['vmaf'] / 100)
    total_weights = 3 + 3 + 3 + 4 + 3 + 4 + 2 + 2 + 4 + 4 + 5
    score /= total_weights
    if score > 0.8:
        summary = "The improved image is significantly better than the base image."
    elif score > 0.5:
        summary = "The improved image shows notable enhancement compared to the base image."
    elif score > 0.2:
        summary = "The improved image has slight improvements over the base image."
    else:
        summary = "The improved image does not show clear improvements over the base image."
    return score, summary