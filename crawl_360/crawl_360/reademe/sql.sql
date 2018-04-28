CREATE TABLE butian (
  id INT(11) UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '自增id',
  author VARCHAR(100) not null DEFAULT '' COMMENT '作者',
  company_name VARCHAR(100) NOT NULL DEFAULT '' COMMENT '公司名',
  vul_level VARCHAR(100) not null DEFAULT '' COMMENT '漏洞级别',
  vul_name VARCHAR(100) not null DEFAULT '' COMMENT '漏洞名',
  vul_money DECIMAL(10,2) not NULL DEFAULT 0 COMMENT '漏洞奖金',
  vul_find_time DATETIME not NULL DEFAULT '0000-00-00 00:00:00' COMMENT '漏洞发现时间',
  link_url VARCHAR(255) not null DEFAULT '' COMMENT '页面url',
  create_time TIMESTAMP not null DEFAULT current_timestamp COMMENT '创建时间',
  PRIMARY KEY (id)
)ENGINE=INNODB DEFAULT CHARSET utf8;
