# Super-resolution correlator

Super-resolution correlator is package for data processing in super-resolution microscopy. It contains a intuitive GUI and high perfomant
GPU based visualization and algorithms for 2D and 3D data. <br />
Main features:
* Cuda accelerated 2D Alpha Shapes
* Automated image alignment via General Hough Transform
* Huge list of filters for localization datasets
* Customizable Opengl widget based on modelview perspective standard
* Roi selection and export function
* Pearson correlation between alpha shape and image data

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. 

### Prerequisites

* impro
* Nvidia GPU with compute capability 3 or higher
* Cuda 9.0 from [CUDA website](https://developer.nvidia.com/cuda-90-download-archive) (CUDA 10 is yet not supported by pycuda)
* pycuda
* Python opencv
* PyQt5
* numpy
* pandas
* scikit
* scipy

```
Some images
```

### Installing

1. Clone git repository
2. Open cmd and cd to repository
3. Start GUI with

```
python main.py
```
4. Install missing packages if necessary

### Run test data

For general instructions read the [guide](guide.pdf). Data in the test data folder can be aligned in the following way:
1. Open SIM and dSTORM data files
2. Flip SIM image left-right
4. Set z-position to -300
5. Set upper SIM LUT threshhold to 19
6. Set dSTORM local density filter to 18 per 100 nm
7. Create alpha shape in 3D dialog
8. Find markers with GHT in registration dialog
9. Adjust offset
10. Recreate alpha shape by double clicking the button
11. Correlate your region of interest in ROI dialog
