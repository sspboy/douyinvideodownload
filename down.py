import requests
import re,json,time
import os


# 抖音视频下载到本地脚本

def get_video_url(share_url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) EdgiOS/121.0.2277.107 Version/17.0 Mobile/15E148 Safari/604.1'
    }
    # 发送请求获取视频页面
    response = requests.get(share_url, headers=headers)
    video_id = response.url.split("?")[0].strip("/").split("/")[-1]
    share_url = f'https://www.iesdouyin.com/share/video/{video_id}'
    response = requests.get(share_url, headers=headers)
    response.raise_for_status()
    # 使用正则表达式提取视频信息
    pattern = re.compile(
        pattern=r"window\._ROUTER_DATA\s*=\s*(.*?)</script>",
        flags=re.DOTALL
    )
    find_res = pattern.search(response.text)
    if not find_res or not find_res.group(1):
        raise ValueError("parse video json info from html fail")
    json_data = json.loads(find_res.group(1).strip())
    data = json_data["loaderData"]["video_(id)/page"]["videoInfoRes"]["item_list"][0]
    # 获取无水印视频链接
    video_url = data["video"]["play_addr"]["url_list"][0].replace("playwm", "play")
    return video_url

def download_video(video_url, save_path='video.mp4'):
    headers = {
        'User-Agent': 'Mozilla/5.0 (iPpip hone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) EdgiOS/121.0.2277.107 Version/17.0 Mobile/15E148 Safari/604.1'
    }
    response = requests.get(video_url, headers=headers, stream=True)
    response.raise_for_status()
    # 保存视频到本地
    with open(save_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    print(f"视频已下载到 {save_path}")

def main():
    share_url = input("请输入抖音视频的分享链接：")
    # share_url = input("请输入抖音视频的分享链接：")
    try:
        video_url = get_video_url(share_url)
        print("无水印视频链接已获取：", video_url)
        vide_name = time.strftime("%Y%m%d", time.localtime()) + ".mp4"
        download_video(video_url, vide_name)
        print("视频下载完成！")
    except Exception as e:
        print("发生错误：", e)



if __name__ == "__main__":
    # url = 'https://v.douyin.com/FrCVzzFRkNo/'
    # url2 = 'https://v.douyin.com/nmA1BnzT8JA/'
    # url3 = 'https://v.douyin.com/jlhumPA4gUo/' # 不允许下载链接
    # video_url = get_video_url('https://v.douyin.com/yweiALuTu9o/')
    # print(video_url)
    # 6.10 reo:/ 02/28 l@c.aa # 脱口秀互动  https://v.douyin.com/6ITrdhzpCyo/ 复制此链接，打开Dou音搜索，直接观看视频！
    # 视频下载整合方法
    main()