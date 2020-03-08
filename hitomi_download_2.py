import urllib.request
import argparse
import math
from myutil.util import create_directory
from myutil.util import download_image
from myutil.util import get_response
from myutil.util import get_response_with_header
from myutil.util import is_file_exists
from multiprocessing import Process

parser = argparse.ArgumentParser()
parser.add_argument('ID', help = 'ID')
parser.add_argument('P', type = int, help = 'number of processes')
parser.add_argument('L', type = int, help = 'last page number')
args = parser.parse_args()

BASE_FOLDER = "hitomi"
REFERAL_LINK = "https://hitomi.la/reader/" + args.ID + ".html"
HASH_TABLE_LINK = "https://ltn.hitomi.la/galleries/" + args.ID + ".js"
#https://aa.hitomi.la/galleries/827706/0002_9JJU8ky_Imgur.png

# from common.js
ADAPOSE = False
#NUMBER_OF_FRONTENDS = 3

def full_path_from_hash(hash):
    if (len(hash) < 3):
        return hash
    return hash[-1:] + "/" + hash[-3:-1] + "/" + hash

def url_from_hash(galleryid, image, dir):
    ext = ''
    if dir == 'webp':
        ext = 'webp'
    else:
        # get extension from image name
        ext = image[1].split('.').pop()
        dir = 'images'
    
    
    #if ("1" in image[2] or ("0" in image[2] and len(image[0]) == 0)): #haswebp
    #    url = '//a.hitomi.la/galleries/' + galleryid + '/' + image[1]
    #else:
    #    ext = image[1].split('.')[1]
    #    url = '//a.hitomi.la/images/'+full_path_from_hash(image[0])+'.'+ext
    #return url
    return 'https://a.hitomi.la/'+ dir + '/' + full_path_from_hash(image[0]) + '.' + ext

def url_from_url(url):
    return url.replace('//a.hitomi.la/', '//'+subdomain_from_url(url)+'.hitomi.la/')

def url_from_url_from_hash(galleryid, image, dir):
    return url_from_url(url_from_hash(galleryid, image, dir))

def subdomain_from_galleryid(g, number_of_frontends):
    if (ADAPOSE):
        return '0'
    
    o = g % number_of_frontends
    return chr(o + 97)

def subdomain_from_url(url):
    retval = 'a'
    try:
        m = url.split('hitomi.la/')[1].split('/') # get the m[2] values
        g = int(m[2], 16)
        number_of_frontends = 3
        if (g < 0x30):
            number_of_frontends = 2
        if (g < 0x09):
            number_of_frontends = 1
        retval = subdomain_from_galleryid(g, number_of_frontends) + retval
        
        #if "a.hitomi.la/images" in url:
        #    temp = url.split('//a.hitomi.la/images/')[1][2:4]
        #    g = int(temp, 16)
        #    url = subdomain_from_galleryid(g) + 'a'
        #elif "a.hitomi.la/galleries" in url:
        #    temp = url.split('//a.hitomi.la/galleries/')[1].split('/')[0][-1:]
        #    g = int(temp, 10)
        #    url = subdomain_from_galleryid(g) + 'a'
    except Exception as e:
        return url
    return retval

def image_url_from_image(galleryid, image, nowebp):
    webp = ''
    if len(image[0]) > 0 and len(image[2]) > 0 and not nowebp:
        webp = 'webp'
    return url_from_url_from_hash(galleryid, image, webp)

def get_image_links():
    raw_js = get_response(HASH_TABLE_LINK)
    temp_table = [] # arrays of (hash, name, haswebp)
    split1 = raw_js.split(']')[0].split('[')[1].split('{')
    for i in range(1, len(split1), 1):
        if "hash" in split1[i]:
            hash = split1[i].split('"hash":')[1].split(',')[0]
            if "null" in hash:
                hash = ''
            else:
                hash = hash.split('"')[1]
        else:
            hash = ''
        name = split1[i].split('"name":"')[1].split('"')[0]
        haswebp = split1[i].split('"haswebp":')[1].split(',')[0]
        temp_table.append([hash, name, haswebp])
    image_links = []
    for i in range(len(temp_table)):
        image_link = image_url_from_image(args.ID, temp_table[i], False)
        image_links.append(image_link)
    return image_links

def run_process(split1, save_folder, padding, process_no, pics_per_process):
    for i in range(len(split1)):
        imageFileName = str(process_no * pics_per_process + i + 1).zfill(padding)
        imageUrl = split1[i]
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
            'Referer': REFERAL_LINK}
        if imageUrl[-4:] in ".png":
            imageFileName = imageFileName + ".png"
        elif imageUrl[-4:] in ".jpg":
            imageFileName = imageFileName + ".jpg"
        elif imageUrl[-5:] in ".jpeg":
            imageFileName = imageFileName + ".jpeg"
        elif imageUrl[-4:] in ".gif":
            imageFileName = imageFileName + ".gif"
        elif imageUrl[-5:] in ".webp":
            imageFileName = imageFileName + ".webp"
        filepath = save_folder + "/" + imageFileName
        download_image(imageUrl, filepath, True, headers) 

def run():
    image_links = get_image_links()
    num_processes = args.P
    last_pic_num = args.L
    total_pics = len(image_links)
    if (last_pic_num <= 0):
        num_pics = total_pics
    else:
        num_pics = min(last_pic_num, total_pics)
    padding = len(str(total_pics))
    save_folder = BASE_FOLDER + "/" + args.ID
    create_directory(save_folder)
    processes = []
    pics_per_process = math.ceil(num_pics / num_processes)
    for i in range(num_processes):
        max_pos = min(i * pics_per_process + pics_per_process, num_pics)
        min_pos = i * pics_per_process
        process = Process(target=run_process, args=(image_links[min_pos:max_pos], save_folder, padding, i, pics_per_process))
        processes.append(process)
        process.start()
    
    for process in processes:
        process.join()

if __name__ == '__main__':
    run()
