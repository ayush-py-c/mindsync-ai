b"""Curated Hindi and English mood-based music catalog.

Provides rich, verified collections of popular Hindi songs across Bollywood,
Indie, and classic releases mapped to detected emotions. Used when Deezer
is unreachable, rate-limited, geo-restricted, or when blending Hindi songs
alongside English recommendations.
"""

import random
import urllib.parse

# Canonical emotion categories
EMOTION_CANONICAL_MAP = {
    "joy": "joy",
    "happy": "joy",
    "happiness": "joy",
    "excited": "joy",
    "amused": "joy",
    "fun": "joy",
    "sadness": "sadness",
    "sad": "sadness",
    "depressed": "sadness",
    "lonely": "sadness",
    "grief": "sadness",
    "love": "love",
    "romance": "love",
    "romantic": "love",
    "anger": "anger",
    "angry": "anger",
    "frustrated": "anger",
    "annoyed": "anger",
    "fear": "fear",
    "fearful": "fear",
    "anxious": "fear",
    "stressed": "fear",
    "calm": "fear",
    "peaceful": "fear",
    "relaxed": "fear",
    "soothing": "fear",
    "neutral": "neutral",
    "bored": "neutral",
    "tired": "neutral",
    "content": "neutral",
    "chill": "neutral",
    "nostalgic": "nostalgic",
    "nostalgia": "nostalgic",
    "throwback": "nostalgic",
    "surprised": "surprised",
    "surprise": "surprised",
    "energetic": "surprised",
    "hopeful": "surprised",
    "proud": "surprised",
    "disgust": "anger",
    "disgusted": "anger",
    "confused": "neutral",
}

