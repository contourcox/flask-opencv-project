from flask import Flask, render_template, send_from_directory
from bite3 import get_image_data  # Ensure this module is implemented correctly
import os

app = Flask(__name__)

# Serve the image from a custom directory
@app.route('/custom_static/<path:filename>')
def custom_static(filename):
    # Define the static folder path
    image_folder = os.path.expanduser('~/Desktop/TEst/static')
    return send_from_directory(image_folder, filename)

# Main route to display the image slider
@app.route('/')
def index():
    # Directory containing the images
    image_folder = os.path.expanduser("~/Desktop/TEst/static")

    # Ensure the folder exists
    if not os.path.exists(image_folder):
        raise RuntimeError(f"Directory {image_folder} does not exist!")

    # Get all image files in the folder
    image_files = [f for f in os.listdir(image_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

    # Initialize a list to store image data
    images_data = []

    # Process each image
    for image_file in image_files:
        image_path = os.path.join(image_folder, image_file)

        try:
            # Get image data (e.g., ZIP codes)
            image_data = get_image_data(image_path)
            images_data.append({
                'image_path': image_file,  # Store only the filename
                'sender_zip': image_data.get('sender_zip', 'Unknown'),  # Handle missing data
                'destination_zip': image_data.get('destination_zip', 'Unknown')  # Handle missing data
            })
        except Exception as e:
            print(f"Error processing {image_file}: {e}")
            images_data.append({
                'image_path': image_file,
                'sender_zip': 'Error',
                'destination_zip': 'Error'
            })

    # Pass the images data to the template
    return render_template('slide.html', images_data=images_data)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=7000)
