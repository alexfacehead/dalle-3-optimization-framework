import os
import numpy as np
from PIL import Image
from skimage.metrics import structural_similarity as ssim
from skimage.metrics import mean_squared_error as mse
import math
from brisque import BRISQUE
import cv2
from scipy.stats import entropy
from termcolor import colored
from pytorch_msssim import ms_ssim
from helpers import evaluate_image_improvement
import torch
import subprocess

# Initialize BRISQUE
brisq = BRISQUE()

def calculate_ms_ssim(image1_np, image2_np):
    # Convert the 2D NumPy arrays to 4D tensors
    image1_tensor = torch.tensor(image1_np).unsqueeze(0).unsqueeze(0).float()
    image2_tensor = torch.tensor(image2_np).unsqueeze(0).unsqueeze(0).float()

    return ms_ssim(image1_tensor, image2_tensor).item()

def calculate_gsim(image1_np, image2_np):
    _, gsim = ssim(image1_np, image2_np, gradient=True)
    return gsim.mean()

def calculate_vmaf(reference_image, distorted_image):
    # Path to the FFmpeg binary
    ffmpeg_path = "/usr/local/bin/FFmpeg/ffmpeg"

    # Construct the command
    command = [
        ffmpeg_path,
        "-i", reference_image,
        "-i", distorted_image,
        "-filter_complex", "libvmaf",
        "-an", "-f", "null", "-"
    ]
    print(command)

    try:
        # Run the command and capture the output
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        for line in result.stderr.split('\n'):
            if "VMAF score" in line:
                return float(line.split()[-1])
    except subprocess.CalledProcessError as e:
        print(f"Error calculating VMAF: {e}")
        return 0


# Calculation section
def calculate_histogram_correlation(img1_np, img2_np):
    hist1 = cv2.calcHist([img1_np], [0], None, [256], [0, 256])
    hist2 = cv2.calcHist([img2_np], [0], None, [256], [0, 256])
    corr = cv2.compareHist(hist1, hist2, cv2.HISTCMP_CORREL)
    return corr

def calculate_entropy(img_np):
    hist = cv2.calcHist([img_np], [0], None, [256], [0, 256])
    hist /= hist.sum()
    return entropy(hist)

def calculate_mse(image1_np, image2_np):
    return mse(image1_np, image2_np)

def calculate_edge_mse(img1_np, img2_np):
    edges1 = cv2.Canny(img1_np, 100, 200)
    edges2 = cv2.Canny(img2_np, 100, 200)
    return mse(edges1, edges2)

def calculate_fft_mse(img1_np, img2_np):
    f1 = np.fft.fft2(img1_np)
    fshift1 = np.fft.fftshift(f1)
    magnitude_spectrum1 = np.abs(fshift1)
    
    f2 = np.fft.fft2(img2_np)
    fshift2 = np.fft.fftshift(f2)
    magnitude_spectrum2 = np.abs(fshift2)
    
    return mse(magnitude_spectrum1, magnitude_spectrum2)

def calculate_ssim(image1_np, image2_np):
    return ssim(image1_np, image2_np)

def calculate_brisque(image_path):
    return brisq.get_score(image_path)

def calculate_psnr(image1_np, image2_np):
    mse_value = mse(image1_np, image2_np)
    if mse_value == 0:
        return float('inf')
    max_pixel_value = 255.0
    return 20 * math.log10(max_pixel_value / math.sqrt(mse_value))

def calculate_colorfulness(img_np):
    if img_np.shape[2] > 3:  # Check if image has more than 3 channels
        img_np = img_np[:, :, :3]  # Keep only the first three channels
    (B, G, R) = cv2.split(img_np.astype("float"))
    rg = R - G
    yb = 0.5 * (R + G) - B
    std_rg = np.std(rg)
    std_yb = np.std(yb)
    mean_rg = np.mean(rg)
    mean_yb = np.mean(yb)
    colorfulness = math.sqrt((std_rg ** 2) + (std_yb ** 2)) + 0.3 * (mean_rg + mean_yb)
    return colorfulness
# End metric calculation section

# Direct comparison between two images
def compare_images(image1_path, image2_path):
    # Check if files exist
    if not os.path.exists(image1_path) or not os.path.exists(image2_path):
        print(f"Error: One or both of the images {image1_path} and {image2_path} do not exist.")
        return None

    # Load images without converting to grayscale
    image1 = Image.open(image1_path)
    image2 = Image.open(image2_path)

    # Convert to grayscale for metrics that require grayscale
    image1_gray = image1.convert("L")
    image2_gray = image2.convert("L")

    image1_np_gray = np.array(image1_gray)
    image2_np_gray = np.array(image2_gray)
    
    # Calculate metrics
    mse_value = calculate_mse(image1_np_gray, image2_np_gray)
    ssim_value = calculate_ssim(image1_np_gray, image2_np_gray)
    psnr_value = calculate_psnr(image1_np_gray, image2_np_gray)
    brisque_value_image1 = calculate_brisque(image1_path)
    brisque_value_image2 = calculate_brisque(image2_path)
    brisque_diff = brisque_value_image2 - brisque_value_image1

    # Calculate new metrics
    hist_corr_value = calculate_histogram_correlation(image1_np_gray, image2_np_gray)
    colorfulness_image1 = calculate_colorfulness(np.array(image1))
    colorfulness_image2 = calculate_colorfulness(np.array(image2))
    edge_mse_value = calculate_edge_mse(image1_np_gray, image2_np_gray)
    entropy_image1 = calculate_entropy(image1_np_gray)
    entropy_image2 = calculate_entropy(image2_np_gray)
    fft_mse_value = calculate_fft_mse(image1_np_gray, image2_np_gray)

    ms_ssim_value = calculate_ms_ssim(image1_np_gray, image2_np_gray)
    gsim_value = calculate_gsim(image1_np_gray, image2_np_gray)
    vmaf_value = calculate_vmaf(image2_path, image1_path)

    return mse_value, ssim_value, psnr_value, brisque_value_image1, brisque_value_image2, hist_corr_value, colorfulness_image1, colorfulness_image2, edge_mse_value, entropy_image1, entropy_image2, fft_mse_value, brisque_diff, ms_ssim_value, gsim_value, vmaf_value

