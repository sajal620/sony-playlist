import json
import urllib.request

JSON_URL = "https://raw.githubusercontent.com/vijay-iptv/JSON/refs/heads/main/sony.json"
OUTPUT_FILE = "playlist.m3u"


def fetch_json(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req) as response:
        return json.loads(response.read().decode("utf-8"))


def generate_m3u(channels, output_file):
    lines = ["#EXTM3U"]
    count = 0

    for ch in channels:
        name = ch.get("channel_name", "Unknown")
        logo = ch.get("logoUrl", "")
        stream = ch.get("direct_url", "") or ch.get("url", "")
        language = ch.get("channelLanguageId", "")
        category = ch.get("channelCategoryId", "Other")
        ch_id = ch.get("channel_id", "")
        is_hd = ch.get("isHD", "False")
        hd_tag = "HD" if is_hd == "True" else "SD"

        if not stream:
            continue

        group = f"{language} - {category}"

        lines.append(
            f'#EXTINF:-1 tvg-id="{ch_id}" tvg-name="{name}" '
            f'tvg-logo="{logo}" group-title="{group}",{name} [{hd_tag}]'
        )
        lines.append(stream)
        count += 1

    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"✅ Playlist তৈরি হয়েছে: {output_file}")
    print(f"📺 মোট channel: {count}")


def main():
    print("⏳ JSON fetch করা হচ্ছে...")
    channels = fetch_json(JSON_URL)
    print(f"✅ {len(channels)} টি channel পাওয়া গেছে।")
    generate_m3u(channels, OUTPUT_FILE)


if __name__ == "__main__":
    main()
