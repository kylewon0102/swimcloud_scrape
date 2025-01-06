# Import necessary classes from swimcloud.py
from swimcloud import swimmer_class, url_class


def test():
    kyle = swimmer_class("https://www.swimcloud.com/swimmer/902649/")
    kyle.url.html.save_soup_to_file("kyle.html")
    kyle.update_info()
    kyle.save_info_as_file("kylewon.txt")
    print(f"Swimmer Name: {kyle.name}")
    print(f"Hometown: {kyle.hometown}")
    print(f"University: {kyle.university}")
    print(f"SNS Links: {kyle.sns}")
    print(f"Events List: {kyle.events_list}")

    print(kyle.search_event("400 L Free"))

test()