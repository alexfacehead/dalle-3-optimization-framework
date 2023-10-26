# An In-Active-Development Framework for Evaluating DALLE-3 (via ChatGPT) Image Output Quality

This project aims to show that DALLE-3's image output can be vastly improved. The end goal is to do so using mathematical, AI-based, and human-feedback metrics.

It requires some setup to get VMAF working with FFmpeg so that quality metrics can be used to gauge image output variation based on optimizations supplied via this repository.

Through unit testing, the goal is to prove that DALLE-3 is not fully optimized, and can indeed be super-charged, backed by 11 different statistical metrics and, also, AI-determined quality increases as well.

## Features
- Detailed metrics with standardization to help assess relative image quality
- Detailed instructions on how to run your own evals
- Premade prompt enhancers that can be used with ChatGPT if you lack an API key or API gpt-4 access.
- (Almost there!) An interface for developing your own prompt enhancers using my "EasyGPT-3.5" prompt generator (requires API key and `.env` setup, repository, with instructions, located at [EasyGPT-3.5](https://github.com/alexfacehead/EasyGPT-3.5))

## It Starts with a Base prompt

This program aims to take a base prompt, extract the output, and save it. Then, the prompt is optimized via various possibilities (mostly through gpt-4-0314 model optimizations via the API) and the resultant, new, "improved" images are saved as well.

# Documentation for Setup
This project requires only a few dependencies, but setting up FFmpeg with VMAF support can be tricky. It requires a few steps.

First and foremost, create a `venv` using your preferered Python version from the root directory, source it, and then install dependencies using `[python-distro] -m pip install -r requirements.txt`

To do this:
0. Have `virtualenv` installed and be familiar with how to seutp a a venv (more on this later)
1. Simply create a venv by running `[python-distro] venv venv` from the root directory.
2. Run `source venv/bin/activate`
3. Run `[python-distro] venv venv`
4. Run `[python-distro] -m pip install -r requirements.txt`
5. 
- If you are encountering errors, run `[python-distro] -m pip install virtualenv`
- Then run `[python-distro] -m venv venv`
- Then, finally, run `source venv/bin/activate`

## Setup the Dependencies and First Build for libvmaf 
0. Deactivate your venv by running `deactivate` if it is still active (as indicated in your terminal with `(venv)` displayed. If the command is not recognized; your venv is deactivated or you have not installed venv properly.)

1. Run `git clone https://github.com/Netflix/vmaf.git` to a directory of your choosing - preferably within your project directory, perhaps within a venv. Wherever it is accessible - rememember the path you installed it to.
2. Navigate to your vmaf directory, and `cd` into it.
3. cd into `libvmaf` and then build `libvmaf`, which will be explained eblow.
4. Install pyenv via [system-package-manager] install pyenv
5. run `pyenv install 3.7` (minimum to get libvmaf working)
6. run `pyenv local 3.7`
7. Since you're in the libvmaf directory, create a venv (`python --version` first to check that you're using 3.7)
8. Once confirming the version, run `python -m venv venv`
9. Run `source venv/bin/activate`
10. Run `python -m pip install meson`
11. Run [package-manager] install nasm ninja doxygen
12. Run `meson build --buildtype release`
13. Run `ninja -vC build`
14. Run `ninja -vC build test` to see if all 13 tests are passed (as of 2023-10-26)
15. Once tests are passed (there may be build issues that arise), proceed to the next step.

## Setup FFmpeg with VMAF Support for Proper Metrics and Analysis

1. You will have to build FFmpeg yourself. Run the following command at your desired directory:
   ```
   git clone https://github.com/FFmpeg/FFmpeg.git
   ```

2. Navigate to the directory where you cloned FFmpeg and run the following commands sequentially:
   ```
   ./configure --enable-libvmaf
   make -j4
   make install
   ```

3. If everything goes well, after a build time of approximately 5-10 minutes on a decent computer, you should have VMAF support enabled.

4. To test this, run the following command, replacing `[path-to-ffmpeg-binary]` with the actual path to your FFmpeg binary:
   ```
   [path-to-ffmpeg-binary] -filters | grep vmaf
   ```
   You should see something like `libvmaf` in the output, likely near the bottom.

5. For macOS users, especially if using Homebrew, the typical path might be:
   ```
   /usr/local/bin/FFmpeg/ffmpeg -filters | grep vmaf
   ```

6. If you encounter permissions errors, navigate to the location of your FFmpeg binary (regardless of its location) and run:
   ```
   chmod -R +x $(pwd)
   ```

7. Once VMAF support is verified, use the following parameters in your program:
   ```
   --ffmpeg-location="/usr/local/bin/FFmpeg/ffmpeg"
   --vmaf-model-location="/path/to/your/vmaf_v0.6.1.json"
   ```

8. Remember to adjust the paths based on your system. To locate your VMAF model file, return to the cloned vmaf directory and find the `vmaf_v0.6.1.json` file.


## You Should Now Be Ready to Run This Program

Now, please enjoy running the evaluations and observing any quality increases, and feel free to provide compelling datasets and share them with the community. To contribute, if you want to be a collaborator, contact me directly at ahugi@uw.edu with "DALLE 3 EVALUATION REPO" as the title for a faster response.

## Generating Your Own Prompts
Using EasyGPT-3.5 is as easy as setting your environment variables within the directory. This will be streamlined in future versions, but command-line support is already active.

**You don't need GPT-4 API access for this, just an OpenAI API account, which is as easy as signing up on their website. It is incredibly cheap to use the gpt-3.5 series models!**

Run it using: `[python-distro] EasyGPT-3.5/main.py` and use the `-h` flag for help. If you do not wish to setup your environment template (located at `EasyGPT-3.5/env.template` - rename it to `.env` if you do wish to use it) then simply use the commandline flags, as speciefied by the `-h` flag.

Prompt it by asking it a simple 1-2 sentence question, for example:
`How can I improve an image prompt designed for a state-of-the-art language model?`

It will return to you a series of expanded prompts and context, where the final two results are:
1. A "tree-of-thought", expertly optimized prompt designed to answer your question.
2. An answer, which you can then use as context for applying an update to your existing prompt.

This will be further adapted and streamlined for future versions of this project.

# TO DO
- Easier system for automatically generating images, grabbing them, and arranging them so they may be tested.
- Unit testing support.
- Add more metrics.
- Fine-tune the standardized formula.
- Incorporate human-sampled feedback.
- Use iterative prompting techniques.
- Explore cheaper models and compare results.