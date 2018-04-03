#  coding: utf-8
import os
from flask_login import login_required
from flask import Blueprint
import platform
from app.decorator.auth import province_required
from app.libs.http import jsonify

bp_admin_system = Blueprint('admin_system_info', __name__, url_prefix='/admin/system_info')

RAM_INFO = 'RAM Total = {} MB\nRAM Used = {} MB\nRAM Free = {} MB\n'
DISK_INFO = 'DISK Total Space = {} B\nDISK Used Space = {} B\nDISK Used Percentage = {}\n'


@bp_admin_system.route("/", methods=["GET"])
@login_required
@province_required
def get_sys_info():  # 返回所有当前用户可以审核的条目
    cpu_usage = get_cpu_use()
    ram_stats = get_ram_info()
    ram_total = round(int(ram_stats[0]) / 1000, 1)
    ram_used = round(int(ram_stats[1]) / 1000, 1)
    ram_free = round(int(ram_stats[2]) / 1000, 1)
    disk_stats = get_disk_space()
    disk_total = disk_stats[0]
    disk_used = disk_stats[1]
    disk_perc = disk_stats[3]

    data = {'cpu': 'CPU Use = ' + cpu_usage, 'memory': RAM_INFO.format(ram_total, ram_used, ram_free),
            'hard_disk': DISK_INFO.format(disk_total, disk_used, disk_perc), 'system': platform.platform()}

    return jsonify(data)


# Return RAM information (unit=kb) in a list
# Index 0: total RAM
# Index 1: used RAM
# Index 2: free RAM
def get_ram_info():
    p = os.popen('free')
    i = 0
    while 1:
        i = i + 1
        line = p.readline()
        if i == 2:
            return line.split()[1:4]


# Return % of CPU used by user as a character string
def get_cpu_use():
    return str(os.popen("top -n1 | awk '/Cpu\(s\):/ {print $2}'").readline().strip())


# Return information about disk space as a list (unit included)
# Index 0: total disk space
# Index 1: used disk space
# Index 2: remaining disk space
# Index 3: percentage of disk used
def get_disk_space():
    p = os.popen("df -h /")
    i = 0
    while 1:
        i = i + 1
        line = p.readline()
        if i == 2:
            return line.split()[1:5]
