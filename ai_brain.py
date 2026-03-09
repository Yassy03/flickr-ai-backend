import requests
from PIL import Image
from io import BytesIO
from transformers import CLIPProcessor, CLIPModel
import torch
from sklearn.cluster import KMeans

# THE FIX: Updated the import name here!
from fetch_images import get_authentic_flickr_images

def analyze_and_cluster(urls, num_clusters=5):
    print("Loading the CLIP AI Model...")
    model_id = "openai/clip-vit-base-patch32"
    processor = CLIPProcessor.from_pretrained(model_id)
    model = CLIPModel.from_pretrained(model_id)

    url_data = {}
    valid_urls = []
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
    }

    print(f"\nAnalyzing {len(urls)} images...")
    for i, url in enumerate(urls):
        print(f"Looking at image {i+1}/{len(urls)}...")
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status() 
            image = Image.open(BytesIO(response.content)).convert("RGB")
            
            inputs = processor(text=["a photo"], images=image, return_tensors="pt", padding=True)
            
            with torch.no_grad():
                outputs = model(**inputs)
                image_embeds = outputs.image_embeds 
            
            url_data[url] = image_embeds.squeeze().tolist()
            valid_urls.append(url)
            
        except Exception as e:
            print(f"  -> Skipped image. Reason: {e}")

    if len(url_data) < num_clusters:
        print("\nUh oh! Not enough images downloaded to cluster. Halting.")
        return {}, {}

    print("\nRunning K-Means Clustering to group the images...")
    embeddings = [url_data[url] for url in valid_urls]
    
    kmeans = KMeans(n_clusters=num_clusters, random_state=42, n_init=10)
    kmeans.fit(embeddings)

    clusters = {i: [] for i in range(num_clusters)}
    for url, cluster_id in zip(valid_urls, kmeans.labels_):
        clusters[cluster_id].append(url)

    print("\nExtracting mathematical centroids...")
    cluster_labels = {}
    
    for i, center_vector in enumerate(kmeans.cluster_centers_):
        math_label = f"[{center_vector[0]:.4f}, {center_vector[1]:.4f}, {center_vector[2]:.4f}, {center_vector[3]:.4f}, {center_vector[4]:.4f}...]"
        cluster_labels[i] = math_label

    return clusters, cluster_labels

if __name__ == "__main__":
    # THE FIX: Updated the function call here too!
    my_urls = get_authentic_flickr_images()
    
    results, labels = analyze_and_cluster(my_urls, num_clusters=5)

    if results:
        print("\n" + "="*50)
        print("🤖 PURE DATA-DRIVEN CLUSTERING RESULTS 🤖")
        print("="*50)
        
        for cluster_id, image_urls in results.items():
            label = labels[cluster_id]
            print(f"\n--- AI Category {cluster_id + 1} ---")
            print(f"Mathematical Centroid: {label}")
            print(f"Contains {len(image_urls)} images:")
            for url in image_urls:
                print(f"  {url}")