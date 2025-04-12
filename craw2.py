import wikipediaapi
import json
from tqdm import tqdm
import os

wiki = wikipediaapi.Wikipedia(
    language="vi",
    user_agent="LichSuBot/1.0 (contact@lichsubot.vn)"
)


def get_pages_from_category(category_name, max_depth=2, current_depth=0, max_pages=100):
    pages = {}
    if current_depth > max_depth or len(pages) >= max_pages:
        return pages

    cat = wiki.page("Thể loại:" + category_name)
    if not cat.exists():
        return pages

    for title in cat.categorymembers:
        if len(pages) >= max_pages:
            break
        member = cat.categorymembers[title]
        if member.ns == wikipediaapi.Namespace.CATEGORY:
            sub_pages = get_pages_from_category(
                member.title.replace("Thể loại:", ""),
                max_depth,
                current_depth + 1,
                max_pages
            )
            pages.update(sub_pages)
        elif member.ns == wikipediaapi.Namespace.MAIN:
            pages[member.title] = member.text[:500]  

    return pages

def save_to_file(data, filename="lich_su_partial.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def crawl_history(max_pages=100):
    all_pages = {}
    try:
        pages = get_pages_from_category("Lịch sử Việt Nam", max_pages=max_pages)

        all_pages.update(pages)
        save_to_file(all_pages)
        print(f"Đã thu thập {len(pages)} bài viết lịch sử Việt Nam.")
    except Exception as e:
        print(f"Đã gặp lỗi: {e}")

    return all_pages

def main():
    pages = crawl_history(max_pages=100)
    print(f"Đã thu thập tổng cộng {len(pages)} bài viết.")
    for title, content in pages.items():
        print(f"{title}: {content}\n")

if __name__ == "__main__":
    main()
