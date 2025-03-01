# ImgClass - Image Classification Web App

A simple web application for image classification using a pre-trained ResNet-18 model with PyTorch and Flask.

## Features

- Upload images for classification
- View top 5 predictions with confidence scores
- Interactive bar chart visualization of results
- Clean, dark-themed UI with IBM Plex Mono font
- Base64 image rendering for reliable display

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/imgclass.git
cd imgclass
```

2. Create a virtual environment:
```bash
python -m venv venv
```

3. Activate the virtual environment:
   - Windows:
   ```bash
   venv\Scripts\activate
   ```
   - macOS/Linux:
   ```bash
   source venv/bin/activate
   ```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Download the ImageNet class labels:
```bash
curl -O https://raw.githubusercontent.com/pytorch/pytorch/master/torch/hub/imagenet_classes.txt
```

## Usage

1. Start the application:
```bash
python app.py
```

2. Open your web browser and go to http://127.0.0.1:5000/

3. Upload an image and click "Classify" to get predictions

## Technologies Used

- Backend: Flask, PyTorch, TorchVision
- Frontend: HTML, CSS, Chart.js
- Font: IBM Plex Mono

## License

MIT
