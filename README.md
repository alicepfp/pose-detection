<a id="readme-top"></a>

[![Forks][forks-shield]][forks-url]
[![Issues][issues-shield]][issues-url]
[![Stargazers][stars-shield]][stars-url]
[![AGLP License][license-shield]][license-url]
[![python][python]][python-url]



<h3 align="center">Pose Detection for Sports</h3>

  <p align="center">
    Pose detection project using YOLO to predict sports movements
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
        <li><a href="#dataset.py">Dataset.py</a></li>
        <li><a href="#model.py">Model.py</a></li>
        <li><a href="#metrics.ipynb">Metrics.ipynb</a></li>
      </ul>
    </li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>



## About The Project

This project focuses on detecting and analyzing human poses from videos  
sourced from YouTube focusing in sports and contact sports to create 
a dataset to train ML models so we can tag and predict movements in 
different video sources.

By leveraging the power of YOLO (You Only Look Once) models, 
it identifies human figures within video frames, extracting pose 
data for each detected individual. 

A core part of the workflow involves downloading YouTube 
videos and processing them into frames, which can 
then be analyzed with YOLO's pose estimation model.

Only then we can analyze the extracted poses and create a  
dataset to train a ML model that can tag, evaluate and predict 
different types of movements in multiple video sources.  

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

To run this project first clone it into the directory of your preference 
and the follow the steps bellow.

### Prerequisites and libraries installation

First you need to clone the repo and install the required python packages 
using the `requirements.txt` file, it's recommended to use a virtual env 
like [conda](https://anaconda.org/anaconda/conda) or [venv](https://docs.python.org/3/library/venv.html).

* Clone the repo
  ```sh
  git clone https://github.com/alicepfp/pose-detection.git
  ```

* Run the `requirements.txt` file
  ```sh
  pip install -r requirements.txt
  ```


<p align="right">(<a href="#readme-top">back to top</a>)</p>



## Usage

This project is organized in folders for different scripts that have 
different functions.

### Extractor 

The extractor folder contains the script responsible for finding and 
downloading videos and them separating each frame into images to extract 
each person in the video keypoints.

To use the script go into the folder and then run:
```sh
  python3 run.py
```
The script will prompt some questions for the user to input their preferences 
for running it.

### Dataset.py

`To be implemented` 

### Model.py

`To be implemented`

### Metrics.ipynb

`To be implemented`

<p align="right">(<a href="#readme-top">back to top</a>)</p>



## Roadmap

- [X] Extractor
    - [X] Video search and download
    - [X] Frame extraction
    - [X] YOLO person pose and keypoints extraction
    - [X] Keypoints csv 
- [ ] Dataset
    - [ ] Keypoints recognition
    - [ ] Tagging based on keypoints
    - [ ] Dataset creation
- [ ] Model
    - [ ] XGBoost classification model
    - [ ] Train YOLO based on XGBoost weights
    - [ ] Use YOLO trained model to tag video movements
- [ ] Metrics
    - [ ] Evaluate XGBoost classification model
    - [ ] Evaluate YOLO precision
    - [ ] Evaluate precision on detected movements in each video 

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
[license-url]: https://github.com/alicepfp/pose-detection/blob/master/LICENSE.txt
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