def compare_all_images(reference_directory, generated_directory):
    if not os.path.exists(reference_directory) or not os.path.exists(generated_directory):
        print(f"Error: One or both of the directories {reference_directory} and {generated_directory} do not exist.")
        return

    reference_images = sorted(os.listdir(reference_directory))
    generated_images = sorted(os.listdir(generated_directory))

    reference_dict = {img.split('_base')[0]: img for img in reference_images}
    generated_dict = {img.split('_improved')[0]: img for img in generated_images}

    # Initialize the dictionary to hold the sum of each metric
    metric_sums = {
        'mse': 0,
        'ssim': 0,
        'psnr': 0,
        'brisque_diff': 0,
        'hist_corr': 0,
        'edge_mse': 0,
        'entropy_diff': 0,
        'fft_mse': 0,
        'ms_ssim': 0,
        'gsim': 0,
        'vmaf': 0
    }

    num_comparisons = 0

    for key in reference_dict.keys() & generated_dict.keys():
        ref_img_path = os.path.join(reference_directory, reference_dict[key])
        gen_img_path = os.path.join(generated_directory, generated_dict[key])

        results = compare_images(ref_img_path, gen_img_path)
        if results:
            num_comparisons += 1
            mse_value, ssim_value, psnr_value, brisque_value_image1, brisque_value_image2, hist_corr_value, colorfulness_image1, colorfulness_image2, edge_mse_value, entropy_image1, entropy_image2, fft_mse_value, brisque_diff, ms_ssim_value, gsim_value, vmaf_value = results
            
            # Print comparison details
            print(f"Comparing {reference_dict[key]} and {generated_dict[key]}:")
            print(f"  MSE: {mse_value}")
            print(f"  SSIM: {ssim_value}")
            print(f"  PSNR: {psnr_value}")
            print(f"  BRISQUE Difference (Improved - Base): {brisque_diff}")
            print(f"  Histogram Correlation: {hist_corr_value}")
            print(f"  Colorfulness for {reference_dict[key]}: {colorfulness_image1}")
            print(f"  Colorfulness for {generated_dict[key]}: {colorfulness_image2}")
            print(f"  Edge MSE: {edge_mse_value}")
            print(f"  Entropy for {reference_dict[key]}: {entropy_image1}")
            print(f"  Entropy for {generated_dict[key]}: {entropy_image2}")
            print(f"  FFT MSE: {fft_mse_value}")
            print(f"  MS-SSIM: {ms_ssim_value}")
            print(f"  GSIM: {gsim_value}")
            print(f"  VMAF: {vmaf_value}")
            
            # Extract metrics and evaluate improvement
            metrics = {
                'mse': mse_value,
                'ssim': ssim_value,
                'psnr': psnr_value,
                'brisque_diff': brisque_diff,
                'hist_corr': hist_corr_value,
                'edge_mse': edge_mse_value,
                'entropy_diff': entropy_image2[0] - entropy_image1[0],  # Difference in entropy
                'fft_mse': fft_mse_value,
                'ms_ssim': ms_ssim_value,
                'gsim': gsim_value,
                'vmaf': vmaf_value
            }

            # Update metric_sums
            for metric, value in metrics.items():
                metric_sums[metric] += value
            
            score, summary = evaluate_image_improvement(metrics)
            
            # Print the summary in red
            res_string_printed = f"{summary} (Score: {score:.2f})"
            print(colored(res_string_printed, 'red'))
            print()
            if num_comparisons > 0 and num_comparisons > 10:
                metric_averages = {metric: value / num_comparisons for metric, value in metric_sums.items()}
                print(colored("FINAL AVERAGE", 'magenta'))
                for metric, average in metric_averages.items():
                    print(f"{metric.upper()}: {average:.4f}")
                print(f"Conclusion on images: {evaluate_image_improvement(metric_averages)}", 'green')


def main():
    default_reference_directory = os.path.join(os.getcwd(), "base")
    default_generated_directory = os.path.join(os.getcwd(), "improved")

    reference_directory = input(f"Enter the path to your reference images directory (default: {default_reference_directory}): ") or default_reference_directory
    generated_directory = input(f"Enter the path to your generated images directory (default: {default_generated_directory}): ") or default_generated_directory

    compare_all_images(reference_directory, generated_directory)

if __name__ == "__main__":
    main()