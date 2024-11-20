<a id="readme-top"></a>

[![Forks][forks-shield]][forks-url]
[![Issues][issues-shield]][issues-url]
[![Stargazers][stars-shield]][stars-url]
[![AGLP License][license-shield]][license-url]
[![python][python]][python-url]



<h1 align="center">Pose Detection for Sports</h1>

  <p align="center">
    Pose detection project that analyzes sports videos to track and predict movements using pose estimation.
    <br />
  </p>
</div>



<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites-and-libraries-installation">Prerequisites and libraries installation</a></li>
      </ul>
    </li>
    <li>
      <a href="#usage">Usage</a>
      <ul>
        <li><a href="#extractor">Extractor</a></li>
      </ul>
      <ul>
        <li><a href="#datasetpy">Dataset.py</a></li>
      </ul>
      <ul>
        <li><a href="#modelpy">Model.py</a></li>
      </ul>
      <ul>
        <li><a href="#metricsipynb">Metrics.ipynb</a></li>
      </ul>
    </li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>



## About The Project

This project is dedicated to detecting and analyzing human poses in YouTube videos, with a particular focus on sports and contact sports. The goal is to create a comprehensive dataset for training machine learning models capable of tagging and predicting movements across various video sources.

By utilizing the powerful YOLO (You Only Look Once) model, the system identifies human figures within video frames and extracts pose data for each detected individual.

A key component of the workflow involves downloading videos from YouTube and processing them into individual frames. These frames are then analyzed using YOLO's pose estimation capabilities.

The extracted pose data serves as the foundation for building a dataset that enables the training of machine learning models. These models aim to evaluate, tag, and predict diverse types of movements across multiple video contexts.  

<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Built With

[![python][python2]][python-url]

[![jupyter][jupyter]][jupyter-url]

[![pandas][pandas]][pandas-url]

[![pytorch][pytorch]][pytorch-url]

[![YOLO][yolo]][yolo-url]

[![OpenCV][opencv]][opencv-url]

