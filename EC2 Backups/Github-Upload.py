# -*- coding: utf-8 -*-
"""
Created on Mon Jan 22 18:49:25 2024

@author: Administrator
"""

# Upload images to a GitHub repo
# Old code snipped - update repo keys and paths

def githubUpload():
    g = Github("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")
    repo = g.get_repo("EFisher828/3D-Weather-Model-Data")
    contents = repo.get_contents("./Images/Rainier/Snow")
    for bil in range(21):
        current_file = contents[bil]
        name_raw = str(current_file.name)
        name_split = name_raw.split('.')
        name = name_split[0]
        sha = current_file.sha
        
        file = open(f"./Exports/Rainier/Snow/{name}.png",'rb')
        repo.update_file(f"./Images/Rainier/Snow/{name}.png", "upload new run", file.read(),sha)
        
githubUpload()