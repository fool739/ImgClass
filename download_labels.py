# Save this as download_labels.py and run it once
import urllib.request

# Download the class labels
url = "https://raw.githubusercontent.com/pytorch/hub/master/imagenet_classes.txt"
urllib.request.urlretrieve(url, "imagenet_classes.txt")
print("Downloaded ImageNet class labels")