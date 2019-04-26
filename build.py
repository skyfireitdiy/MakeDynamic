# coding=utf-8
import argparse
import hashlib
import json
import mimetypes
import os
import shutil
import datetime

from werkzeug.security import generate_password_hash

from md_utils import my_secure_filename


def main():
    parse = argparse.ArgumentParser()
    parse.add_argument("-P", "--project", help="Project name", required=True, dest="project_name")
    parse.add_argument("-d", "--directory", help="Output directory", dest="directory", required=True)
    parse.add_argument("-n", "--name", default="admin", help="Admin user name", required=True, dest="admin_name")
    parse.add_argument("-p", "--password", help="Admin password", required=True, dest="password")
    parse.add_argument("-t", "--template_dir", help="Template file directory", required=False, dest="template_dir")
    parse.add_argument("-s", "--static_dir", help="Static files directory", required=False, dest="static_dir")
    parse.add_argument("-v", "--video", help="Video files directory", required=False, dest="video_dir")
    parse.add_argument("-m", "--music", help="Music files directory", required=False, dest="music_dir")
    parse.add_argument("-i", "--image", help="Image files directory", required=False, dest="image_dir")
    parse.add_argument("-f", "--file", help="General files directory", required=False, dest="file_dir")
    parse.add_argument("-N", "--port", help="Server port", required=False, default="8080", dest="port")
    parse.add_argument("-D", "--jsondata", help="Data file with json", required=False, dest="json_data")
    parse.add_argument("-a", "--article_image", help="Article images directory", required=False, dest="article_folder")
    parse.add_argument("-T", "--data_template", help="Data tempalte file", required=False, dest="data_template")
    parse.add_argument("-e", "--extend_data", help="Extend config file", required=False, dest="extend_config")
    parse.add_argument("-H", "--admin_header", help="Title of backstage management page", default="后台管理页面",
                       dest="title")
    parse.add_argument("-F", "--footer", help="Title of backstage management page",
                       default="Copyright © 2019-%s SkyFire. All rights reserved." % datetime.datetime.now().year,
                       dest="footer")

    args = parse.parse_args()
    if not os.path.exists(args.directory) and os.makedirs(args.directory, exist_ok=True):
        print("Directory not exists and create failed：", args.directory)
        return
    project_path = os.path.join(args.directory, args.project_name)
    if not os.path.exists(project_path) and os.makedirs(project_path, exist_ok=True):
        print("Directory not exists and create failed：", project_path)
        return
    if len(os.listdir(project_path)) != 0:
        print("Directory exists but not empty：", project_path)
        return

    shutil.copytree("admin", os.path.join(project_path, "admin"))
    shutil.copy("admin.py", project_path)
    shutil.copy("config_manager.py", project_path)
    shutil.copy("file_manager.py", project_path)
    shutil.copy("md_utils.py", project_path)
    shutil.copy("website.py", project_path)
    shutil.copy("app.py", project_path)
    shutil.copy("admin_user.py", project_path)

    if args.static_dir is not None:
        shutil.copytree(args.static_dir, os.path.join(project_path, "www/static"))
    if args.template_dir is not None:
        shutil.copytree(args.template_dir, os.path.join(project_path, "www/template"))
    if args.file_dir is not None:
        shutil.copytree(args.file_dir, os.path.join(project_path, "file/file_data"))
    if args.music_dir is not None:
        shutil.copytree(args.music_dir, os.path.join(project_path, "file/music_data"))
    if args.video_dir is not None:
        shutil.copytree(args.video_dir, os.path.join(project_path, "file/video_data"))
    if args.image_dir is not None:
        shutil.copytree(args.image_dir, os.path.join(project_path, "file/image_data"))
    if args.article_folder is not None:
        shutil.copytree(args.article_folder, os.path.join(project_path, "file/article_image"))

    os.makedirs(os.path.join(project_path, "file/file_data"), exist_ok=True)
    os.makedirs(os.path.join(project_path, "file/image_data"), exist_ok=True)
    os.makedirs(os.path.join(project_path, "file/music_data"), exist_ok=True)
    os.makedirs(os.path.join(project_path, "file/video_data"), exist_ok=True)
    os.makedirs(os.path.join(project_path, "file/article_image"), exist_ok=True)
    os.makedirs(os.path.join(project_path, "file/thumbnail_data"), exist_ok=True)
    os.makedirs(os.path.join(project_path, "www/static"), exist_ok=True)
    os.makedirs(os.path.join(project_path, "www/template"), exist_ok=True)
    os.makedirs(os.path.join(project_path, "config"), exist_ok=True)

    website_content = '''
from flask import *
from config_manager import global_data
import json5
website_blueprint = Blueprint("/", __name__, static_folder="./www/static", 
                                template_folder="./www/template",static_url_path="/")

'''
    template_path = os.path.join(project_path, "www/template")
    template_files = []
    for t_root, _, t_files in os.walk(template_path):
        template_files.extend(
            [os.path.join(t_root, y).replace('\\', '/')[len(template_path) + 1:] for y in t_files])

    for file in template_files:
        website_content += '''
@website_blueprint.route("/%s")
def %s():
    with open("config/data_ext.json", "r") as fp:
        data_ext = fp.read()
    return Response(render_template("%s", data=global_data.config, data_ext=json5.loads(data_ext)), mimetype='%s')

''' % (file, "_" + my_secure_filename(file).replace(".", "_").replace(" ", "_"), file,
       mimetypes.types_map[os.path.splitext(file)[-1]])

    with open(os.path.join(project_path, "website.py"), "w") as fp:
        fp.write(website_content)
    config = dict(
        title=args.title,
        footer=args.footer,
        user=dict(
            name=args.admin_name,
            password=generate_password_hash(hashlib.md5(args.password.encode("utf-8")).hexdigest()),
            img=""
        ),
        port=int(args.port),
    )

    with open(os.path.join(project_path, "config/config.json"), 'w') as fp:
        fp.write(json.dumps(config, indent=4))
    if args.json_data is not None:
        shutil.copy(args.json_data, os.path.join(project_path, "config/data.json"))
    else:
        with open(os.path.join(project_path, "config/data.json"), 'w') as fp:
            fp.write(json.dumps({}))
    if args.data_template is not None:
        shutil.copy(args.data_template, os.path.join(project_path, "config/template.json"))
    else:
        with open(os.path.join(project_path, "config/template.json"), "w") as fp:
            fp.write(json.dumps({
                "Number": 0,
                "Array": [],
                "Object": {},
                "String": ""
            }))

    with open(os.path.join(project_path, "config/module.json"), "w") as fp:
        fp.write(json.dumps({
            "基础信息管理": {
                "数据管理": {
                    "数据设置": {
                        "url": "data.html"
                    },
                    "模板设置": {
                        "url": "template.html"
                    }
                },
                "资源管理": {
                    "普通文件管理": {
                        "url": "normal_file_manage.html"
                    },
                    "图片管理": {
                        "url": "image_manage.html"
                    },
                    "音乐管理": {
                        "url": "music_manage.html"
                    },
                    "视频管理": {
                        "url": "video_manage.html"
                    }
                },
                "基础设置": {
                    "后台信息设置": {
                        "url": "base_info_manage.html"
                    }
                },
                "用户及安全": {
                    "用户信息": {
                        "url": "user_info_manage.html"
                    },
                    "密码修改": {
                        "url": "password_manage.html"
                    }
                }
            }
        }))

    if args.extend_config is not None:
        shutil.copy(args.extend_config, os.path.join(project_path, "config/data_ext.json"))
    else:
        with open(os.path.join(project_path, "config/data_ext.json"), "w") as fp:
            fp.write(json.dumps({}))

    print('''finished! Just run "cd %s && python.exe app.py"''' % project_path)


if __name__ == "__main__":
    main()