[![XGBoost][xgboost]][xgboost-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>



## Getting Started

This guide will help you set up and run the project step-by-step. The project focuses on pose detection and keypoint extraction, so it's important to have the necessary tools and dependencies installed correctly. Follow the instructions below to get started.

### Prerequisites and libraries installation

Before running the project, you'll need to prepare your environment by cloning the repository and installing the required Python packages listed in the `requirements.txt` file. Using a virtual environment is strongly recommended to avoid conflicts with other projects and to maintain a clean development setup. Tools like [conda](https://anaconda.org/anaconda/conda) or Python's built-in [venv](https://docs.python.org/3/library/venv.html) are excellent choices for this purpose.

1. **Clone the repository**
    
    The first step is to download the project's source code to your local machine by cloning the repository:

    ```sh  
    git clone https://github.com/alicepfp/pose-detection.git
    ```

2. **Set up a virtual environment (optional but recommended)**
  
    Create and activate a virtual environment using either `conda` or `venv`:

   * Using conda:
    ```sh
    conda create --name pose-detection-env python=3.11
    conda activate pose-detection-env
    ```

    * Using venv:
    ```sh
    python -m venv pose-detection-env  
    source pose-detection-env/bin/activate  # On Windows, use: pose-detection-env\Scripts\activate
    ```

3. **Install required packages**

    Once your virtual environment is active, install the project's dependencies using the requirements.txt file. The example below uses `conda`:
    ```sh
    conda install --yes --file requirements.txt
    ```
    Alternatively, you can use `pip` if you're not using conda, just make sure that the packages in the file are correct:
    ```sh
    pip install -r requirements.txt  
    ```

  After completing these steps, you'll have everything set up to run the project and start working on pose detection.


<p align="right">(<a href="#readme-top">back to top</a>)</p>



## Usage

This project is organized into folders, each containing scripts dedicated to specific functions within the workflow. This modular structure keeps the project organized, making it easier to manage, test, and expand. Each folder focuses on a particular task, such as video downloading, frame extraction, pose detection, or data processing. By separating these functions, the project remains clear and scalable, allowing for easier updates and the addition of new features as needed.

### Extractor  

  The **extractor** folder contains a script designed for:  
   - Locating and downloading videos.  
   - Splitting videos into individual frames.  
   - Extracting keypoints for each person detected in the frames.  

      #### Running the Extractor Script  

      To use the extractor script, follow these steps:  

      * Navigate to the **extractor** folder:  
        
        ```sh  
        cd extractor
        ```

      * Execute the script:

        ```sh
        python3 run.py
        ```

      * Provide input:
        
        The script will prompt you with questions to customize the process, such as specifying the video source or other parameters. Answer the prompts as needed, and the script will handle the rest.

### Dataset.py

`To be implemented` 


### Model.py

`To be implemented`


### Metrics.ipynb

`To be implemented`


<p align="right">(<a href="#readme-top">back to top</a>)</p>



## Roadmap

### Extractor  
- [X] **Video Search and Download**: Implement functionality to search for and download videos.  
- [X] **Frame Extraction**: Develop the script to extract individual frames from downloaded videos.  
- [X] **YOLO Pose and Keypoints Extraction**: Integrate YOLO for detecting human poses and extracting keypoints from each frame.  
- [X] **Keypoints CSV Generation**: Output the extracted keypoints in a structured CSV format for further analysis.  

### Dataset  
- [ ] **Keypoints Recognition**: Implement recognition and classification of keypoints from the extracted data.  
- [ ] **Tagging Based on Keypoints**: Tag movements and positions based on keypoint data for dataset labeling.  
- [ ] **Dataset Creation**: Compile a comprehensive dataset from the tagged keypoints and associated video frames.  

### Model  
- [ ] **XGBoost Classification Model**: Develop an XGBoost model for classifying movements based on keypoint data.  
- [ ] **Train YOLO with XGBoost Weights**: Fine-tune the YOLO model using the weights derived from the XGBoost classifier.  
- [ ] **Movement Tagging with YOLO**: Use the trained YOLO model to tag movements and predict actions in videos.  

### Metrics  
- [ ] **Evaluate XGBoost Classification Model**: Measure the performance of the XGBoost model with appropriate evaluation metrics (e.g., accuracy, F1 score).  
- [ ] **Evaluate YOLO Precision**: Assess the precision of the YOLO model in detecting poses and keypoints.  
- [ ] **Evaluate Movement Detection Precision**: Evaluate the accuracy and precision of detected movements in the video data.  

See the [open issues](https://github.com/alicepfp/pose-detection/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#readme-top">back to top</a>)</p>



## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>



## License

Distributed under the AGPL-3.0 License. See `LICENSE` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



## Contact

[![Gmail][mail-shield]][mail-url]

[![LinkedIn][linkedin-shield]][linkedin-url]

[![Github][git]][git-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>


[forks-shield]: https://img.shields.io/github/forks/alicepfp/pose-detection.svg?style=for-the-badge
[forks-url]: https://github.com/alicepfp/pose-detection/network/members
[stars-shield]: https://img.shields.io/github/stars/alicepfp/pose-detection.svg?style=for-the-badge&color=yellow
[stars-url]: https://github.com/alicepfp/pose-detection/stargazers
[issues-shield]: https://img.shields.io/github/issues/alicepfp/pose-detection.svg?style=for-the-badge
[issues-url]: https://github.com/alicepfp/pose-detection/issues
[license-shield]: https://img.shields.io/github/license/alicepfp/pose-detection.svg?style=for-the-badge
[license-url]: https://github.com/alicepfp/pose-detection/blob/main/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/linkedin_username
[mail-shield]: https://img.shields.io/badge/Gmail-D14836?style=for-the-badge&logo=gmail&logoColor=white
[mail-url]: alicepfp@labnet.nce.ufrj.br
[python]: https://img.shields.io/badge/python-gray?style=for-the-badge&logo=python&logoColor=white&labelColor=blue
[python-url]: https://www.python.org
[python2]: https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue
[pandas]: https://img.shields.io/badge/Pandas-2C2D72?style=for-the-badge&logo=pandas&logoColor=white
[pandas-url]: https://pandas.pydata.org
[jupyter]: https://img.shields.io/badge/Jupyter-F37626.svg?&style=for-the-badge&logo=Jupyter&logoColor=white
[jupyter-url]: https://jupyter.org
[pytorch]: https://img.shields.io/badge/PyTorch-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white
[pytorch-url]: https://pytorch.org
[yolo]: https://img.shields.io/badge/YOLO-8E75B2?style=for-the-badge&logo=googlegemini&logoColor=white
[yolo-url]: https://docs.ultralytics.com
[git]: https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white
[git-url]: https://github.com/alicepfp
[opencv]: https://img.shields.io/badge/OpenCV-purple?style=for-the-badge&logo=opencv&logoColor=white
[opencv-url]: https://opencv.org
[xgboost]:https://img.shields.io/badge/XGBoost-blue?style=for-the-badge&logo=WeightsAndBiases&logoColor=white
[xgboost-url]: https://xgboost.readthedocs.io/en/latest/index.html
