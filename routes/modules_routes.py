from flask import Blueprint, jsonify, request

modules_bp = Blueprint('modules', __name__)

videos = [
    {
        "title": "Module 1",
        "url": "http://192.168.29.93:5000/static/videos/video1.mp4"
    },
    {
        "title": "Module 2",
        "url": "http://192.168.29.93:5000/static/videos/video2.mp4"
    },
    {
        "title": "Module 3",
        "url": "http://192.168.29.93:5000/static/videos/video4.mp4"
    },
    {
        "title": "Module 4",
        "url": "http://192.168.29.93:5000/static/videos/video6.mp4"
    },
    {
        "title": "Module 5",
        "url": "http://192.168.29.93:5000/static/videos/video8.mp4"
    },
    {
        "title": "Module 6",
        "url": "http://192.168.29.93:5000/static/videos/video10.mp4"
    },
    {
        "title": "Module 7",
        "url": "http://192.168.29.93:5000/static/videos/video12.mp4"
    },
    {
        "title": "Module 8",
        "url": "http://192.168.29.93:5000/static/videos/video13.mp4"
    }
]

@modules_bp.route('/get_modules', methods=['GET'])
def get_modules():
    return jsonify({
        "modules": videos
    })