from flask import Flask, jsonify
from flask_cors import CORS

from fetch_images import get_authentic_flickr_images
from ai_brain import analyze_and_cluster

app = Flask(__name__)
CORS(app) 

@app.route('/api/cluster-images', methods=['GET'])
def cluster_images():
    print("React requested images! Starting the AI engine...")
    
    # Using the newly renamed authentic fetcher!
    my_urls = get_authentic_flickr_images()
    results, labels = analyze_and_cluster(my_urls, num_clusters=5)
    
    payload = {
        "clusters": results,
        "labels": labels
    }
    
    print("Finished! Sending data back to React.")
    return jsonify(payload)

if __name__ == '__main__':
    print("Starting the AI Web Server on http://127.0.0.1:8080...")
    app.run(host='127.0.0.1', port=8080, debug=True)