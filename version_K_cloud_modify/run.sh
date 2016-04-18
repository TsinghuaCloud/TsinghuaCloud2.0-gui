cp -rf  ./1/openstack_dashboard /usr/share/openstack-dashboard/
cp -rf ./2/horizon /usr/lib/python2.7/dist-packages/
cp -rf ./3/openstack_auth /usr/lib/python2.7/dist-packages/
cp -rf ./4/openstack_dashboard /usr/share/openstack-dashboard/
cp -rf ./5/openstack-dashboard-ubuntu-theme /usr/share/
service apache2 restart