# Rich collection of popular Hindi songs categorized by mood
HINDI_EMOTION_TRACKS: dict[str, list[dict]] = {
    "joy": [
        {"name": "Badtameez Dil", "artist": "Benny Dayal, Shefali Alvares", "album": "Yeh Jawaani Hai Deewani", "popularity": 92, "duration_ms": 252000, "release_date": "2013-05-31", "image_url": "https://images.unsplash.com/photo-1514525253161-7a46d19cd819?w=300"},
        {"name": "Kar Gayi Chull", "artist": "Badshah, Neha Kakkar, Fazilpuria", "album": "Kapoor & Sons", "popularity": 90, "duration_ms": 187000, "release_date": "2016-03-04", "image_url": "https://images.unsplash.com/photo-1492684223066-81342ee5ff30?w=300"},
        {"name": "Gallan Goodiyaan", "artist": "Shankar Mahadevan, Yashita Sharma", "album": "Dil Dhadakne Do", "popularity": 89, "duration_ms": 296000, "release_date": "2015-05-02", "image_url": "https://images.unsplash.com/photo-1470225620780-dba8ba36b745?w=300"},
        {"name": "London Thumakda", "artist": "Labh Janjua, Sonu Kakkar, Neha Kakkar", "album": "Queen", "popularity": 91, "duration_ms": 230000, "release_date": "2014-01-30", "image_url": "https://images.unsplash.com/photo-1516450360452-9312f5e86fc7?w=300"},
        {"name": "Ghungroo", "artist": "Arijit Singh, Shilpa Rao", "album": "War", "popularity": 94, "duration_ms": 302000, "release_date": "2019-09-05", "image_url": "https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?w=300"},
        {"name": "Matargashti", "artist": "Mohit Chauhan", "album": "Tamasha", "popularity": 88, "duration_ms": 328000, "release_date": "2015-10-09", "image_url": "https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?w=300"},
        {"name": "Ilahi", "artist": "Arijit Singh", "album": "Yeh Jawaani Hai Deewani", "popularity": 93, "duration_ms": 229000, "release_date": "2013-05-31", "image_url": "https://images.unsplash.com/photo-1465847899084-d164df4dedc6?w=300"},
        {"name": "Sooraj Dooba Hain", "artist": "Arijit Singh, Aditi Singh Sharma", "album": "Roy", "popularity": 89, "duration_ms": 264000, "release_date": "2015-01-11", "image_url": "https://images.unsplash.com/photo-1508700115892-45ecd05ae2ad?w=300"},
        {"name": "Subha Hone Na De", "artist": "Mika Singh, Shefali Alvares", "album": "Desi Boyz", "popularity": 87, "duration_ms": 288000, "release_date": "2011-10-25", "image_url": "https://images.unsplash.com/photo-1514525253161-7a46d19cd819?w=300"},
        {"name": "Ullu Ka Pattha", "artist": "Arijit Singh, Nikhita Gandhi", "album": "Jagga Jasoos", "popularity": 85, "duration_ms": 212000, "release_date": "2017-06-02", "image_url": "https://images.unsplash.com/photo-1492684223066-81342ee5ff30?w=300"},
        {"name": "Senorita", "artist": "Farhan Akhtar, Hrithik Roshan, Abhay Deol", "album": "Zindagi Na Milegi Dobara", "popularity": 90, "duration_ms": 231000, "release_date": "2011-06-20", "image_url": "https://images.unsplash.com/photo-1516450360452-9312f5e86fc7?w=300"},
        {"name": "Makhna", "artist": "Tanishk Bagchi, Yasser Desai, Asees Kaur", "album": "Drive", "popularity": 86, "duration_ms": 183000, "release_date": "2019-10-04", "image_url": "https://images.unsplash.com/photo-1470225620780-dba8ba36b745?w=300"},
        {"name": "Kala Chashma", "artist": "Badshah, Neha Kakkar, Amar Arshi", "album": "Baar Baar Dekho", "popularity": 93, "duration_ms": 187000, "release_date": "2016-07-27", "image_url": "https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?w=300"},
        {"name": "Sweetheart", "artist": "Dev Negi", "album": "Kedarnath", "popularity": 88, "duration_ms": 212000, "release_date": "2018-11-15", "image_url": "https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?w=300"},
    ],
    "sadness": [
        {"name": "Channa Mereya", "artist": "Arijit Singh", "album": "Ae Dil Hai Mushkil", "popularity": 96, "duration_ms": 289000, "release_date": "2016-09-29", "image_url": "https://images.unsplash.com/photo-1518495973542-4542c06a5843?w=300"},
        {"name": "Agar Tum Saath Ho", "artist": "Alka Yagnik, Arijit Singh", "album": "Tamasha", "popularity": 97, "duration_ms": 341000, "release_date": "2015-10-27", "image_url": "https://images.unsplash.com/photo-1499209974431-9dddcece7f88?w=300"},
        {"name": "Kabira", "artist": "Tochi Raina, Rekha Bhardwaj", "album": "Yeh Jawaani Hai Deewani", "popularity": 94, "duration_ms": 223000, "release_date": "2013-05-31", "image_url": "https://images.unsplash.com/photo-1516280440614-37939bbacd81?w=300"},
        {"name": "Tujhe Kitna Chahne Lage", "artist": "Arijit Singh", "album": "Kabir Singh", "popularity": 95, "duration_ms": 284000, "release_date": "2019-05-31", "image_url": "https://images.unsplash.com/photo-1509198397868-475647b2a1e5?w=300"},
        {"name": "Kal Ho Naa Ho", "artist": "Sonu Nigam", "album": "Kal Ho Naa Ho", "popularity": 95, "duration_ms": 321000, "release_date": "2003-09-27", "image_url": "https://images.unsplash.com/photo-1447752875215-b2761acb3c5d?w=300"},
        {"name": "Bekhayali", "artist": "Sachet Tandon", "album": "Kabir Singh", "popularity": 93, "duration_ms": 371000, "release_date": "2019-05-24", "image_url": "https://images.unsplash.com/photo-1518495973542-4542c06a5843?w=300"},
        {"name": "Hamari Adhuri Kahani", "artist": "Arijit Singh", "album": "Hamari Adhuri Kahani", "popularity": 90, "duration_ms": 398000, "release_date": "2015-05-08", "image_url": "https://images.unsplash.com/photo-1499209974431-9dddcece7f88?w=300"},
        {"name": "Duaa", "artist": "Nandini Srikar, Arijit Singh, Shekhar Ravjiani", "album": "Shanghai", "popularity": 88, "duration_ms": 260000, "release_date": "2012-05-18", "image_url": "https://images.unsplash.com/photo-1516280440614-37939bbacd81?w=300"},
        {"name": "Kun Faya Kun", "artist": "A.R. Rahman, Javed Ali, Mohit Chauhan", "album": "Rockstar", "popularity": 96, "duration_ms": 473000, "release_date": "2011-09-20", "image_url": "https://images.unsplash.com/photo-1509198397868-475647b2a1e5?w=300"},
        {"name": "Jag Ghoomeya", "artist": "Rahat Fateh Ali Khan", "album": "Sultan", "popularity": 91, "duration_ms": 281000, "release_date": "2016-06-07", "image_url": "https://images.unsplash.com/photo-1447752875215-b2761acb3c5d?w=300"},
        {"name": "Phir Le Aya Dil", "artist": "Arijit Singh", "album": "Barfi!", "popularity": 89, "duration_ms": 305000, "release_date": "2012-08-10", "image_url": "https://images.unsplash.com/photo-1518495973542-4542c06a5843?w=300"},
        {"name": "Ae Dil Hai Mushkil", "artist": "Arijit Singh", "album": "Ae Dil Hai Mushkil", "popularity": 94, "duration_ms": 269000, "release_date": "2016-08-30", "image_url": "https://images.unsplash.com/photo-1499209974431-9dddcece7f88?w=300"},
        {"name": "Tu Jaane Na", "artist": "Atif Aslam", "album": "Ajab Prem Ki Ghazab Kahani", "popularity": 93, "duration_ms": 341000, "release_date": "2009-10-12", "image_url": "https://images.unsplash.com/photo-1516280440614-37939bbacd81?w=300"},
        {"name": "Jiyein Kyun", "artist": "Papon", "album": "Dum Maaro Dum", "popularity": 87, "duration_ms": 266000, "release_date": "2011-03-21", "image_url": "https://images.unsplash.com/photo-1509198397868-475647b2a1e5?w=300"},
    ],
    "love": [
        {"name": "Tum Hi Ho", "artist": "Arijit Singh", "album": "Aashiqui 2", "popularity": 98, "duration_ms": 262000, "release_date": "2013-04-04", "image_url": "https://images.unsplash.com/photo-1518199266791-5375a83190b7?w=300"},
        {"name": "Kesariya", "artist": "Arijit Singh", "album": "Brahmastra", "popularity": 98, "duration_ms": 268000, "release_date": "2022-07-17", "image_url": "https://images.unsplash.com/photo-1516589178581-6cd7833ae3b2?w=300"},
        {"name": "Raataan Lambiyan", "artist": "Jubin Nautiyal, Asees Kaur", "album": "Shershaah", "popularity": 96, "duration_ms": 230000, "release_date": "2021-07-30", "image_url": "https://images.unsplash.com/photo-1529333166437-7750a6dd5a70?w=300"},
        {"name": "Apna Bana Le", "artist": "Arijit Singh, Sachin-Jigar", "album": "Bhediya", "popularity": 97, "duration_ms": 261000, "release_date": "2022-11-05", "image_url": "https://images.unsplash.com/photo-1518199266791-5375a83190b7?w=300"},
        {"name": "Pee Loon", "artist": "Mohit Chauhan", "album": "Once Upon a Time in Mumbaai", "popularity": 93, "duration_ms": 287000, "release_date": "2010-06-25", "image_url": "https://images.unsplash.com/photo-1516589178581-6cd7833ae3b2?w=300"},
        {"name": "Tera Ban Jaunga", "artist": "Akhil Sachdeva, Tulsi Kumar", "album": "Kabir Singh", "popularity": 94, "duration_ms": 236000, "release_date": "2019-06-17", "image_url": "https://images.unsplash.com/photo-1529333166437-7750a6dd5a70?w=300"},
        {"name": "Mast Magan", "artist": "Arijit Singh, Chinmayi Sripada", "album": "2 States", "popularity": 91, "duration_ms": 280000, "release_date": "2014-03-26", "image_url": "https://images.unsplash.com/photo-1518199266791-5375a83190b7?w=300"},
        {"name": "Zehnaseeb", "artist": "Chinmayi Sripada, Shekhar Ravjiani", "album": "Hasee Toh Phasee", "popularity": 90, "duration_ms": 215000, "release_date": "2014-01-07", "image_url": "https://images.unsplash.com/photo-1516589178581-6cd7833ae3b2?w=300"},
        {"name": "Shayad", "artist": "Arijit Singh", "album": "Love Aaj Kal", "popularity": 92, "duration_ms": 247000, "release_date": "2020-01-22", "image_url": "https://images.unsplash.com/photo-1529333166437-7750a6dd5a70?w=300"},
        {"name": "Kaise Hua", "artist": "Vishal Mishra", "album": "Kabir Singh", "popularity": 93, "duration_ms": 234000, "release_date": "2019-06-13", "image_url": "https://images.unsplash.com/photo-1518199266791-5375a83190b7?w=300"},
        {"name": "Hawayein", "artist": "Arijit Singh", "album": "Jab Harry Met Sejal", "popularity": 94, "duration_ms": 290000, "release_date": "2017-07-26", "image_url": "https://images.unsplash.com/photo-1516589178581-6cd7833ae3b2?w=300"},
        {"name": "Pehla Nasha", "artist": "Udit Narayan, Sadhana Sargam", "album": "Jo Jeeta Wohi Sikandar", "popularity": 95, "duration_ms": 291000, "release_date": "1992-05-22", "image_url": "https://images.unsplash.com/photo-1529333166437-7750a6dd5a70?w=300"},
        {"name": "Raabta", "artist": "Arijit Singh, Hamsika Iyer", "album": "Agent Vinod", "popularity": 91, "duration_ms": 244000, "release_date": "2012-02-28", "image_url": "https://images.unsplash.com/photo-1518199266791-5375a83190b7?w=300"},
        {"name": "Bol Do Na Zara", "artist": "Armaan Malik", "album": "Azhar", "popularity": 90, "duration_ms": 293000, "release_date": "2016-04-15", "image_url": "https://images.unsplash.com/photo-1516589178581-6cd7833ae3b2?w=300"},
    ],
    "anger": [
        {"name": "Sadda Haq", "artist": "Mohit Chauhan", "album": "Rockstar", "popularity": 94, "duration_ms": 365000, "release_date": "2011-09-30", "image_url": "https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?w=300"},
        {"name": "Bhaag D.K. Bose", "artist": "Ram Sampath", "album": "Delhi Belly", "popularity": 91, "duration_ms": 242000, "release_date": "2011-05-06", "image_url": "https://images.unsplash.com/photo-1498038432885-c6f3f1b912ee?w=300"},
        {"name": "Zinda", "artist": "Siddharth Mahadevan", "album": "Bhaag Milkha Bhaag", "popularity": 92, "duration_ms": 211000, "release_date": "2013-06-19", "image_url": "https://images.unsplash.com/photo-1465847899084-d164df4dedc6?w=300"},
        {"name": "Aarambh Hai Prachand", "artist": "Piyush Mishra", "album": "Gulaal", "popularity": 95, "duration_ms": 296000, "release_date": "2009-02-27", "image_url": "https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?w=300"},
        {"name": "Chak De! India", "artist": "Sukhwinder Singh", "album": "Chak De! India", "popularity": 93, "duration_ms": 283000, "release_date": "2007-08-01", "image_url": "https://images.unsplash.com/photo-1498038432885-c6f3f1b912ee?w=300"},
        {"name": "Jee Karda", "artist": "Divya Kumar", "album": "Badlapur", "popularity": 90, "duration_ms": 231000, "release_date": "2014-12-09", "image_url": "https://images.unsplash.com/photo-1465847899084-d164df4dedc6?w=300"},
        {"name": "Kar Har Maidaan Fateh", "artist": "Sukhwinder Singh, Shreya Ghoshal", "album": "Sanju", "popularity": 93, "duration_ms": 311000, "release_date": "2018-06-10", "image_url": "https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?w=300"},
        {"name": "Sultan", "artist": "Sukhwinder Singh, Shadab Faridi", "album": "Sultan", "popularity": 89, "duration_ms": 279000, "release_date": "2016-06-23", "image_url": "https://images.unsplash.com/photo-1498038432885-c6f3f1b912ee?w=300"},
        {"name": "Apna Time Aayega", "artist": "Ranveer Singh, DIVINE", "album": "Gully Boy", "popularity": 95, "duration_ms": 140000, "release_date": "2019-01-14", "image_url": "https://images.unsplash.com/photo-1465847899084-d164df4dedc6?w=300"},
        {"name": "Sher Aaya Sher", "artist": "DIVINE", "album": "Gully Boy", "popularity": 88, "duration_ms": 135000, "release_date": "2019-01-24", "image_url": "https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?w=300"},
        {"name": "Malhari", "artist": "Vishal Dadlani", "album": "Bajirao Mastani", "popularity": 91, "duration_ms": 245000, "release_date": "2015-11-28", "image_url": "https://images.unsplash.com/photo-1498038432885-c6f3f1b912ee?w=300"},
        {"name": "Dangal", "artist": "Daler Mehndi", "album": "Dangal", "popularity": 90, "duration_ms": 299000, "release_date": "2016-12-08", "image_url": "https://images.unsplash.com/photo-1465847899084-d164df4dedc6?w=300"},
    ],
    "fear": [
        {"name": "Iktara", "artist": "Kavita Seth, Amitabh Bhattacharya", "album": "Wake Up Sid", "popularity": 95, "duration_ms": 253000, "release_date": "2009-08-21", "image_url": "https://images.unsplash.com/photo-1518495973542-4542c06a5843?w=300"},
        {"name": "Namo Namo", "artist": "Amit Trivedi", "album": "Kedarnath", "popularity": 94, "duration_ms": 322000, "release_date": "2018-11-05", "image_url": "https://images.unsplash.com/photo-1447752875215-b2761acb3c5d?w=300"},
        {"name": "Kabira (Encore)", "artist": "Harshdeep Kaur, Arijit Singh", "album": "Yeh Jawaani Hai Deewani", "popularity": 95, "duration_ms": 268000, "release_date": "2013-05-31", "image_url": "https://images.unsplash.com/photo-1509198397868-475647b2a1e5?w=300"},
        {"name": "Sham", "artist": "Amit Trivedi, Nikhil D'Souza", "album": "Aisha", "popularity": 90, "duration_ms": 284000, "release_date": "2010-07-07", "image_url": "https://images.unsplash.com/photo-1518495973542-4542c06a5843?w=300"},
        {"name": "Der Lagi Lekin", "artist": "Shankar Mahadevan", "album": "Zindagi Na Milegi Dobara", "popularity": 89, "duration_ms": 357000, "release_date": "2011-06-20", "image_url": "https://images.unsplash.com/photo-1447752875215-b2761acb3c5d?w=300"},
        {"name": "Khaabon Ke Parindey", "artist": "Mohit Chauhan, Alyssa Mendonsa", "album": "Zindagi Na Milegi Dobara", "popularity": 92, "duration_ms": 253000, "release_date": "2011-06-20", "image_url": "https://images.unsplash.com/photo-1509198397868-475647b2a1e5?w=300"},
        {"name": "Tu Kisi Rail Si", "artist": "Swanand Kirkire", "album": "Masaan", "popularity": 88, "duration_ms": 234000, "release_date": "2015-07-10", "image_url": "https://images.unsplash.com/photo-1518495973542-4542c06a5843?w=300"},
        {"name": "Qaafirana", "artist": "Arijit Singh, Nikhita Gandhi", "album": "Kedarnath", "popularity": 93, "duration_ms": 342000, "release_date": "2018-11-20", "image_url": "https://images.unsplash.com/photo-1447752875215-b2761acb3c5d?w=300"},
        {"name": "Safarnama", "artist": "Lucky Ali", "album": "Tamasha", "popularity": 91, "duration_ms": 251000, "release_date": "2015-11-03", "image_url": "https://images.unsplash.com/photo-1509198397868-475647b2a1e5?w=300"},
        {"name": "Love You Zindagi", "artist": "Jasleen Royal, Amit Trivedi", "album": "Dear Zindagi", "popularity": 92, "duration_ms": 238000, "release_date": "2016-11-02", "image_url": "https://images.unsplash.com/photo-1518495973542-4542c06a5843?w=300"},
        {"name": "Yun Hi Chala Chal", "artist": "Udit Narayan, Hariharan, Kailash Kher", "album": "Swades", "popularity": 93, "duration_ms": 448000, "release_date": "2004-10-22", "image_url": "https://images.unsplash.com/photo-1447752875215-b2761acb3c5d?w=300"},
        {"name": "Aashiyan", "artist": "Shreya Ghoshal, Nikhil Paul George", "album": "Barfi!", "popularity": 89, "duration_ms": 236000, "release_date": "2012-08-10", "image_url": "https://images.unsplash.com/photo-1509198397868-475647b2a1e5?w=300"},
    ],
    "neutral": [
        {"name": "Hairat", "artist": "Lucky Ali", "album": "Anjaana Anjaani", "popularity": 89, "duration_ms": 248000, "release_date": "2010-09-02", "image_url": "https://images.unsplash.com/photo-1514525253161-7a46d19cd819?w=300"},
        {"name": "Udd Gaye", "artist": "Ritviz", "album": "Udd Gaye", "popularity": 94, "duration_ms": 182000, "release_date": "2017-12-08", "image_url": "https://images.unsplash.com/photo-1470225620780-dba8ba36b745?w=300"},
        {"name": "Liggi", "artist": "Ritviz", "album": "Liggi", "popularity": 91, "duration_ms": 181000, "release_date": "2019-12-17", "image_url": "https://images.unsplash.com/photo-1516450360452-9312f5e86fc7?w=300"},
        {"name": "Sage", "artist": "Ritviz", "album": "Sage", "popularity": 89, "duration_ms": 154000, "release_date": "2019-07-16", "image_url": "https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?w=300"},
        {"name": "Kasoor", "artist": "Prateek Kuhad", "album": "Kasoor", "popularity": 92, "duration_ms": 197000, "release_date": "2020-07-24", "image_url": "https://images.unsplash.com/photo-1465847899084-d164df4dedc6?w=300"},
        {"name": "Cold/Mess", "artist": "Prateek Kuhad", "album": "cold/mess", "popularity": 95, "duration_ms": 283000, "release_date": "2018-07-13", "image_url": "https://images.unsplash.com/photo-1508700115892-45ecd05ae2ad?w=300"},
        {"name": "Baarishein", "artist": "Anuv Jain", "album": "Baarishein", "popularity": 96, "duration_ms": 208000, "release_date": "2018-08-28", "image_url": "https://images.unsplash.com/photo-1514525253161-7a46d19cd819?w=300"},
        {"name": "Alag Aasmaan", "artist": "Anuv Jain", "album": "Alag Aasmaan", "popularity": 93, "duration_ms": 213000, "release_date": "2020-07-31", "image_url": "https://images.unsplash.com/photo-1470225620780-dba8ba36b745?w=300"},
        {"name": "Gul", "artist": "Anuv Jain", "album": "Gul", "popularity": 92, "duration_ms": 218000, "release_date": "2021-07-16", "image_url": "https://images.unsplash.com/photo-1516450360452-9312f5e86fc7?w=300"},
        {"name": "Choo Lo", "artist": "The Local Train", "album": "Aalas Ka Pedh", "popularity": 96, "duration_ms": 234000, "release_date": "2015-09-08", "image_url": "https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?w=300"},
        {"name": "Aaoge Tum Kabhi", "artist": "The Local Train", "album": "Aalas Ka Pedh", "popularity": 93, "duration_ms": 314000, "release_date": "2015-09-08", "image_url": "https://images.unsplash.com/photo-1465847899084-d164df4dedc6?w=300"},
        {"name": "Kho Gaye Hum Kahan", "artist": "Jasleen Royal, Prateek Kuhad", "album": "Baar Baar Dekho", "popularity": 91, "duration_ms": 214000, "release_date": "2016-08-03", "image_url": "https://images.unsplash.com/photo-1508700115892-45ecd05ae2ad?w=300"},
    ],
    "nostalgic": [
        {"name": "Dil Chahta Hai", "artist": "Shankar Mahadevan", "album": "Dil Chahta Hai", "popularity": 94, "duration_ms": 311000, "release_date": "2001-08-10", "image_url": "https://images.unsplash.com/photo-1514525253161-7a46d19cd819?w=300"},
        {"name": "Yeh Shaam Mastani", "artist": "Kishore Kumar", "album": "Kati Patang", "popularity": 95, "duration_ms": 278000, "release_date": "1970-11-20", "image_url": "https://images.unsplash.com/photo-1470225620780-dba8ba36b745?w=300"},
        {"name": "Kya Hua Tera Wada", "artist": "Mohammed Rafi, Sushma Shrestha", "album": "Hum Kisise Kum Naheen", "popularity": 93, "duration_ms": 261000, "release_date": "1977-08-25", "image_url": "https://images.unsplash.com/photo-1516450360452-9312f5e86fc7?w=300"},
        {"name": "Pal", "artist": "KK", "album": "Pal", "popularity": 97, "duration_ms": 361000, "release_date": "1999-04-16", "image_url": "https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?w=300"},
        {"name": "Yaaron", "artist": "KK", "album": "Pal", "popularity": 96, "duration_ms": 278000, "release_date": "1999-04-16", "image_url": "https://images.unsplash.com/photo-1465847899084-d164df4dedc6?w=300"},
        {"name": "Woh Din", "artist": "Tushar Joshi", "album": "Chhichhore", "popularity": 92, "duration_ms": 258000, "release_date": "2019-08-26", "image_url": "https://images.unsplash.com/photo-1508700115892-45ecd05ae2ad?w=300"},
        {"name": "Ghar", "artist": "Nikhita Gandhi, Mohit Chauhan", "album": "Jab Harry Met Sejal", "popularity": 89, "duration_ms": 229000, "release_date": "2017-07-26", "image_url": "https://images.unsplash.com/photo-1514525253161-7a46d19cd819?w=300"},
        {"name": "Give Me Some Sunshine", "artist": "Suraj Jagan, Sharman Joshi", "album": "3 Idiots", "popularity": 94, "duration_ms": 247000, "release_date": "2009-11-27", "image_url": "https://images.unsplash.com/photo-1470225620780-dba8ba36b745?w=300"},
        {"name": "Tanha Dil", "artist": "Shaan", "album": "Tanha Dil", "popularity": 91, "duration_ms": 284000, "release_date": "2000-01-01", "image_url": "https://images.unsplash.com/photo-1516450360452-9312f5e86fc7?w=300"},
    ],
    "surprised": [
        {"name": "Jai Ho", "artist": "A.R. Rahman, Sukhwinder Singh", "album": "Slumdog Millionaire", "popularity": 96, "duration_ms": 319000, "release_date": "2008-11-25", "image_url": "https://images.unsplash.com/photo-1514525253161-7a46d19cd819?w=300"},
        {"name": "Patakha Guddi", "artist": "Nooran Sisters", "album": "Highway", "popularity": 93, "duration_ms": 284000, "release_date": "2014-01-20", "image_url": "https://images.unsplash.com/photo-1470225620780-dba8ba36b745?w=300"},
        {"name": "Badal Pe Paon Hain", "artist": "Hema Sardesai", "album": "Chak De! India", "popularity": 90, "duration_ms": 245000, "release_date": "2007-08-01", "image_url": "https://images.unsplash.com/photo-1516450360452-9312f5e86fc7?w=300"},
        {"name": "Galti Se Mistake", "artist": "Arijit Singh, Amit Mishra", "album": "Jagga Jasoos", "popularity": 92, "duration_ms": 203000, "release_date": "2017-06-09", "image_url": "https://images.unsplash.com/photo-1516450360452-9312f5e86fc7?w=300"},
        {"name": "Chale Jaise Hawaen", "artist": "KK, Vasundhara Das", "album": "Main Hoon Na", "popularity": 91, "duration_ms": 325000, "release_date": "2004-02-27", "image_url": "https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?w=300"},
        {"name": "All Izz Well", "artist": "Sonu Nigam, Shaan, Swanand Kirkire", "album": "3 Idiots", "popularity": 93, "duration_ms": 276000, "release_date": "2009-11-27", "image_url": "https://images.unsplash.com/photo-1465847899084-d164df4dedc6?w=300"},
        {"name": "Ziddi Dil", "artist": "Vishal Dadlani", "album": "Mary Kom", "popularity": 89, "duration_ms": 287000, "release_date": "2014-08-13", "image_url": "https://images.unsplash.com/photo-1508700115892-45ecd05ae2ad?w=300"},
    ],
}

