import cv2
from PIL import Image
import osп
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)

        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            kernel_size = request.form.get('kernel_size')
            if kernel_size:
                try:
                    kernel_size = int(kernel_size)
                    if kernel_size <= 1 or kernel_size % 2 == 0:
                        return "Invalid kernel size. Please enter an odd number greater than 1."
                except ValueError:
                    return "Invalid kernel size. Please enter a numerical value."
            else:
                kernel_size = 5

            task = request.form.get('task')
            processed_image_path, histogram_base64  = process_image(filepath, task, kernel_size)

            return render_template(
                'index.html', 
                filename=processed_image_path.split('/')[-1],
                original_filename=filename, 
                histogram_base64=histogram_base64
            )

    return render_template('index.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename) 

def process_image(image_path, task, kernel_size=5):
    """Processes the image based on the selected task."""

    img = cv2.imread(image_path)
    histogram_base64 = None

    if task == '1':
        processed_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    elif task == '2':
        processed_img = cv2.blur(img, (kernel_size, kernel_size)) 

    elif task == '3':
        processed_img = cv2.GaussianBlur(img, (kernel_size, kernel_size), 0)

    elif task == '4':
        if kernel_size % 2 == 0: 
            kernel_size += 1
        processed_img = cv2.medianBlur(img, kernel_size) 
    elif task == '5':
        img_yuv = cv2.cvtColor(img, cv2.COLOR_BGR2YUV)
        img_yuv[:, :, 0] = cv2.equalizeHist(img_yuv[:, :, 0])
        processed_img = cv2.cvtColor(img_yuv, cv2.COLOR_YUV2BGR)
    else:
        processed_img = img 

    output_filename = f"processed_{os.path.basename(image_path)}"
    output_path = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)

    if 'processed_img' in locals() and isinstance(processed_img, Image.Image):
        processed_img.save(output_path)
    else:
        cv2.imwrite(output_path, processed_img)

    return output_path, histogram_base64

if __name__ == '__main__':
    app.run(debug=True)