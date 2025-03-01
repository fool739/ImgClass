from flask import Flask, render_template, request, url_for
import os
import base64
from werkzeug.utils import secure_filename
import torch
from torchvision import models, transforms
from PIL import Image

app = Flask(__name__)
app.secret_key = 'supersecretkey'
UPLOAD_FOLDER = os.path.join('static', 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Load pre-trained model
model = models.resnet18(weights='IMAGENET1K_V1')
model.eval()

# ImageNet class labels
with open('imagenet_classes.txt', 'r') as f:
    categories = [s.strip() for s in f.readlines()]

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def classify_image(image_path):
    # Define image transformation
    transform = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], 
                             std=[0.229, 0.224, 0.225])
    ])
    
    # Load and preprocess the image
    img = Image.open(image_path).convert('RGB')
    img_t = transform(img)
    batch_t = torch.unsqueeze(img_t, 0)
    
    # Make prediction
    with torch.no_grad():
        outputs = model(batch_t)
    
    # Get top predictions
    _, indices = torch.sort(outputs, descending=True)
    percentages = torch.nn.functional.softmax(outputs, dim=1)[0] * 100
    
    # Return top 5 predictions
    results = []
    for idx in indices[0][:5]:
        results.append({
            'label': categories[idx],
            'confidence': percentages[idx].item()
        })
    
    return results

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return render_template('index.html', result='No file selected')
    
    file = request.files['file']
    if file.filename == '':
        return render_template('index.html', result='No file selected')
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        try:
            # Classify the image
            classification_results = classify_image(filepath)
            
            # Prepare results for display
            result_text = "Top predictions:\n"
            for pred in classification_results:
                result_text += f"- {pred['label']}: {pred['confidence']:.2f}%\n"
            
            # Encode the image as base64 for display
            with open(filepath, "rb") as img_file:
                img_data = img_file.read()
                encoded_img = base64.b64encode(img_data).decode('utf-8')
            
            img = Image.open(filepath)
            img_format = img.format.lower()
            img_mime = f"image/{img_format}"
            
            # Create data URI
            img_data_uri = f"data:{img_mime};base64,{encoded_img}"
            
            # Save the original path as reference, but we won't use it for display
            image_path = 'uploads/' + filename
            
            return render_template(
                'index.html', 
                result_text=result_text, 
                image_path=image_path,
                img_data_uri=img_data_uri,  # Pass the data URI to the template
                predictions=classification_results
            )
            
        except Exception as e:
            import traceback
            print(traceback.format_exc())
            return render_template('index.html', result=f"Error processing image: {str(e)}")
    
    return render_template('index.html', result='Invalid file type')

if __name__ == '__main__':
    app.run(debug=True)
