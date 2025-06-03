import requests
import os

# def download_video(video_url, output_filename):
#     headers = {
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
#         'Referer': 'https://www.pornhub.com/'  # Often required for video access
#     }
    
#     with requests.get(video_url, headers=headers, stream=True) as r:
#         r.raise_for_status()
#         with open(output_filename, 'wb') as f:
#             for chunk in r.iter_content(chunk_size=8192):
#                 f.write(chunk)
#     print(f"Video downloaded as {output_filename}")

# # Example usage with URL you found in Network tab:
# download_video('https://www.pornhub.com/ae758400-6776-4e74-8ec0-8cb797b7d7e7', 'video.mp4')

def download_segments(base_url, output_filename, start_seg=1):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Referer': 'https://www.pornhub.com/'
    }
    segment_files = []
    seg_num = start_seg
    while True:
        seg_url = base_url.replace('seg-1-v1-a1.ts', f'seg-{seg_num}-v1-a1.ts')
        seg_filename = f'segment_{seg_num}.ts'
        try:
            with requests.get(seg_url, headers=headers, stream=True, timeout=10) as r:
                if r.status_code != 200:
                    print(f"Segment {seg_num} not found or request rejected. Stopping.")
                    break
                with open(seg_filename, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)
            print(f"Downloaded segment {seg_num}")
            segment_files.append(seg_filename)
            seg_num += 1
        except Exception as e:
            print(f"Error downloading segment {seg_num}: {e}")
            break

    # Combine segments
    with open(output_filename, 'wb') as outfile:
        for fname in segment_files:
            with open(fname, 'rb') as infile:
                outfile.write(infile.read())
            os.remove(fname)
    print(f"Combined video saved as {output_filename}")

# Example usage:
# Use the first segment URL as base_url
base_url = 'https://hv-h.phncdn.com/hls/videos/202312/04/444112401/720P_4000K_444112401.mp4/seg-1-v1-a1.ts?h=1d86CDOsLAlbyxC08h%2Fsp6TjzL4%3D&e=1748918647&f=1'
download_segments(base_url, 'full_video.ts')

