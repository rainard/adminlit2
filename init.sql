INSERT INTO `auth_usergroup` VALUES (1, '管理组', '全部权限');
INSERT INTO `auth_permission` VALUES (1, '权限', 'auth/permission.html', '系统管理', 'fa fa-laptop', NULL);
INSERT INTO `auth_permission` VALUES (2, '用户', 'auth/user.html', '系统管理', 'fa fa-laptop', NULL);
INSERT INTO `auth_permission` VALUES (3, '用户组', 'auth/usergroup.html', '系统管理', 'fa fa-laptop', NULL);
INSERT INTO `auth_user` VALUES (1, 'admin', 'c87cb5b4678ebe99306d457952d46801', 'dddd@d.com', 'eric', 'wang', 1, 1, 1, '2018-1-5 14:54:06', '2018-1-5 14:13:53', 1);
INSERT INTO `auth_usergroup_permis` VALUES (1, 1, 1);
INSERT INTO `auth_usergroup_permis` VALUES (2, 1, 2);
INSERT INTO `auth_usergroup_permis` VALUES (3, 1, 3);