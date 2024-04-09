# # from flask import Flask, render_template, request
# # import pytube
# # import os

# # app = Flask(__name__)
# # first_submission = True  # Flag to track initial submission

# # @app.route('/')
# # def download_form():
# #     global first_submission
# #     first_submission = True  # Reset flag on each request
# #     return render_template('index.html')

# # @app.route('/', methods=['POST'])
# # def download_video():
# #     global first_submission
# #     url = request.form.get('url')
# #     try:
# #         # Handle initial submission (required URL)
# #         if first_submission and not url:
# #             return render_template('index.html', message="Please enter a YouTube video URL.")

# #         # Subsequent submissions (URL optional)
# #         first_submission = False

# #         if url:
# #             # Use pytube to get video information
# #             yt = pytube.YouTube(url)
# #             video_title = yt.title

# #             # Extract available formats (optional)
# #             formats = yt.streams.filter(progressive=True).order_by('resolution').desc()

# #             # Handle quality selection (optional)
# #             if request.method == 'POST':
# #                 selected_format = request.form.get('format')
# #                 if selected_format:
# #                     stream = yt.streams.get_by_itag(selected_format)

# #                     # Get user's download folder path (platform-independent)
# #                     download_folder = os.path.join(os.path.expanduser('~'), 'Downloads')

# #                     # Download to user's download folder
# #                     stream.download(filename=os.path.join(download_folder, f"{video_title}.mp4"))
# #                     return f"Downloaded {video_title}.mp4 to your Downloads folder!"

# #             return render_template('index.html', video_title=video_title, formats=formats)  # Pass formats for selection (optional)
# #         else:
# #             # Use existing video information (if available)
# #             return render_template('index.html', video_title=video_title, formats=formats)  # Pass formats for selection (optional)

# #     except pytube.exceptions.PytubeError as e:
# #         return f"Error: {e}"

# # if __name__ == '__main__':
# #     app.run(debug=True)
# # ********************************************************************************************
# from flask import Flask, render_template, request
# import subprocess

# app = Flask(__name__)

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/', methods=['GET', 'POST'])
# def download_video():
#     if request.method == 'POST':
#         data = request.form.get('dataToSend', '')
#         data = data.strip()  # Remove whitespace

#         if not data:
#             return 'Please enter a valid YouTube URL.', 400

#         try:
#             # Use subprocess to run yt-dlp command
#             command = ['yt-dlp', '-f', 'best', '-o', '%(title)s.%(ext)s', data]
#             result = subprocess.run(command, check=True)

#             if result.returncode == 0:
#                 return 'Video downloaded successfully!'
#             else:
#                 # Handle potential yt-dlp errors
#                 return f'Error downloading video: {result.stderr.decode()}'
#         except subprocess.CalledProcessError as e:
#             return f'Error: {str(e)}', 500
#     else:
#         return 'Hello, please submit the form to send data.'

# if __name__ == '__main__':
#     app.run(debug=True)

# ============================================================================================

from flask import Flask, render_template, request, flash
from subprocess import run, PIPE, CalledProcessError
import secrets
import os

app = Flask(__name__)
app.secret_key = secrets.token_urlsafe(32)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['GET', 'POST'])
def download_video():
    if request.method == 'POST':
        data = request.form.get('dataToSend', '').strip()

        if not data:
            flash('Please enter a valid YouTube URL.', category='error')
            return render_template('index.html')

        try:
            # Use subprocess with error handling and capture output
            command = ['yt-dlp', '-f', 'best', '-o', '%(title)s.%(ext)s', data]
            process = run(command, stdout=PIPE, stderr=PIPE, check=True)

            # Get user's download folder path (platform-independent)
            download_folder = os.path.join(os.path.expanduser('~'), 'Downloads')

            # Construct success message with download location
            download_message = f'Video downloaded successfully to your Downloads folder: {download_folder}/{process.stdout.decode().splitlines()[0]}.mp4'
            flash(download_message, category='success')
            return render_template('index.html')

        except CalledProcessError as e:
            # Handle yt-dlp errors with informative message
            error_message = f'Error downloading video: {e.stderr.decode()}'
            flash(error_message, category='error')
            return render_template('index.html')

        except Exception as e:  # Catch other potential errors
            error_message = f'An unexpected error occurred: {str(e)}'
            flash(error_message, category='error')
            return render_template('index.html')

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

