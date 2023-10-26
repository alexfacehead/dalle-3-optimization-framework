# An In-Active-Development Framework for Evaluating DALLE-3 (via ChatGPT) Image Output Quality

This project aims to show that DALLE-3's image output can be vastly improved. The end goal is to do so using mathematical, AI-based, and human-feedback metrics.

It requires some setup to get VMAF working with FFmpeg so that quality metrics can be used to gauge image output variation based on optimizations supplied via this repository.

Through unit testing, the goal is to prove that DALLE-3 is not fully optimized, and can indeed be super-charged, backed by 11 different statistical metrics and, also, AI-determined quality increases as well.

## Features
- Detailed metrics with standardization to help assess relative image quality
- Detailed instructions on how to run your own evals
- (soon) Integrated prompt enhancers using OpenAI's API (requires a key)
- (soon) An interface for developing your own prompt enhancers using my "EasyGPT-3.5" prompt generator.

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
1. You will have to build FFmpeg yourself, so run `git clone https://github.com/FFmpeg/FFmpeg.git` wherever, so long as you can access that directory later.
2. Run ```./configure --enable-libvmaf

make -j4

make install``` As three separate commands.
3. If everything goes well, after a semi-lengthy build time of ~5-10 minutes on a decent computer, you should now have VMAF support.
4. To test this, run:
`[path-to-ffmpeg binary] -filters | grep vmaf` and you should see something like `libvmaf` in the output, near the bottom most likely.
5. For example, I would run, on macOS Monterey 12.6.8, using brew as my main package manager system-wide:
`/usr/local/bin/FFmpeg/ffmpeg -filters | grep vmaf`
Be sure to run the binary, not the folder.
6. If you get permissions errors, navigate to the location of your ffmpeg binary (it doesn't need to be in `/usr/local/bin`, as long as it has correct permissions) and run `chmod -R +x $(pwd)`
7. Once you have it installed, and have verified that VMAF is supported, go ahead and use the following as parameters to your program (`--ffmpeg-location="/usr/local/bin/FFmpeg/ffmpeg"` for example, and also `--vmaf-model-location="/Users/alexf/dev/evals-testing/venv/lib/python3.11/site-packages/vmaf/model/vmaf_v0.6.1.json"` for example)
8. Adjust the paths as needed, as these are my system paths. To locate your model location, simply return to the vmaf folder which you cloned earlier and find the `vmaf_v0.6.1.json` file.

## You Should Now Be Ready to Run This Program

Now, please enjoy running the evaluations and observing any quality increases, and feel free to provide compelling datasets and share them with the community. To contribute, if you want to be a collaborator, contact me directly at ahugi@uw.edu with "DALLE 3 EVALUATION REPO" as the title for a faster response.

# TO DO
- Easier system for automatically generating images, grabbing them, and arranging them so they may be tested.
- Unit testing support.
- Add more metrics.
- Fine-tune the standardized formula.
- Incorporate human-sampled feedback.
- Use iterative prompting techniques.
- Explore cheaper models and compare results.