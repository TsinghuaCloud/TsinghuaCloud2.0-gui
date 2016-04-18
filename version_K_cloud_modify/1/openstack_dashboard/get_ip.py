def get_one_ip(atype):
    f = open("/usr/share/openstack-dashboard/openstack_dashboard/set_ip")
    line = f.readline().strip('\n')
    while line:
        str_split = line.split('#')
        if str_split[0] == atype:
            real_ip = str_split[1]
            break
        line = f.readline().strip('\n')

    f.close()
    print "this is real_ip : %s" % real_ip
    return real_ip