# Rich collection of English fallback tracks categorized by mood
ENGLISH_EMOTION_TRACKS: dict[str, list[dict]] = {
    "joy": [
        {"name": "Blinding Lights", "artist": "The Weeknd", "album": "After Hours", "popularity": 95, "duration_ms": 200000, "release_date": "2020-03-20"},
        {"name": "Levitating", "artist": "Dua Lipa", "album": "Future Nostalgia", "popularity": 93, "duration_ms": 203000, "release_date": "2020-03-27"},
        {"name": "Uptown Funk", "artist": "Mark Ronson, Bruno Mars", "album": "Uptown Special", "popularity": 92, "duration_ms": 270000, "release_date": "2014-11-10"},
        {"name": "Can't Stop the Feeling!", "artist": "Justin Timberlake", "album": "Trolls", "popularity": 91, "duration_ms": 236000, "release_date": "2016-05-06"},
        {"name": "Happy", "artist": "Pharrell Williams", "album": "G I R L", "popularity": 90, "duration_ms": 233000, "release_date": "2013-11-21"},
        {"name": "Sunflower", "artist": "Post Malone, Swae Lee", "album": "Spider-Man: Into the Spider-Verse", "popularity": 94, "duration_ms": 158000, "release_date": "2018-10-19"},
        {"name": "Don't Start Now", "artist": "Dua Lipa", "album": "Future Nostalgia", "popularity": 89, "duration_ms": 183000, "release_date": "2019-10-31"},
        {"name": "Good as Hell", "artist": "Lizzo", "album": "Cuz I Love You", "popularity": 88, "duration_ms": 159000, "release_date": "2016-03-08"},
    ],
    "sadness": [
        {"name": "Someone Like You", "artist": "Adele", "album": "21", "popularity": 94, "duration_ms": 285000, "release_date": "2011-01-24"},
        {"name": "Fix You", "artist": "Coldplay", "album": "X&Y", "popularity": 92, "duration_ms": 295000, "release_date": "2005-06-06"},
        {"name": "when the party's over", "artist": "Billie Eilish", "album": "WHEN WE ALL FALL ASLEEP, WHERE DO WE GO?", "popularity": 91, "duration_ms": 196000, "release_date": "2018-10-17"},
        {"name": "All of Me", "artist": "John Legend", "album": "Love in the Future", "popularity": 93, "duration_ms": 269000, "release_date": "2013-08-12"},
        {"name": "Stay With Me", "artist": "Sam Smith", "album": "In the Lonely Hour", "popularity": 90, "duration_ms": 172000, "release_date": "2014-04-14"},
        {"name": "Say Something", "artist": "A Great Big World, Christina Aguilera", "album": "Is There Anybody Out There?", "popularity": 88, "duration_ms": 229000, "release_date": "2013-11-04"},
        {"name": "Let Her Go", "artist": "Passenger", "album": "All the Little Lights", "popularity": 91, "duration_ms": 252000, "release_date": "2012-02-24"},
    ],
    "love": [
        {"name": "Perfect", "artist": "Ed Sheeran", "album": "÷", "popularity": 95, "duration_ms": 263000, "release_date": "2017-03-03"},
        {"name": "Until I Found You", "artist": "Stephen Sanchez", "album": "Easy on My Eyes", "popularity": 94, "duration_ms": 177000, "release_date": "2021-09-01"},
        {"name": "Thinking Out Loud", "artist": "Ed Sheeran", "album": "x", "popularity": 93, "duration_ms": 281000, "release_date": "2014-06-20"},
        {"name": "Love Me Like You Do", "artist": "Ellie Goulding", "album": "Fifty Shades of Grey", "popularity": 91, "duration_ms": 252000, "release_date": "2015-01-07"},
        {"name": "Just the Way You Are", "artist": "Bruno Mars", "album": "Doo-Wops & Hooligans", "popularity": 92, "duration_ms": 220000, "release_date": "2010-07-20"},
        {"name": "Shallow", "artist": "Lady Gaga, Bradley Cooper", "album": "A Star Is Born", "popularity": 94, "duration_ms": 215000, "release_date": "2018-09-27"},
    ],
    "anger": [
        {"name": "Believer", "artist": "Imagine Dragons", "album": "Evolve", "popularity": 95, "duration_ms": 204000, "release_date": "2017-02-01"},
        {"name": "good 4 u", "artist": "Olivia Rodrigo", "album": "SOUR", "popularity": 94, "duration_ms": 178000, "release_date": "2021-05-14"},
        {"name": "In the End", "artist": "Linkin Park", "album": "Hybrid Theory", "popularity": 93, "duration_ms": 216000, "release_date": "2000-10-24"},
        {"name": "Radioactive", "artist": "Imagine Dragons", "album": "Night Visions", "popularity": 92, "duration_ms": 186000, "release_date": "2012-09-04"},
        {"name": "Seven Nation Army", "artist": "The White Stripes", "album": "Elephant", "popularity": 91, "duration_ms": 231000, "release_date": "2003-03-07"},
    ],
    "fear": [
        {"name": "Riptide", "artist": "Vance Joy", "album": "Dream Your Life Away", "popularity": 91, "duration_ms": 204000, "release_date": "2013-05-21"},
        {"name": "Holocene", "artist": "Bon Iver", "album": "Bon Iver", "popularity": 88, "duration_ms": 336000, "release_date": "2011-06-17"},
        {"name": "Breathe Me", "artist": "Sia", "album": "Colour the Small One", "popularity": 87, "duration_ms": 272000, "release_date": "2004-01-12"},
        {"name": "River", "artist": "Leon Bridges", "album": "Coming Home", "popularity": 89, "duration_ms": 240000, "release_date": "2015-06-23"},
        {"name": "Weightless", "artist": "Marconi Union", "album": "Weightless", "popularity": 86, "duration_ms": 485000, "release_date": "2011-10-16"},
    ],
    "neutral": [
        {"name": "Heat Waves", "artist": "Glass Animals", "album": "Dreamland", "popularity": 94, "duration_ms": 238000, "release_date": "2020-06-29"},
        {"name": "As It Was", "artist": "Harry Styles", "album": "Harry's House", "popularity": 96, "duration_ms": 167000, "release_date": "2022-04-01"},
        {"name": "Counting Stars", "artist": "OneRepublic", "album": "Native", "popularity": 92, "duration_ms": 257000, "release_date": "2013-03-25"},
        {"name": "Stay", "artist": "The Kid LAROI, Justin Bieber", "album": "F*CK LOVE 3: OVER YOU", "popularity": 93, "duration_ms": 141000, "release_date": "2021-07-09"},
        {"name": "Shape of You", "artist": "Ed Sheeran", "album": "÷", "popularity": 95, "duration_ms": 233000, "release_date": "2017-01-06"},
    ],
    "nostalgic": [
        {"name": "Take On Me", "artist": "a-ha", "album": "Hunting High and Low", "popularity": 92, "duration_ms": 225000, "release_date": "1985-06-01"},
        {"name": "Dreams", "artist": "Fleetwood Mac", "album": "Rumours", "popularity": 94, "duration_ms": 257000, "release_date": "1977-02-04"},
        {"name": "1979", "artist": "The Smashing Pumpkins", "album": "Mellon Collie and the Infinite Sadness", "popularity": 89, "duration_ms": 266000, "release_date": "1995-10-24"},
        {"name": "Hotel California", "artist": "Eagles", "album": "Hotel California", "popularity": 95, "duration_ms": 391000, "release_date": "1976-12-08"},
    ],
    "surprised": [
        {"name": "Don't Stop Believin'", "artist": "Journey", "album": "Escape", "popularity": 94, "duration_ms": 250000, "release_date": "1981-10-06"},
        {"name": "Eye of the Tiger", "artist": "Survivor", "album": "Eye of the Tiger", "popularity": 93, "duration_ms": 245000, "release_date": "1982-05-29"},
        {"name": "High Hopes", "artist": "Panic! At The Disco", "album": "Pray for the Wicked", "popularity": 91, "duration_ms": 190000, "release_date": "2018-05-23"},
    ],
}


