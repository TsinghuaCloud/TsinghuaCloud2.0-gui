/*
Navicat MySQL Data Transfer

Source Server         : 241
Source Server Version : 50540
Source Host           : 166.111.143.241:3306
Source Database       : test_zxl

Target Server Type    : MYSQL
Target Server Version : 50540
File Encoding         : 65001

Date: 2015-07-16 11:39:20
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for user
-- ----------------------------
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `userid` varchar(255) DEFAULT NULL,
  `account` double DEFAULT NULL,
  `username` varchar(64) DEFAULT NULL,
  `password` varchar(64) DEFAULT NULL,
  `tenantid` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for user_info
-- ----------------------------
DROP TABLE IF EXISTS `user_info`;
CREATE TABLE `user_info` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `userid` varchar(255) DEFAULT NULL,
  `instanceid` varchar(255) DEFAULT NULL,
  `op` varchar(1) DEFAULT NULL,
  `money` double DEFAULT NULL,
  `time` datetime DEFAULT NULL,
  `instancename` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for user_pay
-- ----------------------------
DROP TABLE IF EXISTS `user_pay`;
CREATE TABLE `user_pay` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `userid` varchar(255) DEFAULT NULL,
  `instanceid` varchar(255) DEFAULT NULL,
  `instancename` varchar(255) DEFAULT NULL,
  `updatetime` datetime DEFAULT NULL,
  `unit_price` double DEFAULT NULL,
  `status` char(1) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
