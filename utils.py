import glob, os, math

def clean_folder(folderpath):
    img_paths = glob.glob(f'{folderpath}/*')
    for path in img_paths:
        os.remove(path)



def update_img_seq_data(img_seq_data, new_img_obj_area, new_img_dist_to_ctr):
#     img_seq_data = {
#     'counter' : 0,
#     'max_area' : 0,
#     'min_dist_to_ctr': 400,
#     'img_mid_frame': 0,
#     'img_largest_obj': 0,
#     'img_min_dist_to_ctr': 0,
# }
    
    if int(new_img_obj_area) < 307200 and new_img_obj_area > img_seq_data['max_area']:
        img_seq_data['max_area'] = new_img_obj_area
        img_seq_data['img_largest_obj'] = img_seq_data['counter']

    if int(new_img_dist_to_ctr) > 0 and new_img_dist_to_ctr < img_seq_data['min_dist_to_ctr']:
        img_seq_data['min_dist_to_ctr'] = new_img_dist_to_ctr
        img_seq_data['img_min_dist_to_ctr'] = img_seq_data['counter']
    
    img_seq_data['img_mid_frame'] = math.ceil(img_seq_data['counter']/2)

    return img_seq_data



def return_initial_img_seq_data(): 
    return {
    'counter' : 0,
    'max_area' : 0,
    'min_dist_to_ctr': 400,
    'img_mid_frame': 0,
    'img_largest_obj': 0,
    'img_min_dist_to_ctr': 0,
}



def return_img_seq_data_file_paths(img_seq_data):
    return f'images/{img_seq_data['img_mid_frame']}.jpg', f'images/{img_seq_data['img_largest_obj']}.jpg', f'images/{img_seq_data['img_min_dist_to_ctr']}.jpg'