def _canonical_emotion(emotion: str | None) -> str:
    """Map any emotion synonym to its canonical category."""
    if not emotion:
        return "neutral"
    key = emotion.strip().lower()
    return EMOTION_CANONICAL_MAP.get(key, "neutral")


def format_track(track: dict, language: str = "hindi") -> dict:
    """Format a track dictionary to match the standard MindSync Track schema."""
    name = track["name"]
    artist = track["artist"]
    encoded = urllib.parse.quote(f"{name} {artist}")
    default_img = (
        "https://images.unsplash.com/photo-1514525253161-7a46d19cd819?w=300"
        if language == "hindi"
        else "https://images.unsplash.com/photo-1470225620780-dba8ba36b745?w=300"
    )
    return {
        "name": name,
        "artist": artist,
        "album": track.get("album"),
        "preview_url": track.get("preview_url"),
        "external_url": track.get("external_url") or f"https://www.deezer.com/search/{encoded}",
        "image_url": track.get("image_url") or default_img,
        "popularity": int(track.get("popularity", 80)),
        "duration_ms": int(track.get("duration_ms", 210000)),
        "release_date": track.get("release_date"),
        "language": language,
    }


def get_hindi_tracks(emotion: str, limit: int = 30) -> list[dict]:
    """Return curated, mood-matched Hindi tracks for the given emotion."""
    canonical = _canonical_emotion(emotion)
    tracks = list(HINDI_EMOTION_TRACKS.get(canonical, HINDI_EMOTION_TRACKS["neutral"]))
    # Also blend general hits if the mood set is small
    if len(tracks) < limit:
        extra = [
            t for t in HINDI_EMOTION_TRACKS.get("joy", []) + HINDI_EMOTION_TRACKS.get("love", [])
            if t["name"] not in {x["name"] for x in tracks}
        ]
        tracks.extend(extra)
    return [format_track(t, language="hindi") for t in tracks[:limit]]


def get_english_fallback_tracks(emotion: str, limit: int = 30) -> list[dict]:
    """Return curated, mood-matched English fallback tracks."""
    canonical = _canonical_emotion(emotion)
    tracks = list(ENGLISH_EMOTION_TRACKS.get(canonical, ENGLISH_EMOTION_TRACKS["neutral"]))
    if len(tracks) < limit:
        extra = [
            t for t in ENGLISH_EMOTION_TRACKS.get("joy", []) + ENGLISH_EMOTION_TRACKS.get("neutral", [])
            if t["name"] not in {x["name"] for x in tracks}
        ]
        tracks.extend(extra)
    return [format_track(t, language="english") for t in tracks[:limit]]


def interleave_tracks(
    primary: list[dict],
    secondary: list[dict],
    limit: int = 60,
) -> list[dict]:
    """Evenly interleave two track lists so both languages are represented side-by-side."""
    result: list[dict] = []
    i, j = 0, 0
    len_p, len_s = len(primary), len(secondary)

    while (i < len_p or j < len_s) and len(result) < limit:
        if i < len_p:
            result.append(primary[i])
            i += 1
        if j < len_s and len(result) < limit:
            result.append(secondary[j])
            j += 1

    return result
